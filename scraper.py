from tkinter import *
from tkinter import ttk
#import frame
#import appFunctions
#import tableFunctions
#import emailFunctions
#import searchFunctions
import http.server
from tkinter import filedialog, Tk, messagebox, Button, Label, PhotoImage, Listbox, StringVar, Toplevel
from tkinter import NW

import twint
from deep_translator import GoogleTranslator, single_detection
import pandas as pd
from tkinter import *
import os
from PIL import ImageTk, Image
import tkinter.messagebox
from tkinter import font


# imported modules used for GUI to function



def fileBrowser():
    """This function will only run after user presses browse-a-file button"""



    def hideFrames():
        """This function is used to clear all the contents in the frame after navigating to a new function"""
        contentFrame.pack_forget()  # forgets the frame storing content temporarily until it is being packed again.
        for widget in contentFrame.winfo_children():  # loops through all the widgets used in the content frame and destroy all of them
            widget.destroy()

        mainMenuFrame.pack_forget()  # forgets the mainMenuFrame which is different from the frame storing content.
        for widget in mainMenuFrame.winfo_children():
            widget.destroy()

        return

    MainPageLabel1.destroy()  # From this point on, the gui is remodelling itself by destroying past created labels and buttons
    MainPageLabel2.destroy()
    browseButton.destroy()

    # Window that updates after selecting CSV file
    gui.geometry("900x600+10+10")

    def graphdata():
        """Upon Navigating to the 'Generate Graph' Button, this function will run"""
        hideFrames()
        # To disable button from being able to be pressed again.
        buttonFrame.pack()
        mainframe.pack(fill=BOTH, expand=1)
        contentFrame.pack(fill=BOTH, expand=1)
        dataType = [  # dropdown list options
            "Top 10 words for each emotion",
            "Graph 2",
            "Graph 3",
            "Graph 4",
            "Graph 5",
            "Graph 6",

        ]

        clicked = StringVar()
        clicked.set(dataType[0])

        def displayGraphNameAccordingToDataType(event):
            """This function listens to the 'event' and displays the graph based on the datatype selected using the combobox"""
            if combi.get() == "Top 10 words for each emotion":
                appFunctions.ageBarGraph()

            elif combi.get() == "Graph 2":
                appFunctions.cfmCaseWeekBarChart()

            elif combi.get() == "Graph 3":
                appFunctions.natDaysLineGraph()

            elif combi.get() == "Graph 4":
                appFunctions.srcLineGraph()

            elif combi.get() == "Graph 5":
                appFunctions.facilitiesGeogMap()

            elif combi.get() == "Graph 6":
                appFunctions.facilitiesPieChart()

        combi = ttk.Combobox(contentFrame, value=dataType, font=("Microsoft Sans Serif",20), width=80)  # using tkinter's combobox as the drop down lsit
        combi.current(0)  # displays the default selected option
        combi.bind("<<ComboboxSelected>>", displayGraphNameAccordingToDataType)  # bind any event to a selection
        dropdownListLabel = Label(contentFrame, text="Choose the graph to be generated:", font=("Microsoft Sans Serif",24))

        # packing area (Used to pack any functions from tkinter into the screen)
        dropdownListLabel.pack(pady=50)
        combi.pack()

    def tableData():
        """This function runs when users navigate to the 'View Covid-19 data' Button"""
        hideFrames()

        def hideLocal():  # function to hide local button to prevent users from generating multiple tables
            #tableFunctions.lclicked()
            localbtn.destroy()
            importedbtn.destroy()
            infoTable.destroy()
            return

        def hideImported():  # function to hide imported button to prevent users from generating multiple tables
            #tableFunctions.impclicked()
            localbtn.destroy()
            importedbtn.destroy()
            infoTable.destroy()
            return

        tableFunctions.getFrame(contentFrame)  # passes information on the selected frame to display the table through parameters
        infoTable = Label(contentFrame, text="Click on one of the buttons below to view data of 'Local' or 'Imported' cases.", font=("Microsoft Sans Serif",20))
        localbtn = Button(contentFrame, text="Display Local Cases Table", font=(200), width=100, bg="white",
                             command=hideLocal)  # clicking one button to display local/imported data will hide buttons and display table, vice versa
        importedbtn = Button(contentFrame, text="Display Imported Cases Table", command=hideImported, font=("Microsoft Sans Serif",20), width=100, bg="white")

        # function packing area
        infoTable.pack(fill=BOTH, pady=50)
        localbtn.pack(pady=20)
        importedbtn.pack(pady=20)

        # default packing area
        buttonFrame.pack()  # Navigation bar buttons
        mainframe.pack(fill=BOTH, expand=1)  # frame to store contentFrame
        contentFrame.pack(fill=BOTH, expand=1)  # frame storing content

    def DataFour():
        def buttoncommand():
            searchTerm = entry1.get()
            numberOfTweets = entry2.get()

            if not numberOfTweets:
                tkinter.messagebox.showerror(title="Empty Field!", message="Please enter number of tweets.")
            if numberOfTweets and not numberOfTweets.isnumeric():
                tkinter.messagebox.showerror(title="Error!", message="Please enter an integer.")

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
            data.to_csv("DataSet.csv", index=False)  # Data Scraped for twint is written to a CSV.

            df = pd.read_csv("DataSet.csv")
            df.drop(df[df['language'] == 'und'].index,
                    inplace=True)  # No language detection when tweets contain only URL. Such tweets is labeled as "und" by twint.
            df.to_csv("DataSet.csv", index=False)  # Write/update changes to CSV file

            num = len(df['tweet'])
            count = 1

            for i in range(0, num, 1):
                lang = single_detection(df['tweet'][i], api_key='882c59b16ed56b80efb9405b96bc6926')
                if lang != 'en':
                    df._set_value(i, 'tweet', GoogleTranslator(source='auto', target='en').translate(df['tweet'][i]))
                    df.to_csv("DataSet.csv", index=False)
                    count += 1
                    print("Row Number:" + str(count) + " (Translated Tweet)")
                else:
                    count += 1
                    print("Row Number:" + str(count) + " (English Tweet)")

            print("Refer to DataSet.csv for result")
            os.system('K:/Programs/Python/python.exe textprocessing.py')
            os.system('K:/Programs/Python/python.exe wordcloudgenerator.py')
            os.system('K:/Programs/Python/python.exe topicmodelling.py')
            os.system('K:/Programs/Python/python.exe emotionanalysis.py')
            label1.destroy()
            entry1.destroy()
            label2.destroy()
            entry2.destroy()
            button1.destroy()

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
            scale = Scale(master=gui, orient=HORIZONTAL, from_=1, to=len(listimg), resolution=1, showvalue=False,
                          command=nex_img)
            scale.pack(side=BOTTOM, fill=X)
            canvas = Canvas(gui, width=1920, height=1080)
            canvas.pack()

            # show first image
            nex_img(1)
            return None

        hideFrames()
        title = Label(contentFrame, text="1002 Project", fg="blue", font="lucida 25 bold")
        title.pack()
        label1 = Label(contentFrame, text='Please enter search term:')
        label1.pack()
        entry1 = Entry(contentFrame, width=20)
        entry1.pack()
        label2 = Label(contentFrame, text='Please enter number of tweets to be searched:')
        label2.pack()
        entry2 = Entry(contentFrame, width=20)
        entry2.pack()
        button1 = Button(contentFrame, text="Search", command=buttoncommand)
        button1.pack()
        bottom_frame = Frame(gui)
        bottom_frame.pack()

        # default packing area
        buttonFrame.pack()
        mainframe.pack(fill=BOTH, expand=1)
        contentFrame.pack(fill=BOTH, expand=1)



    def searchData():
        """This function is used to search for column-specific data"""
        hideFrames()  # to reset frame
        topFrame = Frame(contentFrame, height=100, width=100,
                         relief=SUNKEN)  # top frame used to seperate between frame that is used to search and frame that displays data
        Label(topFrame,
              text="Search and display specific data by selecting the columns and conditions below: ", font=("Microsoft Sans Serif",20)).grid(row=0, pady=10)

        colChoice = [  # Drop down options
            "ID",
            "Gender",
            "Age",
            "Nationality",
        ]

        clicked = StringVar()  # used to store the value of the dropdown list
        clicked.set(colChoice[0])  # current default value
        columnChoose = OptionMenu(topFrame, clicked, *colChoice)  # specifies the dropdown list options
        Label(topFrame, text="Column (example: ID): ", font=("Microsoft Sans Serif",10)).grid()
        columnChoose.grid()  # places the dropdown list in the gui using grid method
        Label(topFrame, text="Value (example: case-1): ", font=("Microsoft Sans Serif",10)).grid()

        v = StringVar()  # initialise variable to store user input
        Entry(topFrame, textvariable=v).grid(padx=10)  # user input box

        def searchColumns():
            userInput = v.get()  # gets the user input
            columnInput = clicked.get()  # gets the dropdown list option selected
            searchFunctions.showSearchData(columnInput, userInput)  # execute search/sort by using the user inputs
            return

        searchButton = Button(topFrame, text="Search",
                              command=searchColumns)  # executes the serach columns function
        searchButton.grid()  # places the search button on the gui

        class ScrollableFrame(Frame):  # This class generates the frame that is used to store the data being displayed
            def __init__(self, container, *args, **kwargs):
                super().__init__(container, *args, **kwargs)
                canvas = Canvas(self)
                scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
                self.scrollable_frame = ttk.Frame(canvas)

                self.scrollable_frame.bind( "<Configure>",  lambda e: canvas.configure(scrollregion=canvas.bbox("all")) )

                canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

                canvas.configure(yscrollcommand=scrollbar.set)

                canvas.pack(side="left", expand=True)
                scrollbar.pack(side="right", fill="y")

        scrollFrame = ScrollableFrame(contentFrame)  # places the displaying data frame into the content holding frame
        searchFunctions.getFrameFromGui(scrollFrame.scrollable_frame)  # sends information to the function on where to place the data

        # function packing area
        topFrame.pack()  # display/packs the top frame on screen
        scrollFrame.pack(fill=BOTH, expand=1)

        # default packing area
        buttonFrame.pack()
        mainframe.pack(fill=BOTH, expand=1)
        contentFrame.pack(fill=BOTH, expand=1)

        return

    def sendEmail():
        """This function is used to export and send the data through E-mail in the GUI"""
        hideFrames()  # resets the frame

        treeFrame = LabelFrame(contentFrame, text="Data")  # create a frame to store displayed data
        treeview1 = ttk.Treeview(treeFrame)  # uses the treeview widget
        treeview1.place(relheight=1, relwidth=1)
        treeScrolly = Scrollbar(treeFrame, orient="vertical",
                                command=treeview1.yview)  # command means update the yaxis view of the widget
        treeScrollx = Scrollbar(treeFrame, orient="horizontal",
                                command=treeview1.xview)  # command means update the xaxis view of the widget
        treeview1.configure(xscrollcommand=treeScrollx.set,
                            yscrollcommand=treeScrolly.set)  # assign the scrollbars to the Treeview Widget

        emailMainLabel = Label(contentFrame, text="Sort Table based on: ")

        sortType = [  # dropdown/sorting list options
            "Ascending", "Descending",]



        def sortData(event):
            """Sorts the data and sends it to the emailFunctions file"""
            emailFunctions.clear_data(treeview1)  # Clear any data available
            if sortedData.get() == "Ascending":
                emailFunctions.readData(treeview1, column.get(), True)
            elif sortedData.get() == "Descending":
                emailFunctions.readData(treeview1, column.get(), False)

        sortedData = ttk.Combobox(contentFrame, value=sortType)  # combobox listens to the option being selected and executes the command
        sortedData.current(0)  # set default drop down box value
        sortedData.bind("<<ComboboxSelected>>", sortData)  # bind the combobox with the options

        columnType = [  # radio button selections
            ("ID", "ID"),
            ("Gender", "Gender"),
            ("Age", "Age"),
            ("Nationality", "Nationality"),]

        column = StringVar()  # string var to store the option that will be selected
        column.set("ID")  # set default selected value to ID
        radioButtonFrame = Frame(contentFrame, height=30, width=100)  # generates a frame to store the radio buttons

        i = 0  # counter for column placement
        for text, mode in columnType:  # for every option there is for columns, generate a radio button
            i += 1
            Radiobutton(radioButtonFrame, text=text, variable=column, value=mode).grid(row=0, column=i)  # radio button generated and placed according to their position (i)

        def sendEmailTo():  # send email function
            """Sends the recipient info and the sorted data table settings to the emailFunction file to be sent"""
            a = recipient.get()  # get the user input
            if sortedData.get() == "Ascending":  # sorts according to drop down list option
                emailFunctions.export(a, column.get(), True)
            elif sortedData.get() == "Descending":
                emailFunctions.export(a, column.get(), False)

        def exportOnly():  # export function
            """Sends the sorted data table settings to the emailFunction file to be exported"""
            if sortedData.get() == "Ascending":  # sorts according to drop down list option
                emailFunctions.exportOnly(column.get(), True)
            elif sortedData.get() == "Descending":
                emailFunctions.exportOnly(column.get(), False)

        emailTo = Label(contentFrame, text="Input recipient's e-mail address: ")
        recipient = Entry(contentFrame)  # user input for recipient
        sendButton = Button(contentFrame, text='Export and Send file as E-mail (Following format chosen above)',
                            command=sendEmailTo)
        exportButton = Button(contentFrame, text='Export the file ONLY (Following format chosen above)', command=exportOnly)

        # function packing area
        radioButtonFrame.pack()
        emailMainLabel.pack()
        sortedData.pack()
        emailTo.pack()
        recipient.pack()
        exportButton.pack(pady=5)
        sendButton.pack(pady=5)
        treeFrame.pack(fill=BOTH, expand=1)
        treeScrollx.pack(side="bottom", fill="x")  # make the scrollbar fill the x axis of the Treeview widget
        treeScrolly.pack(side="right", fill="y")  # make the scrollbar fill the y axis of the Treeview widget

        # default packing area
        buttonFrame.pack()
        mainframe.pack(fill=BOTH, expand=1)
        contentFrame.pack(fill=BOTH, expand=1)

    def exitWindow():
        """This function forces the app to exit/quit"""
        gui.quit()

    def startFromMenu():
        """This function re-does the gui navigation bar and frames after navigating from the menu page"""
        mainMenuFrame.pack_forget()  # removes any frame used for the main menu page
        graphdata()  # brings user to the graph data page

        # creating of navigation bars
        homePageMenu = Button(buttonFrame, text="Main Menu", command=mainMenu, padx=20, pady=10)
        barGraphButtonMenu = Button(buttonFrame, text="Generate Graph", padx=20, pady=10, command=graphdata)
        displayDataTableMenu = Button(buttonFrame, text="Read Covid-19 Data", padx=30, pady=10, command=tableData)
        sendEmailButtonMenu = Button(buttonFrame, text="Sort, export and send data as e-mail", padx=30, pady=10,
                                     command=DataFour)
        listDataButtonMenu = Button(buttonFrame, text="List Data", padx=30, pady=10, command=searchData)
        exitButtonMenu = Button(buttonFrame, text="QUIT the Application", padx=30, pady=10, command=exitWindow)

        # default pack/grid area to place the buttons back
        homePageMenu.grid(row=0, column=0)
        barGraphButtonMenu.grid(row=0, column=1)
        #displayDataTableMenu.grid(row=0, column=2)
        #listDataButtonMenu.grid(row=0, column=3)
        sendEmailButtonMenu.grid(row=0, column=4)
        exitButtonMenu.grid(row=0, column=5)

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
        reUpload = Button(mainMenuFrame, text="Upload A New Dataset", font=("Microsoft Yahei UI", 15), padx=24, pady=10,
                          command=abc)  # create reupload button
        exitFromMenu = Button(mainMenuFrame, text="QUIT", padx=30, font=("Microsoft Yahei UI", 15), pady=10,
                              command=exitWindow)  # create exit button

        # button packing area
        startUse.pack()
        reUpload.pack()
        exitFromMenu.pack(expand=1)

        return

    # default Frames Creation
    mainMenuFrame = Frame(gui, relief=SUNKEN, height=800, width=1000, background='Orange')
    buttonFrame = Frame(gui, height=100, width=1000, borderwidth=10, relief=GROOVE, background='Orange')
    mainframe = Frame(gui, height=550, width=1000, borderwidth=10, relief=SUNKEN, background='Orange')
    contentFrame = Frame(mainframe, height=600, width=1000, borderwidth=10)

    # Main Buttons creation section
    homePage = Button(buttonFrame, text="Main Menu", command=mainMenu, padx=20, pady=10)
    barGraphButton = Button(buttonFrame, text="Generate Graph", padx=20, pady=10, command=graphdata)
    # displayDataTable = Button(buttonFrame, text="Read Covid-19 Data", padx=30, pady=10, command=tableData)
    sendEmailButton = Button(buttonFrame, text="Sort, export and send data as e-mail", padx=30, pady=10,
                             command=DataFour)
    # listDataButton = Button(buttonFrame, text="List Data", padx=30, pady=10, command=searchData)
    exitButton = Button(buttonFrame, text="QUIT the Application", padx=30, pady=10, command=exitWindow)

    # packing/grid area to display into the gui
    homePage.grid(row=0, column=0)
    barGraphButton.grid(row=0, column=1)
    #displayDataTable.grid(row=0, column=2)
    #listDataButton.grid(row=0, column=3)
    sendEmailButton.grid(row=0, column=4)
    exitButton.grid(row=0, column=5)
    buttonFrame.pack()
    mainframe.pack(fill=BOTH, expand=1)
    contentFrame.pack()
    Label(contentFrame, text="Start by navigating to one of our functions", font=("Consolas", 20), fg='white', bg='orange').pack(padx=50)  # Welcome page

    def abc():
        try:
            # stores the file path of the user selected data-set to be used with our other functions
            tempdir = filedialog.askopenfilename(initialdir="",  title="Select Dataset File", filetypes=((".csv Files", "*.csv"), ("All Files", "*.*")))
            # sending file path to var so other functions can use the file path
            # parse file path
            if tempdir == '':
                messagebox.showerror("Error", "Choose a file!")
            elif tempdir[-3:].lower() not in ['csv', 'prn', 'xls', 'ods'] and tempdir[-4:].lower() not in ['xlsx', 'xltx', 'xlsm',  'xlsb']:
                messagebox.showerror("Error", "Choose a CSV file!")  # Error messagebox
            else:
                """frame.convertToDF(tempdir)"""
                startFromMenu()
        except:
            messagebox.showerror("Warning", "Error!")


# initialise starting GUI Window
gui = Tk()
gui.iconbitmap('icons/SIT_logo_2.ico')
gui.title("Covid-19 Data Crawler")
gui.geometry("300x200")
gui.attributes('-topmost', True)


def jkl():
    try:
        # stores the file path of the user selected data-set to be used with our other functions
        tempdir = filedialog.askopenfilename(initialdir="",
                                             title="Select Dataset File",
                                             filetypes=((".csv Files", "*.csv"), ("All Files", "*.*")))
        # sending file path to var so other functions can use the file path
        # parse file path
        if tempdir == '':
            messagebox.showerror("Error", "Choose a file!")
        elif tempdir[-3:].lower() not in ['csv', 'prn', 'xls', 'ods'] and tempdir[-4:].lower() not in ['xlsx', 'xltx',
                                                                                                     'xlsm',
                                                                                                     'xlsb']:
            messagebox.showerror("Warning", "Choose a CSV file!")  # Error messagebox
        else:
            """frame.convertToDF(tempdir)"""
            fileBrowser()
    except:
        messagebox.showerror("Warning", "Error!")

try:
    # Create Label to instruct users to browse for data
    MainPageLabel1 = Label(gui, text="Welcome!")
    MainPageLabel2 = Label(gui, text="Click on the button above to browse for a Dataset!")
    # Button to browse for Dataset
    browseButton = Button(gui, text="Browse", padx=20, pady=8, bg="light blue", command=jkl)

    # PACK SECTION
    MainPageLabel1.pack(ipadx=20, ipady=20)
    browseButton.pack()
    MainPageLabel2.pack(ipadx=20, ipady=20)

    gui.mainloop()
except:
    messagebox.showinfo("Exception occurred!")

