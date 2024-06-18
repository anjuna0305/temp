import requests

url = "http://localhost:3000/endpoint"

payload = {}
files=[
  ('docs',('commands.md',open('/home/anjuna/Desktop/commands.md','rb'),'application/octet-stream'))
]
headers = {}

response = requests.request("POST", url, headers=headers, data=payload, files=files)

print(response.text)
