import tkinter
from tkinter import ttk
from PIL import Image, ImageTk
import webbrowser
import scraping

class GUI(tkinter.Tk):
    def showImage(self):
        image = Image.open("./mainImage.jpg")
        image = image.resize((400, 300), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        imageLabel = tkinter.Label(self, image=photo)
        imageLabel.image = photo
        imageLabel.grid(row=0, column=0, padx=200, pady=20)

    def showProductNameInsert(self):
        customFont = ("Arial", 25)
        self.productNameLabel = tkinter.Label(self, text="Insert product name: ", font=customFont)
        self.productNameLabel.grid(row=3, column=0, padx=200, pady=0)
        self.productNameEntry = tkinter.Entry(self, width=40)
        self.productNameEntry.grid(row=4, column=0, padx=200, pady=10)

    def showProductLinkInsert(self):
        customFont = ("Arial", 25)
        self.productLinkLabel = tkinter.Label(self, text="Insert product link: ", font=customFont)
        self.productLinkLabel.grid(row=3, column=0, padx=200, pady=0)
        self.productLinkEntry = tkinter.Entry(self, width=40)
        self.productLinkEntry.grid(row=4, column=0, padx=200, pady=10)

    def showEmailInsert(self):
        customFont = ("Arial", 15)
        self.emailLabel = tkinter.Label(self, text="Insert user email: ", font=customFont)
        self.emailLabel.grid(row=5, column=0, padx=200, pady=0)
        self.emailEntry = tkinter.Entry(self, width=40)
        self.emailEntry.grid(row=6, column=0, padx=200, pady=10)

    def buttonClicked(self):
        scrapTool = scraping.ScrapTool()
        if self.selectedOption == "Price comparison":
            self.productName = self.productNameEntry.get()
            results = scrapTool.priceComparison(self.productName)
            self.comboBoxLabel.grid_forget()
            self.optionBox.grid_forget()
            self.productNameEntry.grid_forget()
            self.productNameLabel.grid_forget()
            self.searchButton.grid_forget()
            self.showResultsTable(results)
        elif self.selectedOption == "Price monitoring":
            self.productLink = self.productLinkEntry.get()
            self.userEmail = self.emailEntry.get()
            scrapTool.priceMonitoring(self.productLink,self.userEmail)

    def showButton(self, posRow):
        self.searchButton = tkinter.Button(self, text="Search", command=self.buttonClicked)
        self.searchButton.grid(row=posRow, column=0, padx=200, pady=10)

    def showBackButton(self,posRow):
        self.backButton = tkinter.Button(self, text="Back", command=self.backButtonClicked)
        self.backButton.grid(row=posRow, column=0, padx=200, pady=10)

    def backButtonClicked(self):
        self.tree.grid_forget()
        self.backButton.grid_forget()
        self.showOptionBox()

    def optionSelected(self, event):
        self.selectedOption = self.optionBox.get()
        if self.selectedOption == "Price monitoring":
            if self.productNameLabel:
                self.productNameEntry.grid_forget()
                self.productNameLabel.grid_forget()
                self.searchButton.grid_forget()
            self.showProductLinkInsert()
            self.showEmailInsert()
            self.showButton(7)
        if self.selectedOption == "Price comparison":
            if self.productLinkLabel:
                self.productLinkEntry.grid_forget()
                self.productLinkLabel.grid_forget()
            if self.emailLabel:
                self.emailLabel.grid_forget()
                self.emailEntry.grid_forget()
                self.searchButton.grid_forget()  
            self.showProductNameInsert()
            self.showButton(6)
        print(self.selectedOption)

    def showOptionBox(self):
        self.comboBoxLabel = tkinter.Label(self, text="Select option: ")
        self.comboBoxLabel.grid(row=1, column=0, padx=200, pady=5)
        self.optionBox = ttk.Combobox(self, values=["Price monitoring", "Price comparison"])
        self.optionBox.grid(row=2, column=0, padx=200, pady=5)
        self.optionBox.bind("<<ComboboxSelected>>", self.optionSelected)

    def siteSelected(self, event):
        self.selectedOption = self.optionBox.get()
        print(self.selectedOption)

    def showResultsTable(self, results):
        self.tree = ttk.Treeview(self, columns=("Link", "Price"), show='headings')
        self.tree.heading("Link", text="Product Link")
        self.tree.heading("Price", text="Price")
        for result in results:
            self.tree.insert("", "end", values=(result[0], result[1]))
        self.tree.bind("<Double-1>", self.onItemClick)
        self.tree.grid(row=5, column=0, padx=200, pady=10)
        self.results = results
        self.searchButton.grid_forget()
        self.showBackButton(6)

    def onItemClick(self, event):
        item = self.tree.selection()[0]
        productLink = self.tree.item(item, "values")[0]
        
        for result in self.results:
            if result[0] == productLink:
                webbrowser.open(result[0])
                break

    def __init__(self):
        super().__init__()
        self.geometry("800x800")
        self.resizable(False, False)
        self.title("Scraping app")
        self.config(bg="gray")
        self.selectedOption = None
        self.searchButton = None
        self.backButton = None
        self.productNameEntry = None
        self.productNameLabel = None
        self.productLinkEntry = None
        self.productLinkLabel = None
        self.emailLabel = None
        self.emailEntry = None
        self.showImage()
        self.showOptionBox()