import requests
from bs4 import BeautifulSoup as bs
import re
import pandas as pd
import os.path
from datetime import datetime

# Create lists
gameTitle = []
rating = []
discountPercent = []
discountPrice = []
originalPrice = []
releaseDate = []
reviewsListRaw = []
reviewsList = []
windowsSupport = []
macSupport = []
linuxSupport = []
windowsList = []
macList = []
linuxList = []
scrapeDate = []

# Loop through pages 1-5
for page in range(1, 6):
    # The URL is largly the same for each page, aside from the page number at the end
    data = requests.get('https://store.steampowered.com/search/?specials=1&page=' + str(page))
    soup = bs(data.content, 'html.parser')
    # Look for the correct div which has the info we want
    divs = soup.find_all('div', class_='responsive_search_name_combined')
    # Loop through that div
    for i in divs:
        # Unless 'col search_price discounted responsive_secondrow' is empty, anything found is game info
        if i.find('div', class_='col search_price discounted responsive_secondrow') is not None:
            # The info we want is all either in a span class or a div.
            # This can be checked by inspecting the steam website

            # Title
            g = i.span.text
            # Append title
            gameTitle.append(g)

            # Game rating
            try:
                ratingContainer = i.find('span', class_='search_review_summary')[
                    'data-tooltip-html'].split('<br>')
                # Convert rating into numbers from 2 to 10
                # And after that we append it to the list
                if ratingContainer[0] == 'Overwhelmingly Positive':
                    rating.append('10')
                if ratingContainer[0] == 'Very Positive':
                    rating.append('9')
                if ratingContainer[0] == 'Positive':
                    rating.append('8')
                if ratingContainer[0] == 'Mostly Positive':
                    rating.append('7')
                if ratingContainer[0] == 'Mixed':
                    rating.append('6')
                if ratingContainer[0] == 'Mostly Negative':
                    rating.append('5')
                if ratingContainer[0] == 'Negative':
                    rating.append('4')
                if ratingContainer[0] == 'Very Negative':
                    rating.append('3')
                if ratingContainer[0] == 'Overwhelmingly Negative':
                    rating.append('2')
            # In case the game doesn't have reviews we convert the value to None
            except:
                rating.append('None')

            # Sale percentage
            disc = i.find('div', class_='col search_discount responsive_secondrow').span.text
            # Append percentage
            discountPercent.append(disc)

            # Sale price
            # Tidy upp text
            discPr = i.find('div', class_='col search_price discounted responsive_secondrow').text.replace(
                ' ', '').replace('\n', '').replace('€', '€|')
            # Remove whitespaces
            priceString1 = ''.join(discPr)
            priceTempList = priceString1.split('|')
            # Remove the original price which steam shows next to the discounted price
            del priceTempList[::2]
            # Tidying upp
            priceString2 = ''.join(priceTempList)
            # Append discounted price
            discountPrice.append(priceString2)

            # Original price
            orig = i.find('div', class_='col search_price discounted responsive_secondrow').span.text
            # Append original price
            originalPrice.append(orig)

            # Release date
            release = i.find('div', class_='col search_released responsive_secondrow').text
            # Append release date
            releaseDate.append(release)
            
            # Supported platforms
            win = i.p.find('span', class_='platform_img win')
            mac = i.p.find('span', class_='platform_img mac')
            lin = i.find('span', class_='platform_img linux')

            # First we convert to lists
            # After that we convert the lists to strings to edit them
            windowsList.append(win)
            macList.append(mac)
            linuxList.append(lin)
            windowsString = str(windowsList)
            macString = str(macList)
            linuxString = str(linuxList)

            # Edit the strings to 1 (Supports platform) or 0 (Doesn't support platform)
            # Clean upp end result with regex
            windowsSupportListCheck = windowsString.replace('[', '').replace(']', '').replace('\'', '').replace(
                '<span class=', '').replace('></span>', '').replace('platform_img win', '1').replace('None', '0')
            # And finally we add the info to the list according to separator
            windowsSupport = windowsSupportListCheck.split(', ')

            macSupportListCheck = macString.replace('[', '').replace(']', '').replace('\'', '').replace(
                '<span class=', '').replace('></span>', '').replace('platform_img mac', '1').replace('None', '0')
            # And finally we add the info to the list according to separator
            macSupport = macSupportListCheck.split(', ')

            linuxSupportListCheck = linuxString.replace('[', '').replace(']', '').replace('\'', '').replace(
                '<span class=', '').replace('></span>', '').replace('platform_img linux', '1').replace('None', '0')
            # And finally we add the info to the list according to separator
            linuxSupport = linuxSupportListCheck.split(', ')

            # Number of ratings
            try:
                reviews = i.find('span', class_='search_review_summary')['data-tooltip-html']
                # Tidying upp text
                reviews = reviews.replace(' user reviews ', '|')
                # Append to temp list
                reviewsListRaw.append(reviews)
                reviewsString = ''.join(reviewsListRaw)
                # Remove everything except numbers
                reviewsString = re.sub(r'(<br>\d+%)', '', reviewsString)
                reviewsString = re.sub(r"[a-zA-Z\s\.',-]", '', reviewsString)
                # Reformat by the | separator
                reviewsList = reviewsString.split('|')
                # Remove the extra value at the end
                del reviewsList[-1]

            # 0 means the game lacks reviews
            except:
                reviewsString = reviewsString + '0|'
                # Append to list and remove extra clutter
                reviewsList.append('0')
                reviewsListRaw.append('<br>00% of the 0|')

            # Date of the scrape
            dateTimeNow = datetime.now()

            # Reformat date
            todaysDateString = dateTimeNow.strftime('%d/%m/%Y %H:%M:%S')
            # You guessed it, append to list :)
            scrapeDate.append(todaysDateString)

# Create a DF by combining the lists we created previously
# Name the columns accordingly
df = pd.DataFrame({'Title': gameTitle, 'Rating': rating, 'Discount': discountPercent, 'Discounted Price': discountPrice, 'Original Price': originalPrice,
                             'Release date': releaseDate, 'Reviews': reviewsList, 'Windows support': windowsSupport, 'Mac Support': macSupport, 'Linux Support': linuxSupport, 'Date scraped': scrapeDate})

# Check if a file already exists.
if os.path.exists('PATH_HERE') == False:
    # Use enconde etf-8-sig to show € sign correctly
    df.to_csv('PATH_HERE', index=False, encoding='utf-8-sig')

# If a file already exists we rewrite it
else:
    with open('C:/Users/nikla/OneDrive - Arcada/steamScraperCSV.csv', 'r+', encoding='utf-8') as steamScraperFile:
        df.to_csv(steamScraperFile, index=False, encoding='utf-8-sig')