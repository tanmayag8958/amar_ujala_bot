from __future__ import print_function
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from datetime import date
import time
from PIL import Image
from io import BytesIO
import smtplib

from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders


def deal_scrape():

    src = []

    today = date.today()
    d = today.strftime("%d/%m/%Y")
    d1 = d.split('/')

    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.implicitly_wait(5)
    driver.get(f"https://epaper.amarujala.com/")
    # driver.find_element_by_link_text("लॉग-इन करें").click()

    # username = driver.find_element_by_xpath('//*[@id="login-form"]/input[1]')
    # username.send_keys("email")

    # password = driver.find_element_by_xpath('//*[@id="login-form"]/input[2]')
    # password.send_keys("password")

    # driver.find_element_by_xpath('//*[@id="login-form"]/input[3]').click()

    time.sleep(5)

    driver.get(f"https://epaper.amarujala.com/haldwani/{d1[2]}{d1[1]}{d1[0]}/01.html?format=img&ed_code=haldwani")
    pages = Select(driver.find_element_by_xpath('//*[@id="select-pageno"]'))
    count = len(pages.options)
    print(count)

    for i in range(1, count+1):
        if i > 9:
            driver.get(f"https://epaper.amarujala.com/haldwani/{d1[2]}{d1[1]}{d1[0]}/{i}.html?format=img&ed_code=haldwani")
        else:
            driver.get(f"https://epaper.amarujala.com/haldwani/{d1[2]}{d1[1]}{d1[0]}/0{i}.html?format=img&ed_code=haldwani")
        img = driver.find_element_by_xpath('//*[@id="cropbox"]')
        src.append(img.get_attribute('src'))

    response = requests.get(src[0])
    image = Image.open(BytesIO(response.content))
    im1 = image.convert('RGB')

    imageList = []
    for i in range(1,count):
        response = requests.get(src[i])
        image = Image.open(BytesIO(response.content))
        im = image.convert('RGB')
        imageList.append(im)

    im1.save(r'.\amar_ujala_papers\amar_ujala.pdf',save_all=True, append_images=imageList)


def send_email():
    today = date.today()
    d = today.strftime("%d/%m/%Y")

    msg = MIMEMultipart()

    msg['From'] = "email"
    msg['To'] = "email"
    msg['Subject'] = f"Amar Ujala {d}"
    body = f"Amar Ujala {d}"
    msg.attach(MIMEText(body, 'plain'))

    filename = f"amar_ujala_{d}.pdf"
    attachment = open(r'.\amar_ujala_papers\amar_ujala.pdf', "rb")

    p = MIMEBase('application', 'octet-stream')

    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(p)

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("email", "password")
    text = msg.as_string()
    s.sendmail("email", "email", text)
    s.quit()
    

deal_scrape()
# send_email()
