# Secure Pass: Password Manager

![Secure Pass Logo](assets/brand_logo.png)

A desktop password manager built with Python and Tkinter. Passwords are encrypted at rest using a master password — nothing is stored in plain text.

## Features

- AES encryption via [cryptography](https://cryptography.io) (Fernet + PBKDF2-HMAC-SHA256)
- Master password required on every launch
- Auto-generate strong passwords
- Copy passwords to clipboard with a double-click
- Multi-language UI: **English**, **Português (Brasil)**, **Español**
- Language preference persisted in the local database

## Requirements

- Python 3.11.7 or newer
- `tkinter` (usually bundled with Python; see note below)

> **Linux note:** if `tkinter` is missing, install it with your package manager:
> ```bash
> # Debian / Ubuntu
> sudo apt install python3-tk
>
> # Fedora
> sudo dnf install python3-tkinter
>
> # Arch
> sudo pacman -S tk
> ```

## Installation

### Automatic (Linux)

```bash
git clone https://github.com/fgmarcal/secure_pass.git
cd secure_pass
chmod +x install_dependencies.sh run.sh
./install_dependencies.sh
```

### Manual

```bash
git clone https://github.com/fgmarcal/secure_pass.git
cd secure_pass
python3 -m venv venv
venv/bin/pip install -r requirements.txt
```

## Running

### With the launcher script (Linux)

```bash
./run.sh
```

### Manually

```bash
venv/bin/python app.py
```

### Windows / macOS

```bash
venv\Scripts\python app.py        # Windows
venv/bin/python app.py            # macOS
```

## Building a Windows Portable Executable

The Windows build runs inside Docker with Wine, so it can be produced from Linux without installing Python on Windows.

```bash
chmod +x build_windows.sh
./build_windows.sh
```

The build creates:

```text
dist/windows/SecurePass/
dist/windows/SecurePass-windows-portable.zip
```

Unzip `SecurePass-windows-portable.zip` on Windows and run `SecurePass.exe`. The portable app creates its own vault files in `SecurePass/database/` on first launch. Existing local `database/data.db` and `database/salt.key` are not included in the Windows package.

## First Time Using the App

When you open the app for the first time, you will be asked to create a master password and confirm it.

1. Enter a strong master password and keep it safe.
2. Confirm it in the second field and click `OK`.
3. Start adding your credentials in the `Main` tab.
4. Open the `Saved` tab to view entries and copy passwords.

Important:
- Your master password is not stored, so it cannot be recovered by the app.
- A salt file is created at `database/salt.key` on first launch. Back up this file together with your database.
- On future launches, you must enter the same master password to unlock existing passwords.

## Project Structure

```
password-manager/
├── app.py                        # Entry point
├── requirements.txt
├── install_dependencies.sh       # Linux installer
├── run.sh                        # Linux launcher
├── assets/
│   └── logo.png
├── database/
│   ├── database.py               # SQLite helpers + settings persistence
│   └── crypto.py                 # Fernet encryption / decryption
├── locales/
│   ├── __init__.py               # Language manager (lang.t / lang.set_language)
│   ├── en.py                     # English strings
│   ├── pt_br.py                  # Brazilian Portuguese strings
│   └── es.py                     # Spanish strings
├── tabs/
│   ├── main_tab.py               # Add new entry
│   ├── saved_tab.py              # View / delete saved entries
│   ├── settings_tab.py           # Language selector
│   └── master_password_dialog.py # Master password prompt
├── styles/
│   └── button_style.py           # Shared button style
└── utils/
    └── utils.py                  # Password generator, clipboard helper
```

## Security Notes

- The master password is never stored. It is used to derive an encryption key via PBKDF2-HMAC-SHA256 (480 000 iterations).
- A random 16-byte salt is generated on first launch and stored in `database/salt.key`. **Back this file up** — losing it means losing access to all saved passwords.
- All passwords in `database/data.db` are Fernet-encrypted and unreadable without the correct master password.
