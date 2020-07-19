# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 10:26:42 2020

@author: sdpatil
"""


import os
import time
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
        resp = namedtuple("Response",["answer","url"])
        raw = requests.get(_url)
        raw_json = raw.json()
        resp.answer = raw_json["answer"]
        resp.image = raw_json["image"]
        self.rspq.put(resp)
    
    def get_image_data(self):
        
        while True:
            try:
                resp = self.rspq.get()
                print("\nRSP QUEUE",self.rspq.qsize())
                if resp:
                    self.time_wait_t1 = 0
                    resp2 = namedtuple("imagedata",["answer","data"])
                    raw_image = requests.get(resp.image)
                    resp2.data = raw_image._content
                    resp2.answer = resp.answer
                    self.dataq.put(resp2)
                self.rspq.task_done()
            except Exception as e:
                print(e)
    
    def save_image(self):
        
        while True:
            try:
                resp2 = self.dataq.get()
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
                self.dataq.task_done()
                
            except Exception as e:
                print(e)
               # print("/n/////////.....stopping3.........////////////////n")
    
    def run(self):
        ##checkout following slide for more info
        ##https://pybay.com/site_media/slides/raymond2017-keynote/threading.html
        t1 = Thread(target=self.get_image_data)
        t1.daemon = True
        t1.start()
        t2 = Thread(target=self.save_image)
        t2.daemon = True
        t2.start()
        for i in range(self.iter):
            t = Thread(target=self.fetch_url_and_answer)
            t.start()
        for i in range(self.iter):
            t.join()
            
        self.rspq.join()
        self.dataq.join()
        del t1
        del t2
        
######################### NO DIFFERENCW AT ALL IN PERFORMANCE #################
start = time.time()
print(f"STARTED")
gs = GIFSaver(10)
gs.run()
print(f"ENDED {time.time() - start}")
        
        

