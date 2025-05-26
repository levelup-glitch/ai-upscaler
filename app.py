from flask import Flask, render_template, request, send_file
import os
from PIL import Image
import uuid

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upscale', methods=['POST'])
def upscale():
    file = request.files['image']
    scale = int(request.form.get('scale', 2))
    ext = file.filename.split('.')[-1].lower()

    if ext not in ['jpg', 'jpeg', 'png', 'webp', 'bmp', 'tiff']:
        return "❌ Unsupported image format", 400

    input_path = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4()}.{ext}")
    file.save(input_path)

    img = Image.open(input_path).convert("RGB")

    # Basic upscale using Pillow (for simple deployment)
    width, height = img.size
    new_size = (width * scale, height * scale)
    upscaled_img = img.resize(new_size, Image.BICUBIC)

    output_path = os.path.join(OUTPUT_FOLDER, f"upscaled_{uuid.uuid4()}.jpg")
    upscaled_img.save(output_path)

    return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
