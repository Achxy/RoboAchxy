def no_modifier(*prefixes):
    def inner(bot, message):
        return prefixes

    return inner
