# -*-coding:Utf-8 -*

# Alias crée : smsMeteoCergy
# Crée par 42leParesseux

import bs4 as BeautifulSoup
import re
from urllib.request import urlopen
from urllib.parse   import quote

pageFile = urlopen("http://www.meteofrance.com/previsions-meteo-france/metz/57000")

def parsing(pageHTML) :
    soup = BeautifulSoup.BeautifulSoup(pageHTML, "lxml")
    jours = soup.find_all("article", class_="bloc-day-summary")
    c, date, min_temp, max_temp, climat = 0, [], [], [], []
    for i in jours :
        if c > 2:
            break
        date.append(i.find("a").get_text())
        #min_temp de chaque jour
        min_temp.append(i.find("span", class_="min-temp").get_text()[0:4])
        max_temp.append(i.find("span", class_="max-temp").get_text()[0:4])
        climat.append(i.find("span", class_="picTemps").get_text())
        c += 1
    
    ### Zoom sur aujourd'hui
    zoomJ1 = soup.find("div", class_="content group-day-detail hourly")
    # Recherche des horaires (heures)
    heures = []
    heuresTraitement = zoomJ1.find_all("th", scope="col")
    for i in heuresTraitement :
        heures.append(i.find("span").get_text())
    # Recherche des climats (climax)
    climax = []
    clima = zoomJ1.find_all("span", class_="picTemps")
    for i in clima:
        climax.append(i.get_text())
    # Recherche des températures (temp)
    temp = []
    tempall = zoomJ1.find("tr", class_="in-between")
    temptext = tempall.find_all("span")
    for i in temptext :
        temp.append(i.get_text())
    
    # Forme du message
    c, texte = 0, "**Metz**\n\n"
    while c < 3:
        if c == 0:
            texte += '##'+ date[c] + '\n'
            lol = 0
            while lol < 8 : # Affichage premier jour
                if lol < 7 :
                    texte += heures[lol] + ' : ' + temp[lol] + '\n <--' + climax[lol] + '-->' + '\n'
                    lol += 1
                else : 
                    texte += heures[lol] + ' : ' + temp[lol]
                    lol += 1
            c += 1
        else :
            texte += '\n\n##' + date[c] + '\n' + climat[c] + '\n' + 'de ' + min_temp[c] + ' à ' +max_temp[c]
            c += 1
    print(texte)
    return(texte)


#----------------------------------
# Lecture de la page HTML & traitement du message
#----------------------------------
pageHTML = pageFile.read()
texte = parsing(pageHTML)
pageFile.close()


#--------------------------------------
#   ENVOI SMS FREE
#--------------------------------------
user='ENTRER_VOTRE_USER'
pas='ENTRER_VOTRE_MDP'

#quote convertit en ascii la chaine utf8
texte = str(texte)
url = 'https://smsapi.free-mobile.fr/sendmsg?&user='+user+'&pass='+pas+'&msg='+quote(texte)
reponse = urlopen(url)
