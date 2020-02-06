#run this file using "python MovieScraper.py"
from bs4 import BeautifulSoup
import requests
import csv
import helper

save_file = "Box_Office_new.csv"
with open(save_file, "w", newline="") as filename:
    file = csv.writer(filename, delimiter=",")
    # Write CSV Header. The first row will outline the data contained
    file.writerow(["Rank", "Title", "Studio", "Release Date", "Opening Box Office", "Opening Theaters", "Genre", "Runtime", "Rating", "Lifetime Gross"])

    for i in range(1, 168): #There are 168 pages. This is hardcoded
        print(i)
        url = "https://www.boxofficemojo.com/alltime/domestic.htm?page=" + i.__str__() + "&p=.htm"
        response = requests.get(url, timeout=5)
        content = BeautifulSoup(response.content, "html.parser")

        allListings = []
        #Find all rows on the home page. We know the tag 'tr' and the colors.
        for listing in content.findAll('tr', attrs={"bgcolor": ["#ffffff", "#f4f4ff"]}):

            #store each row into collection
            collection = []
            for data in listing.findAll('td'):
                collection.append(data)

            #find all urls that the row is linked to and add to the url structure.
            url = []
            for item in listing.findAll('a', href=True):
                url.append(item)

            #go to each url
            url1 = "https://www.boxofficemojo.com" + helper.url_fixer(url[0]["href"])[0]
            response1 = requests.get(url1, timeout=5)
            content1 = BeautifulSoup(response1.content, "html.parser")

            #find all the info in the first table. They fall under the 'b' tag
            body = []
            for data in content1.findAll('b'):
                body.append(data)

            #helps adjust the index for 2 different styles of page.
            adder = helper.url_fixer(url[0]["href"])[1]

            opening = []
            count = 0
            # find the information in the mpboxcontent class so that we can find theater info
            for data in content1.select(".mp_box_content td"):
                if(count == 11 or count == 17): #get info from the 11 and 17th index
                    opening.append(data)
                count += 1

            #make a dictionary
            listingObj = {
                "Studio": body[3 + adder].get_text(),
                "Release Date": body[4 + adder].get_text(),
                "Genre": body[5 + adder].get_text(),
                "Runtime": body[6 + adder].get_text(),
                "Rating": body[7 + adder].get_text(),
                "Rank": collection[0].get_text(),
                "Title": collection[1].get_text(),
                "Lifetime Gross": collection[3].get_text(),
                "Year": collection[4].get_text(),
                "url": helper.url_fixer(url[0]["href"]),
                "Opening": opening[0].get_text(),
                "Theaters": opening[1].get_text(),
            }

            #write to csv
            file.writerow([listingObj["Rank"],
                           listingObj["Title"],
                           listingObj["Studio"],
                           listingObj["Release Date"],
                           listingObj["Opening"],
                           listingObj["Theaters"],
                           listingObj["Genre"],
                           listingObj["Runtime"],
                           listingObj["Rating"],
                           listingObj["Lifetime Gross"]])

