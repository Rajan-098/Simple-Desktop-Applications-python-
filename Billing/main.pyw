from tkinter import *
from tkinter import ttk
import sqlite3
from tkinter import messagebox
__bill_at__=["Restaurant","AC Restaurant","Parcel","Home Delivery"]
class Billing:
    def __init__(self,app):
        self.app=app
        self.app.title("Billing Program")
        self.app.geometry("1400x750")
        self.menu = Menu(app)
        self.app.config(menu=self.menu)

        self.billM = Menu(self.menu)
        self.billM.add_command(label="Open billing",command=self.section_billNow)
        self.menu.add_cascade(label="Bill",menu=self.billM)

        self.itemM = Menu(self.menu)
        self.itemM.add_command(label="Edit",command=self.section_edit_item)
        self.menu.add_cascade(label="Items",menu=self.itemM)

        self.waiterM = Menu(self.menu)
        self.waiterM.add_command(label="Show")
        self.menu.add_cascade(label="Waiter",menu=self.waiterM)
        
        self.bill_app=Frame(self.app)
        self.bill_app.pack()
        self.section_billNow()
        self.selected_number=0
    def sql_items(self):
        connection=sqlite3.connect(r"C:\Users\RAJAN\Desktop\Billing\items.db")
        cursor=connection.cursor()
        command="""SELECT * FROM ITEMS;"""
        cursor.execute(command)
        items=cursor.fetchall()
        for index,item in enumerate(items):
            self.tree.insert('','end',text="",values=(index+1,item[0],item[1].upper(),item[2]))
        self.total_no_of_items=index+1
        connection.commit()
        connection.close()
    def section_billNow(self):
        try:
            self.bill_app.pack_forget()
        except:
            pass
        try:
            self.edit_app.pack_forget()
        except:
            pass
        self.bill_app=Frame(self.app)
        self.bill_app.pack(fill=BOTH,expand=True)

        global __bill_att__
        self.billtype=__bill_at__

        self.bill_input=Frame(self.bill_app)
        self.bill_input.pack(side=TOP,fill=BOTH)
        
        typ_label=Label(self.bill_input,text="Type")
        typ_label.grid(row=0,column=0)
        typ=Spinbox(self.bill_input,width="30",values=self.billtype,state="readonly",xscrollcommand=X)
        typ.grid(row=0,column=1)

        waiter_no_label=Label(self.bill_input,text="Waiter no")
        waiter_no_label.grid(row=0,column=2)
    
        waiter_no=Spinbox(self.bill_input)
        waiter_no.grid(row=0,column=3)
        
        waiter_name_label=Label(self.bill_input,text="Waiter name")
        waiter_name_label.grid(row=0,column=4)
        
        waiter_name=Spinbox(self.bill_input)
        waiter_name.grid(row=0,column=5)

        table_no_label=Label(self.bill_input,text="Table no")
        table_no_label.grid(row=0,column=6)
        table_no=Spinbox(self.bill_input)
        table_no.grid(row=0,column=7)

        item_no_label=Label(self.bill_input,text="Item no")
        item_no_label.grid(row=0,column=8)
        item_no=Spinbox(self.bill_input)
        item_no.grid(row=0,column=9)
        self.bill_number=90
        bill_no=Label(self.bill_input,text=f"Bill no: {self.bill_number}")
        bill_no.grid(row=0,column=10)
        bill_add=Button(self.bill_input,text=f"+Add",command=self.add_current)
        bill_add.grid(row=0,column=11)
        
        self.bill_area=LabelFrame(self.bill_app,height=200)
        self.bill_area.pack(side=TOP,fill=BOTH)

        self.current_rows=ttk.Treeview(self.bill_area,column=("sno","number","name","quantity","rate","price"),show="headings")
        self.current_rows.pack(fill=BOTH,expand=True)
        scroll_y = Scrollbar(self.current_rows, orient=VERTICAL)
        self.current_rows.config(yscrollcommand=scroll_y.set)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_y.config(command=self.current_rows.yview)
    
        self.current_rows.column("sno",anchor=CENTER,width=50)
        self.current_rows.heading("sno",text="S.no")
        self.current_rows.column("number",anchor=CENTER,width=50)
        self.current_rows.heading("number",text="Item no")
        self.current_rows.column("name",anchor=CENTER,width=150)
        self.current_rows.heading("name",text="Item name")
        self.current_rows.column("quantity",anchor=CENTER,width=150)
        self.current_rows.heading("quantity",text="Quantity")
        self.current_rows.column("rate",anchor=CENTER,width=150)
        self.current_rows.heading("rate",text="Price")
        self.current_rows.column("price",anchor=CENTER,width=50)
        self.current_rows.heading("price",text="Total")
        self.current_rows.bind('<ButtonRelease-1>',self.selectItem_current_row)

        self.bill_options=Frame(self.bill_app)
        self.bill_options.pack(side=BOTTOM,fill=X)
        Button(self.bill_options,text="Print",command=self.print_bill).pack(side=RIGHT,ipadx=15,ipady=5,padx=25,pady=20)
        Button(self.bill_options,text="Reset",command=self.reset_bill).pack(side=RIGHT,ipadx=15,ipady=5,padx=25,pady=20)
        Button(self.bill_options,text="Delete",command=self.delete_bill).pack(side=RIGHT,padx=25,pady=20,ipadx=15,ipady=5)
    def add_current(self):
        self.tree.insert('','end',text="",values=(sno,item_no,item_name.upper(),quantity,rate,price))
    def print_bill(self):
        pass
    def reset_bill(self):
        pass
    def delete_bill(self):
        pass
        
    def selectItem_current_row(self,_):
        pass
    def check_changes(self):
        try:
            self.number=int(self.item_no_entry.get())
            self.name=str(self.item_name_entry.get())
            self.price=float(self.item_price_entry.get())
        except:
            messagebox.showerror("Error","Check your data")
            return False
        if str(self.number)[0]=="-" or int(self.number)==0:
            messagebox.showerror("Error","Check the item number")
            return False
        elif len(self.name)<4 or self.name.isnumeric():
            messagebox.showerror("Error","Check the item name")
            return False
        elif str(self.price)[0]=="-":
            messagebox.showerror("Error","Check the item price")
            return False
        else:
            if self.selected_number==self.number:
                if self.selected_name.lower()==self.name.lower():
                    if float(self.selected_price)==float(self.price):
                        return False
                    else:
                        return True
                else:
                    return True
            else:
                return True
    def update_changes(self):
        if self.check_changes():
            new_item_number=self.number
            new_item_name=self.name
            new_item_price=self.price
            connection=sqlite3.connect(r"C:\Users\RAJAN\Desktop\Billing\items.db")
            cursor=connection.cursor()
            command=f"""UPDATE ITEMS SET ITEM_NO = "{new_item_number}", ITEM_NAME = "{new_item_name.upper()}",PRICE = "{new_item_price}" WHERE ITEM_NO={int(self.selected_number)};"""
            cursor.execute(command)
            connection.commit()
            connection.close()
            messagebox.showinfo("Success",f"Item no: {self.selected_number} is Updated successfully")
    def update(self):
        if self.selected_number!=0:
            try:
                add_frame.pack_forget()
            except:
                pass
            try:
                self.update_frame.pack_forget()
            except:
                pass
            self.update_frame=LabelFrame(self.edit_app)
            self.update_frame.pack(side=LEFT)
            item_no_label=Label(self.update_frame,text="Item no")
            item_no_label.grid(row=0,column=0,ipadx=10)
            item_name_label=Label(self.update_frame,text="Item name")
            item_name_label.grid(row=0,column=1,ipadx=10)
            item_price_label=Label(self.update_frame,text="Item price")
            item_price_label.grid(row=0,column=2,ipadx=10)
            
            self.item_no_entry=Entry(self.update_frame)
            self.item_no_entry.grid(row=1,column=0)
            self.item_no_entry.delete(0,END)
            self.item_no_entry.insert(0,self.selected_number)
            
            self.item_name_entry=Entry(self.update_frame,text=self.selected_name)
            self.item_name_entry.grid(row=1,column=1)
            self.item_name_entry.delete(0,END)
            self.item_name_entry.insert(0,self.selected_name)
            
            self.item_price_entry=Entry(self.update_frame,text=self.selected_price)
            self.item_price_entry.grid(row=1,column=2)
            self.item_price_entry.delete(0,END)
            self.item_price_entry.insert(0,self.selected_price)
            
            reset=Button(self.update_frame,text="Reset",command=self.reset)
            reset.grid(ipadx=10,ipady=2,row=0,column=3)
            update=Button(self.update_frame,text="Update",command=self.update_changes)
            update.grid(ipadx=10,ipady=2,row=1,column=3)         

    def delete(self):
        if self.selected_number!=0:
            if messagebox.askokcancel("Sure",f"Sure to delete Item no: {self.selected_number}"):
                connection=sqlite3.connect(r"C:\Users\RAJAN\Desktop\Billing\items.db")
                cursor=connection.cursor()
                command=f"""DELETE FROM ITEMS WHERE ITEM_NO={int(self.selected_number)};"""
                cursor.execute(command)
                connection.commit()
                connection.close()
                messagebox.showinfo("Success",f"Item no: {self.selected_number} is deleted successfully")
    def reset(self):
        self.item_no_entry.delete(0,END)
        self.item_no_entry.insert(0,self.selected_number)
        self.item_name_entry.delete(0,END)
        self.item_name_entry.insert(0,self.selected_name)
        self.item_price_entry.delete(0,END)
        self.item_price_entry.insert(0,self.selected_price)
    def add(self):
        try:
            self.update_frame.pack_forget()
        except:
            pass
        try:
            self.add_frame.pack_forget()
        except:
            pass
        self.add_frame=LabelFrame(self.edit_app)
        self.add_frame.pack(side=LEFT)
        item_no_label=Label(self.add_frame,text="Item no")
        item_no_label.grid(row=0,column=0,ipadx=10)
        item_name_label=Label(self.add_frame,text="Item name")
        item_name_label.grid(row=0,column=1,ipadx=10)
        item_price_label=Label(self.add_frame,text="Item price")
        item_price_label.grid(row=0,column=2,ipadx=10)
        self.item_no_entry=Entry(self.add_frame)
        self.item_no_entry.grid(row=1,column=0)
        self.item_name_entry=Entry(self.add_frame)
        self.item_name_entry.grid(row=1,column=1)
        self.item_price_entry=Entry(self.add_frame)
        self.item_price_entry.grid(row=1,column=2)
        save=Button(self.add_frame,text="Clear",command=self.clear).grid(ipadx=10,ipady=2,row=0,column=3)
        save=Button(self.add_frame,text="Save",command=self.save).grid(ipadx=10,ipady=2,row=1,column=3)
    def save(self):
        try:
            self.number=int(self.item_no_entry.get())
            self.name=str(self.item_name_entry.get())
            self.price=float(self.item_price_entry.get())
        except:
            messagebox.showerror("Error","Check your data")
            return
        if str(self.number)[0]=="-" or int(self.number)==0:
            messagebox.showerror("Error","Check the item number")
        elif len(self.name)<4 or self.name.isnumeric():
            messagebox.showerror("Error","Check the item name")
        elif str(self.price)[0]=="-":
            messagebox.showerror("Error","Check the item price")
        else:
            self.sql_save()
    def clear(self):
        self.item_no_entry.delete(0,END)
        self.item_name_entry.delete(0,END)
        self.item_price_entry.delete(0,END)
    def sql_save(self):
        connection=sqlite3.connect(r"C:\Users\RAJAN\Desktop\Billing\items.db")
        cursor=connection.cursor()
        command="""SELECT * FROM ITEMS;"""
        cursor.execute(command)
        items=cursor.fetchall()
        for index,item in enumerate(items):
            if int(item[0])==self.number:
                messagebox.showerror("Error","Item number already exists")
                return
            elif item[1].lower()==self.name.lower():
                messagebox.showerror("Error","Item name already exists")
                return
        command=f"""INSERT INTO ITEMS(ITEM_NO,ITEM_NAME,PRICE) VALUES("{self.number}","{self.name.upper()}","{self.price}");"""
        cursor.execute(command)
        connection.commit()
        connection.close()
        messagebox.showinfo("Success","Item added succesfully")
    def selectItem(self,a):
        curItem=self.tree.focus()
        selected_item=self.tree.item(curItem)['values']
        self.selected_number=selected_item[1]
        self.selected_name=selected_item[2]
        self.selected_price=selected_item[3]
    def section_edit_item(self):
        try:
            self.bill_app.pack_forget()
        except:
            pass
        try:
            self.edit_app.pack_forget()
        except:
            pass
        self.edit_app=Frame(self.app)
        self.edit_app.pack(expand=True,fill=BOTH)    
        
        self.tree=ttk.Treeview(self.edit_app,column=("sno","number","name","rate"),show="headings")
        
        self.tree.pack(fill=BOTH,expand=True,side=TOP)
        
        scroll_y = Scrollbar(self.tree, orient=VERTICAL)
        self.tree.config(yscrollcommand=scroll_y.set)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_y.config(command=self.tree.yview)
    
        self.tree.column("sno",anchor=CENTER,width=50)
        self.tree.heading("sno",text="S.no")
        self.tree.column("number",anchor=CENTER,width=50)
        self.tree.heading("number",text="Item no")
        self.tree.column("name",anchor=CENTER,width=150)
        self.tree.heading("name",text="Item name")
        self.tree.column("rate",anchor=CENTER,width=50)
        self.tree.heading("rate",text="Item price")
        self.tree.bind('<ButtonRelease-1>',self.selectItem)
        Button(self.edit_app,text="Delete",command=self.delete).pack(side=RIGHT,ipadx=15,ipady=5,padx=25,pady=20)
        Button(self.edit_app,text="Update",command=self.update).pack(side=RIGHT,ipadx=15,ipady=5,padx=25,pady=20)
        Button(self.edit_app,text="+Add new",command=self.add).pack(side=RIGHT,padx=25,pady=20,ipadx=15,ipady=5)
        
        self.sql_items()

app=Tk()
b=Billing(app)
app.mainloop()
