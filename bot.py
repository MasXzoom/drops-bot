import requests
import time
from colorama import init, Fore
import sys

init(autoreset=True)

def display_author():
    secret_author = "JUANGUSTAVVO"
    if secret_author != "JUANGUSTAVVO":
        sys.exit()
    print(Fore.LIGHTCYAN_EX + secret_author)
    print(Fore.LIGHTCYAN_EX + "This script is locked by the author and cannot be changed.\n")

def claim_quest(token, quest_id):
    url = f"https://api.miniapp.dropstab.com/api/quest/{quest_id}/claim"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept-Language": "en-US,en;q=0.9",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.6668.71 Safari/537.36",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    response = requests.put(url, headers=headers)
    if response.status_code == 200:
        result = response.json()
        print(Fore.GREEN + f"Quest {quest_id} claim status: {result.get('status')}")
    else:
        print(Fore.LIGHTRED_EX + f"Failed to claim quest {quest_id}. Status code: {response.status_code}")
        print(f"Response body: {response.text}")

def verify_and_complete_quest(token, quest_id):
    url = f"https://api.miniapp.dropstab.com/api/quest/{quest_id}/verify"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept-Language": "en-US,en;q=0.9",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.6668.71 Safari/537.36",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    response = requests.put(url, headers=headers)
    if response.status_code == 200:
        result = response.json()
        print(Fore.CYAN + f"Quest {quest_id} verification status: {result.get('status')}")
    else:
        print(Fore.LIGHTRED_EX + f"Failed to verify quest {quest_id}. Status code: {response.status_code}")
        print(f"Response body: {response.text}")

def get_quests(token):
    url = "https://api.miniapp.dropstab.com/api/quest"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept-Language": "en-US,en;q=0.9",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.6668.71 Safari/537.36",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(Fore.LIGHTRED_EX + f"Failed to get quests. Status code: {response.status_code}")
        return []

def countdown_timer(seconds):
    while seconds:
        hrs, secs_rem = divmod(seconds, 3600)
        mins, secs = divmod(secs_rem, 60)
        print(Fore.YELLOW + f"\rWaiting {hrs:02}:{mins:02}:{secs:02} before starting auto-claim...", end="")
        time.sleep(1)
        seconds -= 1
    print("\n")

def process_quests_for_account(token):
    quests = get_quests(token)
    for quest_group in quests:
        for quest in quest_group.get("quests", []):
            if quest['status'] == 'NEW':
                print(Fore.GREEN + f"Processing NEW quest: {quest['id']} - {quest['name']}")
                time.sleep(2)
                verify_and_complete_quest(token, quest['id'])
                time.sleep(2)
            else:
                print(Fore.LIGHTMAGENTA_EX + f"Skipping quest {quest['id']}, status: {quest['status']}")

def claim_quests_for_account(token):
    quests = get_quests(token)
    for quest_group in quests:
        for quest in quest_group.get("quests", []):
            if quest['status'] == 'NEW':
                claim_quest(token, quest['id'])
                time.sleep(2)

def load_tokens_from_file(filename):
    with open(filename, "r") as file:
        return [line.strip() for line in file.readlines()]

def get_user_info(token):
    url = "https://api.miniapp.dropstab.com/api/user/current"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept-Language": "en-US,en;q=0.9",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.6668.71 Safari/537.36",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        user_data = response.json()
        username = user_data.get('tgUsername', 'Unknown User')
        balance = user_data.get('balance', 'Unknown Balance')
        return username, balance
    else:
        print(Fore.LIGHTRED_EX + f"Failed to get user info. Status code: {response.status_code}")
        return None, None

def process_all_tasks_for_all_accounts(token_file):
    tokens = load_tokens_from_file(token_file)
    for token in tokens:
        username, balance = get_user_info(token)
        if username and balance:
            print(Fore.LIGHTBLUE_EX + f"\nProcessing account: {username} | Balance: {balance}\n")
            process_quests_for_account(token)
        else:
            print(Fore.LIGHTRED_EX + f"\nSkipping account due to missing user info.\n")

def claim_all_quests_for_all_accounts(token_file):
    tokens = load_tokens_from_file(token_file)
    for token in tokens:
        username, balance = get_user_info(token)
        if username and balance:
            print(Fore.LIGHTBLUE_EX + f"\nClaiming quests for account: {username} | Balance: {balance}\n")
            claim_quests_for_account(token)
        else:
            print(Fore.LIGHTRED_EX + f"\nSkipping account due to missing user info.\n")

if __name__ == "__main__":
    display_author()
    token_file = "token.txt"
    process_all_tasks_for_all_accounts(token_file)
    countdown_timer(600)
    claim_all_quests_for_all_accounts(token_file)
