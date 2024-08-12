import requests

url = 'http://127.0.0.1:8000/fill-doc/'
files = {'file': open('minuta-outorga.docx', 'rb')}
data = {'cpf': '780.146.293-96'}

response = requests.post(url, files=files, data=data)

# Salvar a resposta em um arquivo
with open('filled_docx_file.docx', 'wb') as f:
    f.write(response.content)

print(f"Status Code: {response.status_code}")
print(f"Response: {response.text}")
