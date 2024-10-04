import os, requests



url="https://img5.qy0.ru/data/2589/40/1.png"

headers = {

            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.69",
        }

response = requests.get(url=url, headers=headers)

print(response.status_code)