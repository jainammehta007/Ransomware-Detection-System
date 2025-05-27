import pymongo
import tkinter as tk
from tkinter import messagebox
import time

myclient = pymongo.MongoClient("mongodb+srv://jainam:7sjssduBdkrndj@finalproject.q4jsbp.mongodb.net/Ransomware?retryWrites=true&w=majority&appName=finalproject")
#myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["Ransomware"]
mycol = mydb["machines"]
myquery = { "status": "Attack" }

while True:
    time.sleep(3)
    my_doc = mycol.find_one(myquery)
    if my_doc == None:
        print("No Attack. Will scan again in 3 seconds...")
        continue
    else:   
        for x in my_doc:
            ipaddress = my_doc.get('ipaddress', '0.0.0.0')
            messagebox.showwarning("Ransomware Detector - Alert!!!", f"Machine with IP Address: {ipaddress} has been attacked!")            
            break
        break    
print("Code ended")