import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy import signals
from scrapy import Request
import csv
import re


def extract_numbers(input_string):
    # Use regular expression to find all numbers in the string
    numbers = re.findall(r'\d+\.\d+|\d+', input_string)

    # Convert the list of strings to a list of floats and integers
    numbers = [float(num) if '.' in num else int(num) for num in numbers]

    return numbers


def extract_last_number(input_string):
    # Remove any leading/trailing whitespace and split the string into words
    words = input_string.strip().split()
    #print(words)
    match = re.findall(r'\d+\.\d+|\d+', words[-10])
    if match:
        # Extract the last word from the match
        result = match[-1]
        return result
    else:
        match = re.findall(r'\d+\.\d+|\d+', words[-11])
        result = match[-1]
        return result


def extract_last_word(input_string):
    # Remove any leading/trailing whitespace and split the string into words
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

#To Scrawl from the website type in scrapy crawl conditions into the terminal


class QuotesSpider(scrapy.Spider):

    #Name of the File
    name = "data"

    #Website to scrape from
    #https://brickinsights.com/sets?orderby=ppp_usd__desc&containing=0&containing_type=review_count&page=
    urlMain ="https://brickinsights.com/sets?year=2014&orderby=ppp_usd__desc&containing=0&containing_type=review_count&page="
    start_urls = []
    for i in range(28):
        start_urls.append(urlMain+str(i))
        #print(start_urls[i])



    def parse(self, response):

        # Scrapes provided link for more links
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


            # if i == 106:
            #     break


    def secondFunc(self, response):


        # DONT DELETE

        result = []
        # Scraping at article previous link lead to
        thingy = response.css("div.legible").getall()

        nums = extract_numbers(thingy[3])

        result.append(nums[2])
        result.append(nums[4])
        result.append(nums[5])
        result.append(nums[6])
        result.append(nums[7])
        result.append(nums[10])


        franchise =response.css("div.hero--summary").getall()
        result.append(extract_last_word(franchise[0]))


        yield {
            "Number of Parts": result[0],
            "Original Retail Price": result[1],
            "Inflation Retail Price": result[2],
            "Original Price Per Part": result[3],
            #"Inflation Price Per Part": result[4],
            "Year of Release": extract_last_number(franchise[0]),
            "Theme": result[6],
        }




