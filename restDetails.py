# Import neccesary libraries

from selenium import webdriver  # driver to control chrome browser
import pyautogui
from bs4 import BeautifulSoup  # to parse the html code
import threading  # to do multi threding
import time
import pandas as pd  # to store data in csv file

# enter the filename

print("Enter the filename")  # filename to store data
filename = str(input())

# intiate the chrome webdriver instance
browser = webdriver.Chrome()  # chrome instance
record = []
e = []


def Selenium_extractor():
    time.sleep(2)
    a = browser.find_elements_by_class_name("VkpGBb")
    print(len(a))
    time.sleep(1)
    for i in range(len(a)):
        a[i].click()
        time.sleep(2)
        source = browser.page_source
        # Beautiful soup for scraping the html source
        soup = BeautifulSoup(source, 'html.parser')
        try:
            Name_Html = soup.findAll('div', {"class": "SPZz6b"})

            name = Name_Html[0].text
            if name not in e:
                e.append(name)
                print(name)
                Phone_Html = soup.findAll('span', {"class": "LrzXr zdqRlf kno-fv"})
                phone = Phone_Html[0].text
                print(phone)

                Address_Html = soup.findAll('span', {"class": "LrzXr"})
                # print(Address_Html)

                # Service_Html = soup.findAll('div', {"class": "wDYxhc NFQFxe"})
                # print(Service_Html)
                # service = Service_Html[0].text
                # if len(service) > 16 :
                #     service = service[16:]

                # print(service)

                properties = soup.findAll('div', {"class": "wDYxhc NFQFxe"})
                menu_idx = -1
                order_idx = -1
                service_idx = -1
                service = ""
                menu_arr = []
                order_arr=[]
                for x in range(len(properties)):
                    # print(menu[x].text)
                    if properties[x].text.startswith("Menu:"):
                        menu_idx = x
                    elif properties[x].text.startswith("Order:"):
                        order_idx = x
                    elif properties[x].text.startswith("Service options"):
                        service_idx = x

                if service_idx != -1:
                    service = properties[service_idx].text
                    if len(service) > 16:
                        service = service[16:]


                # print(menu_idx)
                if menu_idx != -1:
                    menu_res = properties[menu_idx].findAll('a')
                    for j in range(len(menu_res)):
                        menu_url = menu_res[j].get('href')
                        # print(menu_url)
                        menu_arr.append(menu_url)
                if order_idx != -1:
                    order_res = properties[order_idx].findAll('a')
                    for j in range(len(order_res)):
                        order_arr.append(order_res[j].get('href'))





                # print(menu_res[0].get('href'))


                # print(menu[0].text)
                # print(menu[1].text)



                # order = soup.findAll('div', {"class": "wDYxhc NFQFxe"})
                # order[0].findAll('a')
                # orders = order[0].get('href')
                # print(orders)

                address = Address_Html[0].text
                # print(address)
                try:
                    Website_Html = soup.findAll('div', {"class": "QqG1Sd"})
                    web = Website_Html[0].findAll('a')

                    website = web[0].get('href')
                except:
                    website = "Not available"
                # print(website)
                record.append((name, service, phone, address, website, menu_arr, order_arr))
                df = pd.DataFrame(record,
                                  columns=['Name', 'Service', 'Phone number', 'Address',
                                           'Website', 'Menu', 'Order'])  # writing data to the file
                df.to_csv(filename + '.csv', index=False, encoding='utf-8')

        except:
            print("error")
            continue

    try:
        time.sleep(2)
        next_button = browser.find_element_by_id("pnnext")  # clicking the next button
        next_button.click()
        browser.implicitly_wait(5)
        time.sleep(10)
        Selenium_extractor()
    except:
        print("ERROR occured at clicking net button")


print("Enter the link of the page")
base_url = "https://www.google.com/search?tbs=lf:1,lf_ui:9&tbm=lcl&q=restaurants+"
location_list = ['Bekok']
for val in location_list:
    link = base_url + val
    print(link)
    browser.get(str(link))
    time.sleep(10)  # pausing the program for 10 secs
    Selenium_extractor()

# link = input()

