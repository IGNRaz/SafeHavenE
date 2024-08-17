# SafeHavenE V:1.0

Vaultify is a PyQt5 application designed to encrypt and decrypt files within a chosen folder. This app offers an easy way to protect your sensitive data from unauthorized access.

## Features

- **User-Friendly Interface**: Simple and intuitive UI built with PyQt5.
- **Secure Encryption**: Uses Fernet symmetric encryption to secure your files.
- **Password Protection**: Ensure strong password security with built-in validation.
- **Automatic File Detection**: Automatically encrypts files that haven't been encrypted yet.
- **Decryption with Caution**: Only decrypts files if the correct password is provided.
- **Failed Attempt Lockout**: After 3 failed password attempts, the app locks you out for 5 minutes before you can try again.

## How to Use

1. **Choose Folder**: Select the folder containing the files you want to encrypt or decrypt.
2. **Set Password**: Enter a strong password that meets the required criteria.
3. **Encrypt**: Click on the "Encrypt" button to encrypt all unencrypted files in the folder.
4. **Decrypt**: Click on the "Decrypt" button to decrypt files, but ensure you remember your password!

### Password Requirements
- Minimum of 8 characters
- At least one lowercase letter
- At least one uppercase letter
- At least one symbol (e.g., `!@#$%^&*`)

### Important Notes
- **Do not forget your password**. If you lose it, you won't be able to recover your files.
- The app prevents double encryption of files, ensuring that files that have already been encrypted won't be encrypted again.
- If you fail to enter the correct password 3 times, the app will lock you out for 5 minutes before allowing further attempts.

## Credits

- **Project Leader & Developer**:
-  Abdo Raz (BEDFTB) - [GitHub: IGNRaz](https://github.com/IGNRaz)
- **Co-Leader & UI Developer**:
- Zaid Alsalh (FEDFTB) - [GitHub: zaedalsalh](https://github.com/zaedalsalh)

## Disclaimer

This app was developed by beginner-level programmers, so you might encounter some bugs or issues. Use it at your own risk.
