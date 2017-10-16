import bs4 as BeautifulSoup
from urllib.request import urlopen
from urllib.parse import quote


def parsing(pageHTML):
	"""
		Get 3 types of element from the page html meteo france :
			- schedule / timetable
			- temperature

		data_* : extraction from the HTML page
		message_* : list of the elements which are used in 
			the final message

		return all data in a string
	"""
	content_page = BeautifulSoup.BeautifulSoup(pageHTML, "lxml" )
	content_page = content_page.find("ul", class_="prevision-horaire")

	data_clock = content_page.find_all("time")
	message_clock = []
	for element in data_clock:
		message_clock.append(element.get_text())

	data_temperature = content_page.find_all("li",
		class_="day-summary-temperature")
	message_temperature = []
	count = 1
	for element in data_temperature:
		if count % 2 == 0:
			message_temperature.append(element.get_text())
		count += 1

	data_sky = content_page.find_all("li", class_="day-summary-image")
	message_sky = []
	count = 1
	for element in data_sky:
		if count % 2 == 0:
			message_sky.append(element.find("span").get_text())
		count += 1
	message_sky.insert(0, content_page.find("li", class_="day-summary-label").get_text())

	message = '# Meteo Metz\n'
	for i in range(len(message_temperature)):
		if i <= len(message_sky) :
			message += ("{} - {} - {} \n".format(message_clock[i], message_sky[i], message_temperature[i]))

	return message

#---------------------
#  Reading 
#---------------------

pageFile = urlopen('http://www.meteofrance.com/'\
	'previsions-meteo-france/metz/57000')
pageHTML = pageFile.read()
message = parsing(pageHTML)
pageFile.close()

#---------------------
# Envoi du sms
#---------------------

user='22084257'
pas='mzd6hmbIgJTAGq'

#quote convert from utf-8 to ASCII
texte = str(message)
url = 'https://smsapi.free-mobile.fr/sendmsg?&user='+user+'&pass='+pas+'&msg='+quote(texte)
reponse = urlopen(url)