#FATIN-BOT\plugins\searchpic.py
#搜图工具

from nonebot import CommandSession, on_command
from selenium import webdriver
import time
import re

CQ_RE = '(https://gchat.qpic.cn/gchatpic_new/.*)]'
LABEL_RE = '<a target="_blank" rel="noopener" href="(https?://(?:[^\./]+)(?:\.[^\./]+)+(?:/[^\./]+)+/?)">([^<]*)</a>'

def info_get(url):
    #打开Firefox浏览器
    driver = webdriver.Firefox()

    #访问网站
    driver.implicitly_wait(20)
    driver.get("https://ascii2d.net/")

    #对元素进行操作
    driver.find_element_by_id("uri-form").send_keys(url)
    driver.find_elements_by_name("search")[0].click()

    #下载html文件
    html = driver.execute_script("return document.documentElement.outerHTML")

    #等待
    time.sleep(1)

    #关闭Firefox浏览器
    driver.close()

    #使用正则表达式查找结果
    
    comp = re.compile(LABEL_RE)
    match = comp.findall(html)

    #在结果输出前需要等待一定的时间 防止客户端过多访问数据
    #time.sleep(2)

    #将结果输出
    return match


@on_command('searchpic', aliases=('搜图', '以图搜图'))
async def searchpicbypic(session : CommandSession):
    arg = session.current_arg
    comp = re.compile(CQ_RE)
    url = comp.findall(arg)
    while not url:
        await session.send("请发送一张图片")
        arg = await session.aget()
        url = comp.findall(arg)

    #await session.send(url[0])
    if url:
        res = info_get(url[0])
    
    #await session.send(str(res))

    str_res = '\n'.join(' : '.join(res[i]) for i in range(len(res)))
    await session.send("Fatin为你找到如下结果:\n" + str_res)

    