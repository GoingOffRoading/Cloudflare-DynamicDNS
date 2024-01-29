import requests
import json

def get_current_ip():
    response = requests.get('https://api64.ipify.org?format=json')
    data = response.json()
    return data['ip']

def get_cloudflare_ip(subdomain, zone_id, api_key, email):
    url = f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records?type=A&name={subdomain}'
    headers = {
        'X-Auth-Key': api_key,
        'X-Auth-Email': email,
        'Content-Type': 'application/json',
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    return data['result'][0]['content']

def update_cloudflare_ip(subdomain, zone_id, api_key, email, new_ip):
    url = f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records'
    headers = {
        'X-Auth-Key': api_key,
        'X-Auth-Email': email,
        'Content-Type': 'application/json',
    }
    data = {
        'type': 'A',
        'name': subdomain,
        'content': new_ip,
        'ttl': 1,
        'proxied': False,
    }
    response = requests.put(url, headers=headers, json=data)
    return response.json()

def main():
    # Replace these values with your own
    subdomain = 'your-subdomain'
    zone_id = 'your-zone-id'
    api_key = 'your-cloudflare-api-key'
    email = 'your-email@example.com'

    current_ip = get_current_ip()
    cloudflare_ip = get_cloudflare_ip(subdomain, zone_id, api_key, email)

    if current_ip != cloudflare_ip:
        print(f'IP address has changed. Updating Cloudflare DNS record to {current_ip}')
        update_response = update_cloudflare_ip(subdomain, zone_id, api_key, email, current_ip)
        print('Update response:', update_response)
    else:
        print('IP address is already up to date.')

if __name__ == "__main__":
    main()
