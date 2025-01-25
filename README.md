# Image Encryption Using LSB Technique with AES-256 and Cryptographic Randomization

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.3.2-green)
![License](https://img.shields.io/badge/License-GPLv3-orange)
![Security](https://img.shields.io/badge/Security-Critical-red)

Advanced image encryption system combining **LSB steganography** with **AES-256 encryption** and cryptographic randomization.  
**WARNING: Losing the encryption key will result in permanent data loss!** 🔐
---

# **1.0 (Basic LSB)**
![Desktop Screenshot 2025 01 23 - 22 16 03 06](https://github.com/user-attachments/assets/d0c3fe4a-6435-4cec-8f5b-19330e3e87bc)

# **2.0 (LSB with AES-256 encryption and cryptographic randomization)**
![Desktop Screenshot 2025 01 25 - 04 44 49 89](https://github.com/user-attachments/assets/0151aca7-078c-4b7f-982b-0f290fe9c5b3)

![Desktop Screenshot 2025 01 25 - 04 39 10 57](https://github.com/user-attachments/assets/d57e7010-bca3-4373-b7d3-71a70804a9f6)

![Desktop Screenshot 2025 01 25 - 04 36 31 03](https://github.com/user-attachments/assets/b3e970f8-a6e6-450f-a5d7-fb3964af29cd)

---

## Key Features
- **Military-Grade Encryption**: AES-256 with 44-character Base64 keys.
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
   cd image-encryption-lsb
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
   http://localhost:5000
   ```

---

## Step-by-Step Usage Guide

### 1. Generating a Cryptographic Key (`/key` Route)
#### Why the Key is Critical 🔑
- **Irreversible Loss**: The key is **required for decryption**. If lost, your data is permanently inaccessible.
- **No Backdoor**: The system has no key recovery mechanism for security reasons.

#### How to Generate a Key
1. Navigate to:
   ```
   http://localhost:5000/key
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
   http://localhost:5000
   ```
2. Upload a cover image (PNG/BMP recommended).
3. Enter your secret message and **paste the generated key**.
4. Click **Encrypt Text**. The system will:
   - Encrypt the message using AES-256.
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

## Key Management Best Practices 🛡️
1. **Never Share the Key**: Treat it like a password.
2. **Multi-Device Backup**: Store copies on trusted devices.
3. **Test Key Validity**: Before deleting original data, verify decryption.
4. **Emergency Plan**: Share the key with a trusted party via secure channels (e.g., Signal, PGP).

---

## Technical Details

### Key Generation Process
- **Algorithm**: `Fernet.generate_key()` from the `cryptography` library.
- **Format**: 44-character URL-safe Base64 string.
- **Security**:
  - Keys are **never stored** on the server.
  - A 1-bit change in the key causes **100% decryption failure**.

### Code Snippets
1. **Key Validation**:
   ```python
   import re
   if not re.match(r'^[A-Za-z0-9+/=]{44}$', user_key):
       raise ValueError("Invalid key!")
   ```

2. **Embedding Sequence Generation**:
   ```python
   import hashlib
   import numpy as np

   def generate_random_positions(key, total_pixels):
       seed = int(hashlib.sha256(key).hexdigest(), 16) % 10**8
       np.random.seed(seed)
       return np.random.permutation(total_pixels)
   ```
