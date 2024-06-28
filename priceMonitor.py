import scraping
import EmailSender

def checkPriceAndNotify():
    scraper=scraping.ScrapTool()
    with open("~/Desktop/ProiectPractica/AplicatieScrapingInternet/priceLogger.txt", "r") as file:
        lines = file.readlines()
    
    for line in lines:
        parts = line.strip().split(', ')
        if len(parts) != 3:
            continue
            
        link, currentPrice, email = parts
        currentPrice=currentPrice.split(' ')[0]
        currentPrice=currentPrice.replace('.','')
        currentPrice=currentPrice.replace(',','.')
        currentPrice = float(currentPrice)

        if "altex" in link:
            newPriceStr = scraper.monitoringAltex(link)
        elif "emag" in link:
            newPriceStr = scraper.monitoringEmag(link)
        elif "cel" in link:
            newPriceStr = scraper.monitoringCel(link)
        else:
            continue

        newPriceStr=newPriceStr.split(' ')[0]
        newPriceStr=newPriceStr.replace('.','')
        newPriceStr=newPriceStr.replace(',','.')

        if newPriceStr:
            newPrice = float(newPriceStr)
            print("verifying link: "+link+" with price: " +str(currentPrice)+" email: "+email + " new price: " +str(newPrice))
            if newPrice < currentPrice:
                emailSender=EmailSender.EmailSender()
                emailSender.sendMail(email,"Price Alert!","The product on link: " + link + " dropped its price!")
                print("Price alert: price drop detected for link: " + link)
    
if __name__ == "__main__":
    checkPriceAndNotify()