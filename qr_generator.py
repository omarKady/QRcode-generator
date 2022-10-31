# pip install lxml
# pip3 install requests
# pip3 install beautifulsoup4
# pip install reportlab
# pip install arabic_reshaper
# pip install python-bidi


from itertools import count
import qrcode
from PIL import ImageDraw
from PIL import ImageFont
import requests
from bs4 import BeautifulSoup
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import arabic_reshaper
from bidi.algorithm import get_display
pdfmetrics.registerFont(TTFont('Arabic', '/home/omar/Desktop/qr/lib/python3.8/site-packages/reportlab/fonts/alfont_com_AlFont_com_4_CA.ttf'))
# pdfmetrics.registerFont(TTFont('Arabic', '/home/omar/Desktop/qr/lib/python3.8/site-packages/reportlab/fonts/alfont_com_2.otf'))

from reportlab.lib.utils import ImageReader


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

# def create_image(link,writer,title,counter):
#     try:
#         qr = qrcode.QRCode(box_size=20)
#         qr.add_data(link)
#         img = qr.make_image()
#         # draw = ImageDraw.Draw(img)
#         # font = ImageFont.truetype("/Library/Fonts/Arial.ttf", 28, encoding="unic")
#         # draw.text((520,800),'https://ar.wikipedia.org/wiki/%D8%A7%D9%84%D8%AB%D9%84%D8%A7%D8%AB%D9%8A%D8%A9_(%D9%86%D8%AC%D9%8A%D8%A8_%D9%85%D8%AD%D9%81%D9%88%D8%B8)', font=font)
#         # draw.text((550,900),writer, font=font)
#         img_name = str(counter)+".png"
#         img.save(img_name)
#         return (True,title)
#     except Exception:
#         raise Exception("Error occured in gen_qrcode func in genqr.py")

def generate_qrcode(links,writers,titles):
    images_list = []
    counter = 1
    for link,writer,title in zip(links,writers,titles):
        # create_image(link,writer,title,counter)
        try:
            qr = qrcode.QRCode(box_size=20)
            qr.add_data(link)
            img = qr.make_image()
            img_name = str(counter)+".png"
            # img.save(img_name)
            images_list.append(img)
            create_pdf(link,img,writer,title,counter)
            # return (True,title)
            counter += 1
        except Exception:
            raise Exception("Error occured in gen_qrcode func in genqr.py")
    #print('##########')
    #print(images_list)


# 3 - create pdf
# 4 - add image to pdf
# 5 - add title and writer to pdf
def create_pdf(link,img,writer,title,counter):
    arabic_title = f'{title}'
    arabic_writer = f'{writer}'
    # arabic_text = f'{title}- {writer}'
    rehaped_text = arabic_reshaper.reshape(arabic_title)
    rehaped_writer = arabic_reshaper.reshape(arabic_writer)
    # bidi_text = get_display(rehaped_text)
    pdf_name = f'{counter}--{writer}-{title}.pdf'
    my_canvas = canvas.Canvas(pdf_name)
    ar = arabic_reshaper.reshape(rehaped_text)
    ar_writer = arabic_reshaper.reshape(rehaped_writer)
    ar = get_display(ar)
    ar_writer = get_display(ar_writer)
    my_canvas.setFont('Arabic', 17)
    my_canvas.drawString(200, 750, ar)
    my_canvas.drawString(200, 700, ar_writer)
    x_start = 100
    y_start = 200
    pil_img = ImageReader(img.get_image())
    my_canvas.drawImage(pil_img , x_start, y_start, width=400, height=400)
    my_canvas.save()

# 6 - make image clickable

page_url = "https://ar.wikipedia.org/wiki/%D9%82%D8%A7%D8%A6%D9%85%D8%A9_%D8%A3%D9%81%D8%B6%D9%84_%D9%85%D8%A6%D8%A9_%D8%B1%D9%88%D8%A7%D9%8A%D8%A9_%D8%B9%D8%B1%D8%A8%D9%8A%D8%A9"
# generate_qrcode(data,'Book name', 'Writer')
scrap_novels(page_url)
