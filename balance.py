import requests
from colorama import Fore, Style, init

init(autoreset=True)

def get_token_balance(bearer):
    url = "https://api.hamsterkombatgame.io/interlude/sync"
    headers = {
        "Authorization": f"Bearer {bearer}",
        "Content-Length": "0",
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0"
    }
    
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        token_balance = data.get("interludeUser", {}).get("tokenBalance", {})
        total = token_balance.get("total", None)
        unclaimed = token_balance.get("unclaimed", None)
        next_unlocked = token_balance.get("nextUnlocked", None)
        return total, unclaimed, next_unlocked
    else:
        print(f"{Fore.RED}Error fetching token balance for bearer {bearer}")
        return None, None, None

def get_account_info(bearer):
    url = "https://api.hamsterkombatgame.io/auth/account-info"
    headers = {
        "Authorization": f"Bearer {bearer}",
        "Content-Length": "0",
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        name = data.get("accountInfo", {}).get("name", "Unknown")
        return name
    else:
        print(f"{Fore.RED}Error fetching account info for bearer {bearer}")
        return None

def format_number(value):
    return f"{value/1e9:,.9f}" if value is not None else "N/A"

def display_account_info():
    total_all = 0
    unclaimed_all = 0
    next_unlocked_all = 0
    account_count = 0

    with open("bearer.txt", "r") as file:
        bearers = file.readlines()

    print(f"{Fore.CYAN}{'='*50}")
    print(f"{Fore.GREEN}{'Airdrop Allocation Check HamsterKombat'}")
    print(f"{Fore.CYAN}{'='*50}")
    
    for bearer in bearers:
        bearer = bearer.strip()
        name = get_account_info(bearer)
        total, unclaimed, next_unlocked = get_token_balance(bearer)

        if name:
            if total is None or unclaimed is None or next_unlocked is None:
                print(f"{Fore.RED}Nama Akun: {Fore.WHITE}{name}")
                print(f"  {Fore.RED}You've been cheating this season!")
                print(f"{Fore.CYAN}{'-'*50}")
                continue
            
            account_count += 1
            total_all += total
            unclaimed_all += unclaimed
            next_unlocked_all += next_unlocked

            print(f"{Fore.YELLOW}Nama Akun: {Fore.WHITE}{name}")
            print(f"  {Fore.GREEN}Total:        {Fore.WHITE}{format_number(total)}")
            print(f"  {Fore.GREEN}Unclaimed:    {Fore.WHITE}{format_number(unclaimed)}")
            print(f"  {Fore.GREEN}Next Unlocked:{Fore.WHITE}{format_number(next_unlocked)}")
            print(f"{Fore.CYAN}{'-'*50}")

    print(f"{Fore.CYAN}{'='*50}")
    print(f"{Fore.GREEN}Jumlah Akun: {Fore.WHITE}{account_count}")
    print(f"{Fore.CYAN}{'='*50}")
    print(f"{Fore.GREEN}Total Keseluruhan:")
    print(f"  {Fore.BLUE}Total:        {Fore.WHITE}{format_number(total_all)}")
    print(f"  {Fore.BLUE}Unclaimed:    {Fore.WHITE}{format_number(unclaimed_all)}")
    print(f"  {Fore.BLUE}Next Unlocked:{Fore.WHITE}{format_number(next_unlocked_all)}")
    print(f"{Fore.CYAN}{'='*50}")

if __name__ == "__main__":
    display_account_info()
