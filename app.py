from flask import Flask
from flask import request
from flask import send_file
from flask import render_template
import os.path
import PIL
import PIL.Image
import random
from io import BytesIO

app = Flask(__name__)

@app.route("/")
def index():
  return render_template('index.html')

@app.route('/post', methods=['POST'])
def process_file():
    if request.method == 'POST':
        f = request.files['file']
        img_io = BytesIO()
        add_watermark(PIL.Image.open(f)).save(img_io, 'PNG')
        img_io.seek(0)
        return send_file(img_io, mimetype='image/png')

def add_watermark(original_image):
    width, height = original_image.size
    
    watermark = PIL.Image.open(os.path.join(os.getcwd(), 'watermark1.png'))
    w_size = int(min(width, height) / 4)
    watermark = watermark.resize((w_size, w_size))
    
    watermark2 = PIL.Image.open(os.path.join(os.getcwd(), 'watermark2.png'))
    w_size2 = int(min(width, height) / 4)
    watermark2 = watermark2.resize((w_size2, w_size2))

    for i in range(0, 8):
      original_image.paste(watermark, (random.randint(0, width - w_size), random.randint(0, height - w_size)), watermark)

    for i in range(0, 8):
      original_image.paste(watermark2, (random.randint(0, width - w_size), random.randint(0, height - w_size)), watermark2)
    
    return original_image

# filename = input('Filename: ')
# add_watermark(PIL.Image.open(os.path.join(os.getcwd(), filename + '.png'))).save(filename + '1.png')