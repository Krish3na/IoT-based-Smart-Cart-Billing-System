import RPi.GPIO as GPIO     #----uncomment for raspberry pi
from mfrc522 import SimpleMFRC522    #----uncomment for raspberry pi
import threading
import random, string
from tkinter import *  
from tkinter import ttk
import tkinter as tk
import tkinter as tkkk
from tkinter.font import Font
from tkinter import messagebox
from PIL import ImageTk, Image
import numpy as np
import os
import tksheet
import datetime
import time
import invoiceNew
import mysql.connector
import re
import webbrowser
import app
import sendMsg
import time
GPIO.setwarnings(False)   #----uncomment for raspberry pi

threads=[]
reader = SimpleMFRC522()   #----uncomment for raspberry pi
u_status=False

mydb = mysql.connector.connect(
  host="localhost",
  user="user",
  #host="mydatabase.cbalscre4knb.ap-south-1.rds.amazonaws.com",
  #user="admin",
  password="123456789",
  database="mydatabase"
)
mycursor = mydb.cursor()



productsList,productsListIds=[],[]
ne=0
idList={}
label=["Product Id", "Name", "Quantity","Cost per Unit"]
ip=''
store=None


class Product:
    def __init__(self,id,name,quantity,pricePerUnit,curr_date_time):
        self.productId=id
        self.productName=name
        self.productQuantity=quantity
        self.productPricePerUnit=pricePerUnit
        self.curr_date_time=curr_date_time

class Store:
    def __init__(self,productList):
        self.productList=productList
    
    def printList(self):
        for p in self.productList:
            print(p.productId,p.productName,p.productQuantity,p.productPricePerUnit,p.curr_date_time)
    def invoi(self,invoid,el1,el2,el3):
        invoiceNew.info(einvoice= invoid,ename= el1, eemail= el2, ephone= el3)
        for p in self.productList:
            print(p.productName,p.productPricePerUnit,p.productQuantity)
            invoiceNew.prodinfo(p.productName,p.productPricePerUnit,p.productQuantity,(p.productPricePerUnit*p.productQuantity))
        invoiceNew.savepdf()


    def checkout(self):
        global e1,ne
        total=0
        for p in productsList:
            if(p.productQuantity>=1):
                total += p.productQuantity * p.productPricePerUnit

        print("Total = ",total)
        print()
        print("#####################")
        #printDatabase(row_count,column_count)
        store.printList()
        ne=Tk()
        ne.title("Bill generation")
        ne.geometry("800x700")
        
        q1=tk.StringVar()
        q2=tk.StringVar()
        q3=tk.StringVar()
        q4=tk.StringVar()
        r=tk.IntVar()
        r.set("0")

        wrap1=LabelFrame(ne,text="Customer Details",height=180,width=200,font=('Arial',8))
        wrap2=LabelFrame(ne,text="Bill",height=360,width=200,font=('Arial',8))
        wrap3=LabelFrame(ne,text="Payment",height=180,width=200,font=('Arial',8))

        wrap1.pack(fill="both",expand="yes",padx=20)
        wrap2.pack(fill="both",expand="yes",padx=20,pady=5)
        wrap3.pack(fill="both",expand="yes",padx=20,pady=5)

        wrap1.grid_propagate(False)
        wrap2.grid_propagate(False)
        wrap3.grid_propagate(False)

        wrap4=LabelFrame(wrap2,height=300)
        wrap5=LabelFrame(wrap2,height=20)

        mycanva=Canvas(wrap4)
        mycanva.pack(side=LEFT)
        yscrollbar=ttk.Scrollbar(wrap4,orient="vertical",command=mycanva.yview)
        yscrollbar.pack(side=RIGHT,fill="y")
        myframe=Frame(mycanva)

        wrap4.pack(fill="both",expand="yes",padx=20)
        wrap5.pack(fill="both",expand="yes",padx=20)
        wrap4.grid_propagate(False)
        wrap5.grid_propagate(False)
        
        l1=Label(wrap1,text="Name:")
        l1.grid(row=4,column=0,padx=5,pady=8)
        l2=Label(wrap1,text="Mail Id:")
        l2.grid(row=10,column=0,padx=5,pady=8)
        l3=Label(wrap1,text="Mobile No:")
        l3.grid(row=14,column=0,padx=5,pady=8)
        l4=Label(wrap1,text="OTP")
        l4.grid(row=18,column=0,padx=5,pady=8)
        
        el1=Entry(wrap1,width=30,textvariable=q1)
        el1.grid(row=4,column=1,padx=5,pady=8,sticky=W)
        el2=Entry(wrap1,width=50,textvariable=q2)
        el2.grid(row=10,column=1,padx=5,pady=8,sticky=W)
        el3=Entry(wrap1,width=40,textvariable=q3)
        el3.grid(row=14,column=1,padx=5,pady=8,sticky=W)
        el4=Entry(wrap1,width=10,textvariable=q4)
        el4.grid(row=18,column=1,padx=5,pady=8,sticky=W)
        
        def disp():
            global ne,el1d,el2d,el3d,el4d
            regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
            def isValid(s):
                Pattern = re.compile("(0/91)?[7-9][0-9]{9}")
                return Pattern.match(s)
            if(el1.get().isalpha() == 1):
                el1d=el1.get()
            else:
                messagebox.showerror(title='Name Warning', message='Enter Valid Name.')
            if(re.search(regex, el2.get())):
                el2d=el2.get()
            else:
                messagebox.showerror(title='Mail Warning', message='Enter valid Mail.')
            el3d = el3.get()
            if(isValid(el3d)):
                el3d = el3.get()
            else:
                messagebox.showerror(title='Number Warning', message='Enter Valid Number.')
            rd=r.get()
            el4d=el4.get()
            if str(el4d)==str(otp):
                print('correct')
            else:
                messagebox.showerror(title='Wrong OTP', message='Try typing correct OTP.')
            
            #store.printList()
            print(el1d,el2d,el3d,el4d)

        def genInvoice():
            if status=='passed':
                invoice_num = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
                store.invoi(invoice_num,el1d,el2d,el3d)
                print("Generated Invoice and sent to email.")
                sendMsg.sendThanks(el3d)
                ne.destroy()
                root.destroy()
            else:
                print("Kindly retry the payment.")
                
        def receive_otp():
            global otp,el3d
            el3d = el3.get()
            otp=sendMsg.sendOtp(el3d)
            print('OTP',otp)
            

        submit=Button(wrap1,text="SUBMIT",command=disp)
        submit.grid(row=18,column=2,padx=5,pady=8)
        sendOTP=Button(wrap1,text="Send OTP",command=receive_otp)
        sendOTP.grid(row=18,column=1,padx=5,pady=8)
        
        head1=Label(wrap4,text="Product ID",width=12,font=('Arial',12,'bold'))
        head1.grid(row=0,column=0)
        head2=Label(wrap4,text="Product Name",width=12,font=('Arial',12,'bold'))
        head2.grid(row=0,column=10,padx=20)
        head3=Label(wrap4,text="Price Per Unit",width=15,font=('Arial',12,'bold'))
        head3.grid(row=0,column=20,padx=20)
        head4=Label(wrap4,text="Quantity",width=8,font=('Arial',12,'bold'))
        head4.grid(row=0,column=30,padx=20)
        head5=Label(wrap4,text="Total",width=10,font=('Arial',12,'bold'))
        head5.grid(row=0,column=40)
        co=1
        for y in self.productList:
            label=Label(wrap4,text=y.productId,width=13,font=('Arial',10))
            label.grid(row=co,column=0)
            label1=Label(wrap4,text=y.productName,width=10,font=('Arial',10))
            label1.grid(row=co,column=10,padx=20)
            
            label2=Label(wrap4,text=y.productPricePerUnit,width=10,font=('Arial',10))
            label2.grid(row=co,column=20,padx=20)
            
            label3=Label(wrap4,text=y.productQuantity,width=8,font=('Arial',10))
            label3.grid(row=co,column=30,padx=20)
            
            label4=Label(wrap4,text=(y.productPricePerUnit*y.productQuantity),width=10,font=('Arial',10))
            label4.grid(row=co,column=40)
    
            co+=1
        label5=Label(wrap5,text="Final Amount:",width=20, fg='black',font=('Arial',16,'bold'))
        label5.grid(row=0,column=30,padx=10,sticky=W)
        label6=Label(wrap5,text=total,width=30, fg='black',font=('Arial',16,'bold'))
        label6.grid(row=0,column=60,padx=10,sticky=W)

        def start_pay():
            global status
            
            ord_id = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
            print('order_id',ord_id)  
            amt=str(total*100)
            inp = open("templates/app2.html").read().replace("cost",amt)
            inp=inp.replace("apple",ord_id)
            file = open('templates/app.html', 'w')
            file.write(inp)
            file.close()
            
            webbrowser.open('http://127.0.0.1:5000/')
            status=app.get_amount(amt)
            print('Your payment status : ',status)
            genInvoice()
            


        def go_back():
            global ne
            ne.destroy()

        def start_againn():
            global ne,productsList,productsListIds,idList
            ne.destroy()
            root.destroy()
            productsList,productsListIds=[],[]
            idList={}
            self.productList=[]
            main_fun()
            
            
        #for (text,valu) in vals.items():
        #R1 = Radiobutton(wrap3, text="Debit", variable=r, value=1,indicator=0,background="light blue",command=lambda: sel(1))
        #R1.pack( fill=X,anchor=W)
        #R2 = Radiobutton(wrap3, text="Net banking", variable=r, value=2,indicator=0,background="light blue",command=lambda: sel(2))
        #R2.pack( fill=X,anchor=W)
        R3 = Radiobutton(wrap3, text="Proceed with Payment", variable=r, value=3,indicator=0,background="light blue",command=start_pay)
        R3.pack( fill=X,anchor=W)

        
        back=Button(wrap3,text="Go Back",command=go_back)
        back.grid(row=10,column=1,padx=5,pady=8)
        back.pack()
        start_again=Button(wrap3,text="Cancel Checkout",command=start_againn)
        start_again.grid(row=14,column=1,padx=5,pady=8)
        start_again.pack()

        la=Label(wrap3)
        la.pack()
        
        ne.mainloop()
        




def createProductList(pid,status=False):
    global curr_lst,productsList,productsListIds,lst
    curr_lst=[]
    if pid:
        # rownum=None
        # for i in range(2, row_count + 1):
        #     data = str(sheet.cell(row=i, column=1).value)
        #     #print(i,pid,data)
            # if data==pid:
                # rownum=i
        pid,pname,pQ,priceU=readData()
        if pid in productsListIds:
            for p in productsList:
                if pid==p.productId:
                    pQ+=1
                    if (result[0][5]>0):
                        # qq=("UPDATE mydatabase.productslist SET Total_Available_Quantity=Total_Available_Quantity -1 WHERE Product_id='%s';" %pid)
                        # mycursor.execute(qq)
                        # mydb.commit()
                        if (status):
                            p.productQuantity+=1
                            #p.productQuantity-=1
                        elif (not status) and p.productQuantity>0:
                            p.productQuantity-=1
                        curr_lst=[pid,pname,p.productQuantity,priceU]
                        print('CCC',curr_lst)
                    else:
                        print(pname,"- Not Available any more")
                        curr_lst=[pid,pname,pQ,priceU]
                        print('CCC---',curr_lst)

                            
                            
        else:
            current_date_and_time = datetime.datetime.now()
            current_date_and_time_string = str(current_date_and_time)
            curr_lst=[pid,pname,pQ,priceU]
            print(curr_lst)
            productsList.append(Product(pid,pname,pQ,priceU,current_date_and_time_string))
            productsListIds.append(pid)
           
       
    else:
        print("enter valid pid no.")

    return curr_lst
        
        
    


def readData():
    #workbook = file
    # sheet =  wb["Sheet"]
    # sheet=wb.active
    pid=result[0][7]
    pname=result[0][1]
    if result[0][5]>0:
        pQ=1
        # sheet.cell(row=rownum, column=3).value= int(sheet.cell(row=rownum, column=3).value)-1
        qq=("UPDATE mydatabase.productslist SET Total_Available_Quantity=Total_Available_Quantity -1 WHERE Product_id='%s';" %pid)
        mycursor.execute(qq)
        mydb.commit()
    else:
        print(pname,"- Not Available any more")
        pQ=0
    priceU=float(result[0][6])
    #wb.save("demo.xlsx")
    return pid,pname,pQ,priceU

def add():
    global tableSheet,idList, lst
    s.destroy()
    messagebox.showinfo("Quantity", "Item is added")
    
    lst=createProductList(ip,status=True)
    print('add',ip,lst)
    print(lst)
     
    v=lst[2]
    r=idList[lst[0]]-1
    createTable(row,lst)
    print(r,v)
    tableSheet.set_cell_data(r,2,value=v)
        

def nothing():
    #tableSheet.set_cell_data(r,2,value=v)
    s.destroy()
    messagebox.showinfo("Quantity", "Ok, No item added")
    
    

    
def rem():
    global idList, tableSheet
    s.destroy()
    messagebox.showinfo("Quantity", "Ok, item removed")
    print(ip)
    
    lst=createProductList(ip,status=False)
    print(lst)
    createTable(row,lst)
    print(lst)

    #v=lst[2]
    #r=idList[lst[0]]-1
    
    if v>=1:
        tableSheet.set_cell_data(r,2,value=v)
    else:
        print(idList,productsListIds)
        tableSheet.delete_row(idx = r, deselect_all = False)
        #messagebox.showinfo("Quantity", "Ok, item will be removed")
        messagebox.showwarning(title='Alert', message='All items are removed')
        for ix in range(len(productsList)) :
            p=productsList[ix]
            if p.productId==ip:
                productsList.remove(productsList[ix])

        del idList[ip]
        productsListIds.remove(ip)
        print(idList,productsListIds)
        flag=False
        #print(v)
        
def createTable(num,listt,flag=True):
    global s,r,v,tableSheet,idList
    
    #print('hello',tableSheet)
    
    if listt[0] in idList.keys():
        v=listt[2]
        r=idList[listt[0]]-1
        print(idList[listt[0]],v)

    elif(flag==False):
        
        v=listt[2]-1
        quit
    else:
        tableSheet.insert_row(listt)
        idList[listt[0]]=num

def display():
        global img, image_data,title,idno,name,price,quantity,row
        global lsts,s,ip,result,lst,tableSheet,idList
        title.destroy()
        idno.destroy()
        name.destroy()
        quantity.destroy()
        price.destroy()
        canvas.delete('all')
        if entry_1.get():
            ip=entry_1.get()
        else:
            ip=text
            print(text)
        q=("SELECT * FROM mydatabase.productslist WHERE Product_id ='%s';" %ip)
        mycursor.execute(q)
        result=mycursor.fetchall()
        print(result)
        print(ip,str(result[0][8]))
        image_data1 = str(result[0][8])
        image_data=str(image_data1[:6])+'/'+str(image_data1[7:])
        basewidth = 150
        img = Image.open(image_data)
        wpercent = (basewidth / float(img.size[0]))
        hsize = int((float(img.size[1]) * float(wpercent)))
        img = img.resize((basewidth, hsize), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        canvas.create_image(30, 190, anchor=NW, image=img)
    
        
        if ip in productsListIds:
            print('same prod id')
            s=Tk()
            s.title("Add Again / Remove ?")
            s.geometry('400x50')
            print(ip)
            #inp=ip
            title.destroy()
            idno.destroy()
            name.destroy()
            quantity.destroy()
            price.destroy()
            pid,pname,pQ,priceU=str(lst[0]),str(lst[1]),1,float(lst[3])
            title = tk.Label(fram1, text="Product Details",font='Helvetica 14 bold')
            title.pack(pady = 5)
            idno =  Label(fram1,text= label[0]+' : '+str(pid).upper() )
            idno.pack()
            name =  Label(fram1,text= label[1]+' : '+str(pname).upper() )
            name.pack()
            quantity =  Label(fram1,text= label[2]+' : '+str(pQ).upper() )
            quantity.pack()
            price =  Label(fram1,text= label[3]+' : '+str(priceU).upper() )
            price.pack()
            
            yes=Button(s,text='Yes',command= add)
        #yes.place(x=0,y=10)
            yes.pack(side = LEFT, padx = 30)
            no=Button(s,text='No',command = nothing)
        #no.place(x=100,y=10)
            no.pack(side = RIGHT, padx = 30)
            remove=Button(s,text='Remove',command= rem,width=100)
            remove.pack(side = RIGHT, padx = 20)
        else:
            lst=createProductList(ip)
            print(lst)
            pid,pname,pQ,priceU=str(lst[0]),str(lst[1]),1,float(lst[3])
        
            title = tk.Label(fram1, text="Product Details",font='Helvetica 14 bold')
            title.pack(pady = 5)
        
            idno =  Label(fram1,text= label[0]+' : '+str(pid).upper() )
            idno.pack()
            name =  Label(fram1,text= label[1]+' : '+str(pname).upper() )
            name.pack()
            quantity =  Label(fram1,text= label[2]+' : '+str(pQ).upper() )
            quantity.pack()
            price =  Label(fram1,text= label[3]+' : '+str(priceU).upper() )
            price.pack()
            createTable(row,lst)
            row+=1 
def main():
    rootmain.destroy()
    main_fun()

def main_fun():
    global title,idno,price,quantity,name,canvas,entry_1,root
    global fram1,fram2,fram3,root,tableSheet,row,e1,store
    # wb = load_workbook("demo.xlsx") 
    # Sheet is the SheetName where the data has to be entered
    mycursor.execute("select * from mydatabase.productslist")
    totallist=mycursor.fetchall()
    for i in totallist:
        i=list(i)
        print(i)
    #GUI--------------------------------------
    #global row
    row=1
    root=Tk()  
    #App Title  
    root.title("Smart Kart Application")  
    #ttk.Label(root, text="Products List").pack()  
    #Create Panedwindow  
    panedwindow=ttk.Panedwindow(root, orient=HORIZONTAL)  
    panedwindow.pack(fill=BOTH, expand=True)  

    panedwindow1=ttk.Panedwindow(root, orient=VERTICAL)  
    panedwindow1.pack(fill=BOTH, expand=True)
    #Create Frams  
    fram1=ttk.Frame(panedwindow,width=300,height=500, relief=SUNKEN)  
    fram2=ttk.Frame(panedwindow,width=400,height=500, relief=SUNKEN)  
    fram3=ttk.Frame(panedwindow1,width=720,height=80, relief=SUNKEN)
    
    panedwindow.add(fram1, weight=1)  
    panedwindow.add(fram2, weight=4)
    panedwindow1.add(fram3, weight=4)

    canvas = Canvas(fram1, width=200, height=400)
    canvas.pack()
    e1 = Entry(fram3, width=50, fg='black',font=('Arial',16,'bold'))

    #Initial Product Details display

    title = tk.Label(fram1, text="Product Details",font='Helvetica 14 bold')
    title.pack(pady = 5)
    idno = Label(fram1,text= label[0]+" : ------------")
    idno.pack()
    name =  Label(fram1,text= label[1]+" : ------------" )
    name.pack()
    quantity =  Label(fram1,text= label[2]+" : ------------" )
    quantity.pack()
    price =  Label(fram1,text=label[3]+" : ------------")
    price.pack()

    #Initial Image display
    image_data = "images/logo.png"
    img = Image.open(image_data)

    basewidth = 150

    wpercent = (basewidth / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((basewidth, hsize), Image.ANTIALIAS)

    img = ImageTk.PhotoImage(img)
    canvas.create_image(30, 190, anchor=NW, image=img)
    
       
    

    entry_1 = tk.StringVar() 
    entry_widget_1 = tk.Entry(fram1, textvariable=entry_1,bd =2)
    entry_widget_1.place(x=30, y=50)
   
    display_b = tk.Button(fram1, text="Enter", command=display)
    display_b.pack()
    display_b.place(x=140, y=80)

    scan = tk.Button(fram1, text="Scan", command=read_tag)
    scan.pack()
    scan.place(x=40, y=80)
    
    tableSheet = tksheet.Sheet(fram2,show_header = True,
    show_x_scrollbar = False,
    show_y_scrollbar = True,
    width = 500,
    height = 500,
    headers = label, theme = "dark blue",popup_menu_bg= "#00bfff")

    tableSheet.grid()

    print("---------------------------------------")
    store=Store(productsList)
    #store.checkout()
    print("---------------------------------------")

    check_out = tk.Button(fram3, text="check out", command=store.checkout)
    #check_out.pack()
    check_out.place(x=600, y=30)

    
    root.mainloop()
    
def read_tag():
        global text,ip
        print("Reading...")
        #text=input('enter : ')
        id, text = reader.read()      #-----uncomment whn rfid attached & comment above line
        ip=str(text).strip()
        print('Product Id : ',ip,text)
        #time.sleep(.5)
        #text1=str(text)+'F'
        #print('N> Product Id : ',text1)
        #reader.write(text1)
        display()
        #time.sleep(1)
        

if __name__=="__main__":
    try:
        #main_fun()
        global rootmain
        rootmain= Tk()
        # width x height
        rootmain.geometry("500x640")
        rootmain.title('Smart Kart Application')
        labelText = StringVar()
        labelText.set("Welcome To SMART KART !")
        text1 = Label(rootmain,textvariable=labelText,
                       font=("Times New Roman", 18), height=4, fg="black")
        text1.pack()

        photopppp = PhotoImage(file="images/logo.png")
        myimage = Label(image=photopppp)
        myimage.pack()

        start_shop = tk.Button(rootmain, text="Start Shopping", command=main)
        #check_out.pack(pady=600)
        start_shop.place(x=185, y=610)


        rootmain.mainloop()
        '''
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor() as executor:
            f1 = executor.submit(main_fun)
            #time.sleep(5)
            #f2 = executor.submit(read_tag)
        
        print(f1.result())
        #print(f2.result())
        #read_tag()
        
        t1 = threading.Thread(target=main_fun)
        t2 = threading.Thread(target=read_tag)
        t1.start()
        threads.append(t1)
        time.sleep(5)
        t2.start()
        threads.append(t2)


        for thread in threads:
            thread.join()
        '''
        
    finally:
        #pass
        GPIO.cleanup()     #----uncomment for raspberry pi
