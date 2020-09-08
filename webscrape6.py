from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import time
import random


categories=['business',  
				'health', 
				'music', 
				'charity-and-causes', 
				'community', 
				'arts', 
				'science-and-tech', 
				'sports-and-fitness',]

def filesCreate(category):
 	filename = "eventsList12.csv"
 	f = open(filename, "w")
 	headers = "title, date, location, link, category, price \n"
 	f.write(headers) 
 	for cat in category:
 		for i in range(1,51):
 			delay_time = random.randint(2, 7)
 			for a in range (delay_time):
 				print(delay_time - a)
 				time.sleep(1)

 			print("scraping page: " + str(i))
 			my_url = 'https://www.eventbrite.co.uk/d/united-kingdom--london/' + cat + '--events/?page=' + str(i)
 			# opening connection and grabbing page
 			uClient = uReq(my_url)
 			page_html = uClient.read()
 			uClient.close()

 			page_soup = soup(page_html, "html.parser")
 			containers = page_soup.findAll("div",{"class":"search-event-card-wrapper"})
 			f2 = open(filename, "a")
 			i=0
 			for container in containers:
 				try:
 					title = container.findAll("div",{"class":"eds-event-card__formatted-name--is-clamped"})
 					event_name = title[0].text.strip()
 					print(event_name)
 				except:
 					event_name = "null"
 				try:
 					date = container.findAll("div",{"class":"eds-text-color--primary-brand eds-l-pad-bot-1 eds-text-weight--heavy eds-text-bs"})
 					event_date = date[0].text.strip()
 					print(event_date)
 				except:
 					event_date= "null"
				

 				try:
 					link_to_event = container.find("a",{"class":"eds-event-card-content__action-link"})["href"]
 					print(link_to_event)

 					uClient = uReq(link_to_event)
 					page_html2 = uClient.read()
 					page_soup2 = soup(page_html2, "html.parser")
 					
 					try:
 						location = page_soup2.findAll("div", {"event-details__data"})[1]	
 						address = ""
 						var = location.findAll('p')
 						for i in range (len(var)):
 							if "View Map" not in var[i].text.strip():
	 							address = address + var[i].text.strip() + "," 
	 							if i == 3:
	 								break
	 					print(address)
 					except:
		 					try:
				 				location = container.findAll("div",{"class":"card-text--truncated__one"})
				 				print(location[0].text)
				 				address = location[0].text
				 				# print(location)
				 			except:
				 				# print("errror getting location!")
				 				address = "null"
 					try:
 						price = page_soup2.find("div",{"js-panel-display-price"}).text.strip()
 						print(price)
 					except:

 						try:
 							price = page_soup2.find("div",{"js-display-price"}).text.strip()
 							print(price)
 						except:
 							price ="null"
 					try:
 						description = page_soup2.find("div",{"structured-content-rich-text structured-content__module l-align-left l-mar-vert-6 l-sm-mar-vert-4 text-body-medium"}).text.strip()
 						descriptionList = description.split()
 						print(descriptionList)

 						# if "and" in descriptionList:
 						# 	print("THE WORD AND IS PRESENT!!!!!")

 						cat2 = cat
 						if "health" not in cat:
 							if "health" in descriptionList   or "physician" in descriptionList  or "doctor" in descriptionList  or "medicine" in descriptionList  or "geneticist" in descriptionList  or "diet" in descriptionList  or "nutrition" in descriptionList  or "wellbeing" in descriptionList  or "lifestyle" in descriptionList  or "pregnant" in descriptionList  or "treatment" in descriptionList  or "trauma" in descriptionList  or "nerves" in descriptionList:
 								cat = cat + "|health"
 						if "science-and-tech" not in cat:
 							if "AI" in descriptionList  or "Artificial" in descriptionList  or "intelegence" in descriptionList  or "science" in descriptionList  or "technology" in descriptionList  or "health" in descriptionList  or "treatment" in descriptionList  or "computer" in descriptionList  or "software" in descriptionList or "hardware" in descriptionList  or "treatment" in descriptionList  or "Python" in descriptionList  or "Java" in descriptionList  or "C++" in descriptionList  or "C#" in descriptionList  or "building" in descriptionList  or "diagnose" in descriptionList or "data" in descriptionList  or "analyse" in descriptionList  or "analysis" in descriptionList  or "tool" in descriptionList  or "programming" in descriptionList  or "analytics" in descriptionList  or "process" in descriptionList or "processing" in descriptionList or "computing" in descriptionList or "scientific" in descriptionList or "laptop" in descriptionList or "intelligence" in descriptionList or "technologies" in descriptionList or "demo" in descriptionList or "tech" in descriptionList:
 								cat = cat + "|science-and-tech"
 						if "sports-and-fitness" not in cat:
 							if "health" in descriptionList or "sport" in descriptionList or "fitness" in descriptionList  or "gym" in descriptionList or "diet" in descriptionList or "nutrition" in descriptionList or "wellbeing" in descriptionList  or "lifestyle" in descriptionList  or "marathon" in descriptionList or "football" in descriptionList or "rugby" in descriptionList or "runner" in descriptionList or "yoga" in descriptionList  or "workout" in descriptionList  or "cycling" in descriptionList or "bicycle" in descriptionList or "crossfit" in descriptionList:
 								cat = cat +"|sports-and-fitness"
 						if "business" not in cat:
 							if "business" in descriptionList  or "invest" in descriptionList  or "money" in descriptionList or "profit" in descriptionList  or "revenue" in descriptionList  or "sales" in descriptionList  or "finance" in descriptionList  or "financial" in descriptionList  or "accounts" in descriptionList  or "marketing" in descriptionList  or "HR" in descriptionList  or "hr" in descriptionList  or "management" in descriptionList  or "employer" in descriptionList  or "employees" in descriptionList  or "strategy" in descriptionList  or "exercise" in descriptionList  or "customer" in descriptionList or "customers" in descriptionList  or "investment" in descriptionList  or "trade" in descriptionList  or "trading" in descriptionList or "market" in descriptionList or "strategies" in descriptionList  or "finances" in descriptionList  or "income" in descriptionList:
 								cat = cat + "|business"
 						if "music" not in cat:
 							if "music" in descriptionList  or "drums" in descriptionList or  "concert" in descriptionList or  "performance" in descriptionList or  "dance" in descriptionList or  "dancing" in descriptionList or  "rap" in descriptionList or  "jazz" in descriptionList or  "party" in descriptionList or  "hip-hop" in descriptionList or  "HR" in descriptionList or  "hip" in descriptionList or  "album" in descriptionList or  "orchestra" in descriptionList or  "rappers" in descriptionList or  "musical" in descriptionList or  "rnb" in descriptionList or  "RNB" in descriptionList or "DJ" in descriptionList or  "Djs" in descriptionList or  "djs" in descriptionList or  "bass" in descriptionList or  "vocals" in descriptionList or  "instrumental" in descriptionList or  "festival"in descriptionList:
 								cat = cat + "|music"
 						if "arts" not in cat:
 							if "arts" in descriptionList or  "artist" in descriptionList or  "artists" in descriptionList or  "paint" in descriptionList or  "painting" in descriptionList or  "craft" in descriptionList or  "performing" in descriptionList or  "art" in descriptionList or  "poem" in descriptionList or  "poets" in descriptionList or  "garden" in descriptionList or  "graffiti" in descriptionList or  "comedy" in descriptionList or  "drawing" in descriptionList or  "draw" in descriptionList or  "sketching"in descriptionList  or  "photography" in descriptionList or  "concert"in descriptionList:
 								cat = cat + "|arts"
 						if "charity-and-causes" not in cat:
 							if "charity" in descriptionList or  "fundraising" in descriptionList:
 								cat = cat + "|charity-and-causes"
 						if "community" not in cat:
 							if "community" in descriptionList or "group" in descriptionList or  "ethnic" in descriptionList or  "African" in descriptionList or  "Africa" in descriptionList or  "language" in descriptionList:
 								cat = cat + "|community"
 						if "environment" not in cat:
 							if "environment" in descriptionList or  "rocks" in descriptionList  or  "geology" in descriptionList or  "climate" in descriptionList or  "global-warming" in descriptionList or  "temperature" in descriptionList or  "pollution" in descriptionList:
 								cat = cat + "|environment"
 						if "coding" not in cat:
 							if "coding" in descriptionList or  "programming" in descriptionList or  "Java" in descriptionList or  "c++" in descriptionList or  "C++" in descriptionList or  "c#" in descriptionList or  "C#" in descriptionList or  "software" in descriptionList or  "Python" in descriptionList or  "HTML" in descriptionList or  "html" in descriptionList:
 								cat = cat + "|coding"
 						if "talks" not in cat:
 							if "seminar" in descriptionList or  "lecture" in descriptionList or  "seminars" in descriptionList or  "lectures" in descriptionList or  "lecturer" in descriptionList or  "meetings" in descriptionList:
 								cat = cat + "|talks"
 						if "media" not in cat:
 							if "media" in descriptionList or  "social" in descriptionList or  "socialmedia" in descriptionList or  "social-media" in descriptionList or  "facebook" in descriptionList or  "instagram" in descriptionList or  "twitter" in descriptionList or  "following" in descriptionList or  "influencer" in descriptionList:
 								cat = cat + "|media"
 						if "tours" not in cat: 
 							if "tours" in descriptionList or  "tour" in descriptionList or  "walk" in descriptionList or  "museum" in descriptionList:
 								cat = cat + "|tours"
 						if "history" not in cat:
 							if "history" in descriptionList or  "slavery" in descriptionList or  "slave" in descriptionList or  "museum" in descriptionList:
 								cat = cat + "|history"
 						if "economy" not in cat:
 							if "economy" in descriptionList or  "recession" in descriptionList or  "eceonomic" in descriptionList or  "finanicial" in descriptionList or  "supply" in descriptionList or  "demand" in descriptionList or  "market" in descriptionList:
 								cat = cat + "|economy"
 						if "career" not in cat:
 							if "career" in descriptionList or  "interview" in descriptionList or  "promotion" in descriptionList or  "skills" in descriptionList or  "networking" in descriptionList or  "job" in descriptionList or  "employment" in descriptionList or  "CV" in descriptionList:
 								cat = cat + "|career"
 						if "cultural" not in cat:
 							if "cultural" in descriptionList or  "culture" in descriptionList or  "African" in descriptionList or  "Asian" in descriptionList or  "European" in descriptionList or  "Africa" in descriptionList:
 								cat = cat + "|cultural"
 						if "investment" not in cat:
 							if "investment" in descriptionList or  "invest" in descriptionList or  "properties" in descriptionList or  "mortgage" in descriptionList or  "long-term" in descriptionList or  "crypto" in descriptionList or  "cryptocurrency" in descriptionList or  "crypto-currency" in descriptionList or  "bitcoin" in descriptionList or  "altcoins" in descriptionList:
 								cat = cat + "|investment"
 						if "networking" not in cat:
 							if "expo" in descriptionList or "Expo" in descriptionList or "networking":
 								cat = cat + "|networking"
 						if "dance" not in cat:
 							if "dance" in descriptionList or  "dancing" in descriptionList or  "choreography" in descriptionList or "music" in descriptionList:
 								cat = cat + "|dance"

 						

 					except:
 						description = "null"
 				except:
 					link_to_event = "null"
 					description = "null"
 					address="null"
 					price ="null"

 				i = i+1

 				
 				f2.write(event_name.replace(",", "|") +","+ event_date.replace(",", "|") +","+ address.replace(",", "|") +","+  link_to_event + "," + cat +","+  price.replace(",", "|") +"\n")
 				cat = cat2
 		f.close()
 		print("FINISHED!!!")
filesCreate(categories)




	# Title:
	# <div class="eds-event-card__formatted-name--is-clamped eds-event-card__formatted-name--is-clamped-three eds-text-weight--heavy" 
	# aria-hidden="true" role="presentation" data-spec="event-card__formatted-name--content">2 Comic Con Spring 2020</div>

	# Date:
	# <div class="eds-text-color--primary-brand eds-l-pad-bot-1 eds-text-weight--heavy eds-text-bs"
	# >Sa2t, Feb 29, 09:00</div>

	# Location:
	# <div class="card-text--truncated__one"
	# >Olympi2a London • London</div>

	# # Price: price may be empty meaning that there is a price range and you can only get the price once you click on th event.
	# <div class="eds-media-card-content__sub eds-text-bm eds-text-color--grey-600 eds-l-mar-top-1 eds-media-card-content__sub--cropped"
	# >Starts at £6.0000</div>

