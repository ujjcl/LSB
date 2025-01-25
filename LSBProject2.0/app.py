from flask import Flask, render_template, request, send_file
from PIL import Image
import os
import hashlib
import random
import math
import numpy as np
import re
from cryptography.fernet import Fernet, InvalidToken
from cryptography.exceptions import InvalidKey

app = Flask(__name__)
app.secret_key = os.urandom(24)

# ------ دوال التشفير ------
def generate_aes_key():
    return Fernet.generate_key()

def encrypt_aes(text, key):
    try:
        cipher = Fernet(key)
        return cipher.encrypt(text.encode())
    except (InvalidKey, ValueError) as e:
        raise ValueError("مفتاح غير صالح!") from e

def decrypt_aes(encrypted_text, key):
    try:
        cipher = Fernet(key)
        return cipher.decrypt(encrypted_text).decode()
    except (InvalidKey, InvalidToken) as e:
        raise ValueError("فشل فك التشفير!") from e

# ------ دوال التوزيع العشوائي ------
def generate_random_positions(key, total_pixels):
    seed = int(hashlib.sha256(key).hexdigest(), 16) % 10**8
    np.random.seed(seed)  # التعديل هنا
    return np.random.permutation(total_pixels)

# ------ دوال قياس الجودة ------
def calculate_psnr_mse(original_path, stego_path):
    try:
        original = np.array(Image.open(original_path).convert('RGB'))
        stego = np.array(Image.open(stego_path).convert('RGB'))
        mse = np.mean((original - stego) ** 2)
        if mse == 0:
            return float('inf'), 0.0
        psnr = 20 * math.log10(255 / math.sqrt(mse))
        return psnr, mse
    except Exception as e:
        return 0, 0

# ------ دوال الإخفاء والاستخراج ------
def embed_text_in_image(image_path, text, key):
    encrypted_data = encrypt_aes(text, key)
    binary_text = ''.join(format(byte, '08b') for byte in encrypted_data)
    binary_text += '1111111111111110'

    img = Image.open(image_path)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    pixels = img.load()
    width, height = img.size
    total_pixels = width * height

    positions = generate_random_positions(key, total_pixels)
    data_index = 0

    for pos in positions:
        if data_index >= len(binary_text):
            break
        x = pos % width
        y = pos // width
        r, g, b = pixels[x, y]

        r = (r & 0xFE) | int(binary_text[data_index])
        data_index += 1
        if data_index < len(binary_text):
            g = (g & 0xFE) | int(binary_text[data_index])
            data_index += 1
        if data_index < len(binary_text):
            b = (b & 0xFE) | int(binary_text[data_index])
            data_index += 1

        pixels[x, y] = (r, g, b)

    output_path = os.path.join('static', 'output', 'encrypted_image.png')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path)
    return output_path

def extract_text_from_image(image_path, key):
    img = Image.open(image_path).convert('RGB')
    width, height = img.size  # التعديل هنا
    total_pixels = width * height

    seed = int(hashlib.sha256(key).hexdigest(), 16) % 10**8
    np.random.seed(seed)
    positions = np.random.permutation(total_pixels)
    
    binary_bits = []
    end_marker = '1111111111111110'
    marker_index = 0
    
    for pos in positions:
        x = pos % width
        y = pos // width
        
        if y >= height or x >= width:
            continue
            
        r, g, b = img.getpixel((x, y))  # التعديل هنا
        
        bits = f"{r&1}{g&1}{b&1}"
        
        for bit in bits:
            if end_marker[marker_index] == bit:
                marker_index += 1
                if marker_index == len(end_marker):
                    encrypted_bytes = bytes(
                        int(''.join(binary_bits[i:i+8]), 2) 
                        for i in range(0, len(binary_bits), 8)
                    )
                    return decrypt_aes(encrypted_bytes, key)
            else:
                marker_index = 0
            binary_bits.append(bit)
    
    raise ValueError("فشل الاستخراج! المفتاح غير صحيح أو الصورة تالفة")

# ------ مسارات التطبيق ------
@app.route('/key')
def generate_key_page():
    # توليد مفتاح جديد
    new_key = Fernet.generate_key().decode()
    
   
    return render_template(
        'key.html',
        key=new_key,
        instruction="احفظ هذا المفتاح في مكان آمن!",
        warning="فقدان المفتاح يعني فقدان البيانات المشفرة إلى الأبد."
    )
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encrypt', methods=['POST'])
def encrypt():
    try:
        image_file = request.files['image']
        text = request.form['text']
        user_key = request.form['key'].encode()
        
        if len(user_key) != 44 or not re.match(r'^[A-Za-z0-9+/=]+$', user_key.decode()):
            return render_template('error.html', message="المفتاح غير صالح!")
        
        uploads_dir = os.path.join('static', 'uploads')
        os.makedirs(uploads_dir, exist_ok=True)
        image_path = os.path.join(uploads_dir, image_file.filename)
        image_file.save(image_path)
        
        encrypted_image_path = embed_text_in_image(image_path, text, user_key)
        psnr, mse = calculate_psnr_mse(image_path, encrypted_image_path)
        
        return render_template('result.html',
                            psnr=f"{psnr:.2f} dB",
                            mse=f"{mse:.4f}",
                            image_path=encrypted_image_path)
    except Exception as e:
        return render_template('error.html', message=str(e))

@app.route('/decrypt', methods=['POST'])
def decrypt():
    try:
        image_file = request.files['image']
        user_key = request.form['key'].encode()
        
        if len(user_key) != 44 or not re.match(r'^[A-Za-z0-9+/=]+$', user_key.decode()):
            return render_template('index.html', error="المفتاح غير صالح!")
        
        uploads_dir = os.path.join('static', 'uploads')
        os.makedirs(uploads_dir, exist_ok=True)
        image_path = os.path.join(uploads_dir, image_file.filename)
        image_file.save(image_path)
        
        extracted_text = extract_text_from_image(image_path, user_key)
        return render_template('index.html', decrypted_text=extracted_text)  # تمرير النص إلى القالب
        
    except Exception as e:
        return render_template('index.html', error=str(e))  # تمرير الخطأ إلى القالب

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)