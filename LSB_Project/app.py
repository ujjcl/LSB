from flask import Flask, render_template, request, send_file
from PIL import Image
import os
from datetime import datetime

app = Flask(__name__)

# استرجاع معلومات المستخدم
def get_user_info():
    user_ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    return {'ip': user_ip, 'user_agent': user_agent}

# تسجيل معلومات المستخدم في ملف مع الطابع الزمني
def log_user_info(info):
    log_file = 'logs.txt'
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # إضافة الوقت
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"[{current_time}] IP: {info['ip']} | User-Agent: {info['user_agent']}\n")

# صفحة اللوق لعرض المعلومات
@app.route('/logs')
def log():
    log_file = 'logs.txt'
    if os.path.exists(log_file):
        with open(log_file, 'r', encoding='utf-8') as f:
            logs = f.readlines()
    else:
        logs = []

    # تنسيق البيانات للعرض
    formatted_logs = []
    for log in logs:
        if '|' in log:
            timestamp, rest = log.split(']', 1)
            ip, user_agent = rest.split('|', 1)
            formatted_logs.append({
                'timestamp': timestamp.strip('['),
                'ip': ip.strip().replace("IP:", ""),
                'user_agent': user_agent.strip().replace("User-Agent:", "")
            })

    return render_template('logs.html', logs=formatted_logs)

@app.route('/')
def index():
    # تسجيل معلومات المستخدم
    user_info = get_user_info()
    log_user_info(user_info)
    return render_template('index.html')




@app.route('/admin')
def admin():
    # قراءة النصوص المخفية من الملف
    if os.path.exists('hidden_texts.txt'):
        with open('hidden_texts.txt', 'r', encoding='utf-8') as f:
            hidden_texts = f.readlines()
    else:
        hidden_texts = []

    return render_template('admin.html', hidden_texts=hidden_texts)


@app.route('/re')
def re():
    return render_template('re.html')

# دالة لإخفاء النص داخل الصورة باستخدام LSB
def embed_text_in_image(image, text):
    # تحويل النص إلى بايتات
    binary_text = ''.join(format(ord(c), '08b') for c in text)
    binary_text += '1111111111111110'  # إضافة بتات النهاية لتمييز نهاية النص

    # فتح الصورة
    img = Image.open(image)
    pixels = img.load()

    width, height = img.size
    data_index = 0

    # التعامل مع كل بيكسل
    for y in range(height):
        for x in range(width):
            if data_index < len(binary_text):
                pixel = pixels[x, y]
                
                # التأكد من أن الصورة تحتوي على 3 قنوات فقط أو 4 قنوات (RGBA)
                if len(pixel) == 3:
                    r, g, b = pixel
                    a = None  # لا يوجد قناة ألفا
                elif len(pixel) == 4:
                    r, g, b, a = pixel
                else:
                    continue  # في حال كان هناك عدد قنوات غير متوقع

                # تعديل البتات الأخيرة في كل من القيم الأحمر والأخضر والأزرق
                r = (r & 0xFE) | int(binary_text[data_index])  # تعديل البت الأخير للـ r
                data_index += 1

                if data_index < len(binary_text):
                    g = (g & 0xFE) | int(binary_text[data_index])  # تعديل البت الأخير للـ g
                    data_index += 1

                if data_index < len(binary_text):
                    b = (b & 0xFE) | int(binary_text[data_index])  # تعديل البت الأخير للـ b
                    data_index += 1

                # إذا كانت الصورة تحتوي على قناة ألفا، لا تعدلها
                if a is not None:
                    pixels[x, y] = (r, g, b, a)
                else:
                    pixels[x, y] = (r, g, b)

    # حفظ الصورة المعدلة
    img.save("output.png")
    return "output.png"

# دالة لاستخراج النص المخفي من الصورة باستخدام LSB
def extract_text_from_image(image):
    img = Image.open(image)
    pixels = img.load()

    width, height = img.size
    binary_text = ''
    
    # التعامل مع كل بيكسل لاستخراج البتات
    for y in range(height):
        for x in range(width):
            pixel = pixels[x, y]

            # التأكد من أن الصورة تحتوي على 3 قنوات فقط أو 4 قنوات (RGBA)
            if len(pixel) == 3:
                r, g, b = pixel
            elif len(pixel) == 4:
                r, g, b, a = pixel
            else:
                continue  # في حال كان هناك عدد قنوات غير متوقع

            binary_text += str(r & 1)
            binary_text += str(g & 1)
            binary_text += str(b & 1)

    # البحث عن نهاية النص
    end_index = binary_text.find('1111111111111110')
    if end_index != -1:
        binary_text = binary_text[:end_index]

    # تحويل البتات إلى نص
    extracted_bytes = [binary_text[i:i+8] for i in range(0, len(binary_text), 8)]
    extracted_text = ''.join(chr(int(byte, 2)) for byte in extracted_bytes)

    return extracted_text


@app.route('/encrypt', methods=['POST'])
def encrypt():
    # التأكد من وجود المجلد "uploads"
    uploads_folder = os.path.join(app.root_path, 'static', 'uploads')
    os.makedirs(uploads_folder, exist_ok=True)

    image_file = request.files['image']
    text = request.form['text']
    image_path = os.path.join(uploads_folder, image_file.filename)
    image_file.save(image_path)

    # إخفاء النص داخل الصورة
    result_image_path = embed_text_in_image(image_path, text)
    return send_file(result_image_path, as_attachment=True)

@app.route('/decrypt', methods=['POST'])
def decrypt():
    # التأكد من وجود المجلد "uploads"
    uploads_folder = os.path.join(app.root_path, 'static', 'uploads')
    os.makedirs(uploads_folder, exist_ok=True)

    image_file = request.files['image']
    image_path = os.path.join(uploads_folder, image_file.filename)
    image_file.save(image_path)

    # استخراج النص المخفي من الصورة
    extracted_text = extract_text_from_image(image_path)

    # حفظ النص المخفي في ملف نصي
    with open('hidden_texts.txt', 'a', encoding='utf-8') as f:
        f.write(extracted_text + '\n')

    return extracted_text


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
