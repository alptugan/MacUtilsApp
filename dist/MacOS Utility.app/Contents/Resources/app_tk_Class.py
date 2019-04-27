from tkinter import *
import os
import sys
from os import system
from platform import system as platform


class Root(Tk):
    def __init__(self):
        super(Root, self).__init__()


    
        # variables
        self.var1     = IntVar()
        self.varFiles = IntVar()
        self.varChage = IntVar()
        
        self.toggle  = Checkbutton()
        self.toggle2 = Checkbutton()
        self.toggle3 = Checkbutton()

        self.title("Mac OS X Utilities")
        self.geometry('275x150')
        #self.minsize(275,170)
        self.resizable(width=False, height=False)
        #self.maxsize(475,170)
        #self.configure(background = '#ffffff')

        # generate label
        self.createWidget()

        # generate hide/desktop icons
        self.createToggle()
    
        # generate show/hide invisible files
        self.createInvisibleFileSwitcher()

        # generate power plug sound
        self.createPowerPlugSound()

        # make Esc exit the program
        self.bind('<Escape>', self.save_state)
        self.createcommand('exit', self.save_and_exit)
        # sys.exit()

        # create a menu bar with an Exit command
        menubar = Menu(self)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Exit", command=self.save_state)
        filemenu.add_command(label="About")
        menubar.add_cascade(label="File", menu=filemenu)
        self.config(menu=menubar)
        
        # root is your root window
        self.protocol('WM_DELETE_WINDOW',self.save_state)  
        
        # load previous state
        self.load_state()

        #print(str(self.var1.get()) + ',' + str(self.varFiles.get()))

        #self.attributes("-topmost", True) # this also works
        #self.lift()
        #self.focus()
        
        # Set window position
        self.setWindowsPosition()

        # put foremost
        if platform() == 'Darwin':  # How Mac OS X is identified by Python
            system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')
        
        # focus
        self.focus_force()
    
    def save_and_exit(self):
        self.save_state()
        sys.exit()

    def setWindowsPosition(self):
        # Gets the requested values of the height and widht.
        windowWidth = self.winfo_reqwidth()
        windowHeight = self.winfo_reqheight()
        

        # Gets both half the screen width/height and window width/height
        positionRight = int(self.winfo_screenwidth()*0.5 - windowWidth*0.5)
        positionDown = int(self.winfo_screenheight()*0.5 - windowHeight*0.5)

        # Positions the window in the center of the page.
        self.geometry("+{}+{}".format(positionRight, positionDown))

    def save_state(self, *event):
        file = open('profiles.txt', 'w')
        file.write(str(self.var1.get()) + ',' 
        + str(self.varFiles.get()) + ',' 
        + str(self.varChage.get())
        )
        file.close()
        self.destroy()

    def load_state(self):
        file = open('profiles.txt', 'r')
        lines = file.readlines()
        for line in lines:
            info = line.split(',')
        self.toggle.setvar(str(self.var1),int(info[0]))
        self.toggle2.setvar(str(self.varFiles),int(info[1]))
        self.toggle3.setvar(str(self.varChage),int(info[2]))

        file.close()

    def createWidget(self):
        fLabel = LabelFrame(self, text="Finder Features")

        label = Label(fLabel, text="Set of utilities to change system properties")
        label.config(font=("System", 12))
        fLabel.grid(column = 0, row = 0, pady=4, padx=4)
        label.pack()
        #label.place(x = 10, y = 20)

    ########################################################################################
    # Hide Desktop Icons
    ########################################################################################
    def createToggle(self):
        self.toggle = Checkbutton(self, text="Hide Desktop Icons", variable=self.var1, command=self.hideDesktopIcons)
        self.toggle.grid(row=1, sticky=W, padx = 4)

    def hideDesktopIcons(self):
        result = self.var1.get()
        if result == 1:
            os.system("defaults write com.apple.finder CreateDesktop false & killall Finder")
        else:
            os.system("defaults write com.apple.finder CreateDesktop true & killall Finder")

    ########################################################################################
    # SHOW INVISIBLE FILES & FOLDER
    ########################################################################################
    def createInvisibleFileSwitcher(self):
        self.toggle2 = Checkbutton(self, text="Show Invisible Files & Folders", variable=self.varFiles, command=self.showInvisibleFiles)
        self.toggle2.grid(row=2, sticky=W, padx = 4)

    def showInvisibleFiles(self):
        result = self.varFiles.get()
        if result == 1:
            os.system("defaults write com.apple.finder AppleShowAllFiles -bool TRUE & killall Finder")
        else:
            os.system("defaults write com.apple.finder AppleShowAllFiles -bool FALSE & killall Finder")

    ########################################################################################
    # Enable an iOS-like power chime when connected to power
    ########################################################################################
    def createPowerPlugSound(self):
        self.toggle3 = Checkbutton(self, text="Enable an iOS-like power chime when connected to power", variable=self.varChage, command=self.enablePowerPlugSound)
        self.toggle3.config(wrap=self.winfo_reqwidth() + 80, justify=LEFT)
        #self.toggle3.pack(anchor = "w")
        #self.toggle3.config(text = "anchor = 'w'")
        self.toggle3.grid(row=3, padx = 4, sticky=W)

    def enablePowerPlugSound(self):
        result = self.varChage.get()
        if result == 1:
            os.system("defaults write com.apple.PowerChime ChimeOnAllHardware -bool true; open /System/Library/CoreServices/PowerChime.app")
        else:
            os.system("defaults write com.apple.PowerChime ChimeOnAllHardware -bool FALSE; killall PowerChime")

root = Root()
root.mainloop()
