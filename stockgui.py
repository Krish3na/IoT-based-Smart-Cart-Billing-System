from tkinter import *  
import tkinter as tk
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="123456789",
  database="mydatabase"
)
mycursor = mydb.cursor()
ne=Tk()
ne.title("Stock")
ne.geometry("800x500")

q1=tk.StringVar()
q2=tk.StringVar()
q3=tk.StringVar()
q4=tk.StringVar()
q5=tk.StringVar()
q6=tk.StringVar()
q7=tk.StringVar()
q8=tk.IntVar()
q9=tk.IntVar()
q10=tk.StringVar()

wrap1=LabelFrame(ne,text="Stock Quantity Update ",height=150,font=('Arial',8))
wrap2=LabelFrame(ne,text="New Stock",height=200,font=('Arial',8))

wrap1.pack(fill="both",expand="yes",padx=20)
wrap2.pack(fill="both",expand="yes",padx=20,pady=5)

wrap1.grid_propagate(False)
wrap2.grid_propagate(False)

l1=Label(wrap1,text="Product ID")
l1.grid(row=4,column=0,padx=5,pady=8,sticky=W)
l2=Label(wrap1,text="Product Name")
l2.grid(row=10,column=0,padx=5,pady=8,sticky=W)
l3=Label(wrap1,text="Qty to be added")
l3.grid(row=20,column=0,padx=5,pady=8,sticky=W)

l4=Label(wrap2,text="Name of the product")
l4.grid(row=40,column=0,padx=5,pady=8,sticky=W)
l5=Label(wrap2,text="Category")
l5.grid(row=50,column=0,padx=5,pady=8,sticky=W)
l6=Label(wrap2,text="Type")
l6.grid(row=60,column=0,padx=5,pady=8,sticky=W)
l7=Label(wrap2,text="Brand")
l7.grid(row=70,column=0,padx=5,pady=8,sticky=W)
l8=Label(wrap2,text="Total Available Quantity ")
l8.grid(row=80,column=0,padx=5,pady=8,sticky=W)
l9=Label(wrap2,text="Cost per Quantity")
l9.grid(row=90,column=0,padx=5,pady=8,sticky=W)

# l7=Label(wrap2,text="Image")

el1=Entry(wrap1,width=40,textvariable=q1)
el1.grid(row=4,column=1,padx=5,pady=8,sticky=W)
el2=Entry(wrap1,width=40,textvariable=q2)
el2.grid(row=10,column=1,padx=5,pady=8,sticky=W)
el3=Entry(wrap1,width=40,textvariable=q3)
el3.grid(row=20,column=1,padx=5,pady=8,sticky=W)
el4=Entry(wrap2,width=40,textvariable=q4)
el4.grid(row=40,column=1,padx=5,pady=8,sticky=W)
el5=Entry(wrap2,width=40,textvariable=q5)
el5.grid(row=50,column=1,padx=5,pady=8,sticky=W)
el6=Entry(wrap2,width=40,textvariable=q6)
el6.grid(row=60,column=1,padx=5,pady=8,sticky=W)
el7=Entry(wrap2,width=40,textvariable=q7)
el7.grid(row=70,column=1,padx=5,pady=8,sticky=W)
el8=Entry(wrap2,width=40,textvariable=q8)
el8.grid(row=80,column=1,padx=5,pady=8,sticky=W)
el9=Entry(wrap2,width=40,textvariable=q9)
el9.grid(row=90,column=1,padx=5,pady=8,sticky=W)


# el1d=el1.get()
# print(el1d)
# el2d=el2.get()
# print(el2d)
# el3d=el3.get()
# print(el3d)
# el3d=float(el3d)




def updateqty():
    global el1,el2,el3
    el1d=el1.get()
    print(el1d)
    el2d=el2.get()
    print(el2d)
    el3d=el3.get()
    el3d=int(el3d)
    print(el3d)
    qq=("UPDATE mydatabase.productslist SET Total_Available_Quantity=Total_Available_Quantity + '%s' WHERE Product_id='%s';" %(el3d,el1d))
    mycursor.execute(qq)
    mydb.commit()
sno=11
def newstock():
    global el4,el5,el6,el7,el8,el9,sno
    el4d=el4.get()
    el5d=el5.get()
    el6d=el6.get()
    el7d=el7.get()
    el8d=el8.get()
    el9d=el9.get()
    prodid=el4d[:2].upper()+el5d[:2].upper()+el6d[:2].upper()+el7d[:2].upper()+"121"
    print(prodid)

    q=("INSERT INTO mydatabase.productslist (sno,name_of_the_product,Category,Type,Brand,Total_Available_Quantity,Cost_per_Quantity,Product_id) VALUES ('%s', '%s', '%s', '%s','%s', '%s', '%s', '%s','%s');" %(sno,el4d,el5d,el6d,el7d,el8d,el9d,prodid))
    mycursor.execute(q)
    mydb.commit()
    sno+=1



submit=Button(wrap1,text="SUBMIT",command=updateqty)
submit.grid(row=10,column=20,padx=150,pady=18,sticky=W)

submit=Button(wrap2,text="SUBMIT",command=newstock)
submit.grid(row=50,column=20,padx=150,pady=18,sticky=W)

ne.mainloop()