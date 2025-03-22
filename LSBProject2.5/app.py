"""
تطبيق ويب لإخفاء النصوص المشفرة داخل الصور باستخدام تقنية LSB مع تعزيز الأمان بالتشفير AES.
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_from_directory
from PIL import Image
import os
import hashlib
import random
import math
import numpy as np
import re
from cryptography.fernet import Fernet, InvalidToken
from cryptography.exceptions import InvalidKey
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
import time
from threading import Thread
import uuid  # لإنتاج أسماء فريدة للملفات

# تهيئة التطبيق
app = Flask(__name__)
app.secret_key = os.urandom(24)  # مفتاح سري عشوائي لتأمين الجلسات

# إعدادات الملفات
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')  # مجلد تحميل الصور
app.config['OUTPUT_FOLDER'] = os.path.join('static', 'output')  # مجلد حفظ الصور المشفرة
app.config['ALLOWED_IMAGE_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'bmp'}  # أنواع الملفات المسموحة
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # الحد الأقصى لحجم الملف (16MB)

# إعداد قاعدة البيانات
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'keys.db')  # قاعدة بيانات SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)  # تهيئة SQLAlchemy لإدارة قاعدة البيانات

# نموذج مفتاح التشفير
class EncryptionKey(db.Model):
    """
    نموذج قاعدة البيانات لحفظ مفاتيح التشفير.
    """
    id = db.Column(db.Integer, primary_key=True)  # معرف فريد للمفتاح
    key_value = db.Column(db.String(100), nullable=False, unique=True)  # قيمة المفتاح
    label = db.Column(db.String(100), nullable=True)  # تسمية اختيارية للمفتاح
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # تاريخ إنشاء المفتاح

    def __repr__(self):
        return f"<EncryptionKey {self.key_value}>"

# ------ دوال التشفير ------
def generate_aes_key():
    """
    توليد مفتاح AES عشوائي.
    :return: مفتاح AES (بايتس)
    """
    return Fernet.generate_key()

def encrypt_aes(text, key):
    """
    تشفير النص باستخدام مفتاح AES.
    :param text: النص المراد تشفيره
    :param key: مفتاح التشفير
    :return: النص المشفر (بايتس)
    """
    try:
        cipher = Fernet(key)
        return cipher.encrypt(text.encode())
    except (InvalidKey, ValueError) as e:
        raise ValueError("مفتاح غير صالح!") from e

def decrypt_aes(encrypted_text, key):
    """
    فك تشفير النص باستخدام مفتاح AES.
    :param encrypted_text: النص المشفر
    :param key: مفتاح التشفير
    :return: النص الأصلي (سلسلة نصية)
    """
    try:
        cipher = Fernet(key)
        return cipher.decrypt(encrypted_text).decode()
    except (InvalidKey, InvalidToken) as e:
        raise ValueError("فشل فك التشفير!") from e

# ------ دوال التوزيع العشوائي ------
def generate_random_positions(key, total_pixels):
    """
    توليد مواضع عشوائية للبكسلات بناءً على المفتاح.
    :param key: مفتاح التشفير
    :param total_pixels: عدد البكسلات الكلي في الصورة
    :return: مصفوفة تحتوي على مواضع عشوائية
    """
    seed = int(hashlib.sha256(key).hexdigest(), 16) % 10**8
    np.random.seed(seed)
    return np.random.permutation(total_pixels)

# ------ دوال قياس الجودة ------
def calculate_psnr_mse(original_path, stego_path):
    """
    حساب PSNR وMSE بين الصورة الأصلية والصورة المشفرة.
    :param original_path: مسار الصورة الأصلية
    :param stego_path: مسار الصورة المشفرة
    :return: قيم PSNR وMSE
    """
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
    """
    إخفاء النص المشفر داخل الصورة باستخدام تقنية LSB.
    :param image_path: مسار الصورة الأصلية
    :param text: النص السري
    :param key: مفتاح التشفير
    :return: مسار الصورة المشفرة (باسم فريد)
    """
    encrypted_data = encrypt_aes(text, key)  # تشفير النص
    binary_text = ''.join(format(byte, '08b') for byte in encrypted_data)  # تحويل النص المشفر إلى ثنائي
    binary_text += '1111111111111110'  # إضافة علامة نهاية النص

    img = Image.open(image_path)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    pixels = img.load()
    width, height = img.size
    total_pixels = width * height

    positions = generate_random_positions(key, total_pixels)  # توليد مواضع عشوائية
    data_index = 0

    for pos in positions:
        if data_index >= len(binary_text):
            break
        x = pos % width
        y = pos // width
        r, g, b = pixels[x, y]

        # تعديل البت الأقل أهمية (LSB)
        r = (r & 0xFE) | int(binary_text[data_index])
        data_index += 1
        if data_index < len(binary_text):
            g = (g & 0xFE) | int(binary_text[data_index])
            data_index += 1
        if data_index < len(binary_text):
            b = (b & 0xFE) | int(binary_text[data_index])
            data_index += 1

        pixels[x, y] = (r, g, b)

    # توليد اسم ملف فريد للصورة المشفرة
    unique_filename = f"encrypted_{uuid.uuid4().hex}.png"
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], unique_filename)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path)
    return output_path

def extract_text_from_image(image_path, key):
    """
    استخراج النص المشفر من الصورة.
    :param image_path: مسار الصورة المشفرة
    :param key: مفتاح التشفير
    :return: النص الأصلي
    """
    img = Image.open(image_path).convert('RGB')
    width, height = img.size
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
            
        r, g, b = img.getpixel((x, y))
        
        bits = f"{r&1}{g&1}{b&1}"
        
        for bit in bits:
            if end_marker[marker_index] == bit:
                marker_index += 1
                if marker_index == len(end_marker):
                    valid_bits = ''.join(binary_bits)[:-len(end_marker)]
                    encrypted_bytes = bytes(
                        int(valid_bits[i:i+8], 2) 
                        for i in range(0, len(valid_bits), 8)
                    )
                    return decrypt_aes(encrypted_bytes, key)
            else:
                marker_index = 0
            binary_bits.append(bit)
    
    raise ValueError("فشل الاستخراج! المفتاح غير صحيح أو الصورة تالفة")

# ------ دوال مساعدة ------
def allowed_image(filename):
    """
    التحقق من أن الملف مسموح به بناءً على الامتداد.
    :param filename: اسم الملف
    :return: True إذا كان الملف مسموحًا به، False إذا لم يكن كذلك
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_IMAGE_EXTENSIONS']

def create_folders():
    """
    إنشاء المجلدات اللازمة إذا لم تكن موجودة.
    """
    try:
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)
    except Exception as e:
        raise RuntimeError(f"فشل إنشاء المجلدات: {str(e)}")

# ------ مسارات التطبيق ------

@app.route('/api/generate_key', methods=['GET'])
def api_generate_key():
    """
    نقطة نهاية API لتوليد مفتاح Fernet جديد.
    """
    try:
        # توليد مفتاح حتى يصبح خالياً من الرموز غير المرغوبة
        valid = False
        while not valid:
            new_key = Fernet.generate_key().decode()
            # التحقق من عدم وجود _ أو -
            if '_' not in new_key and '-' not in new_key:
                valid = True
        
        return jsonify({
            'success': True,
            'key': new_key
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/share')
def share_page():
    image_path = request.args.get('img')
    if not image_path:
        return redirect(url_for('index'))
    
    # إنشاء رابط دائم للصورة
    base_url = request.host_url  # الحصول على عنوان الموقع الأساسي تلقائياً
    image_url = f"{base_url}{image_path.lstrip('./')}"
    
    return render_template('share.html', 
                           image_path=image_url,
                           page_url=request.url)

@app.route('/manifest.webmanifest')
def manifest():
    return send_from_directory('static', 'manifest.webmanifest')

@app.route('/service-worker.js')
def service_worker():
    return send_from_directory('.', 'service-worker.js')

@app.route('/instructions')
def instructions():
    """صفحة التعليمات"""
    return render_template('instructions.html')

@app.route('/')
def index():
    """
    الصفحة الرئيسية للتطبيق.
    """
    return render_template('index.html')

@app.route('/key', methods=['GET', 'POST'])
def generate_key_page():
    if request.method == 'POST':
        label = request.form.get('label', '')
        # توليد مفتاح حتى يصبح خالياً من الرموز غير المرغوبة
        valid = False
        while not valid:
            new_key = Fernet.generate_key().decode()
            # التحقق من عدم وجود _ أو -
            if '_' not in new_key and '-' not in new_key:
                valid = True
        
        key_entry = EncryptionKey(key_value=new_key, label=label)
        db.session.add(key_entry)
        db.session.commit()
        flash("تم توليد المفتاح وحفظه بنجاح!", "success")
        return redirect(url_for('manage_keys'))
    
    # توليد مفتاح مؤقت للعرض (مع التحقق)
    temp_key = Fernet.generate_key().decode()
    while '_' in temp_key or '-' in temp_key:
        temp_key = Fernet.generate_key().decode()
    
    return render_template(
        'key.html',
        key=temp_key,
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        instruction2="احفظ هذا المفتاح في مكان آمن!",
        warning="فقدان المفتاح يعني فقدان البيانات المشفرة إلى الأبد."
    )

@app.route('/manage_keys')
def manage_keys():
    """
    صفحة إدارة المفاتيح.
    """
    keys = EncryptionKey.query.order_by(EncryptionKey.created_at.desc()).all()
    return render_template('manage_keys.html', keys=keys)

@app.route('/delete_key/<int:key_id>', methods=['POST'])
def delete_key(key_id):
    """
    حذف مفتاح معين.
    """
    key_entry = EncryptionKey.query.get_or_404(key_id)
    db.session.delete(key_entry)
    db.session.commit()
    flash("تم حذف المفتاح بنجاح!", "info")
    return redirect(url_for('manage_keys'))

@app.route('/encrypt', methods=['POST'])
def encrypt_route():
    """
    معالجة طلب التشفير.
    """
    try:
        create_folders()

        if 'image' not in request.files:
            raise ValueError("لم يتم اختيار صورة")
        
        image_file = request.files['image']
        if image_file.filename == '':
            raise ValueError("لم يتم اختيار صورة")
        
        original_filename = secure_filename(image_file.filename)
        if not original_filename:
            raise ValueError("اسم الملف غير صالح")
        
        if not allowed_image(original_filename):
            raise ValueError("نوع الملف غير مدعوم. يُسمح بالصيغ: PNG, JPG, JPEG, BMP")
        
        # الحصول على النص السري سواء من ملف أو من حقل نصي
        text = ''
        if 'secret_file' in request.files:
            secret_file = request.files['secret_file']
            if secret_file.filename != '':
                if not secret_file.filename.endswith('.txt'):
                    raise ValueError("يجب أن يكون الملف السري من نوع TXT")
                text = secret_file.read().decode('utf-8')
        
        if not text:
            text = request.form.get('text', '')
            if not text.strip():
                raise ValueError("النص السري فارغ")
        
        # التحقق من صحة المفتاح
        user_key = request.form.get('key', '').encode()
        if len(user_key) != 44 or not re.match(r'^[A-Za-z0-9+/=]+$', user_key.decode()):
            raise ValueError("المفتاح غير صالح")
        
        # حفظ الصورة المرفوعة مع اسم آمن
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], original_filename)
        image_file.save(image_path)
        
        # تنفيذ عملية الإخفاء باستخدام دالة embed_text_in_image
        encrypted_image_path = embed_text_in_image(image_path, text, user_key)
        
        # حساب مؤشرات الجودة للصورة
        psnr, mse = calculate_psnr_mse(image_path, encrypted_image_path)
        
        with Image.open(encrypted_image_path) as img:
            width, height = img.size
            resolution = f"{width}x{height}"
        
        file_size_bytes = os.path.getsize(encrypted_image_path)
        file_size = f"{file_size_bytes / 1024:.2f} KB"
        file_format = os.path.splitext(encrypted_image_path)[1][1:].upper()
        
        return render_template('result.html',
                               psnr=f"{psnr:.2f} dB",
                               mse=f"{mse:.4f}",
                               image_path=encrypted_image_path,
                               file_format=file_format,
                               resolution=resolution,
                               file_size=file_size,
                               timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    except Exception as e:
        return render_template('error.html', message=str(e))

@app.route('/decrypt', methods=['POST'])
def decrypt_route():
    try:
        create_folders()
        
        if 'image' not in request.files:
            raise ValueError("لم يتم اختيار صورة")
        
        image_file = request.files['image']
        if image_file.filename == '':
            raise ValueError("لم يتم اختيار صورة")
        
        original_filename = secure_filename(image_file.filename)
        if not original_filename:
            raise ValueError("اسم الملف غير صالح")
        
        if not allowed_image(original_filename):
            raise ValueError("نوع الملف غير مدعوم. يُسمح بالصيغ: PNG, JPG, JPEG, BMP")
        
        user_key = request.form.get('key', '').encode()
        if len(user_key) != 44 or not re.match(r'^[A-Za-z0-9+/=]+$', user_key.decode()):
            raise ValueError("المفتاح غير صالح. يجب أن يكون مفتاح Fernet صالحًا (44 حرف base64)")
        
        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], 'temp_' + original_filename)
        image_file.save(temp_path)
        
        extracted_text = extract_text_from_image(temp_path, user_key)
        
        try:
            os.remove(temp_path)
        except Exception as e:
            app.logger.error(f"فشل حذف الملف المؤقت: {str(e)}")
        
        return jsonify({
            'success': True,
            'decrypted_text': extracted_text,
            'error': None
        })
        
    except Exception as e:
        if 'temp_path' in locals() and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception as delete_error:
                app.logger.error(f"فشل حذف الملف المؤقت: {str(delete_error)}")
        
        return jsonify({
            'success': False,
            'decrypted_text': None,
            'error': f'خطأ في فك التشفير: {str(e)}'
        }), 400

# ------ وظيفة الحذف التلقائي ------
def delete_old_files():
    """حذف الملفات القديمة كل 24 ساعة"""
    while True:
        try:
            folders = [app.config['UPLOAD_FOLDER'], app.config['OUTPUT_FOLDER']]
            
            for folder in folders:
                if not os.path.exists(folder):
                    continue
                
                time_threshold = datetime.now() - timedelta(hours=24)
                
                for filename in os.listdir(folder):
                    file_path = os.path.join(folder, filename)
                    
                    if filename.startswith('.') or os.path.isdir(file_path):
                        continue
                    
                    file_mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
                    
                    if file_mtime < time_threshold:
                        os.remove(file_path)
                        print(f"تم حذف الملف: {file_path}")
        
        except Exception as e:
            print(f"خطأ أثناء الحذف التلقائي: {str(e)}")
        
        time.sleep(3600)

# ------ تهيئة التطبيق ------
if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)
    
    Thread(target=delete_old_files, daemon=True).start()
    
    port = int(os.environ.get("PORT", 5000))
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=port)
