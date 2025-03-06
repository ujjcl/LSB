# Image Encryption Using LSB Technique with AES and Cryptographic Randomization

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.3.2-green)
![License](https://img.shields.io/badge/License-GPLv3-orange)
![Security](https://img.shields.io/badge/Security-Critical-red)

Advanced image encryption system combining **LSB steganography** with **AES encryption** and cryptographic randomization.  
---

## **1.0 (Basic LSB)**
![Desktop Screenshot 2025 01 23 - 22 16 03 06](https://github.com/user-attachments/assets/d0c3fe4a-6435-4cec-8f5b-19330e3e87bc)

## **2.0 (LSB with AES encryption and cryptographic randomization)**
![Desktop Screenshot 2025 01 25 - 04 44 49 89](https://github.com/user-attachments/assets/0151aca7-078c-4b7f-982b-0f290fe9c5b3)

![Desktop Screenshot 2025 01 25 - 04 39 10 57](https://github.com/user-attachments/assets/d57e7010-bca3-4373-b7d3-71a70804a9f6)

![Desktop Screenshot 2025 01 25 - 04 36 31 03](https://github.com/user-attachments/assets/b3e970f8-a6e6-450f-a5d7-fb3964af29cd)

## **2.1**
![Screenshot (140)](https://github.com/user-attachments/assets/79946296-0e78-4e8e-a7ba-14e015599bfa)

![Screenshot (137)](https://github.com/user-attachments/assets/350c216f-ff66-4ca7-8028-5889435219b8)

![Screenshot (136)](https://github.com/user-attachments/assets/b391e985-c14e-42b0-82f3-80bfd8c0a00a)

## **2.2**
![Screenshot (146)](https://github.com/user-attachments/assets/06899bdb-e130-4a81-aad3-0debd8fbca4d)

![Screenshot (145)](https://github.com/user-attachments/assets/fe5a6424-e502-471b-9502-8a8735df2be6)

![Screenshot (147)](https://github.com/user-attachments/assets/a086dd4c-a07c-4ec9-b2c9-902000c36092)

![Screenshot (141)](https://github.com/user-attachments/assets/93ee2654-36aa-4751-85d4-f789120a88f6)

## **2.2.1**
![Desktop Screenshot 2025 02 03 - 14 19 00 46](https://github.com/user-attachments/assets/e8d8d18b-44b6-45a6-822c-6040d818fa87)
![Desktop Screenshot 2025 02 03 - 14 21 02 62](https://github.com/user-attachments/assets/11a58c4a-330c-401f-9c97-7f0126a8dbc6)
![Desktop Screenshot 2025 02 03 - 14 21 49 75](https://github.com/user-attachments/assets/fe8008fa-67db-4da7-a46b-0997fda8389e)

---

## Key Features
- **Encryption**: AES with 44-character Base64 keys.
- **Secure Key Management**: Keys are generated cryptographically and **never stored**.
- **Anti-Tampering**: Randomized embedding using SHA-256 hashing.
- **Web Interface**: User-friendly encryption/decryption via browser.
- **Data Integrity**: PSNR > 45 dB and MSE < 2.0 guaranteed.

---

## Installation

### Prerequisites
- Python 3.10+
- pip (Python Package Manager)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/ujjcl/LSB.git
   cd LSBProject2.0
   ```


2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python app.py
   ```

4. Access the web interface at:
   ```
  http://127.0.0.1:5000

   ```

---

## Step-by-Step Usage Guide

### 1. Generating a Cryptographic Key (`/key` Route)
#### Why the Key is Critical 
- **Irreversible Loss**: The key is **required for decryption**. If lost, your data is permanently inaccessible.
- **No Backdoor**: The system has no key recovery mechanism for security reasons.

#### How to Generate a Key
1. Navigate to:
   ```
   http://127.0.0.1:5000/key
   ```
2. The system auto-generates a **44-character Base64 key** (e.g., `jX2pK5L9RqZvBtGyVnYr4wTfWmSdPh6E...`).
3. **Copy the key** using the "Copy" button or manually.
4. **Immediately save the key** in **multiple secure locations**:
   - Password managers (e.g., Bitwarden, 1Password).
   - Encrypted USB drives.
   - Offline storage (printed and stored in a safe).

---

### 2. Encrypting Data
1. Go to the homepage:
   ```
   http://127.0.0.1:5000
   ```
2. Upload a cover image (PNG/BMP recommended).
3. Enter your secret message and **paste the generated key**.
4. Click **Encrypt Text**. The system will:
   - Encrypt the message using AES.
   - Embed the data into the image using randomized LSBs.
   - Display the stego image with PSNR/MSE metrics.

---

### 3. Decrypting Data
1. Upload the stego image.
2. **Enter the exact same key** used during encryption.
3. Click **Extract Text**. The system will:
   - Regenerate the embedding sequence using the key.
   - Decrypt and display the hidden message.


---





## Troubleshooting: Keys with Unwanted Symbols (e.g., `_`, `-`)

### Problem: Invalid Symbols in Key
If your generated key contains symbols like `_` or `-` (which are **not allowed** in Fernet keys), follow these steps:

###  Cause
- **Encoding Issue**: While Fernet keys use Base64 encoding (allowed chars: `A-Z, a-z, 0-9, +, /, =`), some systems may incorrectly display/encode characters.
- **Manual Modification**: Accidentally typing/editing the key.

###  Solution: Regenerate Until Valid
1. **Via Web Interface**:
   - Go to `/key` route:  
     ```bash
     http://127.0.0.1:5000/key
     ```
   - Refresh **the page** repeatedly until you get a valid key like:  
     ```
     tyIKetCBoITu82wJ4rN3ryzIWlKvB3EMcRC38jYVKbM=
     ```

   

###  Valid Key Example
```
AValidKey1234567890ABCDEFGHIJKLpMNOPQRSTUVWXYZ=
```

###  Note
- Always use the **COPY** button – never edit keys manually.
