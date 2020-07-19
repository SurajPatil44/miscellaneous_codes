# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 10:34:20 2020

@author: sdpatil
"""

import os,time
from collections import namedtuple
from threading import Thread
from queue import Queue
import requests

###Boilar plate

TIMEOUT2 = 20 ###inactivity in thread2
TIMEOUT1 = 5  ###inactivity in thread1

_url = "https://yesno.wtf/api"
yes_directory = r"./GIFs/yes_threaded"
no_directory = r"./GIFs/no_threaded"
maybe_directory = r"./GIFs/maybe_threaded"

__script_dir__ = os.getcwd()

if not os.path.exists(yes_directory):
    os.makedirs(yes_directory)
    
if not os.path.exists(no_directory):
    os.makedirs(no_directory)

if not os.path.exists(maybe_directory):
    os.makedirs(maybe_directory)

###Main subroutine
    
class GIFSaver:
    
    def __init__(self,_iter):
        self.rspq = Queue(10)
        self.dataq = Queue(5)
        self.iter = _iter
        self.stop_flag = False
        self.time_wait_t1 = 0
        self.time_wait_t2 = 0
    
    def fetch_url_and_answer(self):
        n = 0
        while not self.stop_flag:
            resp = namedtuple("Response",["answer","url"])
            raw = requests.get(_url)
            raw_json = raw.json()
            resp.answer = raw_json["answer"]
            resp.image = raw_json["image"]
            n += 1
            #print(n)
            self.rspq.put(resp)
            if n == self.iter:
                print("............stopping 1............")
                self.stop_flag = True
            
    
    def get_image_data(self):
        
        while True:
            print("\rt1 time          ",self.time_wait_t1,end="")
            if self.time_wait_t1 >= TIMEOUT1:
                print("\nbye bye t1\n")
                break
            try:
                resp = self.rspq.get_nowait()
                print("\nRSP QUEUE",self.rspq.qsize())
                if resp:
                    self.time_wait_t1 = 0
                    resp2 = namedtuple("imagedata",["answer","data"])
                    raw_image = requests.get(resp.image)
                    resp2.data = raw_image._content
                    resp2.answer = resp.answer
                    self.dataq.put(resp2)
                resp.task_done()
            except:
                time.sleep(0.02)
                self.time_wait_t1 += 0.02
                #print("/n/////////.....stopping2.........////////////////n")
                
    
    def save_image(self):
        
        while True:
            print("            \rtime t2  ",self.time_wait_t2,end="")
            if self.time_wait_t2 >= TIMEOUT2:
                print("\nbye bye t2\n")
                break
            try:
                resp2 = self.dataq.get_nowait()
                print("\nDATA Q",self.dataq.qsize())
                self.time_wait_t2 = 0
                if resp2:
                    answer = resp2.answer
                    fname = answer + str(time.time()) + ".gif"
                    print(fname)
                    if "yes" in answer:
                        gif_directory = yes_directory
                    elif "no" in answer:
                        gif_directory = no_directory
                    else:
                        gif_directory = maybe_directory
                        
                    whole_path = os.path.join(gif_directory,fname)
                    print(f"\nwriting {whole_path}..........\n")
                    with open(whole_path,"wb+") as f:
                        f.write(resp2.data)
                    print(f"\n.....Done writing {whole_path}\n")
            except:
                time.sleep(0.02)
                self.time_wait_t2 += 0.02
               # print("/n/////////.....stopping3.........////////////////n")
            
            
                
    
    def run(self):
        t1 = Thread(target=self.fetch_url_and_answer)
        t2 = Thread(target=self.get_image_data)
        t3 = Thread(target=self.save_image)
        t1.start()
        t2.start()
        t3.start()
        t1.join()
        t2.join()
        t3.join()
        
        
gs = GIFSaver(100)
gs.run()
        
        

