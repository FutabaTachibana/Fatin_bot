#FATIN-BOT\plugins\wordle.py
#wordle插件的源文件


import random
import sqlite3

#导入nonebot库
from nonebot import on_command, CommandSession

#词库数量
WORDLIST_LENGTH = 2519

STR_PRE_START = '''现在以一个随机的单词进行新的游戏
要退出游戏 你可以发送exit
现在请发送一个单词'''
STR_HELP = '''输入一个含有5个字母的英文单词以开始游戏
在开始游戏后 计算机会随机生成一个单词 你一共有6次机会猜出那个单词
每当你发送一个可能的单词后 机器人会发送一行提示
🟩代表单词中该位置的字母是正确的
🟨代表单词中含有这个字母 但不在这个位置
⬜代表单词中没有这个字母'''
STR_USAGE = '''用法: 
>>>.wordle 显示此消息
>>>.wordle new 以一个随机的单词进行新的游戏
>>>.wordle stat 查看统计列表(待加入)
>>>.wordle help 显示游戏玩法
符号>>>提示你输入的内容 指令提示符.不可省'''


#对输入单词进行分析
def comp_result (base, dest): 
    ch_return = []
    for (ch, i) in zip(dest, range(5)):

        #字母正确且位置正确
        if base[i] == dest[i]:
            ch_return.append('🟩')
        
        #字母正确但位置错误  
        elif dest[i] in base:
            ch_return.append('🟨')
        
        #字母错误    
        else:
            ch_return.append('⬜')
    
    return ''.join(ch_return)

#在wordlist.db中生成一个随机的单词
def make_random_word(curs):
    rand = random.randint(0, WORDLIST_LENGTH - 1)
    res = curs.execute('SELECT WORD FROM list WHERE ID = {};'.format(rand))
    for word in res:
        return word[0]

#判断是否为一个合法的单词
def is_valid(word, curs):
    res = curs.execute('SELECT WORD FROM list WHERE WORD = \'{}\';'.format(word))
    word = None
    for word in res:
        pass
    return True if word else False

#进行wordle游戏
async def play(session: CommandSession):
    #打开wordlist.bd
    wordlist_conn = sqlite3.connect('.\\resource\\wordlist.db')
    wordlist_curs = wordlist_conn.cursor()

    #在wordlist.db中生成一个随机的单词
    correct_word = make_random_word(wordlist_curs)
    times = 0
    result = '\n'

    #该代码行仅用于调试
    #print(correct_word)

    #游戏主结构
    while times < 6:
        #询问输入
        input_word = (await session.aget()).strip()
        
        #输入exit
        if input_word == 'exit':
            await session.send('{} / 6\n{}\n已结束游戏\n正确的单词是{}哦\n'.format(times, result, correct_word))
            return

        #处理不正确的输入
        if len(input_word) != 5 or not is_valid(input_word, wordlist_curs):
            await session.send('请发送一个含有5个字母的正确单词')
            continue

        #输入正确的单词
        if input_word == correct_word:
            result += comp_result(correct_word, input_word) + '\n'
            await session.send('{} / 6\n'.format(times + 1) + result + '\n恭喜你!\n正确的单词是{}\n你仅用了{}次就猜中了!'.format(correct_word, times + 1))
            break

        #前五次输入不正确的单词
        if times != 5:
            result += comp_result(correct_word, input_word) + '\n'
            await session.send('{} / 6\n'.format(times + 1) + result + '\n请再次发送一个单词')
        times += 1

    #第六次输入不正确的单词
    else:
        result += comp_result(correct_word, input_word) + '\n'
        await session.send('6/ 6\n' + result + '\n正确的单词是' + correct_word + '哦\n请再接再厉!')

#根据参数调用不同的函数
@on_command('wordle')
async def wordle(session: CommandSession):
    args = session.current_arg_text.strip()
    #await session.send(args)

    if not args:
        #未匹配到任何参数时 显示用法
        await session.send(STR_USAGE)
    
    elif args == 'new':
        #匹配到参数'new' 以一个随机的单词进行新的游戏
        await session.send(STR_PRE_START)
        await play(session)

    elif args == 'help':
        #匹配到参数'help' 显示STR_HELP
        await session.send(STR_HELP)
    
    else:
        #处理不存在的参数
        await session.send(args + '是一个无效的参数\n' + STR_USAGE)
    


