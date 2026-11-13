from typing import Self, final


@final
class Extents:
    xmin: float
    ymin: float
    xmax: float
    ymax: float

    def __init__(
        self,
        xmin: float = float("inf"),
        ymin: float = float("inf"),
        xmax: float = float("-inf"),
        ymax: float = float("-inf"),
    ) -> None:
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax

    def add(self, x: float, y: float) -> None:
        self.xmin = min(self.xmin, x)
        self.xmax = max(self.xmax, x)
        self.ymin = min(self.ymin, y)
        self.ymax = max(self.ymax, y)

    def __add__(self, extent: Self | int) -> Self:
        # Support sum(extents): sum() begins with integer 0.
        if isinstance(extent, int) and extent == 0:
            return Extents(self.xmin, self.ymin, self.xmax, self.ymax)
        if isinstance(extent, Extents):
            return Extents(
                min(self.xmin, extent.xmin),
                min(self.ymin, extent.ymin),
                max(self.xmax, extent.xmax),
                max(self.ymax, extent.ymax),
            )
        raise TypeError("Must be an int or Extents.")

    def __radd__(self, extent: Self | int) -> Self:
        if isinstance(extent, int) and extent == 0:
            return Extents(self.xmin, self.ymin, self.xmax, self.ymax)
        if isinstance(extent, Extents):
            return self.__add__(extent)
        raise TypeError("Must be an int or Extents.")

    @property
    def width(self) -> float:
        return self.xmax - self.xmin

    @property
    def height(self) -> float:
        return self.ymax - self.ymin

    def __repr__(self) -> str:
        return f"Extents ({self.xmin},{self.ymin})-({self.xmax},{self.ymax})"
