import docker
import requests
import time
import os

# Configuration (use environment variables for security)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
CHECK_INTERVAL = 60  # Seconds

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"❌ Error sending alert: {e}")

def monitor_containers():
    client = docker.from_env()
    print("🚀 Docker Watchdog started... Monitoring containers.")
    
    # Dictionary to avoid repeating alerts every 60 seconds
    failed_containers = set()

    while True:
        containers = client.containers.list(all=True)
        
        for container in containers:
            name = container.name
            status = container.status # 'running', 'exited', 'paused', etc.

            if status != "running":
                if name not in failed_containers:
                    msg = f"⚠️ *DEVOPS ALERT*\nThe container *{name}* is: *{status}*\nCheck your server soon."
                    send_telegram_alert(msg)
                    failed_containers.add(name)
                    print(f"❗ Alert sent for: {name}")
            else:
                # If the container comes back to life, remove it from the failed list
                if name in failed_containers:
                    send_telegram_alert(f"✅ *RECOVERED*\nThe container *{name}* is back to life.")
                    failed_containers.remove(name)

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    monitor_containers()