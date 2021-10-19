import tkinter.messagebox
from tkinter import *

interface = Tk()
varOption = IntVar()

def run():
    tweets = entry_nooftweets.get()
    if not tweets:
        tkinter.messagebox.showerror(title="Empty Field!", message="Please enter number of tweets.")
    if tweets and not tweets.isnumeric():
        tkinter.messagebox.showerror(title="Error!", message="Please enter an integer.")

def do():
    if varOption.get() == 1:
        sentiment.config(text="Positive")
    else:
        sentiment.config(text="Negative")

"""def listbox_used(event):
    print(listbox.get(listbox.curselection()))


listbox = tkinter.Listbox(height=4)
fruits = ["Apple", "Pear", "Orange", "Banana"]
for item in fruits:
    listbox.insert(fruits.index(item), item)
listbox.bind("<<ListboxSelect>>", listbox_used)
listbox.pack()"""

if __name__== "__main__":
    interface.title("Covid-19 Data Crawler")
    interface.configure(background='orange')
    interface.geometry("900x600")
    font_tuple = ("Microsoft Yahei UI", 20, "bold")
    title = Label(interface, text="Sentiment Analysis of the Public during Covid-19", bg="orange", fg="blue", font=font_tuple).place(
        x=150, y=80)
    rb_pos = Radiobutton(interface, text = "Positive", bg="orange", font=font_tuple, variable = varOption, value = 1).place(x=150, y=150)
    rb_neg = Radiobutton(interface, text="Negative", bg="orange", font=font_tuple, variable=varOption, value=2).place(x=150,y=200)
    entry_nooftweets = Entry(interface, font=font_tuple, width=10)
    submit_button = Button(interface, text="Submit", bg="red3", font=font_tuple, borderwidth=3, command=lambda:[do(), run()], height=1,
                           width=8).place(x=435, y=340)
    entry_nooftweets.place(x=150, y=270)
    sentiment = Label(interface)
    sentiment.pack()
    interface.mainloop()

def setup(self):
    sb = tkinter.Scrollbar(self.root)
    sb.set(0.1, 0.55)

    sb.pack(side='right', fill='y')
    self.nb = tkinter.Notebook(self.root)
    self.nb.pack(fill='both', expand='yes')
    self.tab = self.create_themed_tab()
    self.nb.add(self.tab, text='Tab 1')
    self.nb.add(tkinter.Frame(self.nb), text='Tab 2')
    self.nb.add(tkinter.Frame(self.nb), text='Tab 3')