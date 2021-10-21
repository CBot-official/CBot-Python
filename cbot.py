#!/usr/bin/python3
#
#

import os
import sys
import time
import socket
import string
import logging
from config import *

dirName = os.path.dirname(os.path.abspath(__file__))
logname = f'{dirName}/{LogFileName}.log'
#handlers = [logging.FileHandler(logname), logging.StreamHandler()]
handlers = [logging.FileHandler(logname)]
logging.basicConfig(
				handlers=handlers,
				level=logging.DEBUG,
				format='%(asctime)s %(levelname)s - %(message)s',
				datefmt='%Y-%m-%d %H:%M:%S'
			)

log = logging.getLogger() 

sockChan = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sockChan.connect_ex((BotServer, BotPort))


def sendIRC(msg):
    sockChan.sendall(bytes(f'{str(msg)} \r\n', 'UTF-8')) # Send data to IRC server.
    if DebugMode:
        print(f'Sending to Server: {msg}')


def sendmsg(msg, target=BotHome): # Sends messages to the target.
    ircsend(f'PRIVMSG {target} :{msg}') 


sendIRC(f'USER {BotIdent} * * :{BotRealName}') #Command: USER Parameters: <user> <mode> <unused> <realname>
sendIRC(f'NICK {BotNick}')

if BotPassword != '':
    sendIRC(f'PRIVMSG NICKSERV :IDENTIFY {BotPassword}')

connected = True

def main():
    try:
        while connected:

            line = sockChan.recv(2040).decode('utf-8')

            if DebugMode:
                print(line)
    
            lline = line.split() 
            if 'PING' in lline[0]:
                sendIRC(f'PONG {lline[1]}' )
            if '001' in str(lline[1]):
                if BotHome != '':
                    sendIRC(f'JOIN {BotHome}' )
            if '433' in lline[1]:
                sendIRC(f'NICK {BotAlt}' )

            if 'PRIVMSG' in lline[1]:
                if '!quit' in lline[3]:                
                    sendIRC(f'QUIT {QuitMessage}' )
                    sys.exit()
                if '!join' in lline[3]:
                    sendIRC(f'JOIN {lline[4]}' )
                if '!part' in lline[3]:
                    sendIRC(f'PART {lline[4]}' )
                if '!danceBtch' in lline[3]:
                    sendmsg("""＼(ﾟｰﾟ＼) (ノ^_^)ノ(~‾▿‾)~ """)

    except Exception as iconnex: 
        if DebugMode:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]             
            print(f'Exception: {str(iconnex)}')
            print(f'Failed to connect to {str(server)}:{str(port)}. Retrying in 10 seconds...')
        logging.exception('\n\n\n =========================    --ERROR--    =======================================================================================================================================================================================================================================================================================================================\n ')
            


main()
