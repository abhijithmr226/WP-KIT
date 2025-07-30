# 🔐 WP-KIT BY ABHI - WordPress Attack Toolkit

![WP-KIT Banner](https://img.shields.io/badge/Author-Abhijith%20MR-purple?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.6%2B-blue?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)

**A powerful WordPress security testing script for ethical hackers and bug bounty hunters.**

> ⚠️ This tool is intended **only for educational purposes** and **authorized penetration testing**. Never use it against websites you don't own or have permission to test.

---

## 🚀 Features

- 🎯 **Brute Force XML-RPC Logins**
- 👤 **Username Enumeration via `/author=`**
- 🎨 **Theme, Plugin, Version Detection (APSCAN)**
- 📁 **Directory Fuzzing**
- 🌐 **Proxy Support**
- 🧠 **Smart Password Generator**
- 🛡️ **All-in-One WordPress Recon & Attack Kit**

---

## 📦 Requirements

- Python 3.6+
- `requests`

Install dependencies:
```bash
pip install -r requirements.txt
# 🔐 Bruteforcer Toolkit for WordPress

A powerful toolkit designed to assist ethical hackers and security researchers in enumerating and testing WordPress installations. Includes automatic scanning, user enumeration, directory fuzzing, and brute-force login via XML-RPC.

---

## 🛠️ Usage

Run the toolkit using:

```bash
python3 bruteforcer.py

[1] 🔍 APSCAN               → WP version, themes, plugins
[2] 🕵️  Username Enumeration → Auto-enum via /?author=
[3] 📁 Directory Fuzzer      → Detects sensitive directories
[4] 💥 XML-RPC BruteForce    → Try logins using XML-RPC
[0] ❌ Exit

📁 Input Files
username.txt – List of usernames (auto-generated via Option 2)

pass.txt – List of passwords for brute-forcing

directory.txt – List of directories to fuzz (e.g., admin, wp-admin, .git)

proxies.txt (optional) – One HTTP proxy per line

📄 Output
Successful logins are saved in:

success-log.csv

