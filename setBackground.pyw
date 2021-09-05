import ctypes
import os 
import time 
import numpy as np
import tkinter as tk
import  pandas as pd
import dataframe_image as di
import PIL.Image
from tkinter import *
from winWallpaper import Wallpaper

mainDir = "C:\\Users\\Lenovo\\Pictures\\wallpapers\\" # Directory that contains wallpapers
jpegList = os.listdir(mainDir)
i = 0
while i < len(jpegList):
    if os.path.isdir(os.path.join(mainDir, jpegList[i])):
        jpegList.pop(i)
        i-=1
    i+=1


class getRemiders(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        
        
        self.reminders = []
        self.reminderLabels = []
        self.master.geometry('400x400')
        
        
        
        self.quit = tk.Button(self, text="SAVE", fg="red",command=self.save)
        self.quit.pack(padx =10, pady=10,side=BOTTOM)
        
        self.add = tk.Button(self, bg="white")
        self.add["text"] = "Add reminder"
        self.add["command"] = self.add_clicked
        self.add.pack(padx =10, pady=10,side="right")
        
        
        
        
        
        self.delete = tk.Button(self, bg="white")
        self.delete["text"] = "Remove Selected"
        self.delete["command"] = self.removeSelected
        self.delete.pack(padx =10, pady=10,side="left")
        
        
        self.inputt = tk.Entry(self, width=20)#state = 'disabled'
        self.inputt.focus()
        self.inputt.pack(padx =10, pady=10,side= "left")
        
        
        
        
        
        self.scrollbar = Scrollbar(root)
        self.scrollbar.pack(  side = RIGHT, fill = Y )
        
        self.mylist = Listbox(root, yscrollcommand = self.scrollbar.set, font = ("Helvetica", "16"), selectmode = SINGLE )

        self.mylist.pack(padx =10, pady=10, side = BOTTOM, fill = BOTH )
        self.scrollbar.config( command = self.mylist.yview )

        
        
        
        
        
        if self.isFirstOpening("reminders.txt") == True:
            self.savePrimaryWallpaper()
        else:
            lines = self.getLines("reminders.txt")
            for line in lines:
                self.mylist.insert(END,line[:-1])
                self.reminders.append(line[:-1])
        
    
    def add_clicked(self):
        
        newReminder = self.inputt.get()
        self.reminders.insert(0,newReminder)
        self.mylist.insert(0, newReminder)
        #self.master.geometry("700x" + str((len(self.reminders) + 1) * 50))
        

    def isFirstOpening(self,directory):
        if os.path.exists(directory):
            return False
        return True
    
    def getLines(self,directory):
        if self.isFirstOpening(directory):
            return None
        
        reminderFile = open(directory,"r")
        reminderLines = reminderFile.readlines()
        reminderFile.close()
        return reminderLines

    def removeSelected(self):
        index = self.mylist.curselection()
        if not index == ():
            self.reminders.pop(index[0])
            self.mylist.delete(index)
        
        
    def save(self):
        if len(self.reminders)==0:
            if os.path.exists("reminders.txt"):
                os.remove("reminders.txt")
                
        else:
            file = open("reminders.txt", "w")
            for line in self.reminders:
                if line == "":
                    continue
                file.write(line + "\n")
            file.close()
            
        self.saveRemindersAsImg()
        self.exportToWallpaper()
    
    def saveRemindersAsImg(self):
        dataframe = pd.DataFrame(data = self.reminders, columns = ["Yapilacaklar"])
        di.export(dataframe, "reminders.JPEG")
    def savePrimaryWallpaper(self):
        Wallpaper.get(True).save("defaultWallpaper.JPEG", "JPEG")
        
    def exportToWallpaper(self):
        
        if not os.path.exists("reminders.JPEG") or  not os.path.exists("defaultWallpaper.JPEG"):
            return
        
        
        if len(self.reminders) == 0:
           
            if os.path.exists("reminders.JPEG"):
                os.remove("reminders.JPEG")
            
            if os.path.exists("defaultWallpaper.JPEG"):
                Wallpaper.set("defaultWallpaper.JPEG")
                
            if os.path.exists("newWallpaper.JPEG"):
                os.remove("newWallpaper.JPEG")
            
            return
            
        
        defWallpaper =PIL.Image.open("defaultWallpaper.JPEG")
        
        
        
        arDefWallpaper = np.asarray(defWallpaper)
        

        
        
        newAr = arDefWallpaper.copy()
        
        reminderImg =PIL.Image.open("reminders.JPEG")
        arReminderImg = np.asarray(reminderImg)
        sizeWall = arDefWallpaper.shape
        sizeRem = arReminderImg.shape
        
        scale = 1.0
        
        maxim = min(len(self.reminders),12)   
        
        #if sizeRem[0]>sizeRem[1]:
        #scale = (maxim*(0.0 + sizeWall[0]))/(sizeRem[0] *20)# (1*1080)/(53 *)

        if len(self.reminders)<15:
            scale = (sizeWall[0]/20)/((sizeRem[0]-30)/len(self.reminders)) # 1 reminder -> 1/20 of screen height
        else :
            scale = (maxim*(0.0 + sizeWall[0]))/(sizeRem[0] *20)# now height of reminders decreases as the number grows
       
        
        
        newRem = reminderImg.resize(resample = PIL.Image.LANCZOS,size=(int(float(sizeRem[1])*scale), int(float(sizeRem[0])*scale)))

        arReminderImg = np.asarray(newRem)
        
        
        
        sizeWall = arDefWallpaper.shape
        sizeRem = arReminderImg.shape
        
 
        
        
        
        for i in range(int(30 * scale), sizeRem[0]):
            for j in range(0, sizeRem[1] - int(30 * scale)):
                newAr[i][sizeWall[1] - j -1] = arReminderImg[i][sizeRem[1] - j -1][0:3]
       
        
        PIL.Image.fromarray(newAr).save("newWallpaper.JPEG")
        Wallpaper.set("newWallpaper.JPEG")

root = tk.Tk()
root.title("Wallpaper Reminders")
app = getRemiders(master=root)
app.mainloop()
