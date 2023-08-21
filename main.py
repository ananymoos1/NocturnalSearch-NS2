import os 
import threading
import requests
import random
from dhooks import Webhook, Embed
import ctypes

# Initialize the Discord webhook
webhook_url = my_secret = os.environ['NS2']
hook = Webhook(webhook_url)

# Set the number of threads
threads = 20

# Read proxies from the "proxies.txt" file
with open("proxies.txt") as file:
    proxy_list = [line.strip() for line in file]

# A function to create and send an embed to the webhook
def send_embed(group_id, group_name):
    embed = Embed(
        title="Roblox Group Found!",
        description=f"A new group has been found: [Group Link](https://www.roblox.com/groups/group.aspx?gid={group_id})",
        color=0x00ff00  # Green color
    )
    embed.add_field(name="Group ID", value=str(group_id), inline=True)
    embed.add_field(name="Group Name", value=group_name, inline=True)
    embed.set_footer(text="NocturnalSearch | cyberconnect.tech")

    hook.send(embed=embed)

# A function to perform the group search
def groupfinder():
    while True:
        try:
            # Generate a random group ID
            id = random.randint(1000000, 1150000)

            # Choose a random proxy from the list
            proxy = {'http': random.choice(proxy_list)}

            # Make a request to check the group's availability
            r = requests.get(f"https://www.roblox.com/groups/group.aspx?gid={id}", proxies=proxy)

            if 'owned' not in r.text:
                re = requests.get(f"https://groups.roblox.com/v1/groups/{id}", proxies=proxy)
                group_data = re.json()

                if 'isLocked' not in group_data and 'owner' in group_data:
                    if group_data['publicEntryAllowed'] and group_data['owner'] is None:
                        group_name = group_data.get('name', 'Unknown Group')
                        send_embed(id, group_name)
                        print(f"[+] Hit: {id} - {group_name}")
                    else:
                        print(f"[-] No Entry Allowed: {id}")
                else:
                    print(f"[-] Group Locked: {id}")
            else:
                print(f"[-] Group Already Owned: {id}")

        except Exception as e:
            print(f"[-] An error occurred: {e}")

# Start the threads
for _ in range(threads):
    threading.Thread(target=groupfinder).start()