import os
import pandas as pd
import argparse
from urllib.parse import urlparse

subdomains_filename = "subdomains"
domains_filename = "domains"


class Color:
    RESET = '\033[0m'
    RED = '\033[91m'
    WHITE = '\033[97m'

    
def banner():
    os.system("clear")
    print(f"{Color.RED}thrizz shmk\n\n{Color.RESET}")


def remove_files():
    file_path = os.path.join(os.getcwd(), subdomains_filename)
    if os.path.exists(file_path):
        os.remove(file_path)

    file_path = os.path.join(os.getcwd(), domains_filename)
    if os.path.exists(file_path):
        os.remove(file_path)


def clean_and_add_subdomain(subdomain):
    cleaned_subdomain = subdomain.lstrip("*.")
    with open(subdomains_filename, "a") as subdomains:
        subdomains.write(cleaned_subdomain + "\n")


def get_root_domain(url):
    parts = urlparse(url).hostname.split('.') if urlparse(url).hostname else url.split('.')
    return '.'.join(parts[-2:])


def is_subdomain(url, root_domain):
    parsed_url = urlparse(url)
    hostname = parsed_url.hostname or url
    return hostname != root_domain and hostname.endswith(root_domain) and not hostname.startswith("*.") and not hostname.startswith("www.")


def count_domains_and_subdomains(file_path):
    remove_files()
    subdomains_count = 0
    domains_count = 0
    subdomains_file = False
    domains_file = False

    try:
        dados = pd.read_csv(file_path)

        for index, row in dados.iterrows():
            if row["asset_type"] == "URL" and row["eligible_for_submission"] == True:
                url = row["identifier"]
                root_domain = get_root_domain(url)
                
                if is_subdomain(url, root_domain):
                    print(f"{Color.RED}[+]{Color.RESET} Subdomain: {url} {Color.RESET}")
                    clean_and_add_subdomain(url)
                    subdomains_count += 1
                    subdomains_file = True
                elif url == root_domain or url.startswith("www." + root_domain):
                    with open(domains_filename, "a") as domains:
                        print(f"{Color.RED}[+]{Color.RESET} Domain: {url} {Color.RESET}")
                        domains.write(url + '\n')
                        domains_count += 1
                        domains_file = True

        if subdomains_count + domains_count == 0:
            print("No domains or subdomains found in the CSV file.")
        else:
            print(f"\n{Color.RED}[+] {Color.WHITE}{subdomains_count}{Color.RED} subdomains and {Color.WHITE}{domains_count}{Color.RED} domains extracted. [+]{Color.RESET}")

        if subdomains_file and domains_file:
            print(f"{Color.RED}[+] {Color.WHITE}{domains_filename}{Color.RED} and {Color.WHITE}{subdomains_filename}{Color.RED} file created. [+] {Color.RESET}")
        elif subdomains_file:
            print(f"{Color.RED}[+] {Color.WHITE}{subdomains_filename}{Color.RED} file created. [+] {Color.RESET}")
        elif domains_file:
            print(f"{Color.RED}[+] {Color.WHITE}{domains_filename}{Color.RED} file created. [+] {Color.RESET}")

    except pd.errors.EmptyDataError:
        print("The CSV file is empty.")
    except pd.errors.ParserError:
        print("Error parsing the CSV file. Check the format.")


def main():
    banner()
    parser = argparse.ArgumentParser(
        prog="rizz",
    )
    parser.add_argument("-f", "--file", help="Path to the CSV file.")
    args = parser.parse_args()

    if args.file:
        count_domains_and_subdomains(args.file)
    else:
        print("No CSV file provided. Use the -f option to specify the file path.")


if __name__ == "__main__":
    main()
