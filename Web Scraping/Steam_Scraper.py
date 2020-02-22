# Import all the needed tools

import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import os.path
from datetime import datetime

# Main loop
# Define the lists
gameTitleList = []
releaseDateList = []
discountPercentList = []
originalPriceList = []
discountedPriceList = []
windowsSupportList = []
macSupportList = []
linuxSupportList = []
windowsRawList = []
macRawList = []
linuxRawList = []
ratingList = []
amountOfReviewsListRaw = []
amountOfReviewsList = []
scrapedDateList = []
# Define page number
pageNumber = 1
# Loop through pages 1-5
for pageNumber in range(1, 6):
    data = requests.get(
        "https://store.steampowered.com/search/?specials=1&page=" + str(pageNumber))
    soup = BeautifulSoup(data.text, "html.parser")
    pageNumber + 1
    containers = soup.find_all("div", class_="responsive_search_name_combined")
    for container in containers:
        if container.find("div", class_="col search_price discounted responsive_secondrow") is not None:
            # Title
            gameTitle = container.span.text
            gameTitleList.append(gameTitle)
            # Release date
            releaseDate = container.find(
                "div", class_="col search_released responsive_secondrow").text
            releaseDateList.append(releaseDate)
            # Sale
            discountPercent = container.find(
                "div", class_="col search_discount responsive_secondrow").span.text
            discountPercentList.append(discountPercent)
            # Original price
            originalPrice = container.find(
                "div", class_="col search_price discounted responsive_secondrow").span.text
            originalPriceList.append(originalPrice)
            # Price right now

            # Here we get both the original and new price
            # Remove the unnecessary whitespaces and add €
            # Replace -- with 00 in case the price is an even number
            discountedPrice = container.find("div", class_="col search_price discounted responsive_secondrow").text.replace(
                " ", "").replace("--", "00").replace("\n", "").replace("€", "€|")
            priceString1 = "".join(discountedPrice)
            priceTempList = priceString1.split("|")
            del priceTempList[::2]
            priceString2 = "".join(priceTempList)
            discountedPriceList.append(priceString2)

            # Which platforms support the game
            winContainer = container.p.find("span", class_="platform_img win")
            macContainer = container.p.find("span", class_="platform_img mac")
            linuxContainer = container.find(
                "span", class_="platform_img linux")
            # Make lists -> strings
            windowsRawList.append(winContainer)
            macRawList.append(macContainer)
            linuxRawList.append(linuxContainer)
            windowsString = str(windowsRawList)
            macString = str(macRawList)
            linuxString = str(linuxRawList)

            # Change string into 1 (supports) or 0 (Doens't support)
            windowsSupportListCheck = windowsString.replace("[", "").replace("]", "").replace("\"", "").replace(
                "<span class=", "").replace("></span>", "").replace("platform_img win", "1").replace("None", "0")
            windowsSupportList = windowsSupportListCheck.split(", ")

            macSupportListCheck = macString.replace("[", "").replace("]", "").replace("\"", "").replace(
                "<span class=", "").replace("></span>", "").replace("platform_img mac", "1").replace("None", "0")
            macSupportList = macSupportListCheck.split(", ")

            linuxSupportListCheck = linuxString.replace("[", "").replace("]", "").replace("\"", "").replace(
                "<span class=", "").replace("></span>", "").replace("platform_img linux", "1").replace("None", "0")
            linuxSupportList = linuxSupportListCheck.split(", ")
            # Check game rating
            try:
                ratingContainer = container.find("span", class_="search_review_summary")[
                    "data-tooltip-html"].split("<br>")

                if ratingContainer[0] == "Overwhelmingly Positive":
                    ratingList.append("10")
                if ratingContainer[0] == "Very Positive":
                    ratingList.append("9")
                if ratingContainer[0] == "Positive":
                    ratingList.append("8")
                if ratingContainer[0] == "Mostly Positive":
                    ratingList.append("7")
                if ratingContainer[0] == "Mixed":
                    ratingList.append("6")
                if ratingContainer[0] == "Mostly Negative":
                    ratingList.append("5")
                if ratingContainer[0] == "Negative":
                    ratingList.append("4")
                if ratingContainer[0] == "Very Negative":
                    ratingList.append("3")
                if ratingContainer[0] == "Overwhelmingly Negative":
                    ratingList.append("2")
            # In case some game doens't have a rating, we assume it has 0
            except:
                ratingList.append("0")
            # How many ratings does the game have
            try:
                amountOfReviews = container.find("span", class_="search_review_summary")[
                    "data-tooltip-html"]
                amountOfReviews = amountOfReviews.replace(
                    " user reviews ", "|")
                amountOfReviewsListRaw.append(amountOfReviews)
                amountOfReviewsString = "".join(amountOfReviewsListRaw)
                amountOfReviewsString = re.sub(
                    r"(<br>\d+%)", "", amountOfReviewsString)
                amountOfReviewsString = re.sub(
                    r"[a-zA-Z\s\.',-]", "", amountOfReviewsString)
                amountOfReviewsList = amountOfReviewsString.split("|")
                del amountOfReviewsList[-1]
            # 0 tells us that the game lacks a rating
            except:
                amountOfReviewsString = amountOfReviewsString + "0|"
                amountOfReviewsList.append("0")
                amountOfReviewsListRaw.append("<br>00% of the 0|")
            # Date of the scraping
            dateTimeNow = datetime.now()
            # Formatting that date
            todaysDateString = dateTimeNow.strftime("%d/%m/%Y %H:%M:%S")
            scrapedDateList.append(todaysDateString)


# Create a dataframe to store this information

steamScraper = pd.DataFrame({"Title": gameTitleList, "Rating": ratingList, "Reviews": amountOfReviewsList, "Discount": discountPercentList, "Discounted Price": discountedPriceList, "Original Price": originalPriceList,
                             "Release date": releaseDateList, "Windows support": windowsSupportList, "Mac Support": macSupportList, "Linux Support": linuxSupportList, "Date scraped": scrapedDateList})

# Check in case we already have a csv file. If we have, overwrite it. If we don't, create the file

if os.path.exists("C:/Users/nikla/OneDrive - Arcada/steamScraperCSV2.csv") == False:
    steamScraper.to_csv(
        "C:/Users/nikla/OneDrive - Arcada/steamScraperCSV2.csv", index=False, encoding="utf-8")
else:
    with open("C:/Users/nikla/OneDrive - Arcada/steamScraperCSV2.csv", "r+", encoding="utf-8") as steamScraperFile:
        steamScraper.to_csv(steamScraperFile, index=False, encoding="utf-8")