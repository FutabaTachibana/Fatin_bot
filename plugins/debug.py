from nonebot import CommandSession, on_command

@on_command('alive', aliases = ('heartbeat', '存活', '存活确认'))
async def alive(session : CommandSession):
    await session.send('STATUS OK: ' + session.current_arg.strip())
