from tkinter import ttk
from tkinter import *
import tkinter as tk
from tkinter import messagebox
import pyautogui
from bs4 import BeautifulSoup as bs
import requests
import re
import pandas as pd
import time
import webbrowser

app = Tk()
app.title("Movie's World")
width=900
height=600
app.geometry(f"1400x750")
movie_buttons=[]
links=[]
#app.resizable(False,False)

def request():
    try:
        requests.get("http://www.google.com")
        return True
    except:
        return False
def check_internet():
    if request():
        Label(labelframe_left,text=" (*) Connected").grid(row=1)
    else:
        Label(labelframe_left,text=" (*) Not Connected").grid(row=1)
def switch():
    global is_on
    if is_on:
        exact_search_btn.config(image=off)
        is_on=False
    else:
        exact_search_btn.config(image=on)
        is_on=True
def validated(name):
    if "(in development)" in name:
        return False
    elif "(TV Mini Series)" in name:
        return False
    else:
        return True
def get_movie_details(name,link):
    url=f"https://www.imdb.com/{link}"
    movie_bundle=bs(requests.get(url).content,"html.parser")
    try:
        recent_searches=open('searches.txt','a')
    except:
        recent_searches=open('searches.txt','w')
    recent_searches.write(movie_name.get())
    recent_searches.write('\n')
    recent_searches.close()
    webbrowser.open(url)
row=1
col=0
width_end=False
width=0
def get_movie(movie_name):
    length=0
    global is_on
    global row
    global col
    global width_end
    global width
    popular_series=f"https://www.imdb.com/find?q={movie_name}&s=tt&ttype=tv&ref_=fn_tt_pop"
    popular_movies=f"https://www.imdb.com/find?q={movie_name}&s=tt&ttype=ft&ref_=fn_tt_pop"
    exact_movies=f"https://www.imdb.com/find?q={movie_name}&s=tt&ttype=ft&exact=true&ref_=fn_tt_ex"
    exact_series=f"https://www.imdb.com/find?q={movie_name}&s=tt&ttype=tv&exact=true&ref_=fn_tt_ex"
    if is_on:
        url=[exact_movies,exact_series]
    else:
        url=[popular_movies,popular_series]
    def get_year(name):
        paran=0
        values=[]
        for i in range(len(name)):
            if name[i]=='(':
                values.append(i)
                paran+=1
        for j in range(len(values)):
            if name[values[j]+5]==')':
                return name[values[j]:values[j]+6]
            else:
                return ""
    for j in range(2):
        response=requests.get(url[j])
        soup=bs(response.content,"html.parser")
        movies=soup.select('td.result_text')
        movie_link=soup.select('td.result_text a')
        img=soup.select('td.primary_photo a img')
        for i in range(len(movies)):
            link=movie_link[i].get("href")
            full_name=movies[i].text
            full_name=full_name.replace(movie_link[i].get_text(),"")
            if validated(full_name):
                year=get_year(full_name)
                perfect_movie_name=f"{movie_link[i].get_text()} {year}"
                Button(labelframe_main,text=perfect_movie_name,command=lambda:get_movie_details(perfect_movie_name,link)).grid(row=row,column=col)
                print(movies[i].text)
                print()
                length+=1
                #print(img[i]['src'])
                if not width_end:
                    col+=1
                    width+=len(perfect_movie_name)
                    if width>50:
                        width_end=True
                        global fix_col
                        fix_col=col
                        col=0
                        row+=1
                else:
                    if col<fix_col-1:
                        col+=1
                    else:
                        row+=1
                        col=0
    return length
def search():
    if len(movie_name.get()) != 0 :
        if request():  
            status.config(text="Working on it...")
            length=get_movie(movie_name.get())
            status.config(text="")
            if length != 0:
                status.config(text=f"{length} results found")
            else:
                status.config(text="No result found")
        else:
            messagebox.showwarning("Error:","Internet: Unavailable")
    else:
        pass

labelframe_left=LabelFrame(app,padx=10,pady=10,width=10)
labelframe_left.place(x=10,y=20,width=200,height=530)

labelframe_main=LabelFrame(app,padx=10,pady=10)
labelframe_main.place(x=220,y=20,width=920,height=530)

labelframe_right=LabelFrame(app,padx=10,pady=10)
labelframe_right.place(x=1150,y=20,width=200,height=530)

canvas=Canvas(labelframe_right)
scrollbar_right=Scrollbar(labelframe_right,orient="vertical",command=canvas.yview)
scrollable_frame=Frame(canvas)

labelframe_down=LabelFrame(app,padx=10,pady=10)
labelframe_down.place(x=10,y=560,width=1341,height=130)

Label(labelframe_left,text='Recent Searches',font=10).grid(row=0,column=0)
searches_list=LabelFrame(labelframe_left).grid()
Label(labelframe_main,text='Search a movie:  ',font=10).grid(row=0,column=0)

status=Label(labelframe_down,text="")
status.grid()
check_internet()
movie_name=Entry(labelframe_main)
movie_name.grid(row=0,column=1)
movie_name.focus()
search_button=Button(labelframe_main,text="Enter",command=search).grid(row=0,column=2)
on=PhotoImage(file="on.png")
off=PhotoImage(file="off.png")
Label(labelframe_right,text='Source: www.imdb.com',font=10).grid(row=0,column=0)
search_option=LabelFrame(labelframe_right)
search_option.grid(row=1,column=0)
Label(search_option,text="Exact search").grid(row=1,column=0)
exact_search_btn=Button(search_option,image=on,bd=0,command=switch)
exact_search_btn.grid(row=1,column=1)
is_on=True

app.mainloop()
