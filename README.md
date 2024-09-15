## SafeHavenE 🔒

SafeHavenE is a PyQt5 application designed to encrypt and decrypt files within a chosen folder. Protect your sensitive data with ease!

## Features ✨

- **User-Friendly Interface**: Simple and intuitive UI built with PyQt5.
- **Secure Encryption**: Uses Fernet symmetric encryption to keep your files safe.
- **Password Protection**: Strong password validation ensures security.
- **Automatic File Detection**: Encrypts files that haven't been encrypted yet.
- **Decryption with Caution**: Decrypt files only with the correct password.
- **Failed Attempt Lockout**: Lockout for 5 minutes after 3 failed password attempts.

## How to Use 🛠️

1. **Choose Folder**: Select the folder containing the files you want to encrypt or decrypt.
2. **Set Password**: Enter a strong password meeting the criteria.
3. **Encrypt**: Click "Encrypt" to encrypt all unencrypted files in the folder.
4. **Decrypt**: Click "Decrypt" to decrypt files (remember your password!).

### Password Requirements 🔑
- Minimum of 8 characters
- At least one lowercase letter
- At least one uppercase letter
- At least one symbol (e.g., `!@#$%^&*`)

### Important Notes ⚠️
- **Do not forget your password**. Lost passwords cannot recover files.
- The app prevents double encryption of files, avoiding re-encryption.
- After 3 incorrect password attempts, you will be locked out for 5 minutes.

## Team 👥

- **Project Leader & Developer**:
  - Abdo Raz (BEDFTB) - [GitHub: IGNRaz](https://github.com/IGNRaz)
- **Co-Leader & UI Developer**:
  - Zaid Alsalh (FEDFTB) - [GitHub: zaedalsalh](https://github.com/zaedalsalh)
- **Database Backend Developer**:
  - Majd Abdulhai - [GitHub: 1itsmajd](https://github.com/1itsmajd)

## Disclaimer ⚠️

This app was developed by beginner-level programmers, so some bugs or issues might occur. Use at your own risk.

