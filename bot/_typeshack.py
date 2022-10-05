from typing import TYPE_CHECKING, TypeVar

if TYPE_CHECKING:
    from .core import RoboAchxy
else:
    RoboAchxy = TypeVar("RoboAchxy")
