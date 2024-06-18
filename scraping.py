from bs4 import BeautifulSoup
import requests
import csv

def iterateThroughPage(pageLink):
    pageToScrape=requests.get(pageLink) #Obtinem continutul paginii
    soup=BeautifulSoup(pageToScrape.text,"html.parser")
    quotes=soup.findAll("span",attrs={"class":"text"})
    for quote in quotes:
        print("Quote: " +quote.text + " from page: " + pageLink)
    return

mainPageLink="https://quotes.toscrape.com"

pageToScrape=requests.get(mainPageLink) #Obtinem continutul paginii
soup=BeautifulSoup(pageToScrape.text,"html.parser")
links=soup.findAll('a')
#print(links)
for link in links:
    link=link.get('href')
    print ("Secondary page: " + link)
    if link[0]=='/':
        secondaryPageLink=mainPageLink+link
        iterateThroughPage(secondaryPageLink)
    else:
        iterateThroughPage(link)

    