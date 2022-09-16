from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand

@on_command('statistics', only_to_me=False, patterns=('.*'))
async def statistics(session: CommandSession):
    print("success")
    message = session.current_arg
    print(message)