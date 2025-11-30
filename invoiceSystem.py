# pip install python-docx
# pip install docxtpl
# pip install docx2pdf
# pip install tkcalendar
# pip install pillow #for PIL

import tkinter as tik
import re
import os
import smtplib
import DBhelper as DBH
from tkinter import PhotoImage
from email.message import EmailMessage
from docxtpl import DocxTemplate
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from docx2pdf import convert
from tkcalendar import Calendar, DateEntry  
from datetime import date,datetime
from PIL import Image, ImageTk

# main class 

class main:  
    def __init__(self):
        self.emailID = ""  
        self.name = ""
        self.address = ""
        self.addhar = ""
        self.city = ""
        self.mobile = ""
        self.emailID = ""
        self.discount = ""
        self.gst = ""
        self.today_date = ""
        self.inno = 0

    temp_var=0
    # function to set values and calculation

    def setval(self):#on calculate button press
        self.name = name_txt.get() 
        self.address = add_txt.get("1.0", "end-1c")
        self.addhar = addhar_txt.get()
        self.city = city_txt.get()
        self.mobile = mono_txt.get()
        self.emailID = email_txt.get()
        self.discount = int(dis_txt.get())
        self.gst = int(gst_txt.get())
        self.today_date = date.today()
        self.inno = 0
    
        #validation::--

        # Name validation
        name_regex = r'^[A-Za-z ]+$'
        if(re.fullmatch(name_regex,self.name)):
            pass
        else:
            messagebox.showerror('Invalid Input','ENTER NAME')
            return

        # Mobile validation
        mobile_regex = r'^\d{10}$'
        if(re.fullmatch(mobile_regex,self.mobile)):
            pass
        else:
            messagebox.showerror('Invalid Input','ENTER MOBILE No.')
            return

        # Addhar validation
        addhar_regex = r'^\d{12}$'
        if(re.fullmatch(addhar_regex,self.addhar)):
            pass
        else:
            messagebox.showerror('Invalid Input','ENTER ADDHAR No.')
            return

        #calculations::--

            # total of amount
        self.total_amount = sum(item[5] for item in self.invoice_list)
        
            #cal for dis
        self.subtotal = self.total_amount-((self.total_amount*self.discount)/100)
        
            #cal for cgst
        self.cgst = float((self.subtotal*(self.gst/2))/100)
        
            #cal for sgst1
        self.sgst = float((self.subtotal*(self.gst/2))/100)
            
            #cal for total
        self.total = round((self.subtotal + self.cgst + self.sgst),2)
        
        total_txt.config(text=f"{self.total}")
        
       
        if(self.temp_var!=0):
            pass
        else:
            messagebox.showerror("INFO","ADD ITEM FIRST")
            return
               
    # globalized invoice list
    invoice_list = []    

    #function to add rooms

    def addroom(self,roomno,rate):#on add_room button press
        
        # list of rooms and its calcualtion
        #self.roomno = roomno_txt.get()
        self.checkin = datetime.strptime(checkin_txt.get(),'%d/%m/%Y').date()
        self.checkout = datetime.strptime(checkout_txt.get(),'%d/%m/%Y').date()
        #self.rate = float(rate_txt.get())

        if self.checkout< self.checkin:
            messagebox.showerror("Invalid Date", "Checkout date cannot be earlier than check-in date.")
            return
            
        #cal for no of night
        self.diference = self.checkout-self.checkin
        self.noofnight = self.diference.days 
        
        #cal for Rate
        self.amount = float(float(rate) * self.noofnight)
        
        #putting into tree 
        self.tree_items = [roomno , self.checkin , self.checkout , self.noofnight , rate , self.amount] 
        tree.insert('',0,values=self.tree_items)
        
        self.invoice_list.append(self.tree_items)
        
        self.temp_var+=1
        
        obj.clear_room()   
    
    #function to clear values of room
    def clear_room(self):
        roomno_txt.delete(0, tik.END)
        rate_txt.delete(0, tik.END)

    #function to clear values of tree
    def clear_tree(self):
        # to delete data from tree
        tree.delete(*tree.get_children())
        # to delete invoice room list
        self.invoice_list.clear()

    #function to clear values of customer
    def clear_customer(self):
        for entry in [name_txt,addhar_txt, city_txt, mono_txt, email_txt]:
            entry.delete(0, tik.END)
            add_txt.delete("1.0","end")
        
    #function to clear all data
    def clear_all(self):
        total_txt.config(text="")
        obj.clear_room()
        obj.clear_tree()
        obj.clear_customer()
        
            
    # function to put values in Docs  
    def putval(self): 
        # Name validation
        name_regex = r'^[A-Za-z ]+$'
        if(re.fullmatch(name_regex,self.name)):
            pass
        else:
            messagebox.showerror('Invalid Input','ENTER NAME')
            return

        # Mobile validation
        mobile_regex = r'^\d{10}$'
        if(re.fullmatch(mobile_regex,self.mobile)):
            pass
        else:
            messagebox.showerror('Invalid Input','ENTER MOBILE No.')
            return

        # Addhar validation
        addhar_regex = r'^\d{12}$'
        if(re.fullmatch(addhar_regex,self.addhar)):
            pass
        else:
            messagebox.showerror('Invalid Input','ENTER ADDHAR No.')
            return

        # Gmail validation
        email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(email_regex, self.emailID):
            messagebox.showerror("Invalid Email", "Please enter a valid email address.")
            return
            
        #opening CSV file
        response = messagebox.askquestion("INFO", "Are you sure?")
        if(response == "yes"):    
            # Open the CSV file for reading and writing
            # with open('demo.csv', 'r+') as csvfile:
            #     # Read the current invoice number from the file
            #     reader = csv.reader(csvfile)
            #     row = next(reader)
            #     invoice_number = int(row[0])
            #     # Increment the invoice number
            #     self.inno = invoice_number
            #     invoice_number += 1
            
            #     # Write the new invoice number back to the file
            #     csvfile.seek(0)
            #     writer = csv.writer(csvfile)
            #     writer.writerow([invoice_number])

            self.cid = DBH.insert_customer(self.name,self.mobile,self.addhar,self.city,self.address,self.emailID)

            self.inno = DBH.insert_invoice(self.cid,self.amount,self.discount,(self.cgst+self.sgst))
            
            DBH.insert_invoice_details(self.inno , self.invoice_list)

            doc = DocxTemplate('invoiceSW\Template\INVOICE.docx')        
        
            doc.render({"name":self.name,
                    "mobile":self.mobile,
                    "addhar":self.addhar,
                   "address":self.address,
                   "city":self.city,
                   "email":self.emailID,
                   "invoice_list":self.invoice_list,
                   "discount":self.discount,
                   "amount":self.amount,
                   "cgst":self.cgst,
                   "sgst":self.sgst,
                   "total_amount":self.total_amount,
                   "total":self.total,
                   "inno":self.inno})

            # Save rendered DOCX
            docx_filename = f'{self.inno}.docx'
            pdf_filename = f'{self.inno}.pdf'
            save_dir = os.path.abspath('invoiceSW')

            docx_path = os.path.join(save_dir, docx_filename)
            pdf_path = os.path.join(save_dir, pdf_filename)

            doc.save(docx_path)

            # Convert to PDF using docx2pdf
            convert(docx_path, pdf_path)

            if os.path.exists(docx_path):
                os.remove(docx_path)

            # Save file info
            self.doc_new = pdf_filename
            self.path_save = pdf_path

            messagebox.showinfo("Info", "Invoice Generated and Saved as PDF Successfully!") 

            
            
    def show(self):
        ans = messagebox.askquestion("Openinfo", "DO YOU WANT TO OPEN CURRENT INVOICE?")
        print(ans)

        if ans == "yes":
            if hasattr(self, 'doc_new'):
                base_path = os.path.abspath("invoiceSW")
                file_path = os.path.join(base_path, self.doc_new)

                if os.path.exists(file_path):
                    os.startfile(file_path)
                else:
                    messagebox.showerror("File Not Found", f"Could not find file:\n{file_path}")
            else:
                messagebox.showerror("No Invoice", "No invoice has been generated yet.")
        else:
            initial_dir = os.path.abspath("invoiceSW")
            file_path = filedialog.askopenfilename(
                initialdir=initial_dir,
                filetypes=[("PDF Files", "*.pdf")],
                title="Select an Invoice PDF"
            )

            if file_path:
                os.startfile(file_path)
            else:
                messagebox.showinfo("No File Selected", "No PDF was selected.")
            

    
    def share(self):
        email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        self.emailID = email_txt.get()
        if not re.match(email_regex, self.emailID):
            messagebox.showerror("Invalid Email", "Please enter a valid email address.")
            return

        initial_dir = os.path.abspath("invoiceSW")
        file_path = filedialog.askopenfilename(
            initialdir=initial_dir,
            filetypes=[("PDF Files", "*.pdf")],
            title="Select an Invoice PDF"
        )

        # Create the email
        msg = EmailMessage()
        msg['Subject'] = 'Your Invoice'
        msg['From'] = "your_gmail@gmail.com"
        msg['To'] = self.emailID
        msg.set_content('Please find attached the invoice in PDF format.')

        # Read and attach the PDF
        with open(file_path, 'rb') as f:
            file_data = f.read()
            file_name = os.path.basename(file_path)

        msg.add_attachment(file_data, maintype='application', subtype='pdf', filename=file_name)

        # Connect and send the email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login("your_gmail@gmail.com", "xftl dica xcba tndp")
            smtp.send_message(msg)

        messagebox.showinfo("Info", "Invoice Sent Successfully!") 
    
    

obj = main()

#-----------------------output window creation --------------------------------

# window creation name invoice input
window=tik.Tk()
icon = PhotoImage(file="Logo2.png")
window.iconphoto(True, icon)
window.state('zoomed')
window.title("INVOICIFY")

# main windows frame
frame=tik.Frame(window)
frame.pack(padx=20)

FONT1 = ("Arial", 12)
FONT2 = ("Arial", 16)

room_type_var = tik.StringVar()
room_number_var = tik.StringVar()
price_var = tik.StringVar()

# functions that will be called on command of Button
def generate_invoice():
    obj.putval()


def add_room():
    obj.addroom(room_number_var.get(),price_var.get())

def calc():
    obj.setval()

# close button command define
def close():
    window.quit()

# Print File Function
def share_file():
    obj.share()
   
# open file 
def open_file():
    obj.show()

#gets available rooms
def get_available_rooms(event):
    room_type = room_type_var.get()
    checkin = datetime.strptime(checkin_txt.get(),'%d/%m/%Y').date()
    checkout = datetime.strptime(checkout_txt.get(),'%d/%m/%Y').date()
    
    results = DBH.get_available_rooms(checkin , checkout , room_type)

    available_rooms = [row[0] for row in results]
    
    roomno_txt['values'] = available_rooms


def room_price(event):
    room_type = room_type_var.get()
    room_number = room_number_var.get()

    result = DBH.get_room_price(room_type,room_number)

    if result:
        price = result[0]
        price_var.set(price)
    else:
        print("No matching room found.")

#logo 
logo_get = Image.open("Logo.png").resize((220, 75))
logo = ImageTk.PhotoImage(logo_get)

logo_label = tik.Label(frame,image=logo)
logo_label.image = logo

logo_label.grid(row=0,column=2,columnspan=2)

# title cus info
cus_info_lab=tik.Label(frame, text="-: Customer Info :- ",font=FONT2)
cus_info_lab.grid(row=1,column=0,pady=10,columnspan=6)
# title room info
room_info_lab=tik.Label(frame, text="-: Room Info :- ",font=FONT2)
room_info_lab.grid(row=4,column=0,pady=10,columnspan=6)

# Custome column code
# lab fName
name_lab=tik.Label(frame, text="Name *",font=FONT1)
name_lab.grid(row=2,column=0)
# Txt box for fname
name_txt=tik.Entry(frame,font=FONT1)
name_txt.grid(row=2,column=1,pady=10)

# lab mobile no
mono_lab=tik.Label(frame, text="Mobile No.*",font=FONT1)
mono_lab.grid(row=2,column=2)
# Txt box for mobile no
mono_txt=tik.Entry(frame,font=FONT1)
mono_txt.grid(row=2,column=3,pady=10)

#lab Addhar No.
addhar_lab=tik.Label(frame, text="Addhar No.*",font=FONT1)
addhar_lab.grid(row=2,column=4)
# Txt box for lname
addhar_txt=tik.Entry(frame,font=FONT1)
addhar_txt.grid(row=2,column=5,pady=10)

# lab city
city_lab=tik.Label(frame, text="City",font=FONT1)
city_lab.grid(row=3,column=0)
# Txt box for city
city_txt=tik.Entry(frame,font=FONT1)
city_txt.grid(row=3,column=1,pady=10)

# lab address
add_lab=tik.Label(frame, text="Address",font=FONT1)
add_lab.grid(row=3,column=2)
# Txt box for address
add_txt=tik.Text(frame, height=3, width=20,font=FONT1)
add_txt.grid(row=3,column=3,pady=10)

# lab email
email_lab=tik.Label(frame, text="Email",font=FONT1)
email_lab.grid(row=3,column=4)
# Txt box for email
email_txt=tik.Entry(frame,font=FONT1)
email_txt.grid(row=3,column=5,pady=10)

# room column code
# lab check in
checkin_lab=tik.Label(frame, text="Check In",font=FONT1)
checkin_lab.grid(row=5,column=1)
# Txt box for checkin
checkin_txt=DateEntry(frame,date_pattern="dd/mm/y",font=FONT1,width=18)
checkin_txt.grid(row=5,column=2,pady=10)

# lab check out
checkout_lab=tik.Label(frame, text="Check out",font=FONT1)
checkout_lab.grid(row=5,column=3)
# Txt box for check out
checkout_txt=DateEntry(frame,date_pattern="dd/mm/y",font=FONT1,width=18)
checkout_txt.grid(row=5,column=4,pady=10)

# lab room type
roomtype_lab=tik.Label(frame, text="Room Type*",font=FONT1)
roomtype_lab.grid(row=6,column=0)
# Txt box for roomtype
room_options = ["Standard Non-AC", "Standard AC", "Deluxe Non-AC","Deluxe AC","Suite AC"]
roomtype_txt=tik.ttk.Combobox(frame, values=room_options, textvariable=room_type_var, state="readonly",font=FONT1)
roomtype_txt.current(0)
roomtype_txt.grid(row=6,column=1,pady=10)
roomtype_txt.bind("<<ComboboxSelected>>", get_available_rooms)

# lab roomno
roomno_lab=tik.Label(frame, text="Room No.*",font=FONT1)
roomno_lab.grid(row=6,column=2)
# Txt box for roomno
roomno_txt=tik.ttk.Combobox(frame, textvariable=room_number_var, state="readonly",font=FONT1)
roomno_txt.unbind("<<ComboboxSelected>>")
roomno_txt.grid(row=6,column=3,pady=10)
roomno_txt.bind("<<ComboboxSelected>>", room_price)

# lab rate
rate_lab=tik.Label(frame, text="Rate *",font=FONT1)
rate_lab.grid(row=6,column=4)
# Txt box for rate
rate_txt=tik.Entry(frame, textvariable=price_var,font=FONT1)
rate_txt.grid(row=6,column=5,pady=10)

# lab dis
dis_lab=tik.Label(frame, text="Discount",font=FONT1)
dis_lab.grid(row=7,column=1)
# Txt box for dis
dis_txt=tik.Spinbox(frame, from_= 0, to = 15, increment = 5, justify="center",font=FONT1,width=19)
dis_txt.grid(row=7,column=2,pady=10)

# lab gst
gst_lab=tik.Label(frame, text="GST Rate",font=FONT1)
gst_lab.grid(row=7,column=3)
# Txt box for gst
gst_txt=tik.Spinbox(frame, from_= 12, to = 18, increment = 6, justify="center",font=FONT1,width=19)
gst_txt.grid(row=7,column=4,pady=10)

# making tree to display info
clos = ('Room No','Check In Date','Check Out Date','Number of Night','Price','Total')

tree = ttk.Treeview(frame, columns=clos, show="headings", height=5)
style = tik.ttk.Style()
style.configure("Treeview", font=FONT1, rowheight=28)
style.configure("Treeview.Heading", font=FONT2)

for col in clos:
    tree.column(col, anchor='center')       # Center cell content
    tree.heading(col, anchor='center')      # Center header text
tree.grid(row=8, column=0, columnspan=6, padx=20, pady=20)

# giving name of columns in tree
tree.heading('Room No',text='Room No')
tree.heading('Check In Date',text='Check In Date')
tree.heading('Check Out Date',text='Check Out Date')
tree.heading('Number of Night',text='Number of Night')
tree.heading('Price',text='Rate')
tree.heading('Total',text='Total')

# clear all button
cleartree_butt=tik.Button(frame, text="Clear List" ,font=FONT1,command=obj.clear_tree)
cleartree_butt.grid(row=9,column=0,columnspan=2,pady=10,padx=5,sticky="news")   

# clear all button
clearall_butt=tik.Button(frame, text="Clear All" ,font=FONT1,command=obj.clear_all)
clearall_butt.grid(row=9,column=2,columnspan=2,pady=10,padx=5,sticky="news")

# lab total
total_lab=tik.Label(frame, text="Total",font=FONT2)
total_lab.grid(row=9,column=4)

# Txt box for total
total_txt=tik.Label(frame, text="",font=FONT2)
total_txt.grid(row=9,column=5,pady=5)

# add item button
add_room_butt=tik.Button(frame, text="Add Item" ,font=FONT1,command=add_room)
add_room_butt.grid(row=10,column=0,columnspan=2,pady=10,padx=5,sticky="news")

# calculate button
calc_butt=tik.Button(frame, text="Calculate" ,font=FONT1,command=calc)
calc_butt.grid(row=10,column=2,columnspan=2,pady=10,padx=5,sticky="news")

# generate button
generate_butt=tik.Button(frame, text="Generate",font=FONT1, command=generate_invoice)
generate_butt.grid(row=10,column=4,columnspan=2,pady=10,padx=5,sticky="news")

# to open invoice
open_butt=tik.Button(frame, text="Open",font=FONT1, command=open_file)
open_butt.grid(row=11,column=0,columnspan=2,pady=10,padx=5,sticky="news")

#Print button
share_butt=tik.Button(frame, text="Send" ,font=FONT1,command=share_file)
share_butt.grid(row=11,column=2,columnspan=2,pady=10,padx=5,sticky="news")

# exit button
exit_butt=tik.Button(frame, text="Exit",font=FONT1, command=close)
exit_butt.grid(row=11,column=4,columnspan=2,pady=10,padx=5,sticky="news")

window.mainloop()
