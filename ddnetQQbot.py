from qqbot import _bot as bot
import time
import csv
import requests
import json
import threading

from getServerInfo import Server_Info

servers_CHNTom = [[('119.29.57.22', 8304), 0],
                 [('119.29.57.22', 8403), 0],
                 [('119.29.57.22', 7321), 0],
                 [('119.29.57.22', 7304), 0],
                 [('119.29.57.22', 7317), 0],
                 [('119.29.57.22', 8303), 0],
                 [('119.29.57.22', 8203), 0],
                 [('119.29.57.22', 8406), 0],
                 [('119.29.57.22', 8409), 0],
                 [('119.29.57.22', 8200), 0],
                 [('119.29.57.22', 7303), 0],
                 [('119.29.57.22', 8404), 0],
                 [('119.29.57.22', 8410), 0],
                 [('119.29.57.22', 8201), 0],
                 [('119.29.57.22', 8408), 0],
                 [('119.29.57.22', 8202), 0],
                 [('119.29.57.22', 7306), 0],
                 [('119.29.57.22', 7400), 0],
                 [('119.29.57.22', 8407), 0],
                 [('119.29.57.22', 7401), 0],
                 [('119.29.57.22', 8305), 0],
                 [('119.29.57.22', 8402), 0],
                 [('119.29.57.22', 7305), 0]]

#get the players list to Tom Servers in another thread every 30s
last_players_list = []
lock = threading.Lock()

def get_servers_info():
    global last_players_list
    while True:
        servers_info = []
        #print(str(len(servers_CHNTom)) + " servers")
        for server in servers_CHNTom:
            #[('47.74.9.32', 8303), 0]
            s = Server_Info(server[0], server[1])
            servers_info.append(s)
            s.start()
            time.sleep(0.001) # avoid issues

        num_players = 0
        num_clients = 0

        servers_info_list = []

        while len(servers_info) != 0:
            if servers_info[0].finished == True:
                if servers_info[0].info:
                    servers_info_list.append(servers_info[0].info)
                    num_players += servers_info[0].info["num_players"]
                    if servers_info[0].type == 0:
                        num_clients += servers_info[0].info["num_clients"]
                    else:
                        num_clients += servers_info[0].info["num_players"]

                del servers_info[0]

            time.sleep(0.001) # be nice
        #print(str(num_players) + " players and " + str(num_clients-num_players) + " spectators")

        player_list = []
        for servers_info in servers_info_list:
            if servers_info['players']:
                for player_info in servers_info['players']:
                    player_list.append(player_info['name'].decode())
        lock.acquire()
        try:
            last_players_list = player_list
            print("get data successfully")
            time.sleep(30)
        finally:
            # 改完了一定要释放锁:
            lock.release()

info_thread = threading.Thread(target=get_servers_info)
info_thread.start()


#-u参数表示使用某用户的设置文件登录
#这里需要更改qqbot的设置文件~/.qqbot-tmp/v2.3.conf？
#参考qqbot项目的说明
print("test get server info")
print(last_players_list)

bot.Login(['-u', '2143738142'])

#这里改为你的群名
mainGroup = bot.List('group', 'TeeWorlds中国社区')[0] #2960233702
print("mainGroup.uin: ", mainGroup.uin)
chatGroup = bot.List('group', 'Teeworlds闲聊群')[0] #1516349281
print("chatGroup.uin: ",chatGroup.uin)
isChatGroup = False

#读取词典
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

#读取好友列表
friendFile = "friendList.txt"
friendDict = {}
with open(friendFile, 'r') as f:
    spamreader = csv.reader(f, delimiter=',')
    for row in spamreader:
        if not row:
            continue
        if row[0].startswith('#'):
            print(row)
        else:
            friendDict[row[0]] = map(list, zip(row[1:],([0]*len(row[1:]))))

#图灵机器人平台的API
chatAPI = "http://www.tuling123.com/openapi/api"
requestJson = {"key": "692b5c941e7a43e2be89b1047b605049","info": "", "userid":""}


players_list = []
print(bot.List('buddy'))
#无限轮询消息并作出相应回应
while True:
    time.sleep(2)
    fromType, groupNumber, fromNumber, content = bot.poll()
    print (fromType, groupNumber, fromNumber, content)
    for qqNickName in friendDict:
        for friend in friendDict[qqNickName]:
            if players_list != last_players_list:
                if friend[0] in last_players_list:
                    if friend[1] == 0:
                        players_list = last_players_list
                        myQQId = bot.List('buddy', qqNickName)[0]
                        print(myQQId)
                        bot.SendTo(myQQId, "你的好友{}上线了。".format(friend[0]))
                        friend[1] = 1
                    else:
                        pass
                else:
                    friend[1] = 0
            else:
                pass
    keywordInContent = False
    if groupNumber == mainGroup.uin:
        sendtoGroup = mainGroup
        print("来自主群的消息")
        isChatGroup = False
    elif groupNumber == chatGroup.uin:
        sendtoGroup = chatGroup
        print("来自闲聊群的消息")
        isChatGroup = True
    #这里改为你的ID
    if "大家好" in content:
        bot.SendTo(sendtoGroup, "欢迎新人～如果有什么游戏相关的问题可以带上问号“？”并且@我向我提问～")
    if "@brainfullyTEE" in content:
        print ("@我的消息")
        if "player" in content:
            players_list = last_players_list
            if len(players_list) == 0:
                sendStr = "目前没人在线."
            else:
                sendStr = ("目前在线玩家数为{}，分别为:".format(len(players_list))) + (", ".join(players_list))
            bot.SendTo(sendtoGroup, sendStr)
        elif "?" in content or "？" in content:
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
