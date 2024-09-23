import requests
from datetime import datetime
import pytz
import time
import random
from colorama import Fore, Style, init
import os
import sys
import subprocess
from collections import Counter

def welcome():
    print(r"""
          
this cato not hamster
          """)
    print(Fore.GREEN + Style.BRIGHT + "Catopia BOT")
    print(Fore.GREEN + Style.BRIGHT + "By: notfound\n")

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')
   
def get_random_color():
    colors = [Fore.LIGHTGREEN_EX, Fore.LIGHTYELLOW_EX, Fore.LIGHTBLUE_EX, Fore.LIGHTMAGENTA_EX, Fore.LIGHTCYAN_EX]
    return random.choice(colors)

def login(query):
    url = "https://api.catopia.io/api/v1/auth/telegram"
    headers = {
        "Authorization": "Bearer",
        "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; Nexus 5 Build/N2G47H; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/81.0.4044.117 Mobile Safari/537.36",
        "Content-Type": "application/json; charset=UTF-8",
        "Accept": "*/*",
        "Origin": "https://build.catopia.io",
        "X-Requested-With": "tw.nekomimi.nekogram",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://build.catopia.io/",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en,en-GB;q=0.9,en-US;q=0.8"
    }
    data = {
        "initData": query
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        response_json = response.json()
        access_token = response_json.get('data', {}).get('accessToken', None)
        return access_token
    else:
        print(f"Login request failed with status code {response.status_code}")
        return None

def cek_tanaman(access_token):
    url = "https://api.catopia.io/api/v1/players/plant?limit=3000"
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; Nexus 5 Build/N2G47H; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/81.0.4044.117 Mobile Safari/537.36",
        "Content-Type": "application/json; charset=UTF-8",
        "Accept": "*/*",
        "Origin": "https://build.catopia.io",
        "X-Requested-With": "tw.nekomimi.nekogram",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://build.catopia.io/",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en,en-GB;q=0.9,en-US;q=0.8"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        data = result.get('data', [])
        
        if not data:
            print(f"[ {Fore.LIGHTYELLOW_EX}INFO{Style.RESET_ALL} ] Tidak ada benih, melakukan pembelian benih...")
            beli_benih(access_token)
        else:
            use_boost(access_token)
            for item in data:
                menanam(item.get('id'), access_token)
    else:    
        main()

def ubah_ke_wib(gmt_time_str):
    gmt_format = "%a, %d %b %Y %H:%M:%S GMT"
    gmt_time = datetime.strptime(gmt_time_str, gmt_format)
    gmt_timezone = pytz.timezone('GMT')
    gmt_time = gmt_timezone.localize(gmt_time)
    wib_timezone = pytz.timezone('Asia/Jakarta')
    wib_time = gmt_time.astimezone(wib_timezone)
    wib_format = "%Y-%m-%d %H:%M:%S %Z"
    return wib_time.strftime(wib_format)

def cek_panen(grownAt_str):
    wib_format = "%Y-%m-%d %H:%M:%S %Z"
    wib_time = datetime.strptime(grownAt_str, wib_format)
    wib_timezone = pytz.timezone('Asia/Jakarta')
    wib_time = wib_timezone.localize(wib_time)
    now = datetime.now(wib_timezone)
    if now >= wib_time:
        return "Siap Panen",
    else:
        remaining_seconds = (wib_time - now).total_seconds()
        return "Belum Siap Panen", remaining_seconds

def display_countdown(remaining_seconds):
    while remaining_seconds > 0:
        minutes, seconds = divmod(int(remaining_seconds), 60)
        time_format = f"{minutes:02}:{seconds:02}"
        colortime = get_random_color()
        print(f"\r[ {Fore.LIGHTYELLOW_EX}INFO{Style.RESET_ALL} ] Waktu Panen Selanjutnya: {colortime}{time_format}{Style.RESET_ALL}", end='')
        time.sleep(1)
        remaining_seconds -= 1
    print()

def panen(plantId, landId, access_token):
    url = "https://api.catopia.io/api/v1/players/plant/harvest"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; Nexus 5 Build/N2G47H; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/81.0.4044.117 Mobile Safari/537.36",
        "Content-Type": "application/json; charset=UTF-8",
        "Accept": "*/*",
        "Origin": "https://build.catopia.io",
        "X-Requested-With": "tw.nekomimi.nekogram",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://build.catopia.io/",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en,en-GB;q=0.9,en-US;q=0.8"
    }
    data = {
        "plantId": plantId,
        "landId": landId
    }
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 201:
        print(f"[ {Fore.LIGHTYELLOW_EX}INFO{Style.RESET_ALL} ] Panen berhasil untuk plantId {plantId} di landId {landId}")
        cek_tanah(access_token)
    else:
        main()

def beli_benih(access_token):
    url = "https://api.catopia.io/api/v1/store/buy"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; Nexus 5 Build/N2G47H; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/81.0.4044.117 Mobile Safari/537.36",
        "Content-Type": "application/json; charset=UTF-8",
        "Accept": "*/*",
        "Origin": "https://build.catopia.io",
        "X-Requested-With": "tw.nekomimi.nekogram",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://build.catopia.io/",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en,en-GB;q=0.9,en-US;q=0.8"
    }
    data = {
        "storeId": 17,
        "price": 16000.0,
        "unit": 1
    }
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 201:
        print(f"[ {Fore.LIGHTYELLOW_EX}INFO{Style.RESET_ALL} ] Pembelian benih berhasil")
        cek_tanaman(access_token)
    else:
        main()

def cek_tanah(access_token):
    url = "https://api.catopia.io/api/v1/players/land?limit=3000"
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; Nexus 5 Build/N2G47H; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/81.0.4044.117 Mobile Safari/537.36",
        "Content-Type": "application/json; charset=UTF-8",
        "Accept": "*/*",
        "Origin": "https://build.catopia.io",
        "X-Requested-With": "tw.nekomimi.nekogram",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://build.catopia.io/",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en,en-GB;q=0.9,en-US;q=0.8"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json().get('data', {})
        empty_land = data.get('emptyLand', [])
        occupied_land = data.get('occupiedLand', [])
        
        ids_grownAt = [{'id': land['id'], 'plantId': land.get('plantId'), 'plantName': land['plantName'], 'grownAt': land['grownAt']} for land in occupied_land]
        
        for item in ids_grownAt:
            clear_console()
            results(access_token)
            claim(access_token)
            id_value = item.get('id', 'empty')
            plant_name = item.get('plantName', 'empty')
            for _ in range(len(ids_grownAt)):
              print(f"[ {Fore.LIGHTYELLOW_EX}INFO{Style.RESET_ALL} ] Id: {Fore.LIGHTMAGENTA_EX}{id_value}{Style.RESET_ALL} | Jenis: {Fore.LIGHTMAGENTA_EX}{plant_name}{Style.RESET_ALL}")
            
            item['grownAt'] = ubah_ke_wib(item['grownAt'])
            status, *rest = cek_panen(item['grownAt'])
            
            if status == "Siap Panen":
                print(f"[ {Fore.LIGHTBLUE_EX}INFO{Style.RESET_ALL} ] Saatnya Panen")
                panen(item['plantId'], item['id'], access_token)
            else:
                process_chests(access_token)
                remaining_seconds = rest[0]
                display_countdown(remaining_seconds)
                cek_tanah(access_token)
                return
                
        if empty_land:
            print(f"[ {Fore.LIGHTYELLOW_EX}INFO{Style.RESET_ALL} ] Jumlah tanah kosong: {len(empty_land)}")
            print(f"[ {Fore.LIGHTBLUE_EX}INFO{Style.RESET_ALL} ] Menanam Benih.....")
            for _ in empty_land:
                cek_tanaman(access_token)
    else:
        main()

def menanam(plantId, access_token):
    url = "https://api.catopia.io/api/v1/players/plant"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; Nexus 5 Build/N2G47H; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/81.0.4044.117 Mobile Safari/537.36",
        "Content-Type": "application/json; charset=UTF-8",
        "Accept": "*/*",
        "Origin": "https://build.catopia.io",
        "X-Requested-With": "tw.nekomimi.nekogram",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://build.catopia.io/",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en,en-GB;q=0.9,en-US;q=0.8"
    }
    empty_land_url = "https://api.catopia.io/api/v1/players/land?limit=3000"
    empty_land_response = requests.get(empty_land_url, headers=headers)
    
    if empty_land_response.status_code == 200:
        empty_land_data = empty_land_response.json().get('data', {}).get('emptyLand', [])
        if empty_land_data:
            for land in empty_land_data:
                landId = land.get('id')
                data = {
                    "plantId": plantId,
                    "landId": landId
                }
                response = requests.post(url, headers=headers, json=data)
                if response.status_code == 201:
                    print(f"[ {Fore.LIGHTYELLOW_EX}INFO{Style.RESET_ALL} ] Penanaman berhasil untuk plantId {plantId} di landId {landId}")
                else:
                    cek_tanaman(access_token)
            cek_tanah(access_token)
        else:
            print(f"[ {Fore.LIGHTYELLOW_EX}INFO{Style.RESET_ALL} ] Tidak ada tanah kosong untuk penanaman.")
            cek_tanah(access_token)
    else:
        main()

def cek_data_user(access_token):
    url = "https://api.catopia.io/api/v1/user/me?limit=3000"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; Nexus 5 Build/N2G47H; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/81.0.4044.117 Mobile Safari/537.36",
        "Accept": "*/*",
        "Origin": "https://build.catopia.io",
        "X-Requested-With": "tw.nekomimi.nekogram",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://build.catopia.io/",
        "Accept-Language": "en,en-GB;q=0.9,en-US;q=0.8",
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
      response.raise_for_status()
      return response.json()
    
    else:
         main()

def cek_coin(access_token):
    url = "https://api.catopia.io/api/v1/user-collection?limit=3000"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; Nexus 5 Build/N2G47H; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/81.0.4044.117 Mobile Safari/537.36",
        "Accept": "*/*",
        "Origin": "https://build.catopia.io",
        "X-Requested-With": "tw.nekomimi.nekogram",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://build.catopia.io/",
        "Accept-Language": "en,en-GB;q=0.9,en-US;q=0.8",
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
      response.raise_for_status()
      return response.json()
    
    else:
         main()
    
def results(access_token):
    data_user_response = cek_data_user(access_token)
    coin_response = cek_coin(access_token)
    full_name = data_user_response.get('data', {}).get('fullName')
    level = data_user_response.get('data', {}).get('level')
    golden_coin = coin_response.get('data', {}).get('goldenCoin')
    gem = coin_response.get('data', {}).get('gem')
    separator = '=' * len(full_name)

    welcome()
    print(f"{Fore.LIGHTCYAN_EX}=========={full_name}=========={Style.RESET_ALL}")
    print(f"Balance: {Fore.LIGHTGREEN_EX}{golden_coin}{Style.RESET_ALL}")
    print(f"Diamond: {Fore.LIGHTGREEN_EX}{gem}{Style.RESET_ALL}")
    print(f"Level: {Fore.LIGHTGREEN_EX}{level}{Style.RESET_ALL}")
    print(f"{Fore.LIGHTCYAN_EX}===================={separator}{Style.RESET_ALL}")

def claim(access_token):
    url = "https://api.catopia.io/api/v1/user-collection/claim-gold"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; Nexus 5 Build/N2G47H; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/81.0.4044.117 Mobile Safari/537.36",
        "Content-Type": "application/json; charset=UTF-8",
        "Accept": "*/*",
        "Origin": "https://build.catopia.io",
        "X-Requested-With": "tw.nekomimi.nekogram",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://build.catopia.io/",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en,en-GB;q=0.9,en-US;q=0.8"
    }
    
    response = requests.post(url, headers=headers)
    if response.status_code == 201:
      print(f"[ {Fore.LIGHTYELLOW_EX}INFO{Style.RESET_ALL} ] {Fore.LIGHTGREEN_EX}Success Claim Gold{Style.RESET_ALL}")
    else:
      print(f"[ {Fore.LIGHTYELLOW_EX}INFO{Style.RESET_ALL} ] {Fore.LIGHTRED_EX}Gagal Claim Gold{Style.RESET_ALL}")

def use_boost(access_token):
    url = "https://api.catopia.io/api/v1/players/boost"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; Nexus 5 Build/N2G47H; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/81.0.4044.117 Mobile Safari/537.36",
        "Content-Type": "application/json; charset=UTF-8",
        "Accept": "*/*",
        "Origin": "https://build.catopia.io",
        "X-Requested-With": "tw.nekomimi.nekogram",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://build.catopia.io/",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en,en-GB;q=0.9,en-US;q=0.8"
    }
    payload = {
        "boostId": 1
    }
    
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 201:
      print(f"[ {Fore.LIGHTYELLOW_EX}INFO{Style.RESET_ALL} ] {Fore.LIGHTGREEN_EX}Success Menggunakan Booster{Style.RESET_ALL}")
    else:
      print(f"[ {Fore.LIGHTYELLOW_EX}INFO{Style.RESET_ALL} ] {Fore.LIGHTRED_EX}Gagal Menggunakan Booster{Style.RESET_ALL}")

def cek_chest(access_token):
    url = "https://api.catopia.io/api/v1/players/chest"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; K) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/81.0.4044.117 Mobile Safari/537.36",
        "Content-Type": "application/json; charset=UTF-8",
        "Accept": "*/*",
        "Origin": "https://build.catopia.io",
        "X-Requested-With": "org.telegram.messenger.web",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://build.catopia.io/",
        "Accept-Language": "en,id-ID;q=0.9,id;q=0.8,en-US;q=0.7"
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json().get('data', [])
        else:
            print(f"[ {Fore.LIGHTYELLOW_EX}INFO{Style.RESET_ALL} ] Failed to retrieve chest information. Status code: {response.status_code}{Style.RESET_ALL}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"[ {Fore.RED+Style.BRIGHT}ERROR{Style.RESET_ALL} ] An error occurred while checking chest: {Fore.RED+Style.BRIGHT}{e}{Style.RESET_ALL}")
        return []

def open_chest(access_token, chest_ids):
    url = "https://api.catopia.io/api/v1/chest/open-multiple"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; K) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/81.0.4044.117 Mobile Safari/537.36",
        "Content-Type": "application/json; charset=UTF-8",
        "Accept": "*/*",
        "Origin": "https://build.catopia.io",
        "X-Requested-With": "org.telegram.messenger.web",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://build.catopia.io/",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en,id-ID;q=0.9,id;q=0.8,en-US;q=0.7"
    }
    data = {
        "petTypeIds": [1],  # Sesuaikan `petTypeIds` jika diperlukan
        "chestIds": chest_ids
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 201:
            print(f"[ {Fore.LIGHTYELLOW_EX}INFO{Style.RESET_ALL} ] Successfully opened chests: {Fore.LIGHTGREEN_EX}{chest_ids}{Style.RESET_ALL}")
        else:
            print(f"[ {Fore.LIGHTYELLOW_EX}INFO{Style.RESET_ALL} ] Failed to open chests. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"[ {Fore.RED+Style.BRIGHT}ERROR{Style.RESET_ALL} ] An error occurred while opening chests: {Fore.RED+Style.BRIGHT}{e}{Style.RESET_ALL}")

def cek_pet(access_token):
    url = "https://api.catopia.io/api/v1/players/pet"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; K) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/81.0.4044.117 Mobile Safari/537.36",
        "Content-Type": "application/json; charset=UTF-8",
        "Accept": "*/*",
        "Origin": "https://build.catopia.io",
        "X-Requested-With": "org.telegram.messenger.web",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://build.catopia.io/",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en,id-ID;q=0.9,id;q=0.8,en-US;q=0.7"
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            pets = response.json().get('data', [])
            level_count = Counter([pet['level'] for pet in pets])
            level_str = " | ".join(f"Pet Level {Fore.LIGHTBLUE_EX}{level}{Style.RESET_ALL}: {Fore.LIGHTBLUE_EX}{count}{Style.RESET_ALL}" for level, count in sorted(level_count.items()))
            print(f"[ {Fore.LIGHTYELLOW_EX}INFO{Style.RESET_ALL} ] {level_str}")
        else:
            print(f"[ {Fore.LIGHTYELLOW_EX}INFO{Style.RESET_ALL} ] Failed to retrieve pet information. Status code: {Fore.RED+Style.BRIGHT}{response.status_code}{Style.RESET_ALL}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"[ {Fore.RED+Style.BRIGHT}ERROR{Style.RESET_ALL} ] An error occurred while checking pet: {Fore.RED+Style.BRIGHT}{e}{Style.RESET_ALL}")
        return []

def upgrade_pet(access_token):
    url = "https://api.catopia.io/api/v1/players/pet/fast-upgrade"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; K) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/81.0.4044.117 Mobile Safari/537.36",
        "Content-Type": "application/json; charset=UTF-8",
        "Accept": "*/*",
        "Origin": "https://build.catopia.io",
        "X-Requested-With": "org.telegram.messenger.web",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://build.catopia.io/",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en,id-ID;q=0.9,id;q=0.8,en-US;q=0.7"
    }
    data = {
        "level": 1,
        "petTypeId": 1
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response_json = response.json()
        if response.status_code == 201:
            upgrade_items = response_json.get('data', {}).get('upgradeItem', [])
            level_count = Counter(item['level'] for item in upgrade_items)
            
            # Format output
            level_str = " | ".join(f"{Fore.LIGHTYELLOW_EX}{count}{Style.RESET_ALL} Pet ke Level {Fore.LIGHTYELLOW_EX}{level}{Style.RESET_ALL}" for level, count in sorted(level_count.items()))
            print(f"[ {Fore.LIGHTYELLOW_EX}INFO{Style.RESET_ALL} ] Berhasil Upgrade {level_str}")
        else:
            print(f"[ {Fore.LIGHTYELLOW_EX}INFO{Style.RESET_ALL} ] Failed to upgrade pet. Status code: {Fore.RED+Style.BRIGHT}{response.status_code}{Style.RESET_ALL}")
    except requests.exceptions.RequestException as e:
        print(f"[ {Fore.RED+Style.BRIGHT}ERROR{Style.RESET_ALL} ] An error occurred while upgrading pet: {Fore.RED+Style.BRIGHT}{e}{Style.RESET_ALL}")

def buy(access_token):
    url = "https://api.catopia.io/api/v1/store/buy"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; K) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/81.0.4044.117 Mobile Safari/537.36",
        "Content-Type": "application/json; charset=UTF-8",
        "Accept": "*/*",
        "Origin": "https://build.catopia.io",
        "X-Requested-With": "org.telegram.messenger.web",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://build.catopia.io/",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en,id-ID;q=0.9,id;q=0.8,en-US;q=0.7"
    }
    data = {
        "storeId": 4,
        "price": 60000,
        "unit": 1
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 401:
            time.sleep(10)
            main()
    except requests.exceptions.RequestException as e:
        print(f"[ {Fore.RED+Style.BRIGHT}ERROR{Style.RESET_ALL} ] An error occurred while buy pet: {Fore.RED+Style.BRIGHT}{e}{Style.RESET_ALL}")

def process_chests(access_token):
    while True:
        chest_data = cek_chest(access_token)
        
        # Ambil maksimal 10 chest ids per iterasi
        chest_ids = [chest['id'] for chest in chest_data[:10]]
        
        if not chest_ids:
            print(f"[ {Fore.LIGHTYELLOW_EX}INFO{Style.RESET_ALL} ] No more chests to open...")
            print(f"[ {Fore.LIGHTYELLOW_EX}INFO{Style.RESET_ALL} ] Process buy chests...")
            for _ in range(4):
                buy(access_token)
            break

        # Buka chest yang ditemukan
        open_chest(access_token, chest_ids)

    # Cek dan upgrade pet setelah membuka chests
    cek_pet(access_token)
    upgrade_pet(access_token)

def main():
    init()
    clear_console()
    welcome()
    print(f"[ {Fore.LIGHTYELLOW_EX}INFO{Style.RESET_ALL} ] Login...")
    if len(sys.argv) > 1:
        query = sys.argv[1]
        access_token = login(query)
        if access_token:
            print(f"[ {Fore.LIGHTYELLOW_EX}INFO{Style.RESET_ALL} ] Berhasil login, cek tanaman...")
            cek_tanaman(access_token)
        else:
            print(f"[ {Fore.LIGHTYELLOW_EX}INFO{Style.RESET_ALL} ] Login gagal. Mengulangi...")
            time.sleep(10)
            main()

if __name__ == "__main__":
    while True:
        try:
            main()
        except KeyboardInterrupt:
            print(f"\n[ {Fore.RED+Style.BRIGHT}ERROR{Style.RESET_ALL} ] Proses dihentikan paksa oleh anda!!")
            break
        except Exception as e:
            print(f"[ {Fore.RED}Error{Style.RESET_ALL} ] {e}. Mengulangi...")
            time.sleep(10)
            