from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand

from .data_source import get_weather_of_city

from jieba import posseg

# ································································································
# weather功能运行流程：
# 1.后端识别到前端发送的语句中存在关键词“天气”，进入weather模块
# 2.进入on_natural_language模块进行结巴分词，提取city
# 3.处理结束后，调用IntentCommand()，其中声明’weather‘表明跳转到weather()，并通过CommandSession携带city
# 4.weather()函数获取city的值，调用data_source.get_weather_of_city()查询天气
# 5.最后，使用session中的send()，将天气从send中传输到前端
# ································································································

__plugin_name__ = '天气'
__plugin_usage__ = r"""
天气查询

天气  [城市名称]
"""


@on_command('weather', aliases=('天气', '天气预报', '查天气', '预报'))
async def weather(session: CommandSession):
    print(123)
    city = session.current_arg_text.strip()
    if not city:
        city = (await session.aget(prompt='你想查询哪个城市的天气呢？')).strip()
        while not city:
            city = (await session.aget(prompt='要查询的城市名称不能为空呢，请重新输入')).strip()
    weather_report = await get_weather_of_city(city)
    await session.send(weather_report)

# on_natural_language 装饰器将函数声明为一个自然语言处理器
# keywords 表示需要响应的关键词，类型为任意可迭代对象，元素类型为 str
# 如果不传入 keywords，则响应所有没有被当作命令处理的消息
@on_natural_language(keywords={'天气'}, only_to_me=True)
async def _(session: NLPSession):
    print(456)
    # 去掉消息首尾的空白符
    stripped_msg = session.msg_text.strip()
    # 对消息进行分词和词性标注
    words = posseg.lcut(stripped_msg)

    city = None
    # 遍历 posseg.lcut 返回的列表
    for word in words:
        # 每个元素是一个 pair 对象，包含 word 和 flag 两个属性，分别表示词和词性
        if word.flag == 'ns':
            #print(12345)
            # ns 词性表示地名
            city = word.word
            break

    # 返回意图命令，前两个参数必填，分别表示置信度和意图命令名
    return IntentCommand(90.0, 'weather', current_arg=city or '')