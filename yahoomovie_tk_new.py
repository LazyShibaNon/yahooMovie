# -*- coding: utf-8 -*-
"""
Created on Fri Feb 11 15:17:23 2022

"""

from mypackage import myfuntion as my

import requests , urllib , os , json , datetime
import tkinter as tk
from tkinter import messagebox
from bs4 import BeautifulSoup

def _movieInfo():
    
    global runPage ,paGe ,myHead,pageCount

    urL = "https://movies.yahoo.com.tw/movie_intheaters.html"
    rQ = requests.get(urL,headers=myHead).text.encode("utf-8-sig")
    souP = BeautifulSoup(rQ,"html5lib")

    
    pageSoup = souP.find("div","page_numbox")
    for pageNum in pageSoup.find_all("li"):
        pageCount += 1
    allPages = pageCount-4
    stR.set("上映中電影共有: "+str(allPages)+"頁")  

def _downLoad():
    global runPage ,paGe ,myHead
    paGe = enteR.get()
    enteR.delete(0,tk.END)
    texT.delete(1.0,tk.END)
    
    
    toDay = datetime.date.today()
    try:    #先判斷目錄是否存在，若不存在才建立新目錄
        os.makedirs(str(toDay))
    except FileExistsError:    
        texT.insert(tk.END, str(toDay)+"-這個目錄已經存在!!!"+"\n")
    goDir=str(toDay)+"/"
    os.chdir(goDir)
    
    while runPage <= int(paGe):
        urL="https://movies.yahoo.com.tw/movie_intheaters.html"+"?page="+str(runPage)
        rQ = requests.get(urL,headers=myHead).text
        souP = BeautifulSoup(rQ,"html5lib")
            
        movieDict={}
        soupS = souP.find("ul","release_list")
        for mySoup in soupS.find_all("li"):
            titlE = mySoup.find("div","release_movie_name").a.text.strip()
            picUrl=mySoup.a.img["src"]
            
            try:    #先判斷目錄是否存在，若不存在才建立新目錄
                os.makedirs(titlE)    
            except FileExistsError:    
                texT.insert(tk.END, "-目錄已經存在!!!"+"\n")

            newDir=titlE+"/"
            os.chdir(newDir)    #切換到新建的目錄底下
            try:
                urllib.request.urlretrieve(picUrl,titlE+".jpg")
                itemDict={"中文片名":mySoup.find("div","release_movie_name").a.text.strip(),
                          "英文片名":mySoup.find("div","en").a.text.strip(),
                          "期 待 度":mySoup.find("div","leveltext").find("span").text.strip(),
                          "上映日期":mySoup.find("div","release_movie_time").text.strip(),
                          "電影介紹":mySoup.find("div","release_btn color_btnbox").find_all("a")[0]["href"].strip(),
                          "時 刻 表":mySoup.find("div","release_btn color_btnbox").find_all("a")[3]["href"].strip(),
                          "劇情簡介":mySoup.find("div","release_text").text.strip()}
                    
                movieDict.update(itemDict)
                with open(titlE+".json","w",encoding="utf-8") as filE:
                    json.dump(movieDict,filE,ensure_ascii=False,indent=4)
                    
                texT.insert(tk.END, titlE+"\n")
                texT.insert(tk.END, "----------------------"+"\n")
                #print("------------------")
                itemDict.clear()
                movieDict.clear()
                os.chdir("../") #回到上一層目錄
                
            except:
                continue
        runPage += 1
        
    os.chdir("../")
        
def _exIt():
    qQ=tk.messagebox.askokcancel("提示","確定要結束程式嗎???")
    if qQ:
        wiN.destroy()
    
myHead = my._headers()
runPage = 1
pageCount = 0

wiN = tk.Tk()
wiN.title("~ 奇摩電影 :在線熱映中 ~")
wiN.geometry("500x365")
wiN.configure(bg="MistyRose")

btN1 = tk.Button(wiN, text="收集可下載的頁數",bg="LightBlue", font=("微軟正黑體", 12), width=15, height=1, command=_movieInfo)
btN1.place(x=35,y=15)


stR=tk.StringVar()
lbL2 = tk.Label(wiN,textvariable = stR, bg="MistyRose", font=("微軟正黑體", 12))
lbL2.place(x=200,y=20)

lbL = tk.Label(wiN,text="請輸入想下載的頁數: ",bg="MistyRose",  font=("微軟正黑體", 12))
lbL.place(x=40,y=60)

enteR=tk.Entry(wiN,font=("微軟正黑體",12),width=13,bd=5)
enteR.place(x=198,y=59)

btN2 = tk.Button(wiN, text="開始下載",bg="Khaki", font=("微軟正黑體", 12), width=8, height=1, command=_downLoad)
btN2.place(x=335,y=56)

sBar=tk.Scrollbar(wiN)
sBar.pack(side=tk.RIGHT,fill=tk.Y)
texT=tk.Text(wiN, font=("微軟正黑體", 16),width=38, height=10,yscrollcommand=sBar.set)
texT.place(x=12,y=100)
sBar.config(command=texT.yview)

btN5 = tk.Button(wiN, text="離開",bg="Thistle", font=("微軟正黑體", 12), width=4, height=1, command=_exIt)
btN5.place(x=360,y=16)

wiN.mainloop()
