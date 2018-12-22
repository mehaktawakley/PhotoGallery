from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import sqlite3 as sql
 
def watermark_text(input_image_path,
                   output_image_path,
                   text):
    photo = Image.open(input_image_path)
    photo.save("static/photos/pics/" + output_image_path)
    # make the image editable
    drawing = ImageDraw.Draw(photo)
 
    black = (3, 8, 12)
    font = ImageFont.load_default()
    drawing.text((0,0), text, fill=black, font=font)
    photo.show()
    PA = "static/photos/pics1/"
    photo.save(PA + output_image_path)
    photo.save(PA + output_image_path)
    con = sql.connect("static/datab.db")
    cur = con.cursor()
    cur.execute("INSERT into photos_photo_table (image_name,image_category,image_tags) VALUES(?,?,?)",(input_image_path[:-4],'People','people'))
    cur.execute("select author from upload_photos where image_name = ?",(input_image_path,))
    a = cur.fetchone()
    a=str(a)
    a=a[2:-3]
    print(a)
    cur.execute("update admin set rewards = rewards + 100 where name = ?",(a,))
    con.commit()
    cur.close()
    con.close()
 
 
if __name__ == '__main__':
    img = 'nature.jpg'
    img1 = 'nature.jpg'
    watermark_text(img, img1,text='PHOTOGALLERY')