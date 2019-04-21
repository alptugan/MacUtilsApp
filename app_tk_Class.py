from tkinter import *
import os
import sys


class Root(Tk):
    def __init__(self):
        super(Root, self).__init__()
        self.lift()

        # variables
        self.var1     = IntVar()
        self.varFiles = IntVar()
        self.varChage = IntVar()
        
        self.toggle  = Checkbutton()
        self.toggle2 = Checkbutton()
        self.toggle3 = Checkbutton()

        self.title("Mac OS X Utilities")
        self.minsize(275,170)
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
        self.bind('<Escape>', lambda e: self.save_state)
        # sys.exit()

        # create a menu bar with an Exit command
        menubar = Menu(self)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Exit", command=self.save_state)
        menubar.add_cascade(label="File", menu=filemenu)
        self.config(menu=menubar)
        
        # root is your root window
        self.protocol('WM_DELETE_WINDOW', self.save_state)  
        
        # load previous state
        self.load_state()
        #print(str(self.var1.get()) + ',' + str(self.varFiles.get()))

        script = 'tell application "System Events" to set frontmost of the first process whose unix id is {pid} to true'.format(pid=os.getpid())
        os.system("/usr/bin/osascript -e '{script}'".format(script=script))

    def save_state(self):
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
