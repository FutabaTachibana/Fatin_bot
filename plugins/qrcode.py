#FATIN-BOT\plugins\qrcode.py
#qrcode插件的源文件


from nonebot import on_command, CommandSession
import re

def qrcode_decode():
    pass

def qrcode_encode():
    pass

@on_command('qrcode', aliases = ('二维码', 'QRcode', 'QRCode', 'Qrcode', 'QRCODE'))
async def qrcode(session : CommandSession):
    input = session.current_arg.strip()
    
    input_img = re.match("\[CQ:image,file=.+", input)

    if input_img:
        await session.send('你发送了一张图片')
        #qrcode_decode(input_img)
    else:
        await session.send('你发送了一串url')
        #qrcode_encode(input)

    pass