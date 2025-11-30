
import win32com.client as win32
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()


initial_dir = r"F:\New_final_software\invoiceSW\ "
file_path = r"F:\New_final_software\invoiceSW\Template\INVOICE.docx "

if file_path:
    word = win32.Dispatch("Word.Application")
    doc = word.Documents.Open(file_path)
    word.Visible = True
    
# initial_dir = r"F:\New_final_software\invoiceSW\ "
# file_path = filedialog.askopenfilename(initialdir=initial_dir)

# if file_path:
#     word = win32.Dispatch("Word.Application")
#     doc = word.Documents.Open(file_path)
#     word.Visible = True
#------------------------------------------------------------------------
# import tkinter as tk
# from tkinter import filedialog         filedialog.askopenfilename(initialdir=initial_dir)

# root = tk.Tk()
# root.withdraw()

# file_path = filedialog.askopenfilename()

# if file_path:
#     print("Selected file:", file_path)
# -------------------------------------------------------
# import win32com.client as win32
# import tkinter as tk
# from tkinter import filedialog

# root = tk.Tk()
# root.withdraw()

# file_path = filedialog.askopenfilename()

# if file_path:
#     print("Selected file:", file_path)

    