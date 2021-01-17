import requests
import threading
from queue import Queue
from time import sleep
import os

#=========================Globals=========================

files_list = Queue()

#===================Thread=Functions========================

def create_files_list(username):
    import os
    files_list = globals()['files_list']
    for address, dirs, files in os.walk(f'./users/{username}'):
        for file in files:
            filename_sys = os.path.join(address, file)
            filename_serv = os.path.join(address[len('./server_files') + 1:], file)
            files_list.put({'sys': filename_sys, 'serv': filename_serv})

#=======================Main==============================


def main(username):
    creator = threading.Thread(target=create_files_list, args=(username,))
    creator.start()

    for repeats in range(5):
        thread = Sender(files_list)
        thread.setDaemon(True)
        thread.start()

    creator.join()
    files_list.join()
    return












