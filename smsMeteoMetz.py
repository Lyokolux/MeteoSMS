import bs4 as BeautifulSoup
from urllib.request import urlopen
from urllib.parse import quote


def parsing(pageHTML):
	"""
		Get 3 types of element from the page html meteo france :
			- schedule / timetable
			- temperature

		data_* : extraction from the HTML page
		msg_* : list of the elements which are used in 
			the final msg

		return all data in a string
	"""
	content_page = BeautifulSoup.BeautifulSoup(pageHTML, "lxml" )
	content_page = content_page.find("ul", class_="prevision-horaire")

	data_clock = content_page.find_all("time")
	msg_clock = [element.get_text() for element in data_clock]

	data_temperature = content_page.find_all("li", class_="day-summary-temperature")
	msg_temperature = [temp.get_text() for (i, temp) in enumerate(data_temperature) if i % 2 == 1]

	data_sky = content_page.find_all("li", class_="day-summary-image")
	msg_sky = [content_page.find("li", class_="day-summary-label").get_text()]
	for (i, element) in enumerate(data_sky):
		if i % 2 == 1:
			msg_sky.append(element.find("span").get_text())


	msg = '# Meteo Metz\n'
	for i in range(len(msg_temperature)):
		msg += (f"{msg_clock[i]} - {msg_sky[i]} - {msg_temperature[i]} \n")

	return msg

#---------------------#
#  Reading 		      #
#---------------------#

pageFile = urlopen('http://www.meteofrance.com/previsions-meteo-france/metz/57000')
pageHTML = pageFile.read()
msg = parsing(pageHTML)
pageFile.close()

#---------------------#
# Envoi du sms        #
#---------------------#
user='YOUR_USER'
pas='YOUR_PASSWORD'

#quote convert from utf-8 to ASCII
texte = str(msg)
url = 'https://smsapi.free-mobile.fr/sendmsg?&user='+user+'&pass='+pas+'&msg='+quote(texte)
reponse = urlopen(url)