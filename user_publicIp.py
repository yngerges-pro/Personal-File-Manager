import requests

def user_publicIp():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        if response.status_code == 200:
            ip_address = response.json()['ip']
            print(f"Your public IP address is: {ip_address}")
            return ip_address
        else:
            print("Failed to retrieve public IP address")
            return None
    except Exception as e:
        print("Error:", e)
        return None


  