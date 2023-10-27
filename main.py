import requests
headers = {
    'application/json'
    'query': 'gravestone'
}

r = requests.get('https://api.modrinth.com/search/', headers = headers)

print(r.status_code)
print(r.text)

#print(r.json())
