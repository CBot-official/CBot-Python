import socket
from config import *

sockChan = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sockChan.connect((BotServer, BotPort))

def SendIRC (msg):
  sockChan.sendall(bytes(f'{str(msg)} \r\n', 'UTF-8'))
  
SendIRC(f'USER {BotIdent} * * :{BotRealname}')
SendIRC(f'NICK {BotNick}')
connected = True

def main():
    try:
        while connected:

            line = sockChan.recv(2040).decode('UTF-8')
            print(line)
            if line != "":
                lline = line.split()
            if 'PING' in lline[0]:
                SendIRC(f'PONG {lline[1]}')

            if '433' in lline[0]:
                SendIRC(f'NICK {BotAlt}')

            if '001' in lline[0]:
                SendIRC(f'JOIN {BotHome}')

            if 'PRIVMSG' in lline[1]:
                zline = lline.split('!')
                zline = zline.split(':')
                zline = zline.split('@')
                nick = zline[0]
                ident = zline[1]
                host = zline[2]
                targ = zline[4]
                text = zline[5]

            if 'NOTICE' in lline[1]:
                zline = lline.split('!')
                zline = zline.split(':')
                zline = zline.split('@')
                nick = zline[0]
                ident = zline[1]
                host = zline[2]
                targ = zline[4]
                text = zline[5]


    except: 
        print('fuck it broke')         

main()
