# ddnetQQbot

## To-Do List
- 完善游戏词库和wiki
- 使用分词或者文本识别之类的方法完善回应逻辑

## 项目简介
A customize QQ bot for China TeeWorlds/DDNet community.

为teeworlds中国社区QQ群而写的迎新自动回复机器人。

## 环境需求
- Python 3
- Python的qqbot库，项目地址：https://github.com/pandolia/qqbot

安装方法：
> pip install qqbot

## 使用方法：
通过
> git clone git@github.com:QingGo/ddnetQQbot.git

下载代码包，或者下载zip包再解压。

然后在命令行下进入ddnetQQbot目录，输入
> python ddnetQQbot.py

启动机器人。然后用手机QQ客户端扫描二维码即可登录成功。

## 增加词库的方法
先点右上角的Fork复制我的代码到你自己的代码库。然后更改其中的autoReply.txt文件，其格式为

>#以#开头的行为注释，空行则直接忽略

>"关键词1", "回复内容1"

>"关键词2", "回复内容2"

>...

- 注意双引号和逗号要使用英文的半角符号。
- 关键词里的英文是大小写不敏感的，比如ddnet和DDnet表示同一个关键词。
- 不要重复添加关键词。

修改完关键词以后再向我的dev分支发起Pull request，让我来合并内容。
