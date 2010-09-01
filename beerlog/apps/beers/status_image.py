import os
import Image, ImageDraw, ImageFont

CURRENT_DIR = os.path.dirname(__file__)

def status_image(text):
    img = Image.new('RGB', (300, 20), '#E2FC98')
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(CURRENT_DIR + '/fonts/ArialBold.ttf', 15)
    draw.text((1,1), text, font=font, fill="#4B5C77")
    text_width = draw.textsize(text, font=font)
    img = img.crop((0,0,text_width[0]+1,20))
    
    return img