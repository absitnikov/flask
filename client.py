import requests

response = requests.post('http://127.0.0.1:5000/advertisement',
                         json={'title': 'Test', 'description': 'Yekaterinburg', 'owner_id': 'Andrey'})

print(response.status_code)
print(response.json())

response = requests.get('http://127.0.0.1:5000/advertisement/1')
print(response.status_code)
print(response.json())

response = requests.delete('http://127.0.0.1:5000/advertisement/1')
print(response.status_code)
print(response.json())
