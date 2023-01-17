# Copyright (C) 2013-2014 Florian Festi
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
from __future__ import annotations

import math
from typing_extensions import TypeAlias, Annotated  # Backport for <py3.10

VectorMut: TypeAlias = "Annotated[list[float], 2]"
VectorIm: TypeAlias = "tuple[float, float]"
Vector: TypeAlias = "VectorMut | VectorIm"

PointMut: TypeAlias = "Annotated[list[float], 2]"
PointIm: TypeAlias = "tuple[float, float]"
Point: TypeAlias = "PointMut | PointIm"


def normalize(v: Vector) -> VectorIm:
    """set length of vector to one"""
    l = (v[0] ** 2 + v[1] ** 2) ** 0.5
    if l == 0.0:
        return (0.0, 0.0)
    return (v[0] / l, v[1] / l)


def vlength(v: Vector) -> float:
    return (v[0] ** 2 + v[1] ** 2) ** 0.5


def vclip(v: Vector, length: float) -> Vector:
    l = vlength(v)
    if l > length:
        return vscalmul(v, length / l)
    return v


def vdiff(p1: Point, p2: Point) -> VectorIm:
    """vector from point1 to point2"""
    return (p2[0] - p1[0], p2[1] - p1[1])


def vadd(v1: Vector, v2: Vector) -> VectorIm:
    """Sum of two vectors"""
    return (v1[0] + v2[0], v1[1] + v2[1])


def vorthogonal(v: Vector) -> VectorIm:
    """Orthogonal vector"""
    return (-v[1], v[0])


def vscalmul(v: Vector, a: float) -> VectorIm:
    """scale vector by a"""
    return (a * v[0], a * v[1])


def dotproduct(v1: Vector, v2: Vector) -> float:
    """Dot product"""
    return v1[0] * v2[0] + v1[1] * v2[1]


def circlepoint(r: float, a: float) -> VectorIm:
    return (r * math.cos(a), r * math.sin(a))


def tangent(x: float, y: float, r: float) -> VectorIm:
    """angle and length of a tangent to a circle at x,y with radius r"""
    l1 = vlength((x, y))
    a1 = math.atan2(y, x)
    a2 = math.asin(r / l1)
    l2 = math.cos(a2) * l1

    return (a1 + a2, l2)


def rotm(angle: float) -> list[list[float]]:
    """Rotation matrix"""
    return [[math.cos(angle), -math.sin(angle), 0],
            [math.sin(angle), math.cos(angle), 0]]


def vtransl(v: list[float], m: list[list[float]]) -> list[float]:
    m0, m1 = m
    return [m0[0] * v[0] + m0[1] * v[1] + m0[2],
            m1[0] * v[0] + m1[1] * v[1] + m1[2]]


def mmul(m0: list[list[float]], m1: list[list[float]]) -> list[list[float]]:
    result = [[0.0, ] * len(m0[0]) for i in range(len(m0))]
    for i in range(len(m0[0])):
        for j in range(len(m0)):
            for k in range(len(m0)):
                result[j][i] += m0[k][i] * m1[j][k]
    return result


def kerf(points: list[Point], k: float, closed: bool = True) -> list[VectorIm]:
    """Outset points by k
    Assumes a closed loop of points
    """
    result = []
    lp = len(points)

    for i in range(len(points)):
        # get normalized orthogonals of both segments
        v1 = vorthogonal(normalize(vdiff(points[i - 1], points[i])))
        v2 = vorthogonal(normalize(vdiff(points[i], points[(i + 1) % lp])))

        if not closed:
            if i == 0:
                v1 = v2
            if i == lp - 1:
                v2 = v1
        # direction the point has to move
        d = normalize(vadd(v1, v2))
        # cos of the half the angle between the segments
        cos_alpha = dotproduct(v1, d)
        result.append(vadd(points[i], vscalmul(d, -k / cos_alpha)))

    return result
