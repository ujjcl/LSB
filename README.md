
# Image Encryption Using LSB Technique with AES and Cryptographic Randomization

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.3.2-green)
![Encryption](https://img.shields.io/badge/Encryption-Fernet-important)
![LSB](https://img.shields.io/badge/Steganography-LSB-success)

Image encryption system that combines LSB steganography with AES encryption and cryptographic randomization. The system securely embeds encrypted data within images using robust cryptographic practices and randomized data distribution, ensuring both confidentiality and integrity.
---

## Live Demo

Access the application online at:  
[https://lsb-tjxx.onrender.com](https://lsb-tjxx.onrender.com)

> **Note:** The site may be in sleep mode and can take about one minute to start up.

---

## Project Versions

### 1.0 (Basic LSB)
![Version 1.0 Screenshot](https://github.com/user-attachments/assets/d0c3fe4a-6435-4cec-8f5b-19330e3e87bc)

### 2.0 (LSB with AES Encryption and Cryptographic Randomization)
![Version 2.0 Screenshot 1](https://github.com/user-attachments/assets/0151aca7-078c-4b7f-982b-0f290fe9c5b3)  
![Version 2.0 Screenshot 2](https://github.com/user-attachments/assets/d57e7010-bca3-4373-b7d3-71a70804a9f6)  
![Version 2.0 Screenshot 3](https://github.com/user-attachments/assets/b3e970f8-a6e6-450f-a5d7-fb3964af29cd)

### 2.1
![Version 2.1 Screenshot 1](https://github.com/user-attachments/assets/79946296-0e78-4e8e-a7ba-14e015599bfa)  
![Version 2.1 Screenshot 2](https://github.com/user-attachments/assets/350c216f-ff66-4ca7-8028-5889435219b8)  
![Version 2.1 Screenshot 3](https://github.com/user-attachments/assets/b391e985-c14e-42b0-82f3-80bfd8c0a00a)

### 2.2
![Version 2.2 Screenshot 1](https://github.com/user-attachments/assets/06899bdb-e130-4a81-aad3-0debd8fbca4d)  
![Version 2.2 Screenshot 2](https://github.com/user-attachments/assets/fe5a6424-e502-471b-9502-8a8735df2be6)  
![Version 2.2 Screenshot 3](https://github.com/user-attachments/assets/a086dd4c-a07c-4ec9-b2c9-902000c36092)  
![Version 2.2 Screenshot 4](https://github.com/user-attachments/assets/93ee2654-36aa-4751-85d4-f789120a88f6)

### 2.2.1
![Version 2.2.1 Screenshot 1](https://github.com/user-attachments/assets/e8d8d18b-44b6-45a6-822c-6040d818fa87)  
![Version 2.2.1 Screenshot 2](https://github.com/user-attachments/assets/11a58c4a-330c-401f-9c97-7f0126a8dbc6)  
![Version 2.2.1 Screenshot 3](https://github.com/user-attachments/assets/fe8008fa-67db-4da7-a46b-0997fda8389e)

### 2.4
![Version 2.4 Desktop Screenshot](https://github.com/user-attachments/assets/9ba6f5d6-761e-4721-bb30-0585a6f0f07b)

### 2.5
![Version 2.5 Screenshot](https://github.com/user-attachments/assets/35562bca-fcee-457c-bee3-31994b610779)

---


## Key Features

- **Strong Encryption:** Implements Fernet encryption, which uses AES-128 in CBC mode with HMAC-SHA256 for data integrity.
- **Secure Key Management:** Keys are generated using a cryptographically secure process and are Base64 encoded (44 characters). The system does not store keys.
- **Randomized Data Embedding:** Utilizes a SHA-256–based seed to randomize pixel selection during data embedding.
- **High Data Integrity:** Maintains quality with PSNR typically above 45 dB and MSE below 2.0, ensuring minimal visual distortion.
- **Responsive Web Interface:** Provides a user-friendly interface for encryption and decryption tasks with detailed quality metrics.
- **Detailed Quality Analysis:** Offers reports on image quality post-embedding, helping users understand the impact of the steganography process.

---
## Technical Overview

### LSB Steganography
- **Concept:** The system hides encrypted data by modifying the least significant bits (LSB) of pixel values in the cover image.
- **Randomized Embedding:** Instead of sequential embedding, pixel positions are randomized. A seed derived from the encryption key (using a SHA-256 hash) ensures that the embedding sequence is secure and unpredictable.

### Fernet Encryption
- **Encryption Mechanism:** The system uses Python’s Fernet module from the cryptography library.  
- **Underlying Algorithm:** Fernet utilizes AES in CBC mode with a 128-bit key for encryption and HMAC-SHA256 for data integrity.  
- **Key Details:** Fernet generates a 32-byte key that is Base64-encoded to a 44-character string. Although the encoded key is 256 bits in total, only 128 bits are used for the AES encryption while the remainder is used for authentication.
- **Security Practice:** The key is generated cryptographically and is never stored in plaintext by the system. Users are responsible for its secure management.

### Cryptographic Randomization
- **Random Position Generation:** The pixel positions for embedding are determined by computing a SHA-256 hash of the key and using a modulus operation (modulo 10^8) to seed a random number generator. This adds an additional layer of security to the embedding process.
- **Data Integrity:** The system calculates quality metrics—Peak Signal-to-Noise Ratio (PSNR) and Mean Squared Error (MSE)—to ensure that the stego image maintains high visual quality.

---
## Installation

### Prerequisites

- Python 3.10 or higher
- pip (Python Package Manager)

### Installation Steps

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/ujjcl/LSB.git
   cd LSBProject2.0
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application:**
   ```bash
   python app.py
   ```

4. **Access the Web Interface:**
   ```
   http://127.0.0.1:5000
   ```

---

## Usage Guide

### 1. Generating a Cryptographic Key

*Importance:*  
The key is essential for both encryption and decryption. If lost, the encrypted data becomes permanently inaccessible. For security reasons, there is no key recovery mechanism built into the system.

*Steps to Generate a Key:*
1. Navigate to the key generation route:
   ```
   http://127.0.0.1:5000/key
   ```
2. A 44-character Base64 key will be generated automatically.
3. Copy the key using the provided button or manually.
4. Store the key securely using password managers, encrypted storage devices, or offline methods.

### 2. Encrypting Data

1. Visit the homepage:
   ```
   http://127.0.0.1:5000
   ```
2. Upload a cover image (preferably in PNG or JPEG format).
3. Enter your secret message or upload a TXT file containing the message.
4. Paste the generated key.
5. Click the "Encrypt Text" button.  
   The system will:
   - Encrypt the secret message using Fernet.
   - Embed the encrypted data into the image using a randomized LSB approach.
   - Display the stego image along with quality metrics (PSNR and MSE) and a secure sharing link.

### 3. Decrypting Data

1. Upload the stego image.
2. Enter the exact key used during encryption.
3. Click the "Extract Text" button.  
   The system will:
   - Reconstruct the embedding sequence using the provided key.
   - Decrypt and display the hidden message.

> **Note:** The stego image must remain unaltered for decryption to succeed.

---

## Security Specifications

| Specification         | Value                                                       |
|-----------------------|-------------------------------------------------------------|
| Encryption Algorithm  | Fernet (AES-128 in CBC mode with HMAC-SHA256)               |
| Key Length            | 44 characters (Base64-encoded 32 bytes)                     |
| Randomization Seed    | Derived from a SHA-256 hash of the key                        |
| Quality Metrics       | PSNR typically > 45 dB and MSE < 2.0                        |

---

## Performance and Quality Analysis

- **Quality Metrics:**  
  The system computes PSNR and MSE to ensure that the visual quality of the stego image is preserved. A PSNR above 45 dB indicates minimal visual distortion, while a low MSE confirms high data integrity.

- **Efficiency Considerations:**  
  The encryption and embedding processes are optimized for images up to 8K resolution. Testing with different image sizes is recommended for optimal performance.

- **Security Analysis:**  
  The combination of Fernet encryption and randomized data embedding ensures robust protection against both steganalysis and cryptanalysis. It is recommended to use high-quality cover images to further reduce the risk of detection.

---

## Troubleshooting

| Issue                                     | Solution                                                              |
|-------------------------------------------|-----------------------------------------------------------------------|
| Key contains invalid characters (e.g., '_' or '-') | Regenerate the key until a valid 44-character Base64 key is obtained, * Refresh until you get a valid key like: ```*tyIKetCBoITu82wJ4rN3ryzIWlKvB3EMcRC38jYVKbM=  ``` *|
| Decryption error                          | Verify that the decryption key exactly matches the encryption key and that the image has not been modified or compressed. |
| Slow performance                          | Use cover images smaller than 5MB to improve processing speed.         |
| Installation issues                       | Ensure you are using Python 3.10+ and that all dependencies are properly installed. |

---

