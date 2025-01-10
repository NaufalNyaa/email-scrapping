from collections import deque
import re

from bs4 import BeautifulSoup
from time import sleep
from os import system
import sys, datetime
import requests
import urllib.parse

def ketik(o):
    for s in o + "\n":
        sys.stdout.write(s)
        sys.stdout.flush()
        sleep(0.015)

system("clear")
sleep(1)

def tamp():
    print("\033[34;1m<=====================================================================>")
    ketik("\033[36;1m|  \/  | ___ | | | | |   | |  \033[31;1m /  ___|")
    ketik("\033[36;1m| .  . | |_/ | | | | |   | |  \033[31;1m \ `--.  ___ _ __ __ _ _ __  _ __   ___ _ __ ")
    ketik("\033[36;1m| |\/| | ___ | | | | |   | |  \033[31;1m  `--. \/ __| '__/ _` | '_ \| '_ \ / _ | '__|")
    ketik("\033[36;1m| |  | | |_/ | |_| | |___| |___\033[31;1m/\__/ | (__| | | (_| | |_) | |_) |  __| |")
    ketik("\033[36;1m\_|  |_\____/ \___/\_____\_____\033[31;1m\____/ \___|_|  \__,_| .__/| .__/ \___|_|") 
    ketik("                              \033[31;1m                      | |   | |")
    ketik("                              \033[31;1m                      |_|   |_|")
    print("\033[34;1m<=====================https://github.com/NaufalNyaa==================>")
    kal = datetime.datetime.now()
    ketik(f"\033[31;1mDay > {kal:%d} [{kal:%A}] ")
    ketik(f"\033[33;1mMonth > {kal:%B}")
    ketik(f"\033[32;1mYear > {kal:%G}")
    print("\033[34;1m<=====================================================================>")

tamp()

user_url = str(input('[+] Masukan url: '))
urls = deque([user_url])
scraped_urls = set()
emails = set()
count = 0
limit = int(input('[+] Masukan limit pencarian: '))

try:
    while count < limit and urls:  
        count += 1
        
        
        url = urls.popleft()
        scraped_urls.add(url)
        parts = urllib.parse.urlsplit(url)
        base_url = f'{parts.scheme}://{parts.netloc}'
        path = url[:url.rfind('/')+1] if '/' in parts.path else url

        print(f'{count} Memproses {url}')
        
        try:
            response = requests.get(url)
        except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
            continue

        
        new_emails = set(re.findall(r'[a-z0-9\.\-+_]+@\w+\.+[a-z\.]+', response.text, re.I))
        emails.update(new_emails)

        
        soup = BeautifulSoup(response.text, 'html.parser')
        for anchor in soup.find_all('a'):
            link = anchor.attrs['href'] if 'href' in anchor.attrs else ''
            if link.startswith('/'):
                link = base_url + link
            elif not link.startswith('http'):
                link = path + link

            
            if link not in urls and link not in scraped_urls:
                urls.append(link)
except KeyboardInterrupt:
    print('[-] Program dihentikan oleh pengguna.')

print('\nProses selesai!')
print(f'\n{len(emails)} email ditemukan \n===============================')

for mail in emails:
    print('  ' + mail)
print('\n')
