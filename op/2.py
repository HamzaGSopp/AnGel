import os
import requests
from datetime import datetime, timezone
from colorama import init, Fore, Style

init(autoreset=True)

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def rgb_to_colorama(rgb):
    return f"\x1b[38;2;{rgb[0]};{rgb[1]};{rgb[2]}m"

def generate_gradient_line(width, start_rgb, end_rgb):
    gradient = []
    for i in range(width):
        r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * (i / (width - 1)))
        g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * (i / (width - 1)))
        b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * (i / (width - 1)))
        gradient.append(rgb_to_colorama((r, g, b)))
    return gradient

def apply_gradient(text, gradient):
    colored_text = []
    gradient_length = len(gradient)
    for i, char in enumerate(text):
        colored_text.append(gradient[i % gradient_length] + char)
    return ''.join(colored_text) + Fore.RESET

def format_info(title, value, gradient):
    gradient_title = apply_gradient(title, gradient)
    return f"{gradient_title} {Fore.WHITE}{value}"

def display_discord_info(invite_link):
    gradient_colors = ((255, 105, 180), (0, 0, 255))
    gradient = generate_gradient_line(20, gradient_colors[0], gradient_colors[1])
    

    try:
        res = requests.get(f"https://discord.com/api/v9/invites/{invite_link}")
        res.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        input("\nPress ENTER to return to the main menu")
        main()

    try:
        res_json = res.json()
    except ValueError as e:
        print(f"Error: Invalid JSON response ({e})")
        input("\nPress ENTER to return to the main menu")
        main()

    if "code" not in res_json or "channel" not in res_json or "guild" not in res_json:
        print("Error: Missing necessary data in the response")
        input("\nPress ENTER to return to the main menu")
        main()

    print("\nInvitation Information:")
    print(f"Invite Link: https://discord.gg/{res_json.get('code', 'N/A')}")
    print(f"Channel: {res_json.get('channel', {}).get('name', 'Unknown')} ({res_json.get('channel', {}).get('id', 'Unknown')})")
    print(f"Expiration Date: {res_json.get('expires_at', 'Never')}\n")

    print("Inviter Information:")
    inviter = res_json.get("inviter", {})
    print(f"Username: {inviter.get('username', 'Unknown')}#{inviter.get('discriminator', '0000')}")
    print(f"User ID: {inviter.get('id', 'Unknown')}\n")

    print("Server Information:")
    guild = res_json.get("guild", {})
    print(f"Name: {guild.get('name', 'Unknown')}")
    print(f"Server ID: {guild.get('id', 'Unknown')}")
    print(f"Banner: {guild.get('banner', 'None')}")
    print(f"Description: {guild.get('description', 'No description')}")
    print(f"Custom Invite Link: {guild.get('vanity_url_code', 'None')}")
    print(f"Verification Level: {guild.get('verification_level', 'Unknown')}")
    print(f"Splash: {guild.get('splash', 'None')}")
    print(f"Features: {', '.join(guild.get('features', []))}")

    input(apply_gradient("Press Enter to return to the main menu...", gradient))
    clear_console()

def main():
    clear_console()
    gradient_colors = ((255, 105, 180), (0, 0, 255))
    gradient = generate_gradient_line(20, gradient_colors[0], gradient_colors[1])
    invite_link = input(apply_gradient("Enter Server Invite (Only what is after the .gg/):", gradient))
    clear_console()
    display_discord_info(invite_link)

if __name__ == "__main__":
    main()