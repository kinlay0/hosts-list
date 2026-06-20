import requests

# ссылка на список хостов с гитхаба
url = "https://raw.githubusercontent.com/V3nilla/IPSets-For-Bypass-in-Russia/refs/heads/main/%D0%A0%D0%B0%D0%B7%D0%B1%D0%BB%D0%BE%D0%BA%D0%B8%D1%80%D0%BE%D0%B2%D0%BA%D0%B0%20%D0%BC%D0%BD%D0%BE%D0%B6%D0%B5%D1%81%D1%82%D0%B2%D0%B0%20%D1%81%D0%B5%D1%80%D0%B2%D0%B8%D1%81%D0%BE%D0%B2(%D0%BF%D1%80%D0%B8%D0%BC%D0%B5%D1%80%20-%20ChatGPT)/hosts"

print("скачиваю файл...")

lines = []
try:
    r = requests.get(url, timeout=5)
    if r.status_code == 200:
        lines = r.text.splitlines()
        print("скачал, строк:", len(lines))
    else:
        print("сервер ответил не 200, код:", r.status_code)
except:
    print("не получилось скачать, что-то с интернетом или гитхабом")

if not lines:
    print("пробую локальный файл hosts.txt")
    try:
        f = open('parser/hosts.txt', 'r', encoding='utf-8', errors='ignore')
        lines = f.readlines()
        f.close()
        print("открыл, строк:", len(lines))
    except FileNotFoundError:
        print("нет файла parser/hosts.txt, дальше делать нечего")
        exit()

proxy = open('proxy.txt', 'w', encoding='utf-8')
block = open('block.txt', 'w', encoding='utf-8')

proxy_count = 0
block_count = 0

for line in lines:
    line = line.strip()
    if line == '' or line.startswith('#'):
        continue

    parts = line.split(None, 1)  # делим по пробелам на айпи и всё остальное (умоляю не трогай больше)
    if len(parts) < 2:
        continue

    ip = parts[0]
    domain = parts[1]
    domain = domain.split('#')[0].strip()  # убирается коммент после домена 

    if ip == '0.0.0.0':
        block.write(domain + '\n')
        block_count += 1
    else:
        proxy.write(ip + ' ' + domain + '\n')
        proxy_count += 1

proxy.close()
block.close()

print("готово! proxy.txt -", proxy_count, "строк, block.txt -", block_count, "строк")
