from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import re
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

SENDER_EMAIL = 'sean.utility.python@gmail.com'
PW = '5r6!4jumwG'


price_form = re.compile("(\$ ?[0-9,]+\.[0-9]{2}|CAD ?[0-9,]+\.[0-9]{2})")
number_form = re.compile("[0-9,]+\.[0-9]{2}")


def getDriver():
    try:
        #options = webdriver.ChromeOptions()    
        #options.add_argument("--headless")
        #options.add_argument("--enable-javascript")
        #driver = webdriver.Chrome('C:\Program Files\ChromeDriver\\temp\chromedriver.exe', options=options)
        chrome_options = webdriver.ChromeOptions() 
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument('--disable-notifications')
        chrome_options.add_argument("--enable-javascript")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Linux; Android 6.0; HTC One M9 Build/MRA58K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.98 Mobile Safari/537.36")
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
        #driver.implicitly_wait(5)
        return driver
    except Exception as err:
        print("Error reached " + str(err))
        return None

def send_email(receiver_name, receiver, item_name ,site ,url ,sale_price , old_price):
    print("\n\n\n\nSending email\n\n\n\n")
    msg = MIMEMultipart()
    msg['Subject'] = item_name + ' is on sale for $' + str(sale_price)
    msg['From'] = SENDER_EMAIL
    msg['To'] = receiver

    content = "Hi " + receiver_name + ",\n\n"
    content += receiver_name + " is now on sale at " + site + ". You asked for me to alert you when the price drops below "
    content += "$" + str(old_price) + " and it is now on sale for $" + str(sale_price) + ".\n\n"
    content += "You can access it here: " + url + "\n\n"
    content += "Remember that you may need to access it through an icognito window to view the sale price.\n\n"
    content += "Happy Shopping!"
    text = MIMEText(content)
    msg.attach(text)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(SENDER_EMAIL, PW)
        server.sendmail(SENDER_EMAIL, receiver, msg.as_string())



class Checker():
    def __init__(self):
        self.driver = getDriver()

    def check(self, f_item_name, f_min_price, f_receiver_name,f_receiver, urls):
        i = 0
        emailSent = False
        l_price = f_min_price
        for url in urls:
            self.driver.get(url[0])
            price = float(number_form.findall(price_form.findall(self.driver.page_source)[0])[0])
            if price < l_price:
                from_site = url[1]
                e_url = url[0]
                l_price = price
            i += 1

        if l_price < f_min_price:
            emailSent = True
            e_price = l_price
            send_email(f_receiver_name,f_receiver, f_item_name ,from_site ,e_url ,e_price , f_min_price)
        
            return e_price, emailSent, from_site, e_url
        return None
    
    def closeDriver(self):
        self.driver.quit()
