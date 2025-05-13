import subprocess, time
from colorama import Fore as f
from colorama import init

init()

print(f.LIGHTGREEN_EX + "")  # LightGreen Console colour
# Current User Profile
data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8', errors='ignore').split('\n')
profiles = [i.split(":")[1][1:-1] for i in data if "Current User Profile" in i]

for i in profiles:
    results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear']).decode('utf-8', errors='ignore').split('\n')
    results = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]

    auth = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear']).decode('utf-8', errors='ignore').split('\n')
    auth = [c.split(":")[1][1:-1] for c in auth if "Authentication" in c]

    cipher = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear']).decode('utf-8', errors='ignore').split('\n')
    cipher = [d.split(":")[1][1:-1] for d in cipher if "Cipher" in d]

    ssid = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear']).decode('utf-8', errors='ignore').split('\n')
    ssid = [e.split(":")[1][1:-1] for e in ssid if "SSID name" in e]

    try:
        print("+----------------+-------------------+------------------+---------------+----------------+")
        print("|  Name          |  SSID             |  Authentication  |  Encryption   |  Password      |")
        print("+----------------+-------------------+------------------+---------------+----------------+")
        print(f.LIGHTYELLOW_EX + "")
        print("{:>0}|  {:<}".format("", i), end="")
        print("{:>4}| {:<}".format("", ssid[0]), end="")
        print("{:>6}| {:<}".format("", auth[0]), end="")
        print("{:>4}| {:<}".format("", cipher[0]), end="")
        print("{:>10}| {:<}".format("", results[0]))
        print(f.LIGHTGREEN_EX + "")
    except IndexError:
        print("{:<15}:    {:<}".format(i, "Error"))

time.sleep(1)

# All User Profiles
data2 = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8', errors='ignore').split('\n')
profiles2 = [i.split(":")[1][1:-1] for i in data2 if "All User Profile" in i]

for i in profiles2:
    results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear']).decode('utf-8', errors='ignore').split('\n')
    results = [x.split(":")[1][1:-1] for x in results if "Key Content" in x]

    auth = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear']).decode('utf-8', errors='ignore').split('\n')
    auth = [y.split(":")[1][1:-1] for y in auth if "Authentication" in y]

    cipher = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear']).decode('utf-8', errors='ignore').split('\n')
    cipher = [z.split(":")[1][1:-1] for z in cipher if "Cipher" in z]

    ssid = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear']).decode('utf-8', errors='ignore').split('\n')
    ssid = [w.split(":")[1][1:-1] for w in ssid if "SSID name" in w]

    try:
        print(f.LIGHTGREEN_EX + "")
        print("\n+----------------+-------------------+------------------+---------------+----------------+")
        print("|  Name          |  SSID             |  Authentication  |  Encryption   |  Password      |")
        print("+----------------+-------------------+------------------+---------------+----------------+")
        print(f.LIGHTYELLOW_EX + "")
        print("{:>0}|  {:<}".format("", i), end="")
        print("{:>4}| {:<}".format("", ssid[0]), end="")
        print("{:>6}| {:<}".format("", auth[0]), end="")
        print("{:>4}| {:<}".format("", cipher[0]), end="")
        print("{:>10}| {:<}".format("", results[0]))
        print("")
        print(f.LIGHTGREEN_EX + "")
    except IndexError:
        print("{:<15}:    {:<}".format(i, "Error"))

input("\nExit >")
