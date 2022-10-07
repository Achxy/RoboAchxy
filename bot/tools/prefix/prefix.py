from collections.abc import Generator, Iterable
from asyncpg import Pool
from itertools import cycle
from operator import itemgetter

from bot.options import MAX_GUILD_PREFIX_LIMIT
from bot._typeshack import RoboAchxy, PrefixModifier, Self, EmptySend
from discord import Message
from asyncio import Future, gather
from bot.tools.prefix._helpers import no_modifier


class MaxGuildPrefixLimitExceeded(RuntimeError):
    def __init__(self, guild: int, limit: int) -> None:
        super(RuntimeError, self).__init__(f"Exceeded max prefix limit {limit} for guild {guild}")


class Prefix:
    def __init__(
        self,
        bot: RoboAchxy,
        pool: Pool,
        modifier: PrefixModifier = no_modifier,
        use_modifier_on_dm: bool = True,
        on_dm_return: str = str(),
    ) -> None:
        self.bot: RoboAchxy = bot
        self.pool: Pool = pool
        self.modifier: PrefixModifier = modifier
        self.on_dm_return: str = on_dm_return
        self.use_modifier_on_dm: bool = use_modifier_on_dm
        self._initialized: bool = False

    def __await__(self) -> Generator[Future, EmptySend, Self]:
        if self._initialized:
            return self
        coro = self.__async_init__()
        gener = coro.__await__()
        yield from gener
        return self

    async def __async_init__(self) -> None:
        await self.pool
        self._initialized = True
        await self.init_table()

    async def __call__(self, bot: RoboAchxy, message: Message) -> Iterable[str]:
        return await self.get_prefixes(bot, message)

    async def init_table(self) -> None:
        if not self._initialized:
            # This means that the pool has not been initialized.
            # We can await this instance and have pool initialized and table created.
            # We can return and cause termination because desired effect has then been achieved.
            await self
            return

        query = """
        CREATE TABLE IF NOT EXISTS guild_prefixes
            (
              guild_id BIGINT NOT NULL,
              prefix   VARCHAR(10) NOT NULL,
              UNIQUE (guild_id, prefix)
            );
        """
        await self.pool.execute(query)

    async def get_prefix_count_of_guild(self, guild_id: int) -> int:
        await self
        query = """
        SELECT COUNT(*) as prefix_count FROM guild_prefixes
        WHERE guild_id = $1;
        """
        return await self.pool.fetchval(query, guild_id)

    async def add_prefixes(self, guild_id: int, *prefixes: str, get_limit_unchecked: bool = False) -> None:
        await self
        if (
            not get_limit_unchecked
            and (await self.get_prefix_count_of_guild(guild_id) + len(prefixes)) > MAX_GUILD_PREFIX_LIMIT
        ):
            raise MaxGuildPrefixLimitExceeded(guild_id, MAX_GUILD_PREFIX_LIMIT)
        query = """
        INSERT INTO guild_prefixes
            (
                guild_id,
                prefix
            )
        VALUES
            (
                $1,
                $2
            );
        """
        await self.pool.executemany(query, zip(cycle([guild_id]), prefixes))

    async def remove_prefixes(self, guild_id: int, *prefixes: str) -> None:
        await self
        query = """
        DELETE FROM guild_prefixes
        WHERE guild_id = $1 AND prefix = $2;
        """
        await self.pool.executemany(query, zip(cycle([guild_id]), prefixes))

    async def remove_all_prefixes(self, guild_id: int) -> None:
        await self
        query = """
        DELETE FROM guild_prefixes
        WHERE guild_id = $1;
        """
        await self.pool.execute(query, guild_id)

    async def get_raw_prefixes(self, guild_id: int) -> set[str]:
        await self
        query = """
        SELECT prefix FROM guild_prefixes
        WHERE guild_id = $1;
        """
        result = await self.pool.fetch(query, guild_id)
        return {*map(itemgetter("prefix"), result)}

    def _get_dm_case(self, bot, message) -> Iterable[str]:
        empty = self.modifier()
        if self.use_modifier_on_dm:
            return empty(bot, message)
        return []

    async def get_prefixes(self, bot: RoboAchxy, message: Message) -> Iterable[str]:
        if message.guild is None:
            return self._get_dm_case(bot, message)
        prefixes = await self.get_raw_prefixes(message.guild.id)
        modified = self.modifier(*prefixes)
        return modified(bot, message)
