'''
@Date: 2020-04-07 14:33:41
@LastEditors: code
@Author: code
@LastEditTime: 2020-05-02 15:26:58
'''
from nonebot import on_command, CommandSession
from aiocqhttp.exceptions import Error as CQHttpError
import nonebot
from datetime import datetime
# from nonebot import on_natural_language, NLPSession, IntentCommand
from .datastore import db, ArtWork, SingleImage2, fn
from typing import List, Tuple
import json
import urllib
import httpx
import asyncio

MAX_COUNT = 6
MIN_COUNT = 1


@on_command('pixiv', aliases=('色图', '涩图', '来份色图'))
async def pixiv(session: CommandSession):
    # session.event.group_id
    # session.event.operator_id
    illust_msg: str = session.get(session.current_key, prompt='gkd mode')
    illust_type = get_illust_type(illust_msg)
    illust_count = first_number(illust_msg)
    if illust_count > MAX_COUNT:
        illust_count = MAX_COUNT
    elif illust_count < MIN_COUNT:
        illust_count = MIN_COUNT
    print(
        f'illust_type:{illust_type}, illust_count:{illust_count}, illust_msg:{illust_msg}')
    short_urls = await get_short_url(illust_count, illust_type)
    msg_text = '\n\n'.join(short_urls)
    await session.send(f'{msg_text}')
    session.pause()


def get_illust_type(string: str) -> int:
    type_dict = {
        '插画': 0,
        '漫画': 1,
        '动图': 2,
    }
    for type_str in type_dict:
        if type_str in string:
            return type_dict[type_str]
    return type_dict['插画']


def first_number(s: str, default_num=1) -> int:
    num = '0123456789'
    s1 = ''
    for s2 in s:
        if s2 in num:
            s1 += s2
            if len(s1) >= 2:
                break
        else:
            continue
    if len(s1) == 0:
        return default_num
    else:
        return int(s1)


@pixiv.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()

    if session.is_first_run:
        if stripped_arg:
            session.state[session.current_key] = stripped_arg
        return

    if (not stripped_arg) or len(list(filter(lambda v: v in stripped_arg, ['插画', '漫画', '动图', *'123456789']))) == 0:
        session.pause('')

    if '退出' in stripped_arg:
        session.finish('已退出')

    session.state[session.current_key] = stripped_arg


async def get_short_url(illust_count: int = 0, illust_type: int = None) -> List[str]:
    if illust_type == None:
        illust_type = 0
    condition = ArtWork.illust_type == illust_type
    db.connect()
    db.create_tables([ArtWork, SingleImage2])
    artworks: ArtWork = (ArtWork.select()
                         .where(ArtWork.is_full_upload == True, condition)
                         .order_by(fn.Random())
                         .limit(illust_count))
    long_urls: List[str] = []
    for artwork in artworks:
        single_images = SingleImage2.select().where(
            SingleImage2.illust_id == artwork.illust_id)
        object_ids = json.dumps(
            list(map(lambda single_image: str(single_image.object_id), single_images)))
        object_ids = urllib.parse.quote(object_ids)
        long_url = f'https://lisonge.gitee.io/pixiv/chaoxing_show.html?illust_id={artwork.illust_id}&object_ids={object_ids}'
        long_urls.append(long_url)
    db.close()
    short_urls = await shorten_urls(long_urls)
    return short_urls


async def shorten_url(client: httpx.AsyncClient, url: str) -> str:
    api_url = 'https://api.uomg.com/api/long2dwz'
    params = {
        'url': url,
        'dwzapi': 'tcn'
    }
    try:
        reponse = await client.get(api_url, params=params)
        short_url: str = reponse.json()['ae_url']
        if len(short_url) > 5:
            return short_url[short_url.find('t.cn'):]
    except Exception as e:
        print(e)
    return ''


async def shorten_urls(long_urls: List[str]) -> List[str]:
    short_urls: List[str] = []
    async with httpx.AsyncClient() as client:
        client: httpx.AsyncClient
        short_urls = await asyncio.gather(*list(map(lambda url: shorten_url(client, url), long_urls)))
    return short_urls
# '[CQ:rich,text=战友星计划 | 赢万元大奖 给CFer们的一封信&amp;#44;致敬敢突破的你,url=https://cfm.qq.com/cp/a20200421zyxjh/index.html?xxx=kdb3c751ce5edac14037c08a9541a4b6df&amp;amp;ADTAG=tgi.qq.share.qq]'


@nonebot.scheduler.scheduled_job('cron', hour='*')
async def _():
    bot = nonebot.get_bot()
    now = datetime.now()
    group_ids = [892309127]
    short_urls = await get_short_url(6)
    msg_text = '\n\n'.join(short_urls)
    for group_id in group_ids:
        try:
            await bot.send_group_msg(
                group_id=group_id,
                message=f'现在是{now.hour}点\n{msg_text}'
            )
        except CQHttpError:
            pass


@nonebot.scheduler.scheduled_job('cron', hour='3,10,14,18,22')
async def cfm_star():
    bot = nonebot.get_bot()
    msg_text = '战友星计划 | 赢万元大奖\nhttps://cfm.qq.com/cp/a20200421zyxjh/index.html?xxx=kdb3c751ce5edac14037c08a9541a4b6df'
    group_ids = [42381896, 117492014, 138544585, 149336576, 250597091, 290223818, 319344559, 324321441, 342117818, 379021504, 389371351, 432093651, 439868924, 452165170, 488102079, 511582741, 528207955, 531966885, 535200910, 537131311, 546439138, 579694959, 593038638, 613251876, 613790573, 633059287, 639744882, 650093067,
                 666736249, 697705017, 701042369, 717729962, 727144576, 753252486, 755616462, 756731698, 805194362, 807757593, 815345852, 826615165, 923853415, 930264331, 933432460, 948688626, 955377501, 955818228, 966657240, 1001984530, 1002680716, 1018879593, 1041050666, 1041751461, 1049762004, 1060195976, 1064156151]
    for group_id in group_ids:
        try:
            await bot.send_group_msg(
                group_id=group_id,
                message=msg_text
            )
        except Exception:
            pass
