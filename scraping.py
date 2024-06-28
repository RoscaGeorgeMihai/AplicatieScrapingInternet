from bs4 import BeautifulSoup
import requests
import csv

class ScrapTool():
    def __init__(self):
        self.altexWebsite = "https://altex.ro/"
        self.emagWebsite = "https://www.emag.ro/"
        self.zalandoWebsite = "https://www.zalando.ro/"
        self.pcgarageWebsite = "https://www.pcgarage.ro/"
        self.celWebsite = "https://www.cel.ro/"

    def scrapAltex(self,productName):
        #scraping altex
        #Vom culege informatiile direct din json-ul menit sa populeze pagina html cu produse
        print("CAUTARE ALTEX")
        s = requests.Session() 
        xhrBaseUrl = 'https://fenrir.altex.ro/v2/catalog/search/'
        xhrUrl = f"{xhrBaseUrl}{productName.replace(' ', '%20')}?size=48"

        #Headerele necesare requestului
        xhrHeaders = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,/;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Host": "fenrir.altex.ro",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0"
        }

        res = s.get(xhrUrl, headers=xhrHeaders)
        res.raise_for_status()
        data = res.json()
        productNames = None
        productPrices = None
        urlKeys = None
        skus = None

        if data:
            productPrices = [p['price'] for p in data['products']]
            urlKeys = [p['url_key'] for p in data['products']]
            skus = [p['sku'] for p in data['products']]
        else:
            print("Produsul nu a fost gasit pe Altex!")
            return None,None

        productUrl = "https://altex.ro/" + urlKeys[0] + "/cpd/"
        productUrl = productUrl + skus[0]
        print("link: " + productUrl)
        print("Price: " + str(productPrices[0]) + " Lei")
        return productUrl, productPrices[0]

    def scrapEmag(self,productName):
        #scraping emag
        print("CAUTARE EMAG")
        websiteToScrap = self.emagWebsite + "search/" + productName
        emagScrape = requests.get(websiteToScrap)
        websiteSoup = BeautifulSoup(emagScrape.content,"html.parser")
        
        links=websiteSoup.findAll('a',attrs={"data-zone":"thumbnail"})
        link=None
        if links:
            link=links[0].get('href')
            print("link: " +link)
        else:
            print("Produsul nu a fost gasit pe Emag!")
            return None, None
        
        productPrices=websiteSoup.findAll('p',attrs={"class":"product-new-price"})
        productPrice=productPrices[0].text
        print("Price: " + productPrice)
        return link, productPrice

    def scrapCel(self,productName):
        #scraping cel
        print("CAUTARE CEL")
        websiteToScrap = f"{self.celWebsite}cauta/{productName.replace(' ', '+')}"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": "https://www.cel.ro/",
            "Connection": "keep-alive",
            "Cookie": "cel_id=smlfq7r4tu5fbmtjvjoq2gn275; ct=Z3MxNGEpZXVkdjc9NCYzdGcjMTUyLTV3MCVhZjMmZCg%3D; cel_cust=YCgxPn5tPCAwKCFncG1yfmx3cVtseiQqTylwPjQqPDNiZ3BwanNjY153bmVsciQqcigxMz88MSM2JTs1Nn1kJ2B0ZzVjemR0ZXFDR0BSKGNuMDh5; alternativega=false; _ga_PH04D6N29P=GS1.1.1719470980.1.0.1719470980.60.0.0; _ga=GA1.1.332367684.1719470981; _tt_enable_cookie=1; _ttp=DJnVal7qxyHXluSc49abHd9tYbs; gdpr_accept=true; searched=1719470990",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "TE": "trailers"
        }
        
        celScrape = requests.get(websiteToScrap,headers=headers)
        websiteSoup = BeautifulSoup(celScrape.content,"html.parser")
        firstATag = websiteSoup.find('div', class_='productListing-poza').find('a')
        if firstATag:
            link = firstATag.get('href')
            print(link)
        else:
            print("Produsul nu a fost gasit pe Cel!")
            return
        price=websiteSoup.find('span',attrs={'class':'price','data-productprice':'1'})
        print(price.text)
        return link, price.text
        
    def priceComparison(self,productName):
        results = []
        altexLink, altexPrice = self.scrapAltex(productName)
        if altexLink and altexPrice:
            results.append((altexLink, altexPrice))
        emagLink, emagPrice = self.scrapEmag(productName)
        if emagLink and emagPrice:
            results.append((emagLink, emagPrice))
        celLink, celPrice = self.scrapCel(productName)
        if celLink and celPrice:
            results.append((celLink, celPrice))
        return results


    def monitoringEmag(self,productLink):
        emagScrape = requests.get(productLink)
        websiteSoup = BeautifulSoup(emagScrape.content,"html.parser")        
        productPrice=websiteSoup.find('p',class_='product-new-price')
        return productPrice.text

    def monitoringAltex(self,productLink):
        headers = {
            "Host": "altex.ro",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "TE": "trailers"
        }
        altexScrape = requests.get(productLink,headers=headers)
        websiteSoup = BeautifulSoup(altexScrape.content,"html.parser")
        productPrice=websiteSoup.findAll('span',attrs={'class':'Price-int leading-none'})
        return productPrice[1].text

    def monitoringCel(self,productLink):
        headers = {
            "Host": "www.cel.ro",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": "https://www.cel.ro/cauta/iphone+15/",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "TE": "trailers"
        }

        celScrape = requests.get(productLink,headers=headers)
        websiteSoup = BeautifulSoup(celScrape.content,"html.parser")
        productPrice=websiteSoup.findAll('span',attrs={'id':'product-price'})
        return productPrice[0].text       


    def priceMonitoring(self,productLink,email):
        if "emag" in productLink:
            price = self.monitoringEmag(productLink)
            if price:
                with open("priceLogger.txt", "a") as file:
                    file.write(f"{productLink}, {price}, {email}\n")
        if "altex" in productLink:
            price = self.monitoringAltex(productLink)
            if price:
                with open("priceLogger.txt", "a") as file:
                    file.write(f"{productLink}, {price}, {email}\n")
        if "cel" in productLink:
            price = self.monitoringCel(productLink)
            if price:
                with open("priceLogger.txt", "a") as file:
                    file.write(f"{productLink}, {price}, {email}\n")
        print(email)