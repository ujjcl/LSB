# **LSB Steganography**

![Desktop Screenshot 2025 01 23 - 22 16 03 06](https://github.com/user-attachments/assets/e490af57-9fb1-421e-9cff-af28ff6d5c2b)

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

### **encrypt (Hide Text)**
- **Method**: `POST`
- **Description**: Upload an image and a text message to hide the text within the image.
- **Parameters**:
  - `image`: The image file.
  - `text`: The text you want to embed in the image.
- **Return**: The image with the embedded text (downloadable).

### **decrypt (Extract Text)**
- **Method**: `POST`
- **Description**: Upload an image with hidden text and extract the message.
- **Parameters**:
  - `image`: The image file containing hidden text.
- **Return**: The extracted hidden text.

### **`/logs` (View Logs)**
- **Description**: Displays the logs containing user information (IP addresses, User-Agent details).

### **`/admin` (Admin Panel)**
- **Description**: Displays the hidden texts that were extracted from images by users.

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
   -  Click on the "Decrypt" button.
   - Upload the image from which you want to extract the hidden text.
   - The app will extract the hidden text and display it to you.
