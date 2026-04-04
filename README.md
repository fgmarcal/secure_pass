# Secure Pass: Password Manager

A desktop password manager built with Python and Tkinter. Passwords are encrypted at rest using a master password — nothing is stored in plain text.

## Features

- AES encryption via [cryptography](https://cryptography.io) (Fernet + PBKDF2-HMAC-SHA256)
- Master password required on every launch
- Auto-generate strong passwords
- Copy passwords to clipboard with a double-click
- Multi-language UI: **English**, **Português (Brasil)**, **Español**
- Language preference persisted in the local database

## Requirements

- Python 3.10 or newer
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
