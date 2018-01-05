from qqbot import _bot as bot
import time
import csv

bot.Login(['-q', '2143738142'])

g = bot.List('group', 'TeeWorlds中国社区')[0]

#for test
#g = bot.List('group')[1]

replyFile = "autoReply.txt"
replyDict = {}
with open(replyFile, 'r') as f:
    spamreader = csv.reader(f, delimiter=',')
    for row in spamreader:
        replyDict[row[0]] = row[1]

while True:
    time.sleep(2)
    fromType, fromNumber, groupNumber, content = bot.poll()
    print (fromType, fromNumber, groupNumber, content)
    keywordInContent = False
    if "@brainfullyTEE" in content:
        print ("@我的消息")
        if "?" in content or "？" in content:
            for keyword in replyDict:
                if keyword.lower() in content.lower():
                    bot.SendTo(g, replyDict[keyword])
                    keywordInContent = True
        else:
            bot.SendTo(g, "询问关键词的话请加上问号")
        if not keywordInContent:
            bot.SendTo(g, "不好意思，你所说的关键词尚未收录。快去https://github.com/QingGo/ddnetQQbot贡献词库吧。")
