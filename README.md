# Image Encryption Using LSB Technique with AES and Cryptographic Randomization

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.3.2-green)
![License](https://img.shields.io/badge/License-GPLv3-orange)
![Security](https://img.shields.io/badge/Security-Critical-red)

An advanced image encryption system combining **LSB steganography** with **AES encryption** and cryptographic randomization. This project ensures secure data embedding within images, strengthened by robust cryptographic practices.

---

## Live Demo

Experience the application online at: [https://lsb-tjxx.onrender.com](https://lsb-tjxx.onrender.com)

---

## Project Versions

### **1.0 (Basic LSB)**
![Version 1.0 Screenshot](https://github.com/user-attachments/assets/d0c3fe4a-6435-4cec-8f5b-19330e3e87bc)

### **2.0 (LSB with AES encryption and cryptographic randomization)**
![Version 2.0 Screenshot 1](https://github.com/user-attachments/assets/0151aca7-078c-4b7f-982b-0f290fe9c5b3)
![Version 2.0 Screenshot 2](https://github.com/user-attachments/assets/d57e7010-bca3-4373-b7d3-71a70804a9f6)
![Version 2.0 Screenshot 3](https://github.com/user-attachments/assets/b3e970f8-a6e6-450f-a5d7-fb3964af29cd)

### **2.1**
![Version 2.1 Screenshot 1](https://github.com/user-attachments/assets/79946296-0e78-4e8e-a7ba-14e015599bfa)
![Version 2.1 Screenshot 2](https://github.com/user-attachments/assets/350c216f-ff66-4ca7-8028-5889435219b8)
![Version 2.1 Screenshot 3](https://github.com/user-attachments/assets/b391e985-c14e-42b0-82f3-80bfd8c0a00a)

### **2.2**
![Version 2.2 Screenshot 1](https://github.com/user-attachments/assets/06899bdb-e130-4a81-aad3-0debd8fbca4d)
![Version 2.2 Screenshot 2](https://github.com/user-attachments/assets/fe5a6424-e502-471b-9502-8a8735df2be6)
![Version 2.2 Screenshot 3](https://github.com/user-attachments/assets/a086dd4c-a07c-4ec9-b2c9-902000c36092)
![Version 2.2 Screenshot 4](https://github.com/user-attachments/assets/93ee2654-36aa-4751-85d4-f789120a88f6)

### **2.2.1**
![Version 2.2.1 Screenshot 1](https://github.com/user-attachments/assets/e8d8d18b-44b6-45a6-822c-6040d818fa87)
![Version 2.2.1 Screenshot 2](https://github.com/user-attachments/assets/11a58c4a-330c-401f-9c97-7f0126a8dbc6)
![Version 2.2.1 Screenshot 3](https://github.com/user-attachments/assets/fe8008fa-67db-4da7-a46b-0997fda8389e)


### **2.4**
![Desktop Screenshot 2025 03 07 - 00 57 05 06](https://github.com/user-attachments/assets/9ba6f5d6-761e-4721-bb30-0585a6f0f07b)

---

## Key Features
- **Encryption**: AES with 44-character Base64 keys.
- **Secure Key Management**: Keys are generated cryptographically and never stored.
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

## Usage Guide

### 1. Generating a Cryptographic Key
**Why the Key is Critical:**
- The key is required for decryption. If lost, your data is permanently inaccessible.
- The system has no key recovery mechanism for security reasons.

**How to Generate a Key:**
1. Navigate to the key generation route:
   ```
   http://127.0.0.1:5000/key
   ```
2. A **44-character Base64 key** will be auto-generated.
3. Copy the key using the "Copy" button or manually.
4. Save the key securely in multiple locations:
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
3. Enter your secret message and paste the generated key.
4. Click **Encrypt Text**. The system will:
   - Encrypt the message using AES.
   - Embed the data into the image using randomized LSBs.
   - Display the stego image with PSNR/MSE metrics.

---

### 3. Decrypting Data
1. Upload the stego image.
2. Enter the exact same key used during encryption.
3. Click **Extract Text**. The system will:
   - Regenerate the embedding sequence using the key.
   - Decrypt and display the hidden message.

---

## Troubleshooting

### Keys with Unwanted Symbols (e.g., `_`, `-`)

**Problem:** Invalid symbols in the key.

**Cause:**
- Encoding issue: While Fernet keys use Base64 encoding (allowed chars: `A-Z, a-z, 0-9, +, /, =`), some systems may incorrectly encode characters.
- Manual modification: Accidentally editing the key.

**Solution:** Regenerate until valid.

1. **Via Web Interface:**
   - Navigate to the key generation route:
     ```
     http://127.0.0.1:5000/key
     ```
   - Refresh until you get a valid key like:
     ```
     tyIKetCBoITu82wJ4rN3ryzIWlKvB3EMcRC38jYVKbM=
     ```

**Valid Key Example:**
```
AValidKey1234567890ABCDEFGHIJKLpMNOPQRSTUVWXYZ=
```

**Note:** Always use the **COPY** button — never edit keys manually.

---



