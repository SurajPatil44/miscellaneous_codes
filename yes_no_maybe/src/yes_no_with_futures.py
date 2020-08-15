import requests
import concurrent.futures
import random
import os,time


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


def yesorno(url='https://yesno.wtf/api'):
    try:
        with requests.Session() as s:
            raw =s.get(url)
        try: 
            return raw.json()
        except:
            return raw
    except Exception as e:
        return e
        
        
def save_image(url,ans):
    try:
        with requests.Session() as s:
            raw = s.get(url)
        _data = raw._content
        name = ans + str(random.randint(0,1000)) + ".gif"
        if "yes" in name:
            gif_directory = yes_directory
        elif "no" in name:
            gif_directory = no_directory
        else:
            gif_directory = maybe_directory
        whole_path = os.path.join(gif_directory,name)
        print(f"SAVING {whole_path}.......")
        with open(whole_path,"wb") as _f:
            _f.write(_data)
        print(f"SAVED {whole_path}.......")
        
    except Exception as e:
        print(f"Error occured {e}")
            
    
if __name__ == "__main__": 

    fut2calc = []
    fut2image = []
    
    start = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        with concurrent.futures.ProcessPoolExecutor(max_workers=8) as executor2:
            ##second executor is process pool
            for i in range(10):
                fut2calc.append(executor.submit(yesorno))  
             
            num1 = fut2calc[0]
            ## spin loop 1
            while True:                
                if not fut2calc:
                    break
                if num1.done():
                    fut = num1
                    fut2calc.remove(num1)
                    res = fut.result()
                    _url = res["image"]
                    _ans = res["answer"]
                    fut2image.append(executor2.submit(save_image,_url,_ans))
 
                try:
                    num1 = random.choice(fut2calc)
                except Exception as e:
                    break
             ## spin loop 2
            num2 = fut2image[0]           
            while True:
                #print("in second loop")
                if not fut2image:
                    break
                if num2.done():
                    fut2 = num2
                    fut2image.remove(num2)
                    #print(f"done with {num2}")
                    try:
                        fut2.result()
                        #print(f"{dir(res)}")
                    except Exception as e:
                        print(f"error is {e}")
                try:
                    num2 = random.choice(fut2image)
                except Exception as e:
                    print(f"exception is {e}")
                    break
 
        
    print(f"finished in {start - time.time()}")
            
                
                
    

        
