# Aplicatie de Scraping pe Internet

# Scopul si cerintele aplicatiei
Scopul aplicatiei este acela de a oferi utilizatorului posibilitatea de a alege intre doua moduri de utilizare: unul de monitorizare al pretului unui produs de pe un anumit website, iar daca pretul produsului scade, utilizatorul sa fie anuntat printr-un email. Al doilea mod este cel de comparare a preturilor de pe mai multe website-uri pentru care aplicatia sa ofere suport. Aceasta optiune va pune la dispozitia utilizatorului posibilitatea de a insera numele produsului dorit, iar apoi va afisa link-uri catre mai multe website-uri pe care a fost gasit produsul impreuna cu pretul acestuia.

# 17.06.2024

Am ales tema proiectului si m-am informat despre ce inseamna scraping-ul de pe website-ul: https://www.parsehub.com/blog/what-is-web-scraping/

# 18.06.2024

Am inceput un simplu proiect pentru a intelege mai bine cum functioneaza biblioteca BeautifulSoup si ce functii are aceasta. Am reusit sa parcurg un website, sa iau toate link-urile din website si sa le parcurg pentru a obtine citatele din acesta. Mi-am aprofundat cunostintele in acest domeniu de pe website-ul: https://www.tutorialspoint.com/beautiful_soup/index.htm

# 19.06.2024

Am realizat o interfata grafica pentru aplicatie folosind biblioteca tkinter din python. Punand astfel la dispozitia utilizatorului posibilitatea de a alege in ce mod va functiona aplicatia (monitorizare pret/comparare preturi)

# 20.06.2024

Am intampinat probleme cu scraping-ul website-ului altex. Am rezolvat problema intalnita intelegand mai bine cum functioneaza website-urile de tip "Single-page application", pentru aceasta am citit din: https://stackoverflow.com/questions/57062946/how-to-scrape-through-single-page-application-websites-in-python-using-bs4 si https://medium.com/analytics-vidhya/scraping-web-apps-using-direct-http-request-f5c02a2874fe .Am avut mai multe incercari insa toate au esuat

# 21.06.2024

Am rezolvat problema cu scraping-ul website-ului altex, produsele fiind livrate printr-un json ca raspuns la un request de tip xhr. Am incercat si scraping-ul website-ului pcgarage insa m-am blocat deoarece am intalnit o problema, identificandu-mi request-ul drept unul facut de un bot.

# 26.06.2024

Am incercat sa fac scraping site-urilor pcgarage.ro si cel.ro , insa am intampinat probleme deoarece request-ul meu era recunoscut drept unul facut de un bot. Pentru a rezolva aceasta problema m-am documentat de pe stackoverflow si tutoriale de pe youtube.

# 27.06.2024

Am reusit sa fac scraping site-ului cel.ro. Am imbunatatit interfata grafica astfel incat sa ofer utilizatorului posibilitatea de a adauga un email atunci cand vrea sa monitorizeze pretul unui produs, deoarece ulterior cand va avea loc o reducere a pretului produsului, utilizatorul va fi anuntat cu privire la modificare pe mail. Am facut scraping pentru ca atunci cand user-ul introduce un link catre un produs sa ii fie luat pretul pe care il va monitoriza ulterior. Pentru monitorizarea pretului se creaza un fisier "priceLogger.txt" in care vor exista link-uri catre produsele cautate pana in prezent, pretul produsului, impreuna cu email-ul userului.

# 28.06.2024

Am adaugat posibilitatea de trimitere a unui mail catre utilizator in momentul in care pretul produsului scade. Pentru a monitoriza permanent statusul pretului produsului am realizat un cronjob care ruleaza o sursa in python la fiecare doua minute. De fiecare data cand se efectueaza o verificare, aceasta va fi logata intr-un fisier de log: "logger.txt"

cronjob-ul este urmatorul: */2 * * * * python3 /home/rosca/Desktop/ProiectPractica/AplicatieScrapingInternet/priceMonitor.py >> /home/rosca/Desktop/ProiectPractica/AplicatieScrapingInternet/logger.txt 2> /home/rosca/Desktop/ProiectPractica/AplicatieScrapingInternet/logger.txt 