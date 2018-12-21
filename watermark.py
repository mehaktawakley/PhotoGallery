from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import sqlite3 as sql
 
def watermark_text(input_image_path,
                   output_image_path,
                   text, pos):
    photo = Image.open(input_image_path)
 
    # make the image editable
    drawing = ImageDraw.Draw(photo)
 
    black = (3, 8, 12)
    font = ImageFont.truetype("Pillow/Tests/fonts/FreeMono.ttf", 40)
    drawing.text(pos, text, fill=black, font=font)
    photo.show()
    photo.save(output_image_path)
    con = sql.connect("static/datab.db")
    cur = con.cursor()
    cur.execute("INSERT into photos_photo_table (image_name,image_category,image_tags) VALUES(?,?,?)",(input_image_path[:-4],'People','people'))
    con.commit()
    cur.close()
    con.close()
 
 
if __name__ == '__main__':
    img = 'Image2.jpg'
    watermark_text(img, 'w.png',
                   text='PHOTOGALLERY',
                   pos=(0, 0))