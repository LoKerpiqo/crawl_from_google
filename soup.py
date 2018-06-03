from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json
import os
import urllib.request
import argparse
import re
import os
import sys
import urllib
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



class Search(object):

    def __init__(self):
        self.server = 'https://www.google.com'
        print('Using server:'+self.server)


    def crawl(self,q,num_img):
        searchterm = q
        browser = webdriver.Chrome('/Users/wuxinheng/Downloads/chromedriver')
        header={'User-Agent':"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36"}
        counter = 0
        succounter = 0
        BaseSavedir = '/Users/wuxinheng/Documents/crawl_data'
        num_page = 10

        for ipage in range(num_page):
            url = 'https://www.google.com.sg/search?q=' + searchterm + '&safe=active&hl=en&source=lnt&tbs=itp%3Aphoto%2Cic%3Acolor%2Ccdr%3A1%2Ccd_min%3A1%2F1%2F' + str(
            2008 + ipage) + '%2Ccd_max%3A1%2F1%2F' + str(2009 + ipage) + '&tbm=isch'
            browser.get(url)
            WebDriverWait(browser, 6000).until(EC.presence_of_element_located((By.XPATH, "//div[@id='searchform']")))
            if not os.path.exists(os.path.join(BaseSavedir, searchterm)):
                os.mkdir(os.path.join(BaseSavedir, searchterm))


#for _ in range(500):
#    browser.execute_script("window.scrollBy(0,10000)")

            for x in browser.find_elements_by_xpath('//div[contains(@class,"rg_meta")]'):
                counter = counter + 1
                print ("Total Count:", counter)
                print ("Succsessful Count:", succounter)
                print ("URL:",json.loads(x.get_attribute('innerHTML'))["ou"])

                img = json.loads(x.get_attribute('innerHTML'))["ou"]
                imgtype = json.loads(x.get_attribute('innerHTML'))["ity"]
                txt_1 = json.loads(x.get_attribute('innerHTML'))['pt']
                txt_2 = json.loads(x.get_attribute('innerHTML'))['s']
                txt = txt_1+txt_2
                try:
        #req = urllib2.Request(img, headers={'User-Agent': header})
        #raw_img = urllib2.urlopen(req).read()

                    req = urllib.request.Request(img,headers=header)
                    with urllib.request.urlopen(req,timeout=10) as response:
                        raw_img = response.read()

                    save_img_file = open(os.path.join(BaseSavedir,searchterm , searchterm + "_" + str(counter) + "." + imgtype), "wb")
                    save_img_file.write(raw_img)
                    save_img_file.close()

                    save_txt_file = os.path.join(BaseSavedir, searchterm,searchterm + "_" + str(counter) +  '.txt')
                    fp = open(save_txt_file, 'wb')
                    fp.write(txt.encode('utf-8'))
                    fp.close()
                    succounter = succounter + 1
                    if succounter >= num_img:
                        break
                except Exception as e:
                    print (e)
            print (succounter, "pictures succesfully downloaded")
            if succounter>=num_img:
                break
        browser.close()
        return



if __name__ == "__main__":
    if len(sys.argv) < 3:
        print ("Usage:")
        print ("\t %s query #images" % ('soup.py',))
        sys.exit(0)

    s = Search()
    q = sys.argv[1]
    num_img = int(sys.argv[2])
    s.crawl(q,num_img)



