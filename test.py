import re
from playwright.sync_api import sync_playwright 
import requests
import time
new_list = []
old_list = []
change_ent = []
while(True):
    print("After 1 Minute Running Start")
    with sync_playwright() as p:

        # Get Value from User for Price and Store here
        BASE_URL = "https://api.telegram.org/bot7821071523:AAH4T1ZlXLSoltjSF0ep89r1sjB97InuUqA/getUpdates"
        res = requests.get(BASE_URL)
        priceThreshold = res.json()['result'][-1]['message']['text']
        
        priceThreshold =str(priceThreshold)
        print(priceThreshold)
        tell = f"https://api.telegram.org/bot7821071523:AAH4T1ZlXLSoltjSF0ep89r1sjB97InuUqA/sendMessage?chat_id=6780967733&text={priceThreshold}"
        requests.get(tell)
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(f"https://collect.fifa.com/marketplace?priceHigh={priceThreshold}00&tags=right-to-buy")
        
        page.wait_for_load_state('networkidle')

        titles = page.locator(".browse-collectible-item_title__dgUCS").all()
        links = page.locator(".browse-collectible-item_root__4t9EB").all()
        price = page.locator(".browse-collectible-item_priceStartingAt__RAz61").all()
        
        i = 0
        for t in titles:
            tt = str(t.inner_text())
            l = links[i].get_attribute('href')
            p = price[i].inner_text() 
            if "2025" not in tt and tt != "":
                print("here",tt)
                if(p <= priceThreshold):
                    message = f"{p} , {tt} , https://collect.fifa.com{l}"
                    new_list.append(message)

            i = i+1
        print("appends are done data should be in new list which is scrapped")

        def compare(old,new):
            print(new)
            print("Comparing thje old and new data now")
            res = [x for x in new if x not in old]
            if(res): #not equal means
                #send this res as message
                print(res)
                return res
            else:
                return False
        print("starting Compare")
        change_ent = compare(old_list,new_list)
        print("I have now new Notifi Products")
        print(change_ent)
        if(change_ent != False):
            for g in change_ent:
                print("sending Product info",g)
                #lichi URL
                base = f"https://api.telegram.org/bot7821071523:AAH4T1ZlXLSoltjSF0ep89r1sjB97InuUqA/sendMessage?chat_id=6780967733&text={g}"
                #my url
                #base = f"https://api.telegram.org/bot7163422787:AAE5zvdjSy3gzyCfDF84eFfG05ZyUUNr0xo/sendMessage?chat_id=8068882175&text={g}"
                requests.get(base) #send msg
                time.sleep(2) #wait so no spamming 
        old_list = list(new_list) #add all new entries into old one
        print("Lets sleep for 1 mint Now")
        browser.close()
        time.sleep(60)

