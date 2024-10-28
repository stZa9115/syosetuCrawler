from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup
import random
import requests
import pandas as pd
from ebooklib import epub
from IPython.display import clear_output

chNames = []
chLinks = []

driver = webdriver.Chrome()
driver.maximize_window()

driver.get("https://ncode.syosetu.com/n8558fh/")
novelTitle = driver.find_element(By.CLASS_NAME,'p-novel__title')
novelTitle = novelTitle.text
novelAuthor = driver.find_element(By.CLASS_NAME,'p-novel__author')
novelAuthor = novelAuthor.find_element(By.TAG_NAME,'a')
novelAuthor = novelAuthor.text


while(True):
    time.sleep(3)
    chapterDiv = driver.find_element(By.CLASS_NAME, 'p-eplist')
    divs = driver.find_elements(By.TAG_NAME,'div')
    print('Crawling: ', driver.current_url)
    for div in divs:

        if div.get_attribute('class')=='p-eplist__chapter-title':
            #print(div.text)
            chNames.append(div.text)
            chLinks.append('')
            
        elif div.get_attribute('class')=='p-eplist__sublist':
            ch = div.find_element(By.CLASS_NAME,'p-eplist__subtitle')
            #print(ch.text)
            #print('\t',ch.get_attribute('href'))
            chNames.append(ch.text)
            chLinks.append(ch.get_attribute('href'))

        # chapter = driver.find_elements(By.CLASS_NAME,'p-eplist__subtitle')
        # print(ch.text)
        # print('\t',ch.get_attribute('href'))
        # chNames.append(ch.text)
        # chLinks.append(ch.get_attribute('href'))
    
    nextPage = driver.find_element(By.CLASS_NAME,'c-pager__item--next')
    
    if nextPage.tag_name!='a':
        break
    driver.get(nextPage.get_attribute('href'))


chapterTable = pd.DataFrame({
    'Name':chNames,
    'URL':chLinks
})

chapterTable.loc[len(chapterTable),:] = ["",'']

print('章節抓取完成')####
time.sleep(5)

clear_output()####


book = epub.EpubBook()

book.set_identifier("n8558fh")
book.set_title(novelTitle)
book.set_language("jp")
book.add_author(novelAuthor)

chapterList = []
rolling = 1

sectionList = []
firstSection = 1
sectionStart = 0
sectionPart = []

for i in chapterTable.index:
    
    link = chapterTable.loc[i,'URL']
    time.sleep(random.randint(3,8))

    print('catching ',link)
    if link=='':
        if firstSection==1:

            firstSection=0
            sectionStart=i

        else:
            aSection = [epub.Section(chapterTable.loc[sectionStart,'Name']), sectionPart]
            sectionList.append(aSection)

            sectionPart = []
            sectionStart = i
        continue
    stream = ''
    driver.get(link)
    time.sleep(random.randint(5,8))
    textDiv = driver.find_element(By.CLASS_NAME,'p-novel__body')

    content = textDiv.get_attribute('outerHTML')

    chapterText = "<h1>{name}</h1>".format(name=chapterTable.loc[i,'Name'])+content
    
    chapter = epub.EpubHtml(title=chapterTable.loc[i,'Name'], file_name="{}.xhtml".format(str(rolling)), lang="jp")
    chapter.content = chapterText
    rolling+=1

    chapterList.append(chapter)
    book.add_item(chapter)
    sectionPart.append(chapter)

# add default NCX and Nav file

driver.quit()

book.add_item(epub.EpubNcx())
book.add_item(epub.EpubNav())


# define CSS style
style = """
BODY {color: white;}

"""
nav_css = epub.EpubItem(
    uid="style_nav",
    file_name="style/nav.css",
    media_type="text/css",
    content=style,
)

book.toc = (
    #epub.Link("chap_01.xhtml", "Introduction", "intro"),
    sectionList
)

# add CSS file
book.add_item(nav_css)

# basic spine
book.spine = ["nav"]+chapterList

# write to the file
epub.write_epub("{}.epub".format(novelTitle), book, {})