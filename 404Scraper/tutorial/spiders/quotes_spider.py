import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy import signals
from scrapy import Request
import csv
import re

#You can run this by going to the runSpider and just running it from there

def remove_html_tags(text):
    #Also removes whitespace

    text = re.sub(r'<.*?>', '', text)
    return re.sub(r'\s+', '', text)

def remove_until_fourth_newline(text):
    count = 0
    for i, char in enumerate(text):
        if char == '\n':
            count += 1
            if count == 4:
                return text[i+1:]
    return ""
def extract_numbers(input_string):
    numbers = re.findall(r'\d+\.\d+|\d+', input_string)
    numbers = [float(num) if '.' in num else int(num) for num in numbers]
    return numbers

def extract_last_word(input_string):
    # Remove any leading/trailing whitespace and split the string into words
    input_string = input_string.replace(" ", "")
    words = input_string.strip().split()
    match = re.search(r'>([A-Za-z]+)<', words[-3])
    if match:
        # Extract the last word from the match
        result = match.group(1)
        return result
    else:
        match = re.search(r'>([A-Za-z]+)<', words[-4] + words[-3])
        if match:
            # Extract the last word from the match
            result = match.group(1)
            return result
        else:
            return None




class QuotesSpider(scrapy.Spider):

    #Name of the CSV file that will be made
    name = "data"

    #Website to scrape from
    #https://brickinsights.com/sets?orderby=ppp_usd__desc&containing=0&containing_type=review_count&page=
    urlMain ="https://brickinsights.com/sets?year=2014&orderby=ppp_usd__desc&containing=0&containing_type=review_count&page="
    start_urls = []

    #Number is the number of pages that we need to iterate through
    for i in range(28):
        start_urls.append(urlMain+str(i))





    def parse(self, response):

        #Scrapes provided link for more links
        correctLinks = False
        i = 0

        for div in response.css("a"):
            i += 1
            #print(div)

            url = div.css("a::attr(href)").get()

            try:
                if correctLinks:
                    if url[30] == "?":
                        break

            except IndexError:
                pass


            if correctLinks:
                #print(url)
                yield scrapy.Request(url, self.secondFunc)
            if url == "https://brickinsights.com/faq":
                correctLinks =True




        yield scrapy.Request(url, self.secondFunc)



    def secondFunc(self, response):




        result = []

        # Scraping at article previous link lead to
        thingy = response.css("div.legible").getall()

        theme = response.css("div.hero--summary").getall()

        num = remove_html_tags(remove_until_fourth_newline(thingy[3]))
        nums = extract_numbers(num)



        if "PricePerPart(USD):" not in num:
            pass
        else:

            result.append(nums[0])
            if "Minifigs:" not in num:
                result.append(nums[1])
            result.append(nums[2])
            result.append(nums[3])
            result.append(nums[4])
            result.append(nums[5])
            result.append(extract_last_word(theme[-1]))

            if result[-1] == "Gear" or result[-1] == "CollectableMinifigures":
                pass
            else:


                yield {
                    "Number of Parts": result[0],
                    "Original Retail Price": result[1],
                    "Inflation Retail Price": result[2],
                    "Original Price Per Part": result[3],
                    "Inflation Price Per Part": result[4],
                    "Year of Release": 2014,
                    "Theme": result[-1],
                    "Link to page": response
                }




