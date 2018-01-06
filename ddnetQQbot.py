from qqbot import _bot as bot
import time
import csv
import requests
import json

#这里改为你的q号？
bot.Login(['-q', '2143738142'])

#这里改为你的群名
mainGroup = bot.List('group', 'TeeWorlds中国社区')[0] #2960233702
chatGroup = bot.List('group', 'Teeworlds闲聊群')[0] #1516349281
isChatGroup = False

#for test
#mainGroup = bot.List('group')[1]

replyFile = "autoReply.txt"
replyDict = {}
with open(replyFile, 'r') as f:
    spamreader = csv.reader(f, delimiter=',')
    for row in spamreader:
        if not row:
            continue
        if row[0].startswith('#'):
            print(row)
        else:
            replyDict[row[0]] = row[1]

chatAPI = "http://www.tuling123.com/openapi/api"
requestJson = {"key": "692b5c941e7a43e2be89b1047b605049","info": "", "userid":""}

while True:
    time.sleep(2)
    fromType, groupNumber, fromNumber, content = bot.poll()
    print (fromType, groupNumber, fromNumber, content)
    keywordInContent = False
    if groupNumber == "2960233702":
        sendtoGroup = mainGroup
        print("来自主群的消息")
        isChatGroup = False
    elif groupNumber == "1516349281":
        sendtoGroup = chatGroup
        print("来自闲聊群的消息")
        isChatGroup = True
    #这里改为你的ID
    if "@brainfullyTEE" in content:
        print ("@我的消息")
        if "?" in content or "？" in content:
            for keyword in replyDict:
                if keyword.lower() in content.lower():
                    bot.SendTo(sendtoGroup, replyDict[keyword])
                    keywordInContent = True
            if not keywordInContent:
                bot.SendTo(sendtoGroup, "不好意思，你所说的关键词尚未收录。快去https://github.com/QingGo/ddnetQQbot 贡献词库吧。如果要进行普通对话请不要带问号。")
        else:
            if isChatGroup:
                requestJson["info"] = content.replace("@brainfullyTEE ","")
                requestJson["userid"] = fromNumber
                respone = requests.post(chatAPI, requestJson)
                responeContent = json.loads(respone.text)
                bot.SendTo(sendtoGroup, responeContent["text"]+responeContent.get("url", ""))
            else:
                bot.SendTo(sendtoGroup, "询问关键词的话请加上问号")
