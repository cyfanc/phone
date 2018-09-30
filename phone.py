#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import re
import os
import sys
import queue
import string
import threading
import requests
type = sys.getfilesystemencoding()

class phone:
    def __init__(self):
        self.f=''
        self.threads=[]
        self.mu=threading.Lock()
        self.urlQue=queue.Queue()
        self.url='http://shouji.ip38.com/'

    def write_file(self,res):
        print (res)
        if self.f == '':
            self.f = open("phone.txt", "w+", encoding="UTF-8")
        if self.mu.acquire(True):
            self.f.write(res+'\n')
            self.f.flush()
            self.mu.release()

    def create_phone_num(self):
        for i in range(1300000,1999999):
            self.urlQue.put(self.url + str(i) + '7302.html')

    def get_phone_thread(self):
        for i in range(0,100):
            self.threads.append(threading.Thread(target=self.get_phone_num,args=()))

    def start(self):
        for t in self.threads:
            t.setDaemon(True)
            t.start()
        t.join()

    def get_phone_num(self):
        while not self.urlQue.empty():
            url=self.urlQue.get()
            try:
                r = requests.get(url)
                if r.status_code == 200:
                    pattern = re.compile("</span>([^<]*)")
                    result = pattern.findall(r.content.decode(type))
                    if(result[2] != '' and result[5] != ''):
                        self.write_file('%s|%s|%s|%s' % (result[7][0:7],result[6],result[5],result[2]))
            except:
                self.urlQue.put(url)

    def run(self):
        self.create_phone_num()
        self.get_phone_thread()
        self.start()

if __name__ == '__main__':
    phone().run()
