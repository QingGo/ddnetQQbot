
# coding: utf-8

# In[1]:


from socket import *
import struct
import sys
import threading
import time


# In[2]:


NUM_MASTERSERVERS = 4
MASTERSERVER_PORT = 8300

TIMEOUT = 2

SERVERTYPE_NORMAL = 0
SERVERTYPE_LEGACY = 1

PACKET_GETLIST = b"\x20\x00\x00\x00\x00\x00\xff\xff\xff\xffreqt"
PACKET_GETLIST2 = b"\x20\x00\x00\x00\x00\x00\xff\xff\xff\xffreq2"
PACKET_GETINFO = b"\xff\xff\xff\xff\xff\xff\xff\xff\xff\xffgief"
PACKET_GETINFO2 = b"\xff\xff\xff\xff\xff\xff\xff\xff\xff\xffgie2" + b"\x00"
PACKET_GETINFO3 = b"\xff\xff\xff\xff\xff\xff\xff\xff\xff\xffgie3" + b"\x00"



class Server_Info(threading.Thread):

    def __init__(self, address, type):
        self.address = address
        self.type = type
        self.finished = False
        threading.Thread.__init__(self, target = self.run)

    def run(self):
        self.info = None
        if self.type == SERVERTYPE_NORMAL:
            self.info = get_server_info3(self.address)
        elif self.type == SERVERTYPE_LEGACY:
            self.info = get_server_info(self.address)
            if self.info:
                self.info = get_server_info2(self.address)
        self.finished = True


def get_server_info(address):
    try:
        sock = socket(AF_INET, SOCK_DGRAM)
        sock.settimeout(TIMEOUT);
        sock.sendto(PACKET_GETINFO, address)
        data, addr = sock.recvfrom(1024)
        sock.close()

        data = data[14:] # skip header
        slots = data.split(b"\x00")

        server_info = {}
        server_info["version"] = slots[0]
        server_info["name"] = slots[1]
        server_info["map"] = slots[2]
        server_info["gametype"] = slots[3]
        server_info["flags"] = int(slots[4])
        server_info["progression"] = int(slots[5])
        server_info["num_players"] = int(slots[6])
        server_info["max_players"] = int(slots[7])
        server_info["players"] = []

        for i in range(0, server_info["num_players"]):
            player = {}
            player["name"] = slots[8+i*2]
            player["score"] = int(slots[8+i*2+1])
            server_info["players"].append(player)

        return server_info

    except Exception as e:
        #print(e)
        return None


def get_server_info2(address):
    try:
        sock = socket(AF_INET, SOCK_DGRAM)
        sock.settimeout(TIMEOUT);
        sock.sendto(PACKET_GETINFO2, address)
        data, addr = sock.recvfrom(1024)
        sock.close()

        data = data[14:] # skip header
        slots = data.split(b"\x00")

        server_info = {}
        server_info["token"] = slots[0]
        server_info["version"] = slots[1]
        server_info["name"] = slots[2]
        server_info["map"] = slots[3]
        server_info["gametype"] = slots[4]
        server_info["flags"] = int(slots[5])
        server_info["progression"] = int(slots[6])
        server_info["num_players"] = int(slots[7])
        server_info["max_players"] = int(slots[8])
        server_info["players"] = []

        for i in range(0, server_info["num_players"]):
            player = {}
            player["name"] = slots[9+i*2]
            player["score"] = int(slots[9+i*2+1])
            server_info["players"].append(player)

        return server_info

    except Exception as e:
        #print(e)
        return None


def get_server_info3(address):
    try:
        sock = socket(AF_INET, SOCK_DGRAM)
        sock.settimeout(TIMEOUT);
        sock.sendto(PACKET_GETINFO3, address)
        data, addr = sock.recvfrom(1400)
        sock.close()

        data = data[14:] # skip header
        slots = data.split(b"\x00")

        server_info = {}
        server_info["token"] = slots[0]
        server_info["version"] = slots[1]
        server_info["name"] = slots[2]
        server_info["map"] = slots[3]
        server_info["gametype"] = slots[4]
        server_info["flags"] = int(slots[5])
        server_info["num_players"] = int(slots[6])
        server_info["max_players"] = int(slots[7])
        server_info["num_clients"] = int(slots[8])
        server_info["max_clients"] = int(slots[9])
        server_info["players"] = []

        for i in range(0, server_info["num_clients"]):
            player = {}
            player["name"] = slots[10+i*5]
            player["clan"] = slots[10+i*5+1]
            player["country"] = int(slots[10+i*5+2])
            player["score"] = int(slots[10+i*5+3])
            if int(slots[10+i*5+4]):
                player["player"] = True
            else:
                player["player"] = False
            server_info["players"].append(player)

        return server_info

    except Exception as e:
        #print(e)
        return None



class Master_Server_Info(threading.Thread):

    def __init__(self, address):
        self.address = address
        self.finished = False
        threading.Thread.__init__(self, target = self.run)

    def run(self):
        self.servers = get_list(self.address) + get_list2(self.address)
        self.finished = True


def get_list(address):
    servers = []

    try:
        sock = socket(AF_INET, SOCK_DGRAM)
        sock.settimeout(TIMEOUT)
        sock.sendto(PACKET_GETLIST, address)

        while 1:
            data, addr = sock.recvfrom(1024)

            data = data[14:]
            num_servers = len(data) // 6

            for n in range(0, num_servers):
                ip = ".".join(map(str, map(int, data[n*6:n*6+4])))
                port = int(data[n*6+5]) * 256 + int(data[n*6+4])
                servers += [[(ip, port), SERVERTYPE_LEGACY]]

    except Exception as e:
        #print(e)
        sock.close()

    return servers


def get_list2(address):
    servers = []

    try:
        sock = socket(AF_INET, SOCK_DGRAM)
        sock.settimeout(TIMEOUT)
        sock.sendto(PACKET_GETLIST2, address)

        while 1:
            data, addr = sock.recvfrom(1400)

            data = data[14:]
            num_servers = len(data) // 18

            for n in range(0, num_servers):
                if data[n*18:n*18+12] == b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff":
                    ip = ".".join(map(str, map(int, data[n*18+12:n*18+16])))
                else:
                    ip = ":".join(map(str, map(int, data[n*18:n*18+16])))
                port = (int(data[n*18+16])<<8) + int(data[n*18+17])
                servers += [[(ip, port), SERVERTYPE_NORMAL]]

    except Exception as e:
        #print(e)
        sock.close()

    return servers
