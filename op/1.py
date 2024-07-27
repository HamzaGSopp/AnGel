import os
import sys
import requests
import colorama
from colorama import Fore, Style

colorama.init(autoreset=True)

DISCORD_TOKEN = 'MTI1MjU1NDk3MDEzODY3NzMxMA.GYI-L-.cLsOGM8GX6z8r6DENwpndFmTjFNx3hDSG2haV4' 

def clear_console():
    """Efface la console en fonction du système d'exploitation."""
    os.system('cls' if os.name == 'nt' else 'clear')

def rgb_to_colorama(rgb):
    """Convertit les valeurs RGB en couleur Colorama."""
    return f"\x1b[38;2;{rgb[0]};{rgb[1]};{rgb[2]}m"

def generate_gradient_line(width, start_rgb, end_rgb):
    """Génère un dégradé linéaire de couleurs."""
    gradient = []
    for i in range(width):
        r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * (i / (width - 1)))
        g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * (i / (width - 1)))
        b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * (i / (width - 1)))
        gradient.append(rgb_to_colorama((r, g, b)))
    return gradient

def apply_gradient(text, gradient):
    """Applique le dégradé de couleurs au texte."""
    colored_text = []
    gradient_length = len(gradient)
    for i, char in enumerate(text):
        colored_text.append(gradient[i % gradient_length] + char)
    return ''.join(colored_text) + Fore.RESET

def get_user_info(user_id):
    """Récupère les informations de l'utilisateur Discord en utilisant l'API Discord."""
    url = f'https://discord.com/api/v10/users/{user_id}'
    headers = {
        'Authorization': f'Bot {DISCORD_TOKEN}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def display_user_info(user_info):
    """Affiche les informations de l'utilisateur avec des couleurs et des styles."""
    if user_info:
        user_name = f"{user_info['username']}#{user_info['discriminator']}"
        user_id = user_info['id']
        user_avatar = f"https://cdn.discordapp.com/avatars/{user_id}/{user_info['avatar']}.png"
        
        gradient_colors = ((0, 0, 255), (128, 0, 128))  
        gradient = generate_gradient_line(os.get_terminal_size().columns, gradient_colors[0], gradient_colors[1])
        
        print(apply_gradient(f"Username: {user_name}", gradient))
        print(apply_gradient(f"User ID: {user_id}", gradient))
        print(apply_gradient(f"Avatar URL: {user_avatar}", gradient))
    else:
        print(Fore.RED + "User not found or error fetching information.")

def main():
    """Fonction principale du programme."""
    clear_console()
    
    gradient_colors_input = ((0, 0, 255), (128, 0, 128))  
    gradient_input = generate_gradient_line(30, gradient_colors_input[0], gradient_colors_input[1])
    
    gradient_text = apply_gradient("Enter Discord User ID: ", gradient_input)
    user_id = input(gradient_text)
    
    user_info = get_user_info(user_id)
    clear_console()
    display_user_info(user_info)
    
    print("\n" + apply_gradient("Press Enter to return to the menu...", gradient_input))
    input() 

if __name__ == "__main__":
    main()
