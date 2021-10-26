from tkinter import *
from tkinter import ttk
from tkinter import filedialog, messagebox
from tkinter import NW
import twint
from deep_translator import GoogleTranslator, single_detection
import pandas as pd
import os
from PIL import ImageTk, Image
import tkinter.messagebox


# imported modules used for GUI to function

def startFromMenu():
    """This function re-does the gui navigation bar and frames after navigating from the menu page"""
    mainMenuFrame.pack_forget()  # removes any frame used for the main menu page
    graphData()  # brings user to the graph data page

        # creating of navigation bars
    homePageMenu = Button(buttonFrame, text="Main Menu", command=mainMenu, padx=20, pady=10)
    graphButtonMenu = Button(buttonFrame, text="Generate Graph", padx=20, pady=10,
                                    command=graphData)
    exitButtonMenu = Button(buttonFrame, text="QUIT the Application", padx=30, pady=10, command=exitWindow)

        # default pack/grid area to place the buttons back
    homePageMenu.grid(row=0, column=0)
    graphButtonMenu.grid(row=0, column=1)
    exitButtonMenu.grid(row=0, column=3)

    # default Frames Creation
    
def mainMenu():
    """Function runs when users navigate to the main menu"""
    mainframe.pack_forget()  # hides any frames used for the content page/navigation bar
    buttonFrame.pack_forget()
    for widget in buttonFrame.winfo_children():  # removes all the buttons in the navigation bar
        widget.destroy()

    mainMenuFrame.pack(fill=BOTH, expand=1)  # create a new frame specifically for the main menu page
    Label(mainMenuFrame, text="MAIN MENU", font=("Microsoft Yahei UI", 44, "bold"), bg="Orange", fg="White").pack(
            anchor=N, expand=1)
    Label(mainMenuFrame, text="Covid-19 Data Crawler", font=("Microsoft Yahei UI", 25), bg="Orange", fg="Blue").pack(
            anchor=N, expand=1)
    startUse = Button(mainMenuFrame, text="Start Application", font=("Microsoft Yahei UI", 15), padx=44, pady=10,
                          command=startFromMenu)  # create start application button
    exitFromMenu = Button(mainMenuFrame, text="QUIT", padx=30, font=("Microsoft Yahei UI", 15), pady=10,
                              command=exitWindow)  # create exit button

        # button packing area
    startUse.pack()
    exitFromMenu.pack(expand=1)

    return

def chooseFile():
    global tempdir
            # stores the file path of the user selected data-set to be used with our other functions
    tempdir = filedialog.askopenfilename(initialdir="",  title="Select Dataset", filetypes=((".csv Files", "*.csv"), ("All Files", "*.*")))
            # sending file path to var so other functions can use the file path
            # parse file path
    if tempdir == '':
        messagebox.showerror("Error", "Choose a file!")
    elif tempdir[-3:].lower() not in ['csv', 'prn', 'xls', 'ods'] and tempdir[-4:].lower() not in ['xlsx', 'xltx', 'xlsm',  'xlsb']:
        messagebox.showerror("Error", "Choose a CSV file!")  # Error messagebox

def hideFrames():
    """This function is used to clear all the contents in the frame after navigating to a new function"""
    contentFrame.pack_forget()  # forgets the frame storing content temporarily until it is being packed again.
    for widget in contentFrame.winfo_children():  # loops through all the widgets used in the content frame and destroy all of them
        widget.destroy()

    mainMenuFrame.pack_forget()  # forgets the mainMenuFrame which is different from the frame storing content.
    for widget in mainMenuFrame.winfo_children():
        widget.destroy()

    return

def runData(x):
    global file_path
    file_path = x
    file_name = file_path  # In same Folder
    def twint_to_pd(columns):
        return twint.output.panda.Tweets_df[columns]

    c = twint.Config()
    c.Search = 'covid'  # Search tweet that contain the word "covid"
    c.Geo = "1.352083,103.819839,20km"  # Geo define the geolocation of the origin of the Tweet. Hence, Singapore's Geo Location will be use in this Singapore-Based Project
    c.Since = "2021-09-24"  # Search tweet from the date 2021/09/24
    c.Limit = '20'  # Limit Define the number of tweet to Extract
    c.Pandas = True
    twint.run.Search(c)

    data = twint_to_pd(['id', 'conversation_id', 'created_at', 'date', 'timezone', 'place',
                        'tweet', 'language', 'hashtags', 'cashtags', 'user_id', 'user_id_str',
                        'username', 'name', 'day', 'hour', 'link', 'urls', 'photos', 'video',
                        'thumbnail', 'retweet', 'nlikes', 'nreplies', 'nretweets', 'quote_url',
                        'search', 'near', 'geo', 'source', 'user_rt_id', 'user_rt',
                        'retweet_id', 'reply_to', 'retweet_date', 'translate', 'trans_src',
                        'trans_dest'])
    data.to_csv(file_name, index=False)  # Data Scraped for twint is written to a CSV.
    
    df = pd.read_csv(file_name, sep=",")
    df.drop(df[df['language'] == 'und'].index,
                        inplace=True)  # No language detection when tweets contain only URL. Such tweets is labeled as "und" by twint.
    df.to_csv(file_name, index=False)  # Write/update changes to CSV file
    num = len(df['tweet'])
    count = 1

    for i in range(0, num, 1):
        lang = single_detection(df['tweet'][i], api_key='882c59b16ed56b80efb9405b96bc6926')
        if lang != 'en':
            df._set_value(i, 'tweet',
                                      GoogleTranslator(source='auto', target='en').translate(df['tweet'][i]))
            df.to_csv(file_name, index=False)
            count += 1
            print("Row Number:" + str(count) + " (Translated Tweet)")
        else:
            count += 1
            print("Row Number:" + str(count) + " (English Tweet)")

def graphData():
    def buttoncommand():
        searchTerm = entry1.get()
        numberOfTweets = entry2.get()

        if not tempdir:
            tkinter.messagebox.showerror(title="Error!", message="Please choose a dataset.")
        elif not numberOfTweets:
            tkinter.messagebox.showerror(title="Empty Field!", message="Please enter number of tweets.")
        elif numberOfTweets and not numberOfTweets.isnumeric():
            tkinter.messagebox.showerror(title="Error!", message="Please enter an integer.")
        else:     
            buttonFrame.pack_forget()
            runData(tempdir)
            
            print("Refer to " + tempdir + " for result")
            """This function listens to the 'event' and displays the graph based on the datatype selected using the combobox"""
            os.system('K:/Programs/Python/python.exe emotionanalysis.py')
            os.system('K:/Programs/Python/python.exe topicmodelling.py')
            os.system('K:/Programs/Python/python.exe wordcloudgenerator.py')
            label1.destroy()
            entry1.destroy()
            label2.destroy()
            entry2.destroy()
            label3.destroy()
            button1.destroy()
            uploadButton.destroy()

            def nex_img(i):  # takes the current scale position as an argument
                # delete previous image
                canvas.delete('image')
                # create next image
                canvas.create_image(20, 20, anchor=NW, image=listimg[int(i) - 1], tags='image')

            image1 = ImageTk.PhotoImage(Image.open('Topics.png'))
            image2 = ImageTk.PhotoImage(Image.open('WordCloud.png'))
            img = Image.open('emotionanalysis.png')
            img = img.resize((800, 950), Image.ANTIALIAS)
            image3 = ImageTk.PhotoImage(img)
            listimg = [image1, image2, image3]
            scale = Scale(master=contentFrame, orient=HORIZONTAL, from_=1, to=len(listimg), resolution=1, showvalue=False,
                          command=nex_img)
            scale.pack(side=BOTTOM, fill=X)
            canvas = Canvas(contentFrame, width=1920, height=1080)
            canvas.pack()
            # show first image
            nex_img(1)
            return None

    hideFrames()
    title = Label(contentFrame, text="Covid-19 Data Crawler", fg="blue", font="lucida 25 bold")
    title.pack()
    label1 = Label(contentFrame, text="Upload a dataset:")
    label1.pack()
    uploadButton = Button(contentFrame, text="Upload", command=chooseFile)
    uploadButton.pack()
    label2 = Label(contentFrame, text='Please enter search term:')
    label2.pack()
    entry1 = Entry(contentFrame, width=20)
    entry1.pack()
    label3 = Label(contentFrame, text='Please enter number of tweets to be searched:')
    label3.pack()
    entry2 = Entry(contentFrame, width=20)
    entry2.pack()
    dataType = [  # dropdown list options
            "Top 10 words for each emotion",
            "LDA Topics",
            "Wordcloud of tweets",
        ]

    clicked = StringVar()
    clicked.set(dataType[0])

    button1 = Button(contentFrame, text="Search", command=buttoncommand)
    button1.pack()

    bottom_frame = Frame(gui)
    bottom_frame.pack()

        # default packing area
    buttonFrame.pack()
    mainframe.pack(fill=BOTH, expand=1)
    contentFrame.pack(fill=BOTH, expand=1)

def exitWindow():
    """This function forces the app to exit/quit"""
    gui.quit()

gui = Tk()
gui.iconbitmap('icons/SIT_logo_2.ico')
gui.title("Covid-19 Data Crawler")
gui.geometry("900x600+10+10")
gui.attributes('-topmost', True)
mainMenuFrame = Frame(gui, relief=SUNKEN, height=800, width=1000, background='Orange')
buttonFrame = Frame(gui, height=100, width=1000, borderwidth=10, relief=GROOVE, background='Orange')
mainframe = Frame(gui, height=550, width=1000, borderwidth=10, relief=SUNKEN, background='Orange')
contentFrame = Frame(mainframe, height=600, width=1000, borderwidth=10)

    # Main Buttons creation section
homePage = Button(buttonFrame, text="Main Menu", command=mainMenu, padx=20, pady=10)
barGraphButton = Button(buttonFrame, text="Generate Graphs", padx=20, pady=10, command=graphData)
exitButton = Button(buttonFrame, text="Quit the Application", padx=30, pady=10, command=exitWindow)

Label(contentFrame, text="Start by navigating to one of our functions!", font=("Consolas", 20), fg='white', bg='orange').pack(padx=10)  # Welcome page
    # packing/grid area to display into the gui
homePage.grid(row=0, column=0)
barGraphButton.grid(row=0, column=1)
exitButton.grid(row=0, column=3)
buttonFrame.pack()
mainframe.pack(fill=BOTH, expand=1)
contentFrame.pack()

gui.mainloop()
# initialise starting GUI Window
