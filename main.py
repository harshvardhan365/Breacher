import requests
import subprocess
from tabulate import tabulate
# Output Colours
class c:
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    UNDERLINE = '\033[4m'

# ANSI color codes
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
END = '\033[0m'

# Function to load breached emails from a file
def load_breached_emails(filename):
    breached_emails = {}
    with open(filename, 'r', encoding='utf-8', errors='replace') as file:
        for line in file:
            parts = line.strip().split(':')
            if len(parts) >= 9:
                email = parts[0]
                password = parts[1]
                breach_date = parts[2]
                address = parts[3]
                phone_number = parts[4]
                gender = parts[5]
                location = parts[6]
                website = parts[7]
                leak_ip = parts[8]

                if email in breached_emails:
                    breached_emails[email].append((password, breach_date, address, phone_number, gender, location, website, leak_ip))
                else:
                    breached_emails[email] = [(password, breach_date, address, phone_number, gender, location, website, leak_ip)]

    return breached_emails

# Your NumVerify API key
api_key = "451ffcc1947a093f571dfbb971f6426c"

# Function to fetch phone number information using NumVerify
def fetch_phone_number_info(phone_number):
    try:
        # Use the global API key
        global api_key
        response = requests.get(f"http://apilayer.net/api/validate?access_key={api_key}&number={phone_number}")

        if response.status_code == 200:
            phone_info = response.json()
            return f"[+] Country Code: {phone_info.get('country_code', 'N/A')}\n" \
                   f"[+] National Number: {phone_info.get('national_number', 'N/A')}\n" \
                   f"[+] International Format: {phone_info.get('international_format', 'N/A')}\n" \
                   f"[+] National Format: {phone_info.get('local_format', 'N/A')}\n" \
                   f"[+] Location: {phone_info.get('location', 'N/A')}\n" \
                   f"[+] ISP: {phone_info.get('carrier', 'N/A')}\n" \
                   f"[+] Line Type: {phone_info.get('line_type', 'N/A')}"
        else:
            return "Phone number information not found."
    except Exception as e:
        return f"Phone number information error - {str(e)}"

# Function to track IP location
def track_ip_location(ip):
    try:
        response = requests.get(f"https://ipinfo.io/{ip}/json")
        if response.status_code == 200:
            ip_info = response.json()
            return f"IP Location: {ip_info.get('city', 'N/A')}, {ip_info.get('region', 'N/A')}, {ip_info.get('country', 'N/A')}\n" \
                f"Latitude/Longitude: {ip_info.get('loc', 'N/A')}\n" \
                f"Timezone: {ip_info.get('timezone', 'N/A')}\n" \
                f"Area Code: {ip_info.get('postal', 'N/A')}\n" \
                f"ISP: {ip_info.get('org', 'N/A')}\n" \
                f"AS Number: {ip_info.get('asn', 'N/A')}"
    except Exception as e:
        return f"IP Location: Error - {str(e)}"

# Modify the function to return all user details
# ... (other code remains the same)

def check_email(email, breached_emails):
    matching_entries = []  # Initialize a list to store matching entries for the email

    for key in breached_emails:
        if email in key:
            matching_entries.extend(breached_emails[key])

    if not matching_entries:
        print(f"{RED}Email not found in the breached list.{END}")
    else:
        print(f"{RED}{email}:{END}")
        match_number = 1
        for data in matching_entries:
            print("-" * 50)
            print(f"{RED}Match {match_number}{END}")
            match_number += 1

            email_output = [
                [f"{YELLOW}Attribute{END}", f"{YELLOW}Value{END}"],
                [f"{RED}Password{END}", f"{GREEN}{data[0]}{END}"],
                [f"{RED}Breach Date{END}", f"{GREEN}{data[1]}{END}"],
                [f"{RED}Address{END}", f"{GREEN}{data[2]}{END}"],
                [f"{RED}Phone Number{END}", f"{GREEN}{data[3]}{END}"],
                [f"{RED}Gender{END}", f"{GREEN}{data[4]}{END}"],
                [f"{RED}Location{END}", f"{GREEN}{data[5]}{END}"],
                [f"{RED}Leaked on Website{END}", f"{GREEN}{data[6]}{END}"],
                [f"{RED}Leak IP{END}", f"{GREEN}{data[7]}{END}"]
            ]

            # Display user details as a table
            print(tabulate(email_output, tablefmt="pretty"))

            if data[7] != "N/A":
                ip_info = track_ip_location(data[7])
                print(f"{YELLOW}" + "-" * 50 + f"{END}")
                print(f"{YELLOW}Fetching IP details{END}")
                print(f"{YELLOW}" + "-" * 50 + f"{END}")
                print(ip_info)

            if data[3] != "N/A":
                phone_info = fetch_phone_number_info(data[3])
                print(f"{YELLOW}" + "-" * 50 + f"{END}")
                print(f"{YELLOW}Fetching phone number information{END}")
                print(f"{YELLOW}" + "-" * 50 + f"{END}")
                print(phone_info)
                

            # Run the "holehe" command here
            try:
                result = subprocess.run(['holehe', email, '--only-used', '--no-clear'], capture_output=True, text=True)
                if result.returncode == 0:
                    # Subprocess executed successfully
                    holehe_output = result.stdout
                    print(f"{YELLOW}" + "-" * 50 + f"{END}")
                    print(f"{YELLOW}Email Used On Website Details:{END}")
                    print(f"{YELLOW}" + "-" * 50 + f"{END}")
                    print(holehe_output)
                else:
                    # Subprocess encountered an error
                    error_message = result.stderr
                    print(f"{RED}Error running 'holehe' subprocess: {error_message}{END}")
            except Exception as e:
                print(f"{RED}Exception during 'holehe' subprocess execution: {str(e)}{END}")

        print(f"{RED}" + "-" * 50 + f"{END}")


# Main function (unchanged)
def main():
    filename = 'breached.txt'
    breached_emails = load_breached_emails(filename)
    print(c.GREEN + '''
-----------------------------------------------------------------------------          
-----------------------------------------------------------------------------                                  
.########..########..########....###.....######..##.....##.########.########.
.##.....##.##.....##.##.........##.##...##....##.##.....##.##.......##.....##
.##.....##.##.....##.##........##...##..##.......##.....##.##.......##.....##
.########..########..######...##.....##.##.......#########.######...########.
.##.....##.##...##...##.......#########.##.......##.....##.##.......##...##..
.##.....##.##....##..##.......##.....##.##....##.##.....##.##.......##....##.
.########..##.....##.########.##.....##..######..##.....##.########.##.....##
-----------------------------------------------------------------------------
                       Developed By Team Breachers 
             Solving email mysteries, uncovering individuals.
-----------------------------------------------------------------------------                  
             ''' + c.END)

    while True:
        email_to_check = input(f"{c.PURPLE}Enter the email address to check (or 0 to exit): {c.END}")

        if email_to_check == '0':
            print(f"{c.RED}Exiting the program.{c.END}")
            break

        check_email(email_to_check, breached_emails)

if __name__ == "__main__":
    main()
