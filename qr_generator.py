# pip install lxml
# pip3 install requests
# pip3 install beautifulsoup4

from itertools import count
import qrcode
from PIL import ImageDraw
from PIL import ImageFont
import requests
from bs4 import BeautifulSoup

# qr_file = "mkqrcode.png"
# QRimage = qrcode.make(data)
# QRimage.save(qr_file)

# Steps :
# 1 - get data (titles, links, writers)
# order = []
titles = []
writers = []
# countries = []
links = []

def scrap_novels(url):
    site_result = requests.get(url)
    source = site_result.content
    soup = BeautifulSoup(source, "lxml")
    novels_table = soup.find('table', {"class":"wikitable"})
    data = []
    for tr in novels_table.find("tbody").find_all("tr"):
        data.append([td.get_text(strip=True) for td in tr.find_all("td")])

    for tr in novels_table.find("tbody").find_all("tr"):
        for td in tr.find_all("td"):
            if tr.find_all("td").index(td) == 1:
                site_url = 'https://ar.wikipedia.org/'
                links.append(site_url + td.find('a').attrs['href'])
    # print(links)

    for row in data:
        if row:
            # order.append(row[0])
            titles.append(row[1])
            writers.append(row[2])
    generate_qrcode(links,writers,titles)
            # countries.append(row[3])
    # print(writers)
    # print('@@@@@@@@@@')
    # print(titles)
    # print('!!!!!!!!')
    # print(countries)
    # print('$$$$$$$$$$$$$$$')
    # print(links)

# 2 - create image

def create_image(link,writer,title,counter):
    try:
        qr = qrcode.QRCode(box_size=20)
        qr.add_data(link)
        img = qr.make_image()
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("/Library/Fonts/Arial.ttf", 28, encoding="unic")
        draw.text((520,600),title, font=font)
        draw.text((550,600),writer, font=font)
        img_name = str(counter)+".png"
        img.save(img_name)
        return (True,title)
    except Exception:
        raise Exception("Error occured in gen_qrcode func in genqr.py")

def generate_qrcode(links,writers,titles):
    counter = 1
    for link,writer,title in zip(links,writers,titles):
        create_image(link,writer,title,counter)
        counter += 1
        


# 3 - create pdf
# 4 - add image to pdf
# 5 - add title and writer to pdf
# 6 - make image clickable

# def generate_qrcode(url,author,book_name):

#     try:
#         qr = qrcode.QRCode(box_size=20)
#         qr.add_data(url)
#         img = qr.make_image()
#         draw = ImageDraw.Draw(img)
#         font = ImageFont.truetype("/Library/Fonts/Arial.ttf", 28, encoding="unic")
#         draw.text((220,600),book_name, font=font)
#         draw.text((50,600),author, font=font)
#         img.save("plementus_qr.pdf")
#         return (True,book_name)
#     except Exception:
#         raise Exception("Error occured in gen_qrcode func in genqr.py")


# data = "https://plementus.com/"
page_url = "https://ar.wikipedia.org/wiki/%D9%82%D8%A7%D8%A6%D9%85%D8%A9_%D8%A3%D9%81%D8%B6%D9%84_%D9%85%D8%A6%D8%A9_%D8%B1%D9%88%D8%A7%D9%8A%D8%A9_%D8%B9%D8%B1%D8%A8%D9%8A%D8%A9"
# generate_qrcode(data,'Book name', 'Writer')
scrap_novels(page_url)
