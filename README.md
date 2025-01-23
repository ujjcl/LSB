# **LSB**

This is a web application built with **Flask** that utilizes **Steganography** techniques to hide and extract text within images. The app works by manipulating the least significant bits (LSB) of the image’s pixel data, embedding the message you want to hide. Additionally, the app logs user information (like IP address and User-Agent) and allows an admin to view extracted texts from hidden messages.

### **Features:**
1. **Hide Text in Image (Steganography)**
   - Upload an image, provide a text message, and the text will be embedded into the image's least significant bits (LSB).
   
2. **Extract Hidden Text from Image**
   - Upload an image with hidden text and extract the embedded message.
   
3. **User Logging**
   - The app automatically logs user information such as IP addresses and User-Agent details whenever the user visits the site.
   
4. **Admin Panel**
   - Admins can view the extracted texts from uploaded images through a simple admin panel.

---

## **How it Works**

### **Steganography Process**
Steganography is the practice of hiding information within other, seemingly harmless data. In this application, text is encoded into the least significant bits (LSB) of the pixel values of an image. The LSB technique works by altering the smallest bit of each color channel (Red, Green, and Blue) of each pixel, which is typically not noticeable to the human eye. Here's how it works step-by-step:

1. **Embed Text into Image (Encrypt)**:
   - Convert the input text into its binary form.
   - The binary data is hidden in the least significant bits (the last bit) of the Red, Green, and Blue channels of the image pixels.
   - The result is an image with an embedded hidden message that is not visually noticeable.

2. **Extract Text from Image (Decrypt)**:
   - Scan the image and extract the least significant bits from each pixel’s color channels.
   - The binary data is then converted back to text.
   - The extracted text is displayed and stored in a log file for admin access.

---

## **Installation and Setup**

Follow these instructions to run the project locally:

### **Prerequisites:**
- **Python 3.x**: This project is built using Python 3, so make sure you have Python 3 installed.
- **Flask**: Web framework to handle HTTP requests.
- **Pillow**: Python Imaging Library (PIL), used for image manipulation.

### **Steps to Run the Project:**

1. **Clone or Download the Project:**
   - You can clone the repository using Git:
     ```bash
     git clone https://github.com/ujjcl/LSB.git
     ```
   - Or simply download the ZIP file and extract it.

2. **Navigate to the Project Directory:**
   Open a terminal or command prompt and go to the project folder:
   ```bash
   cd ...
   ```

3. **Install the Required Dependencies:**
   Install Flask and Pillow (if not already installed) by running:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Flask App:**
   Now, you can run the Flask application:
   ```bash
   python app.py
   ```
   The app will start running locally at `http://127.0.0.1:5000/`.

5. **Open the App in Your Browser:**
   Visit `http://127.0.0.1:5000/` to access the web interface.

---

## **App Routes**

### **`/` (Home)**
- **Description**: The homepage where user information is logged and the user can interact with the application.
- **Function**: Logs IP address and User-Agent whenever a user visits the page.

###**encrypt (Hide Text)**
- **Method**: `POST`
- **Description**: Upload an image and a text message to hide the text within the image.
- **Parameters**:
  - `image`: The image file.
  - `text`: The text you want to embed in the image.
- **Return**: The image with the embedded text (downloadable).

###**decrypt (Extract Text)**
- **Method**: `POST`
- **Description**: Upload an image with hidden text and extract the message.
- **Parameters**:
  - `image`: The image file containing hidden text.
- **Return**: The extracted hidden text.

### **`/logs` (View Logs)**
- **Description**: Displays the logs containing user information (IP addresses, User-Agent details).
- **Access**: Available to all users.

### **`/admin` (Admin Panel)**
- **Description**: Displays the hidden texts that were extracted from images by users.
- **Access**: This page is meant for admin users only.

### **`/re`**
- **Description**: A sample route with a simple response (not part of the core functionality).

---

## **How to Use the App**

1. **Hiding Text in an Image**:
   - Visit the homepage at `http://127.0.0.1:5000/`.
   - Click on the "Encrypt" button.
   - Upload an image and provide the text you want to hide.
   - After clicking submit, you will receive a downloadable image with the embedded message.

2. **Extracting Text from an Image**:
   - Visit the "Decrypt" page.
   - Upload the image from which you want to extract the hidden text.
   - The app will extract the hidden text and display it to you.

---

## **Detailed Explanation of Code**

### **Log User Information**
The app logs user information such as IP and User-Agent details to a file `logs.txt`. This information is useful for tracking user activity.

```python
def log_user_info(info):
    log_file = 'logs.txt'
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"[{current_time}] IP: {info['ip']} | User-Agent: {info['user_agent']}\n")
```

### **Steganography Functions**
The `embed_text_in_image()` and `extract_text_from_image()` functions are responsible for hiding and extracting text, respectively.

- **Embedding Text**: Converts the text into binary and embeds it in the least significant bits of the image.
- **Extracting Text**: Scans the image for binary data in the least significant bits and converts it back into readable text.

### **Image Processing**
The app uses the **Pillow** library to handle image manipulation (embedding and extracting text).

```python
from PIL import Image

def embed_text_in_image(image, text):
    # Embeds text into image using LSB technique
    # Returns the modified image path
    ...

def extract_text_from_image(image):
    # Extracts hidden text from the image
    # Returns the extracted text
    ...
```

---

## **Important Files:**

- **`app.py`**: The main Python file containing the Flask app logic.
- **`logs.txt`**: Stores the logs of user information (IP and User-Agent).
- **`hidden_texts.txt`**: Stores all extracted hidden texts for admin viewing.
- **`static/uploads`**: Folder where uploaded images are temporarily stored.
