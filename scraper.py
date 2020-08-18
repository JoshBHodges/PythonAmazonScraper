import requests
from bs4 import BeautifulSoup
import smtplib
import time
import sys

URL = sys.argv[1] if len(sys.argv) > 1 else "https://smile.amazon.co.uk/dp/B0078LENZC/ref=cm_sw_r_tw_dp_x_M9PoFbXY02VTW"

headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'}


def check_price():
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'lxml')

    price = soup.find(id='priceblock_ourprice').get_text()
    converted_price = float(price[1:6])

    if converted_price < float(sys.argv[2] if len(sys.argv) > 2 else 0):
        send_mail()


def send_mail():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login((sys.argv[3] if len(sys.argv) > 3 else 0), (sys.argv[4] if len(sys.argv) > 4 else 0))

    subject = 'Price fell down!'
    body = 'Check Amazon link https://smile.amazon.co.uk/dp/B0078LENZC/ref=cm_sw_r_tw_dp_x_M9PoFbXY02VTW'

    msg = f'Subject: {subject}\n\n{body}'

    server.sendmail(
        (sys.argv[3] if len(sys.argv) > 3 else 0),
        (sys.argv[3] if len(sys.argv) > 3 else 0),
        msg
    )
    print('Email has been sent')
    server.quit()


while True:
    check_price()
    time.sleep(60*60*24)
