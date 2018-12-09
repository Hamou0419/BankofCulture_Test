from selenium import webdriver
from lxml import etree
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
import csv

Destination='花蓮縣'
StarDate='2019/01/15'
EndDate='2019/01/16'
page=1
url='https://www.expedia.com.tw/Hotel-Search?destination={}&startDate={}&endDate={}&rooms=1&adults=2'.format(Destination,StarDate,EndDate)

browser = webdriver.Chrome()
browser.get(url)
while page <=3:
        sleep(10)
        #print (browser.page_source)
        tree=etree.HTML(browser.page_source)
        hotellist=tree.xpath('//article[@data-automation="organic"]/h3')
        price=tree.xpath('//span[@class="actualPrice"]')
        score=[]

        for i in tree.xpath('//div[@class="price-col-1"]'):
                try:
                        score.append(i.xpath('ul/li/span[@aria-hidden="true"]')[0].text)
                except:
                        score.append(None)

        if page==1:
                with open('output.csv', 'w', newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(['','Lowest_Price', 'Rank_Index','Rank_Page', 'Review_Score'])
                        for i in range(0,len(hotellist)):
                                print ([hotellist[i].text , price[i].text.strip() , str(page) , str(i) , score[i]])
                                try:
                                        writer.writerow([hotellist[i].text , price[i].text.strip() , str(page) , str(i) , score[i]])
                                except:
                                        writer.writerow([hotellist[i].text.encode("utf8").decode("cp950", "ignore") , price[i].text.strip() , str(page) , str(i) , score[i]])
        else:
                with open('output.csv', 'a', newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        for i in range(0,len(hotellist)):
                                print ([hotellist[i].text , price[i].text.strip() , str(page) , str(i) , score[i]])
                                try:
                                        writer.writerow([hotellist[i].text , price[i].text.strip() , str(page) , str(i) , score[i]])
                                except:
                                        writer.writerow([hotellist[i].text.encode("utf8").decode("cp950", "ignore") , price[i].text.strip() , str(page) , str(i) , score[i]])

        browser.find_element_by_xpath(u"(.//*[normalize-space(text()) and normalize-space(.)='前往頁數'])[7]/following::button[1]").click()
        page+=1

browser.close()