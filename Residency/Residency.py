import pandas as pd
import sqlite3
import tkinter as tk
from tkinter import *
import tkinter.font as font
from tkinter import messagebox
from datetime import timedelta
from datetime import datetime
#command="""CREATE TABLE CURRENT_ROOMS"""
#command="""DROP TABLE CURRENT_ROOMS """
class Residency:
    def __init__(self,app):
        self.app=app
        self.app.title("Lakshimi Nivas Residency")
        self.app.geometry("1400x750")
        self.__available_rooms=[101,102,103,104,105,106,107,108,109,110]
        connection=sqlite3.connect("Residency.db")
        cursor=connection.cursor()
        #command="""DELETE FROM CURRENT_ROOMS WHERE ID>5 """
        #cursor.execute(command)
        command=f"""SELECT ROOM_NO FROM CURRENT_ROOMS """
        booked_rooms=cursor.execute(command).fetchall()
        connection.commit()
        connection.close()
        #print(booked_rooms)
        for room in booked_rooms:
            if int(room[0]) in self.__available_rooms:
                self.__available_rooms.remove(int(room[0]))
        #print(self.__available_rooms)
        self.__all_frames=['Bill',"Booked Rooms",'All Data']
        self.menu=Menu(self.app)
        self.app.config(menu=self.menu)
        self.font=font.Font(family='Times New Roman',size=16,weight='normal')
        #menu and associated frames
        self.BILL_FRAME=Frame(self.app)
        self.menu.add_command(label="Bill",command=self.BILL)

        self.BOOKED_FRAME=Frame(self.app,relief=GROOVE)
        self.menu.add_command(label="Booked Rooms",command=self.BOOKED)

        self.ALLDATA_FRAME=Frame(self.app)
        self.menu.add_command(label='All Data',command=self.ALLDATA)

        self.BILL()
        
        self.app.mainloop()
    def bookThisRoom(self,room_no, guest_name, nof_person, mobile, nation, state, aadhar,purpose,expected,advance,check_in=False):
        if not (int(room_no) in self.__available_rooms):
            if int(room_no) in [101,102,103,104,105,106,107,108,109,110]:
                messagebox.showerror("Room is Unavailable",f"Room no {room_no} is already Booked")
            else:
                messagebox.showerror("Room is Unavailable",f"Room no {room_no} is out of Range")
            return
        self.__valuesForDataBase=['room no','booking time','name','no of persons','mobile','nationality','state','aadhar','checkin time','purpose','expected checkout']
        connection=sqlite3.connect("Residency.db")
        cursor=connection.cursor()
        command=f"""INSERT INTO CURRENT_ROOMS(ROOM_NO,DATETIME_OF_BOOKING,GUEST_NAME,NO_OF_PERSONS,MOBILE,NATIONALITY ,STATE,AADHAR_NO,DATETIME_OF_CHECKIN,PURPOSE,
        EXPECTED_STAY,ADVANCE)VALUES(110,datetime('now'),"Rajan",1,9384923904,'India','Tamil Nadu',211043002800,datetime('now'),'testing','2022-09-02 6:0:0',200)"""

        command=f"""INSERT INTO CURRENT_ROOMS(ROOM_NO,DATETIME_OF_BOOKING,GUEST_NAME,NO_OF_PERSONS,MOBILE,NATIONALITY ,STATE,AADHAR_NO,PURPOSE,
        EXPECTED_STAY,ADVANCE)VALUES(  '{room_no}',datetime("now"),'{guest_name}','{nof_person}','{mobile}','{nation}','{state}','{aadhar}','{purpose}','{expected}','{advance}');"""                           
        cursor.execute(command)
        connection.commit()
        connection.close()
        if check_in:
            self.checkInRoom(room_no)
        else:
            messagebox.showinfo("Booked",f"Room no {room_no} booked succesfully for {guest_name.upper()}")
    def verify_data(self,room_no,guest_name,nof_person,
                    mobile,nation,state,aadhar,
                    purpose,expected,advance):
        try:
            int(room_no)
            int(aadhar)
            int(advance)
            int(nof_person)
            int(mobile)
        except:
            messagebox.showerror("Invalid Data Type","Enter a Valid Data type")
            return
        if not int(room_no) in self.__available_rooms:
            messagebox.showerror("Error",f"Room {room_no} is not available")
            return
        elif len(guest_name)<4:
            messagebox.showerror("Error",f"Enter the valid guest name ")
            return
        elif int(nof_person)<1 or int(nof_person)>10:
            if int(nof_person)<1:
                messagebox.showerror("Error",f"Enter a valid number")
                return
            else:
                messagebox.showerror("Error",f"{nof_person} members are not allowed in a single room")
                return
        elif len(mobile)!=10:
            messagebox.showerror("Error",f"Mobile number is Invalid")
            return
        elif len(aadhar)!=12:
            messagebox.showerror("Error",f"Aadhar number id Invalid")
            return
        #elif (checkin-datetime.now())>timedelta(days=7):
        #    messagebox.showerror("Error",f"Checkin time is too long to make a book")
        #    return
        #elif (checkin-datetime.datetime.now())<timedelta(hours=5):
        #    messagebox.showerror("Error",f"Considering too late of booking")
        #    return
        #elif (expected-datetime.datetime.now())<timedelta(months=1):
        #    messagebox.showerror("Error",f"Couldnot make a bill for below two hours of stay")
        #    return
        elif int(advance)<0:
            messagebox.showerror("Error",f"Advance may zero or positive, not negative")
            return            
        self.__book_button.config(state=NORMAL)
        #self.bookThisRoom(room_no, guest_name, nof_person, mobile, nation, state, aadhar, checkin,purpose,expected)
    def tracingFunction(self):
        room_no=self.__room_no_entry.get()
        guest_name=self.__guest_name_entry.get()
        nof_person=self.__mobile_entry.get()
        mobile=self.__mobile_entry.get()
        nation=self.__nation_entry.get()
        state=self.__state_entry.get()
        aadhat=self.__aadhar_entry.get()
        checkin=self.__checkin_entry.get()
        purpose=self.__purpose_entry.get()
        expected=self.__expected_entry.get()
        if len(room_no) !=0:
            self.BILL_FRAME.config()
    def BILL(self):
        #closing frames except this frame
        self.BOOKED_FRAME.pack_forget()
        self.ALLDATA_FRAME.pack_forget()
        self.BILL_FRAME.pack_forget()
        #initializing this frame
        self.BILL_FRAME.pack()
        
        ###########
        
        bill_no=0
        self.__bill_label=Label(self.BILL_FRAME,text=f'Bill no: {bill_no}')
        self.__bill_label.config(font=font.Font(family='Times New Roman',size=17,weight='bold'))
        self.__bill_label.grid(row=0,column=0,ipadx=20,ipady=20)

        #self.__room_no_str=StringVar(self.BILL_FRAME)
        self.__room_no_label=Label(self.BILL_FRAME,text='Room no:')
        self.__room_no_label.config(font=self.font)
        self.__room_no_label.grid(row=0,column=1,ipadx=20,ipady=20)
        self.__room_no_entry=Entry(self.BILL_FRAME,width=3)
        self.__room_no_entry.config(font=self.font)
        self.__room_no_entry.grid(row=0,column=2,ipadx=5,ipady=5)

        self.__guest_name_label=Label(self.BILL_FRAME,text="Guest name:")
        self.__guest_name_label.config(font=self.font)
        self.__guest_name_label.grid(row=0,column=3,ipadx=20,ipady=20)
        self.__guest_name_entry=Entry(self.BILL_FRAME,width=15)
        self.__guest_name_entry.config(font=self.font)
        self.__guest_name_entry.grid(row=0,column=4,ipadx=5,ipady=5)

        self.__nof_person_label=Label(self.BILL_FRAME,text="No.of Person:")
        self.__nof_person_label.config(font=self.font)
        self.__nof_person_label.grid(row=0,column=5,ipadx=20,ipady=20)
        self.__nof_person_entry=Entry(self.BILL_FRAME,width=3)
        self.__nof_person_entry.config(font=self.font)
        self.__nof_person_entry.grid(row=0,column=6,ipadx=5,ipady=5)

        self.__mobile_label=Label(self.BILL_FRAME,text="Mobile:")
        self.__mobile_label.config(font=self.font)
        self.__mobile_label.grid(row=2,column=4,ipadx=20,ipady=20)
        self.__mobile_entry=Entry(self.BILL_FRAME,width=13)
        self.__mobile_entry.config(font=self.font)
        self.__mobile_entry.grid(row=2,column=5,ipadx=5,ipady=5)

        self.__nation_label=Label(self.BILL_FRAME,text="Nationality:")
        self.__nation_label.config(font=self.font)
        self.__nation_label.grid(row=1,column=0,ipadx=20,ipady=20)
        self.__nation_entry=Entry(self.BILL_FRAME,width=8)
        self.__nation_entry.config(font=self.font)
        self.__nation_entry.grid(row=1,column=1,ipadx=5,ipady=5)

        self.__state_label=Label(self.BILL_FRAME,text="State:")
        self.__state_label.config(font=self.font)
        self.__state_label.grid(row=1,column=2,ipadx=20,ipady=20)
        self.__state_entry=Entry(self.BILL_FRAME,width=9)
        self.__state_entry.config(font=self.font)
        self.__state_entry.grid(row=1,column=3,ipadx=5,ipady=5)

        self.__aadhar_label=Label(self.BILL_FRAME,text="Aadhar:")
        self.__aadhar_label.config(font=self.font)
        self.__aadhar_label.grid(row=1,column=4,ipadx=20,ipady=20)
        self.__aadhar_entry=Entry(self.BILL_FRAME,width=13)
        self.__aadhar_entry.config(font=self.font)
        self.__aadhar_entry.grid(row=1,column=5,ipadx=5,ipady=5)

        #self.__checkin_label=Label(self.BILL_FRAME,text="CheckIn time:")
        #self.__checkin_label.config(font=self.font)
        #self.__checkin_label.grid(row=1,column=6,ipadx=20,ipady=20)
        #self.__checkin_entry=Entry(self.BILL_FRAME,width=13)
        #self.__checkin_entry.config(font=self.font)
        #self.__checkin_entry.grid(row=1,column=7,ipadx=5,ipady=5)

        self.__purpose_label=Label(self.BILL_FRAME,text="Purpose:")
        self.__purpose_label.config(font=self.font)
        self.__purpose_label.grid(row=2,column=0,ipadx=20,ipady=20)
        self.__purpose_entry=Entry(self.BILL_FRAME,width=13)
        self.__purpose_entry.config(font=self.font)
        self.__purpose_entry.grid(row=2,column=1,ipadx=5,ipady=5)

        self.__expected_label=Label(self.BILL_FRAME,text="No.of days")
        self.__expected_label.config(font=self.font)
        self.__expected_label.grid(row=2,column=2,ipadx=20,ipady=20)
        self.__expected_entry=Entry(self.BILL_FRAME,width=13)
        self.__expected_entry.config(font=self.font)
        self.__expected_entry.grid(row=2,column=3,ipadx=5,ipady=5)
 
        self.__advance_label=Label(self.BILL_FRAME,text="Advance:")
        self.__advance_label.config(font=self.font)
        self.__advance_label.grid(row=2,column=6,ipadx=20,ipady=20)
        self.__advance_entry=Entry(self.BILL_FRAME,width=13)
        self.__advance_entry.config(font=self.font)
        self.__advance_entry.grid(row=2,column=7,ipadx=5,ipady=5)
        
        self.__book_button=Button(self.BILL_FRAME,text="BOOK NOW",state=DISABLED,command=lambda: self.bookThisRoom(
                                        self.__room_no_entry.get(),
                                        self.__guest_name_entry.get(),
                                        self.__nof_person_entry.get(),
                                        self.__mobile_entry.get(),
                                        self.__nation_entry.get(),
                                        self.__state_entry.get(),
                                        self.__aadhar_entry.get(),
                                        self.__purpose_entry.get(),
                                        self.__expected_entry.get(),
                                        self.__advance_entry.get()))
        self.__book_button=Button(self.BILL_FRAME,text="CHECKIN",state=DISABLED,command=lambda: self.bookThisRoom(
                                        self.__room_no_entry.get(),
                                        self.__guest_name_entry.get(),
                                        self.__nof_person_entry.get(),
                                        self.__mobile_entry.get(),
                                        self.__nation_entry.get(),
                                        self.__state_entry.get(),
                                        self.__aadhar_entry.get(),
                                        self.__purpose_entry.get(),
                                        self.__expected_entry.get(),
                                        self.__advance_entry.get(),
                                        check_in=True))        
        self.__book_button.grid()
        self.__verify_button=Button(self.BILL_FRAME,text="VERIFY DETAILS",state=NORMAL,
                                    command=lambda:self.verify_data(self.__room_no_entry.get(),
                                        self.__guest_name_entry.get(),
                                        self.__nof_person_entry.get(),
                                        self.__mobile_entry.get(),
                                        self.__nation_entry.get(),
                                        self.__state_entry.get(), 
                                        self.__aadhar_entry.get(),
                                        self.__purpose_entry.get(),
                                        self.__expected_entry.get(),
                                        self.__advance_entry.get()))
        self.__verify_button.grid()
    def updateMoneyToDataBase(self,room_no,money):
        connection=sqlite3.connect("Residency.db")
        cursor=connection.cursor()
        command=f"""SELECT ADVANCE FROM CURRENT_ROOMS WHERE ROOM_NO={room_no}"""
        advance=int(cursor.execute(command))#.fetchall()
        command=f"""UPDATE CURRENT_ROOMS SET ADVANCE=ADVANCE+{money} WHERE ROOM_NO={room_no}"""
        cursor.execute(command)
        connection.commit()
        connection.close()
        detail=f"Advance: {advance}\nNow paid: {money}\nTotal: {advance+money}"
        messagebox.showinfo("Money Paid",f"Room no {room_no}\n"+detail)
    def addMoney(self,room_no,frame_no):
        money=Entry(self.room_button[frame_no])
        money.pack(side=LEFT,ipady=3,ipadx=4,pady=4,padx=5)
        Button(self.room_button[frame_no],command=lambda:self.updateMoneyToDataBase(room_no,money.get())).pack(side=LEFT,ipady=3,ipadx=4,pady=4,padx=5)
    def checkInRoom(self,room_no):
        connection=sqlite3.connect('Residency.db')
        cursor=connection.cursor()
        command=f"""UPDATE CURRENT_ROOMS SET DATETIME_OF_CHECKIN=datetime("now")"""
        cursor.execute(command)
        connection.commit()
        connection.close()
        messagebox.showinfo("Checked In",f"Room no {room_no} Checked In")
    def checkOutRoom(self,room_no):
        connection=sqlite3.connect('Residency.db')
        cursor=connection.cursor()
        command=f"""SELECT * FROM CURRENT_ROOMS WHERE ROOM_NO={room_no}"""
        checkout_room=cursor.execute(command).fetchall()
        guest_name=checkout_room[0][3]
        mobile=checkout_room[0][5]
        nof_person=checkout_room[0][4]
        nation=checkout_room[0][6]
        aadhar=checkout_room[0][8]
        booking=datetime.strptime(checkout_room[0][2],'%Y-%m-%d %H:%M:%S')
        checkin=checkout_room[0][9]
        purpose=checkout_room[0][10]
        expected=checkout_room[0][11]
        total_amount=checkout_room[0][12]
        state=checkout_room[0][7]
        #command="""INSERT INTO ROOMS_DATA(ROOM_NO,DATETIME_OF_BOOKING,GUEST_NAME,NO_OF_PERSONS,MOBILE,NATIONALITY ,STATE,AADHAR_NO,DATETIME_OF_CHECKIN,PURPOSE,
        #STAY,ADVANCE)VALUES(110,datetime('now'),"Rajan",1,9384923904,'India','Tamil Nadu',211043002800,datetime('now'),'testing','2022-09-02 6:0:0',200)"""
        #command=f"""INSERT INTO ROOMS_DATA(ROOM_NO,DATETIME_OF_BOOKING,
        #                                GUEST_NAME ,NO_OF_PERSONS ,MOBILE ,NATIONALITY ,
        #                                STATE ,AADHAR_NO ,DATETIME_OF_CHECKIN ,
        #                                PURPOSE ,STAY ,AMOUNT_PAID ,DATETIME_OF_CHECKOUT )
        #                                VALUES({room_no},{booking},{guest_name},{nof_person},{mobile},{nation},{state},{aadhar},{checkin},
        #                                {purpose},{expected},{total_amount},datetime('now'))"""

        #stay=
        command=f""" INSERT INTO ROOMS_DATA(ROOM_NO ,DATETIME_OF_BOOKING ,
                                        GUEST_NAME ,NO_OF_PERSONS ,MOBILE ,NATIONALITY ,
                                        STATE ,AADHAR_NO ,DATETIME_OF_CHECKIN,
                                        PURPOSE ,STAY ,AMOUNT_PAID ,DATETIME_OF_CHECKOUT )
                                        SELECT CR.ROOM_NO,CR.DATETIME_OF_BOOKING,CR.GUEST_NAME,CR.NO_OF_PERSONS,CR.MOBILE,
                                        CR.NATIONALITY ,CR.STATE,CR.AADHAR_NO,CR.DATETIME_OF_CHECKIN,CR.PURPOSE,{stay},CR.ADVANCE,datetime("now")
                                        FROM CURRENT_ROOMS CR WHERE ROOM_NO={room_no}"""
        cursor.execute(command)
        command=f""" DELETE FROM CURRENT_ROOMS WHERE ROOM_NO={room_no}"""
        cursor.execute(command)
        connection.commit()
        connection.close()
        messagebox.showinfo("Checked Out",f"Room no {room_no} is checked out succesfully.\nGuest name: {guest_name}\nAmount paid: {total_amount}")
    def editDetails(self,room_no):
        pass
    def unBookRook(self):
        pass
    def BOOKED(self):
        #closing frames except this frame
        self.BILL_FRAME.pack_forget()
        self.ALLDATA_FRAME.pack_forget()
        self.BOOKED_FRAME.pack_forget()
        
        #initializing this frame
        self.BOOKED_FRAME.pack()
        
        connection=sqlite3.connect("Residency.db")
        cursor=connection.cursor()
        command="""SELECT * FROM CURRENT_ROOMS"""
        booked_data_list=cursor.execute(command).fetchall()
        connection.commit()
        connection.close()
        booked_frame=[]
        heading_frame=[]
        middle_frame=[]
        description_frame=[]
        i=0
        def canvasFunction(event):
            booked_frame_canvas.configure(scrollregion=booked_frame_canvas.bbox("all"),width=200,height=200)
        booked_frame_canvas=Canvas(self.BOOKED_FRAME)
        booked_frame_canvas_frame=Frame(booked_frame_canvas)
        scroll=Scrollbar(self.BOOKED_FRAME,orient=VERTICAL,command=booked_frame_canvas.yview)
        booked_frame_canvas.configure(yscrollcommand=scroll.set)
        scroll.pack(fill=Y,side=RIGHT)
        booked_frame_canvas.pack(side=RIGHT)
        booked_frame_canvas.create_window((0,0),window=booked_frame_canvas_frame,anchor="nw")
        booked_frame_canvas_frame.bind("<Configure>",canvasFunction)
        self.room_button=[]
        for room in booked_data_list:
            
            booked_frame.append(LabelFrame(self.BOOKED_FRAME))
            booked_frame[i].pack(side=BOTTOM,fill=X,pady=30)
            
            heading_frame.append(Frame(booked_frame[i],bg='lightblue'))
            heading_frame[i].pack(fill=X,ipady=5,ipadx=5)
            Label(heading_frame[i],text=f"Room no: {room[1]}",bg='lightblue').grid(row=0,column=0,pady=10,padx=90)
            Label(heading_frame[i],text=f"Guest name: {room[3].upper()}",bg='lightblue').grid(row=0,column=2,pady=10,padx=90)
            Label(heading_frame[i],text=f"Mobile no: {room[5]}",bg='lightblue').grid(row=0,column=3,pady=10,padx=90)
            
            middle_frame.append(Frame(booked_frame[i]))
            middle_frame[i].pack()
            Label(middle_frame[i],text=f"No of Person: {room[4]}").grid(row=0,column=1)
            Label(middle_frame[i],text=f"State: {room[7]}").grid(row=1,column=1)
            Label(middle_frame[i],text=f"Nationality: {room[6]}").grid(row=2,column=1)
            Label(middle_frame[i],text=f"Advance: {room[12]}").grid(row=3,column=1)
            Label(middle_frame[i],text=f"Aadhar no: {room[8]}").grid(row=0,column=2)
            Label(middle_frame[i],text=f"Booked at: {room[2]}").grid(row=1,column=2)
            print(type(room[9]))
            if type(room[9])=="":
                Label(middle_frame[i],text=f"Check In: {room[9]}").grid(row=2,column=2)
            Label(middle_frame[i],text=f"Expected Stay: {room[11]} days").grid(row=3,column=2)
            
            description_frame.append(Frame(booked_frame[i]))
            description_frame[i].pack(fill=X)
            Label(description_frame[i],text=f"Description: {room[10]}").pack(fill=X)
            
            self.room_button.append(Frame(booked_frame[i],bg='grey'))
            self.room_button[i].pack(fill=X,ipady=3,ipadx=3)
            if type(room[9])=="":
                Button(self.room_button[i],text='CheckOut',command= lambda: self.checkOutRoom(room[1])).pack(side=RIGHT,ipady=3,ipadx=4,pady=4,padx=5)
            else:
                Button(self.room_button[i],text='UnBook',command= lambda: self.unBookRoom(room[1])).pack(side=RIGHT,ipady=3,ipadx=4,pady=4,padx=5)
                Button(self.room_button[i],text='CheckIn',command= lambda: self.checkInRoom(room[1])).pack(side=RIGHT,ipady=3,ipadx=4,pady=4,padx=5)
            Button(self.room_button[i],text='Add Money',command=lambda:self.addMoney(room[1],i)).pack(side=RIGHT,ipady=3,ipadx=4,pady=4,padx=5)
            Button(self.room_button[i],text='Update Details',command=lambda:self.editDetails(room[1])).pack(side=RIGHT,ipady=3,ipadx=4,pady=4,padx=5)

            i+=1
    def ALLDATA(self):
        #closing frames except this frame
        self.BILL_FRAME.pack_forget()
        self.BOOKED_FRAME.pack_forget()
        self.ALLDATA_FRAME.pack_forget()
        #initializing this frame
        self.ALLDATA_FRAME.pack()
           

def print_all():
    connection=sqlite3.connect("Residency.db")
    cursor=connection.cursor()
    #command="""INSERT INTO CURRENT_ROOMS(ROOM_NO,DATETIME_OF_BOOKING,GUEST_NAME,NO_OF_PERSONS,MOBILE,NATIONALITY ,STATE,AADHAR_NO,DATETIME_OF_CHECKIN,PURPOSE,
    #EXPECTED_STAY,ADVANCE)VALUES(110,datetime('now'),"Rajan",1,9384923904,'India','Tamil Nadu',211043002800,datetime('now'),'testing','2022-09-02 6:0:0',200)"""
    #command="""DELETE FROM CURRENT_ROOMS WHERE ID<100"""
    command="""SELECT * FROM CURRENT_ROOMS """
    print(cursor.execute(command).fetchall())
    command="""SELECT *  FROM ROOMS_DATA """
    print(cursor.execute(command).fetchall())
    #command=""" DROP TABLE ROOMS_DATA"""
    #cursor.execute(command)
    #command=""" CREATE TABLE ROOMS_DATA(ID INTEGER PRIMARY KEY AUTOINCREMENT,ROOM_NO INT,DATETIME_OF_BOOKING DATE,
    #                                    GUEST_NAME VARCHAR(40),NO_OF_PERSONS INT(2),MOBILE INT(35),NATIONALITY VARCHAR(30),
    #                                    STATE VARCHAR(30),AADHAR_NO INT(12),DATETIME_OF_CHECKIN DATE,
    #                                    PURPOSE VARCHAR(100),STAY VARCHAR(30),AMOUNT_PAID INT(5),DATETIME_OF_CHECKOUT DATE)"""
    #command=f"""CREATE TABLE CURRENT_ROOMS(ID INTEGER PRIMARY KEY AUTOINCREMENT,ROOM_NO,DATETIME_OF_BOOKING,GUEST_NAME,NO_OF_PERSONS,MOBILE,NATIONALITY ,STATE,AADHAR_NO,DATETIME_OF_CHECKIN,PURPOSE,
    #EXPECTED_STAY,ADVANCE)"""#VALUES(110,datetime('now'),"Rajan",1,9384923904,'India','Tamil Nadu',211043002800,datetime('now'),'testing','2022-09-02 6:0:0',200)"""
    #command="""DROP TABLE CURRENT_ROOMS"""
    #cursor.execute(command)
    connection.commit()
    connection.close()
print_all()
my_app=Residency(Tk())
