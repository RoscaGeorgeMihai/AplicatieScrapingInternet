from bs4 import BeautifulSoup
import requests
import csv

class ScrapTool():
    def __init__(self):
        self.altexWebsite = "https://altex.ro/"
        self.emagWebsite = "https://www.emag.ro/"
        self.zalandoWebsite = "https://www.zalando.ro/"
        self.pcgarageWebsite = "https://www.pcgarage.ro/"

    def priceComparison(self,productName):
        #scraping emag
        print("CAUTARE EMAG")
        websiteToScrap = self.emagWebsite + "search/" + productName
        emagScrape = requests.get(websiteToScrap)
        websiteSoup = BeautifulSoup(emagScrape.content,"html.parser")
        links=websiteSoup.findAll('a',attrs={"data-zone":"thumbnail"})
        link=links[0].get('href')
        productPrices=websiteSoup.findAll('p',attrs={"class":"product-new-price"})
        productPrice=productPrices[0].text
        print("link: " +link)
        print("price: " + productPrice)

        #scraping altex
        #Vom culege informatiile direct din json-ul menit sa populeze pagina html cu produse
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
            productNames = [p['name'] for p in data['products']]
            productPrices = [p['price'] for p in data['products']]
            urlKeys = [p['url_key'] for p in data['products']]
            skus = [p['sku'] for p in data['products']]
            print("Product name: " + productNames[0])
        else:
            print("Produsul nu a fost gasit pe Altex!")
        if productPrices:
            print("Product price: " + str(productPrices[0]) + " Lei")
        else:
            print("Produsul nu a fost gasit pe Altex!")
        if urlKeys:
            productUrl = "https://altex.ro/" + urlKeys[0] + "/cpd/"
        else:
            print("Produsul nu a fost gasit pe Altex!")
        if skus:
            productUrl = productUrl + skus[0]
            print("link: " + productUrl)
        else:
            print("Produsul nu a fost gasit pe Altex!")

        #scraping pcgarage
        print("CAUTARE PCGARAGE")
        websiteToScrap = f"{self.pcgarageWebsite}cauta/{productName.replace(' ', '+')}"
        headers={
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Host": "www.pcgarage.ro",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0"
        }
        pcgarageScrap = requests.get(websiteToScrap,headers=headers)
        websiteSoup = BeautifulSoup(pcgarageScrap.content,"html.parser")
        print(websiteSoup)
        links=websiteSoup.findAll('h2',attrs={"class":"my-0"})
        link=links[0].get('href')
        productPrices=websiteSoup.findAll('div',attrs={"class":"product_box_bottom"})
        productPrice=productPrices[0].get('price')
        print("link: " +link)
        print("price: " + productPrice)
