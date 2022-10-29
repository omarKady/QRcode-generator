
import qrcode
from PIL import ImageDraw
from PIL import ImageFont

# qr_file = "mkqrcode.png"
# QRimage = qrcode.make(data)
# QRimage.save(qr_file)

def generate_qrcode(url,author,book_name):

    try:
        qr = qrcode.QRCode(box_size=20)
        qr.add_data(url)
        img = qr.make_image()
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("/Library/Fonts/Arial.ttf", 35, encoding="unic")
        draw.text((550,850),book_name, font=font)
        draw.text((250,850),author, font=font)
        img.save("book5.png")
        return (True,book_name)
    except Exception:
        raise Exception("Error occured in gen_qrcode func in genqr.py")


data = "https://ar.wikipedia.org/wiki/%D8%B4%D8%B1%D9%81_(%D8%B1%D9%88%D8%A7%D9%8A%D8%A9)"
generate_qrcode(data,'صنع الله إبراهيم ','شرف')