import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

class CSVEntry:
    def __init__(self, emails, channelname, subscribercount=0):
        self.emails = emails
        self.channelname = channelname
        self.subscribercount = subscribercount
    def toCSV(self, searchsubject,outputfile = 0):
        output = ""
        print (self.emails)
        if len(self.emails) >= 1:
            for email in self.emails:
                output = output + email.encode('utf-8', 'ignore') + ','
        output = output + self.channelname.encode('utf-8', 'ignore') + ','
        output = output + self.subscribercount.encode('utf-8', 'ignore')
        output = output + '\n'
        
        if outputfile == 0:
            return output     
        else:
            if not os.path.isfile(outputfile):
                try:
                    with open(outputfile, 'w+') as f:
                        f.write("Search Subject:," + searchsubject + ", Amount of days before today searched:," + str(daysinthepast) + "\n")
                        f.write("Email Addresses in description, Channel Name, Subscriber Count\n")
                        f.close()
                except Exception as e:
                    print ("Exception! Error writing to output file.")
                    print (type(e))
                    print (str(e))
                    a = raw_input(" ")
            with open(outputfile, 'a+') as f:
                f.write(output)
                f.close()
            return

 

def StartupTest(driver):
    try:
        driver.get("http://www.youtube.com")
    except:
        time.sleep(1)
        StartupTest(driver)
    return driver

def main(SearchTerm):
    APIKEY = "YOUR_API_KEY_HERE"  
    print(SearchTerm)
    
    driver = webdriver.Chrome()
    driver = StartupTest(driver)
    driver = NavigateToYoutubeAndSearch(driver, SearchTerm)
    BeginSearchParsing(driver)
    
def NavigateToYoutubeAndSearch(driver, searchterm):
    try:
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@id='search']"))
        )
        search_box.send_keys(searchterm)

        search_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[@id='search-icon-legacy']"))
        )
        search_button.click()
    except:
        print("Error during navigation and search")
    return driver

def BeginSearchParsing(driver):
    emailregexpattern = r'(\w(?:[-.+]?\w+)+\@(?:[a-zA-Z0-9](?:[-+]?\w+)*\.)+[a-zA-Z]{2,})'
    p = re.compile(emailregexpattern)

    max_attempts = 10  # Max number of scrolls before quitting
    current_attempts = 0
    while current_attempts < max_attempts:
        try:
            video_descriptions = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//*[@id='dismissible']/div/div[3]/yt-formatted-string"))
            )
            
            for desc in video_descriptions:
                if "@" in desc.text:
                    if bool(p.search(desc.text)):
                        emails = re.findall(emailregexpattern, desc.text)
                        print(emails)   

            driver.execute_script("window.scrollTo(0, document.querySelector('ytd-app').scrollHeight);")

            time.sleep(5)  
            current_attempts += 1

        except Exception as e:
            print (type(e))
            print (str(e))
            print("Error during parsing")
            driver.quit()
            break

if __name__ == "__main__":
    main("hello")
