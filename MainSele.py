from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib.request
from urllib.request import FancyURLopener
from selenium.webdriver.common.action_chains import ActionChains
import time
import re
import os



user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0"
headers = {'User-Agent': user_agent}

class MyOpener(FancyURLopener):
    version = user_agent

userdir = input("Enter your directory here where the files are: ")
ppath = userdir

def doesfolderExist(entry): #Checks if the folder exists, and if not it makes the folder.
    if os.path.isdir(ppath + "/" + entry):
        return True
    else:
        os.makedirs(ppath + "/" + entry)

def findWholeWord(w):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

def numFiles(entry): #Finds the number of files in the folder and returns the value.
    fileCount = 0
    for root, dirs, files in os.walk(ppath + "/" + entry):
        for file in files:
            fileCount += 1
    return fileCount

searchTerm = input("Please input a person to search for: ")

driverProf = webdriver.FirefoxProfile()
driverProf.set_preference("browser.helperApps.neverAsk.saveToDisk", 'image/jpeg, image/tiff, image/png, image/jpg ')
driverProf.set_preference("browser.download.folderList", 2)
driverProf.set_preference("browser.download.manager.showWhenStarting", False)
driver = webdriver.Firefox(driverProf)
action = ActionChains(driver)


driver.get("https://www.google.com/advanced_image_search?")

subjectSearch = driver.find_element_by_id("_dKg")
subjectSearch.send_keys(searchTerm)

dropdownID = driver.find_element_by_id("imgsz_button")  # 7f
dropdownID.click()

for elem in dropdownID.text:
    elem = dropdownID.text
    if "Larger than 6MP" not in elem:
        dropdownID.send_keys(Keys.ARROW_DOWN)

dropdownID.send_keys(Keys.ENTER)

submitButton = driver.find_element_by_xpath("html/body/div[1]/div[5]/form/div[5]/div[10]/div[2]/input")
submitButton.send_keys(Keys.SPACE)

### The above code gets user input and searches google images for 4k images (Larger than 6 MP).

# switch windows
driver.switch_to.window(driver.window_handles[-1])
time.sleep(2)

newURL = driver.current_url
print(newURL)

searchPage = driver.get(newURL)
myopener = MyOpener()

#This works!, now I have to get the images to the computer and check if the folder is made. If so, put it in there.

firstCount = 0
urlList = []
while firstCount < 10: # Grabs ten images
    firstCount = firstCount + 1 # Increments the count of the images
    elem = driver.find_element_by_xpath(".//*[@id='rg_s']/div[%s]/div" %firstCount) #targets the area that has the full sized link for the image
    stringGrab = elem.get_attribute('innerHTML') #Grabs the html that contains the image
    result = re.search("""ou":"(.*)","ow""", stringGrab) #Isolates the link of the image from the html
    imageLink = result.group(1)  # Returns image URL
    urlList.append(imageLink) # Adds the imageLink URL to the urlList list
    doesfolderExist(searchTerm)  # Calls the method to find if the model's folder exists and if not, create it.
    imageNumber = numFiles(searchTerm)  # Checks how many files are in that folder and returns the number to name this file
    openLink = myopener.open
    openLink2 = openLink(imageLink).url # This opens the link using fancyurlopener with the new user agent
    myopener.retrieve(openLink2, (ppath + "/" + searchTerm + "/" + searchTerm + " " + "0" + str(imageNumber) + ".jpg"))


driver.close()

driver.quit()













