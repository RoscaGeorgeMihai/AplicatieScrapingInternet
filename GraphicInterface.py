import tkinter 
from tkinter import ttk
from tkinter.simpledialog import askstring
from PIL import Image, ImageTk

class GUI(tkinter.Tk):
    def showImage(self):
        image = Image.open("./mainImage.jpg")
        image = image.resize((400,300),Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        imageLabel=tkinter.Label(self,image=photo)
        imageLabel.image=photo
        imageLabel.grid(row=0,column=0,padx=200,pady=75)

    def showProductNameInsert(self):
        customFont=("Arial",25)
        textLabel=tkinter.Label(self,text="Insert product name: ",font=customFont)
        textLabel.grid(row=1,column=0,padx=200,pady=0)
        self.entry=tkinter.Entry(self,width=40)
        self.entry.grid(row=2,column=0,padx=200,pady=10)

    def buttonClicked(self):
        self.productName=self.entry.get()
        print(self.productName)

    def showButton(self,posRow):
        self.searchButton=tkinter.Button(self,text="Search",command=self.buttonClicked)
        self.searchButton.grid(row=posRow,column=0,padx=200,pady=10)
    
    def optionSelected(self,event):
        self.selectedOption=self.optionBox.get()
        if self.searchButton != None:
            self.searchButton.grid_forget()
        if self.selectedOption == "Price monitoring": 
            self.showSiteOptionsBox()
            self.showButton(8)
        if self.selectedOption == "Price comparison":
            if self.siteBox != None:
                self.siteBox.grid_forget()
                self.siteBoxLabel.grid_forget()
            self.showButton(6)
        print(self.selectedOption)

    def showOptionBox(self):
        self.comboBoxLabel=tkinter.Label(self,text="Select option: ")
        self.comboBoxLabel.grid(row=4,column=0,padx=200,pady=5)
        self.optionBox=ttk.Combobox(self,values=["Price monitoring","Price comparison"])
        self.optionBox.grid(row=5,column=0,padx=200,pady=0)
        self.optionBox.bind("<<ComboboxSelected>>",self.optionSelected)

    def siteSelected(self,event):
        self.selectedOption=self.optionBox.get()
        print(self.selectedOption)

    def showSiteOptionsBox(self):
        self.siteBoxLabel=tkinter.Label(self,text="Select the website to monitor: ")
        self.siteBoxLabel.grid(row=6,column=0,padx=200,pady=5)
        self.siteBox=ttk.Combobox(self,values=["Emag","Altex","Zalando"])
        self.siteBox.grid(row=7,column=0,padx=200,pady=0)
        self.siteBox.bind("<<ComboboxSelected>>",self.siteSelected)

    def __init__(self):
        super().__init__()
        self.geometry("800x800")
        self.resizable(False,False)
        self.title("Scraping app")
        self.config(bg = "gray")
        self.selectedOption = None
        self.siteBox = None
        self.searchButton = None
        self.showImage()
        self.showProductNameInsert()
        self.showOptionBox()
        return 