import requests

url = ["https://raw.githubusercontent.com/kinlay0/IPSets-For-Bypass-in-Russia/refs/heads/main/%D0%A0%D0%B0%D0%B7%D0%B1%D0%BB%D0%BE%D0%BA%D0%B8%D1%80%D0%BE%D0%B2%D0%BA%D0%B0%20%D0%BC%D0%BD%D0%BE%D0%B6%D0%B5%D1%81%D1%82%D0%B2%D0%B0%20%D1%81%D0%B5%D1%80%D0%B2%D0%B8%D1%81%D0%BE%D0%B2(%D0%BF%D1%80%D0%B8%D0%BC%D0%B5%D1%80%20-%20ChatGPT)/hosts"]

url_block = ["https://raw.githubusercontent.com/hagezi/dns-blocklists/main/wildcard/pro-onlydomains.txt"]


domains_exclude = [
    "yougame.biz",
]


def download(link):
    try:
        r = requests.get(link, timeout=5)
        if r.status_code == 200:
            return r.text.splitlines()
        print("сервер ответил не 200, код:", r.status_code)
    except:
        print("не получилось скачать:", link)
    return []


print("скачиваю файл...")
lines = []
for u in url:
    lines = download(u)
    if lines:
        break
print("скачал, строк:", len(lines))

if not lines:
    print("пробую локальный файл hosts.txt")
    try:
        with open('parser/hosts.txt', 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        print("открыл, строк:", len(lines))
    except FileNotFoundError:
        print("нет файла parser/hosts.txt, дальше делать нечего")
        exit()

block_domains = []
block_seen = set()

proxy_count = 0
proxy = open('proxy.txt', 'w', encoding='utf-8')

for line in lines:
    line = line.strip()
    if line == '' or line.startswith('#'):
        continue

    parts = line.split(None, 1)  # делим по пробелам на айпи и всё остальное (умоляю не трогай больше)
    if len(parts) < 2:
        continue

    ip, domain = parts
    domain = domain.split('#')[0].strip()

    if ip == '0.0.0.0':
        if domain not in block_seen and domain not in domains_exclude:
            block_seen.add(domain)
            block_domains.append(domain)
    else:
        proxy.write(ip + ' ' + domain + '\n')
        proxy_count += 1

proxy.close()

for b_url in url_block:
    print("скачиваю block-лист:", b_url)
    b_lines = download(b_url)

    added = 0
    for line in b_lines:
        domain = line.strip().split('#')[0].strip()
        if domain and domain not in block_seen and domain not in domains_exclude:
            block_seen.add(domain)
            block_domains.append(domain)
            added += 1
    print("добавил доменов:", added)

with open('block.txt', 'w', encoding='utf-8') as f:
    for domain in block_domains:
        f.write(domain + '\n')

print("готово! proxy.txt -", proxy_count, "строк, block.txt -", len(block_domains), "строк")