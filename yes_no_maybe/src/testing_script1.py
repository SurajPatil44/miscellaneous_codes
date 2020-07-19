# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 19:10:36 2020

@author: sdpatil
"""

##completeName = os.path.join(save_path, name_of_file+".txt")

import os,time
import requests
from collections import namedtuple

_url = "https://yesno.wtf/api"
yes_directory = r"./GIFs/yes"
no_directory = r"./GIFs/no"
maybe_directory = r"./GIFs/maybe"

__script_dir__ = os.getcwd()

if not os.path.exists(yes_directory):
    os.makedirs(yes_directory)
    
if not os.path.exists(no_directory):
    os.makedirs(no_directory)

if not os.path.exists(maybe_directory):
    os.makedirs(maybe_directory)

def read_url(_url):   
    while True:
        resp = namedtuple("response",["answer","image"])
        raw = requests.get(_url).json()
        resp.answer = raw['answer']
        resp.image = raw['image']
        yield resp  
    
def read_image(json_gen,num=10):
    yes_no = {"yes":0,"no":0,"maybe":0}
    for ind,resp in enumerate(json_gen):
        if ind == num:
            break
        answer = resp.answer
        img_url = resp.image
        yes_no[answer] += 1
        f_name = f"{answer}_{yes_no[answer]}.gif"
        print(f_name)
        yield {"image":img_url,"fname":f_name}

def save_gif(results):
    for res in results:
        raw_data = requests.get(res["image"])
        _data = raw_data._content
        fname = res["fname"]
        if "yes" in fname:
            gif_directory = yes_directory
        elif "no" in fname:
            gif_directory = no_directory
        else:
            gif_directory = maybe_directory
        whole_path = os.path.join(gif_directory,fname)
        print(f"writing file {res['fname']} .... ")
        with open(whole_path,"wb+") as f:          
            f.write(_data)
        print(f"Done writing file {res['fname']} .... ")

start = time.time()
print(f"STARTED")
url_gen = read_url(_url)
img_url_gen = read_image(url_gen,10)
save_gif(img_url_gen)
print(f"ENDED {time.time() - start}")
