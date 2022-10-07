from typing import TYPE_CHECKING, Literal, TypeVar
from collections.abc import Callable, Iterable

from discord import Message

if TYPE_CHECKING:
    from bot.core import RoboAchxy
    from typing_extensions import Unpack, Self

else:
    RoboAchxy = TypeVar("RoboAchxy")
    Self = TypeVar("Self")

PrefixModifier = Callable[["Unpack[tuple[str, ...]]"], Callable[[RoboAchxy, Message], Iterable[str]]]
EmptySend = Literal[None]
