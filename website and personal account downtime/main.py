import tkinter as tk
from tkinter import ttk
from tkinter import BOTH

from forms import Tab_view, Tab_readme, Tab_setup, Tab_setup_url


if __name__ == '__main__':

    window = tk.Tk()
    window.title("Простой сайта и ЛК")
    window.geometry('330x330')
    window.resizable(width=0, height=0)
    notebook = ttk.Notebook(window)
    notebook.pack(expand=True, fill=BOTH)
    form1 = tk.Frame(notebook)
    form2 = tk.Frame(notebook)
    form3 = tk.Frame(notebook)
    form4 = tk.Frame(notebook)
    form1.pack(fill=BOTH, expand=True)
    form2.pack(fill=BOTH, expand=True)
    form3.pack(fill=BOTH, expand=True)
    form4.pack(fill=BOTH, expand=True)
    notebook.add(form1, text="START")
    notebook.add(form2, text="README")
    notebook.add(form3, text="LOG/PASS")
    notebook.add(form4, text="URL")
    view = Tab_view(form_tab=form1)
    readme = Tab_readme(form_tab=form2)
    setup_log_pass = Tab_setup(form_tab=form3)
    setup_url = Tab_setup_url(form_tab=form4)
    window.mainloop()
