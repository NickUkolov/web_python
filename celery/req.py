import requests


url = "http://127.0.0.1:5000/upscale"
file_path = "./app/lama_300px.png"

with open(file_path, "rb") as file:
    files = {"image": file}
    response = requests.post(url, files=files)

print(response.status_code)
print(response.json())

