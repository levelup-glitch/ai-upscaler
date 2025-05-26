from flask import Flask, render_template, request, send_file
import os
import uuid
import requests

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

COLAB_API_URL = 'https://your-colab-endpoint.ngrok.io/upscale'  # replace this!

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upscale', methods=['POST'])
def upscale():
    image = request.files['image']
    scale = request.form.get('scale', '2')
    ext = image.filename.split('.')[-1].lower()
    filename = f"{uuid.uuid4()}.{ext}"
    input_path = os.path.join(UPLOAD_FOLDER, filename)
    image.save(input_path)

    with open(input_path, 'rb') as img_file:
        files = {'image': img_file}
        res = requests.post(f"{COLAB_API_URL}?scale={scale}", files=files)

    if res.status_code == 200:
        output_path = os.path.join(OUTPUT_FOLDER, f"upscaled_{uuid.uuid4()}.jpg")
        with open(output_path, 'wb') as f:
            f.write(res.content)
        return send_file(output_path, as_attachment=True)
    else:
        return f"❌ Error from AI backend: {res.text}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
