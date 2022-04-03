#FATIN-BOT\plugins\tools.py
#一系列有用无用的小工具
from nonebot import CommandSession, on_command
import random

@on_command('random', aliases = ('Random', 'rand', '随机数', 'Rand', '随机'))
async def rand(session : CommandSession):
    arg = session.current_arg.strip()
    if arg:
        if '~' in arg:
            args = arg.split('~')
            await session.send(str(random.randrange(int(args[0]), int(args[1]))))
        else:
            args = arg.split()
            if len(args) == 1:
                try:
                    await session.send(str(random.randrange(1, int(session.current_arg))))
                except ValueError:
                    await session.send("唔...Fatin好像不太懂你的意思呢...")
            else:
                await session.send(random.choice(args))
    else:
        await session.send("唔...Fatin好像不太懂你的意思呢...")

    


