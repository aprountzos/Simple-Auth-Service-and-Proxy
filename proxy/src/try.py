import requests

url = "http://127.0.0.1:8000/auth/token/verify/"

payload={'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjc4MjgzMTExLCJpYXQiOjE2NzgyODEzMTEsImp0aSI6ImUxZDZmNjRjYjU2NjQyNTY4OGE5OWVlODk0M2M3ZjBjIiwidXNlcl9pZCI6MX0.x9DYTJF9MB2ae_PALA3nKZiy9mEjCVC6WGKwX9-GqcU'}
files=[

]
proxies = {
    'http': 'http://127.0.0.5:65430',
}
headers = {

}

response = requests.request("POST", url, headers=headers, data=payload, files=files, proxies=proxies)

print(response.text)
