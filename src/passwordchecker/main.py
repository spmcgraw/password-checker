import hashlib
import json
import subprocess
import sys

import requests


def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching: {res.status_code} check the API and check again.')
    return res

def get_password_leaks_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0

def pwned_api_check(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_char)
    return get_password_leaks_count(response, tail)

def get_proton_vault_items(vault):
    try:
        result = subprocess.run(['pass-cli','item','list','--vault-name',vault,'--filter-type','login','--output','json'],
                                capture_output=True,
                                text=True,
                                check=True)
        item_list = json.loads(result.stdout)
        return [{'id': item['id'], 'share_id' : item['share_id'], 'title': item['title']} for item in item_list.get('items', [])]
    except subprocess.CalledProcessError as e:
        print(f'Error calling Proton Pass CLI: {e.stderr}', file=sys.stderr)
        return[]
    except json.JSONDecodeError:
        print('Failed to parse JSON output from CLI') 

def get_proton_passwords(items):
    passwords = []
    for item in items:
        try:
            result = subprocess.run(['pass-cli', 'item', 'view', 'pass://'+item['share_id']+'/'+item['id']+'/'+'password'],
                                    capture_output=True,
                                    text=True,
                                    check=True)
        except subprocess.CalledProcessError as e:
                print(f'Error calling Proton Pass CLI: {e.stderr}', file=sys.stderr)
                continue
        password = result.stdout.strip()
        if password:
            passwords.append({'title': item['title'], 'password': password})
    return passwords

def main():
    items = get_proton_vault_items('Personal')
    password_list = get_proton_passwords(items)
    for password in password_list:
        count = pwned_api_check(password['password'])
        if count:
            print(f'{password['password']} for {password['title']} was found {count} times... you should probably change your password')
        else:
            print(f'{password['password']} was NOT found. Carry on!')
    return 'done!'

if __name__ == '__main__':
    sys.exit(main())