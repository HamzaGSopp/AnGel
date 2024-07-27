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

def display_discord_info(token_discord):
    try:
        headers = {'Authorization': token_discord, 'Content-Type': 'application/json'}
        user = requests.get('https://discord.com/api/v8/users/@me', headers=headers).json()
        r = requests.get('https://discord.com/api/v8/users/@me', headers=headers)

        status = "Valid" if r.status_code == 200 else "Invalid"
        username_discord = user.get('username', "None") + '#' + user.get('discriminator', "None")
        display_name_discord = user.get('global_name', "None")
        user_id_discord = user.get('id', "None")
        email_discord = user.get('email', "None")
        email_verified_discord = str(user.get('verified', "None"))
        phone_discord = str(user.get('phone', "None"))
        mfa_discord = str(user.get('mfa_enabled', "None"))
        country_discord = user.get('locale', "None")

        created_at_discord = "None"
        if 'id' in user:
            created_at_discord = datetime.fromtimestamp(((int(user['id']) >> 22) + 1420070400000) / 1000, timezone.utc)

        nitro_discord = {0: 'False', 1: 'Nitro Classic', 2: 'Nitro Boosts', 3: 'Nitro Basic'}.get(user.get('premium_type'), 'None')

        avatar_url_discord = f"https://cdn.discordapp.com/avatars/{user_id_discord}/{user.get('avatar')}.png"
        if requests.get(avatar_url_discord).status_code != 200:
            avatar_url_discord = "None"

        avatar_discord = user.get('avatar', "None")
        avatar_decoration_discord = str(user.get('avatar_decoration_data', "None"))
        public_flags_discord = str(user.get('public_flags', "None"))
        flags_discord = str(user.get('flags', "None"))
        banner_discord = user.get('banner', "None")
        banner_color_discord = user.get('banner_color', "None")
        accent_color_discord = user.get("accent_color", "None")
        nsfw_discord = str(user.get('nsfw_allowed', "None"))
        linked_users_discord = ' / '.join([str(linked_user) for linked_user in user.get('linked_users', [])]) or "None"
        bio_discord = "\n" + user.get('bio', "None")

        authenticator_types_discord = ' / '.join([str(authenticator_type) for authenticator_type in user.get('authenticator_types', [])]) or "None"

        guilds_response = requests.get('https://discord.com/api/v9/users/@me/guilds?with_counts=true', headers=headers)
        guild_count = "None"
        owner_guild_count = "None"
        owner_guilds_names = "None"

        if guilds_response.status_code == 200:
            guilds = guilds_response.json()
            guild_count = len(guilds)
            owner_guilds = [guild for guild in guilds if guild['owner']]
            owner_guild_count = f"({len(owner_guilds)})"
            owner_guilds_names = "\n" + "\n".join([f"{guild['name']} ({guild['id']})" for guild in owner_guilds])

        billing_discord = requests.get('https://discord.com/api/v6/users/@me/billing/payment-sources', headers=headers).json()
        payment_methods_discord = ' / '.join(['CB' if method['type'] == 1 else 'Paypal' if method['type'] == 2 else 'Other' for method in billing_discord]) or "None"

        friends_response = requests.get('https://discord.com/api/v8/users/@me/relationships', headers=headers)
        friends_discord = "None"

        if friends_response.status_code == 200:
            friends = friends_response.json()
            friends_list = [f"{friend['user']['username']}#{friend['user']['discriminator']} ({friend['user']['id']})" for friend in friends if friend['type'] not in [64, 128, 256, 1048704]]
            friends_discord = ' / '.join(friends_list) or "None"

            with open('friends_list.txt', 'w', encoding='utf-8') as file:
                for friend in friends_list:
                    file.write(friend + '\n')

        gift_codes_response = requests.get('https://discord.com/api/v9/users/@me/outbound-promotions/codes', headers=headers)
        gift_codes_discord = "None"

        if gift_codes_response.status_code == 200:
            gift_codes = gift_codes_response.json()
            codes = [f"Gift: {gift_code['promotion']['outbound_title']}\nCode: {gift_code['code']}" for gift_code in gift_codes]
            gift_codes_discord = '\n\n'.join(codes) if codes else "None"

        console_width = os.get_terminal_size().columns
        gradient_colors = ((255, 105, 180), (0, 0, 255))
        gradient = generate_gradient_line(console_width, gradient_colors[0], gradient_colors[1])

        info_lines = [
            format_info("Status :", status, gradient),
            format_info("Token :", token_discord, gradient),
            format_info("Username :", username_discord, gradient),
            format_info("Display Name :", display_name_discord, gradient),
            format_info("Id :", user_id_discord, gradient),
            format_info("Created :", created_at_discord, gradient),
            format_info("Country :", country_discord, gradient),
            format_info("Email :", email_discord, gradient),
            format_info("Verified :", email_verified_discord, gradient),
            format_info("Phone :", phone_discord, gradient),
            format_info("Nitro :", nitro_discord, gradient),
            format_info("Avatar Decor :", avatar_decoration_discord, gradient),
            format_info("Avatar URL :", avatar_url_discord, gradient),
            format_info("Banner :", banner_discord, gradient),
            format_info("Multi-Factor Authentication :", mfa_discord, gradient),
            format_info("Authenticator Type :", authenticator_types_discord, gradient),
            format_info("Billing :", payment_methods_discord, gradient),
            format_info("Gift Code :", gift_codes_discord, gradient),
            format_info("Guilds :", guild_count, gradient),
        ]

        colored_info = "\n".join(info_lines)
        print(colored_info)
        print()
        input(apply_gradient("Press Enter to return to the main menu...", gradient))

    except Exception as e:
        print(f"{Fore.RED}Error when retrieving information: {e}")

def main():
    clear_console()
    gradient_colors = ((255, 105, 180), (0, 0, 255))
    gradient = generate_gradient_line(20, gradient_colors[0], gradient_colors[1])
    token_discord = input(apply_gradient("Enter Discord token:", gradient))
    clear_console()
    display_discord_info(token_discord)

if __name__ == "__main__":
    main()
