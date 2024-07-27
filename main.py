import os
import sys
import subprocess
import requests
import ctypes
import webbrowser
from colorama import init, Fore, Style
import time

init(autoreset=True)

GITHUB_REPO = "https://api.github.com/repos/HamzaGSopp/AnGel"
GITHUB_URL = "https://github.com/HamzaGSopp/AnGel"
CURRENT_VERSION = "1.0.1"

DEPENDENCIES = ["colorama", "requests"]

def install_dependencies():
    for package in DEPENDENCIES:
        try:
            __import__(package)
        except ImportError:
            print(f"{Fore.YELLOW}[ i ] Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def rename_console(title):
    if os.name == 'nt':
        os.system(f"title {title}")
    else:
        sys.stdout.write(f"\x1b]2;{title}\x07")

def check_for_update():
    print(f"{Fore.YELLOW}[ i ] Checking for updates...")
    try:
        response = requests.get(GITHUB_REPO + "/releases/latest")
        response.raise_for_status()
        
        # Extraction de la version la plus récente
        data = response.json()
        latest_version = data.get("tag_name", "Version info not available")
        
        # Affichage des informations sur les versions
        print(f"{Fore.CYAN}[ i ] Current version: {CURRENT_VERSION}")
        print(f"{Fore.CYAN}[ i ] Latest version: {latest_version}")
        
        if latest_version != CURRENT_VERSION:
            print(f"{Fore.GREEN}[ i ] New version available: {latest_version}")
            webbrowser.open(GITHUB_URL)
        else:
            print(f"{Fore.GREEN}[ i ] No new updates found.")
    except requests.RequestException as e:
        print(f"{Fore.RED}[ ! ] Failed to check for updates: {e}")

def rgb_to_colorama(rgb):
    """Convert RGB tuple to a colorama compatible color."""
    return f"\x1b[38;2;{rgb[0]};{rgb[1]};{rgb[2]}m"

def generate_gradient_line(width, start_rgb, end_rgb):
    """Generate a gradient of colors from start_rgb to end_rgb."""
    gradient = []
    for i in range(width):
        r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * (i / (width - 1)))
        g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * (i / (width - 1)))
        b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * (i / (width - 1)))
        gradient.append(rgb_to_colorama((r, g, b)))
    return gradient

def apply_gradient(text, gradient):
    """Apply gradient colors to the text."""
    colored_text = []
    gradient_length = len(gradient)
    for i, char in enumerate(text):
        colored_text.append(gradient[i % gradient_length] + char)
    return ''.join(colored_text) + Fore.RESET

def center_text(text, width):
    """Center the text based on the width of the console."""
    return text.center(width)

def enlarge_text(text, size=2):
    """Enlarge text by duplicating each character."""
    enlarged = []
    for char in text:
        if char == ' ':
            enlarged.append(' ' * size)
        else:
            enlarged.append(char * size)
    return ''.join(enlarged)

def display_menu():
    ascii_art = r"""
      ______              ______             __ 
     /      \            /      \           |  \
    |  $$$$$$\ _______  |  $$$$$$\  ______  | $$
    | $$__| $$|       \ | $$ __\$$ /      \ | $$
    | $$    $$| $$$$$$$\| $$|    \|  $$$$$$\| $$
    | $$$$$$$$| $$  | $$| $$ \$$$$| $$    $$| $$
    | $$  | $$| $$  | $$| $$__| $$| $$$$$$$$| $$
    | $$  | $$| $$  | $$ \$$    $$ \$$     \| $$
     \$$   \$$ \$$   \$$  \$$$$$$   \$$$$$$$ \$$
    """
    
    console_width = os.get_terminal_size().columns
    
    # Dégradé de couleur de Rose (RGB) à Bleu (RGB)
    gradient_colors = ((255, 105, 180), (0, 0, 255))
    gradient = generate_gradient_line(console_width, gradient_colors[0], gradient_colors[1])
    
    # Centrer le texte ASCII et appliquer le dégradé ligne par ligne
    ascii_lines = ascii_art.split('\n')
    for line in ascii_lines:
        centered_line = center_text(line, console_width)
        colored_line = apply_gradient(centered_line, gradient)
        print(colored_line)
    
    # Texte "AnGel by HamzaGSopp" en blanc
    print(Fore.WHITE + center_text("AnGel by HamzaGSopp", console_width))
    
    # Créer le menu avec une bordure
    menu_options = [
        "1. User Info", 
        "2. Guild Info", 
        "3. Webhook Spammer", 
        "4. soon", 
        "5. soon", 
        "6. Exit"
    ]
    
    # Déterminer la largeur du menu et les colonnes
    menu_width = 30  # Largeur de chaque colonne
    column_count = 2
    line_length = menu_width * column_count + column_count - 1  # Inclure les espaces entre les colonnes
    
    # Centrer la bordure du menu
    border_line = '+' + '-' * line_length + '+'
    print(Fore.WHITE + center_text(border_line, console_width))
    
    # Préparer les options pour les afficher en croissant
    rows = (len(menu_options) + 1) // 2  # Calculer le nombre de lignes nécessaires
    for row in range(rows):
        left_index = row
        right_index = row + rows
        
        left_option = menu_options[left_index] if left_index < len(menu_options) else ""
        right_option = menu_options[right_index] if right_index < len(menu_options) else ""
        
        # Agrandir le texte des options
        left_option = enlarge_text(left_option, size=2).ljust(menu_width)
        right_option = enlarge_text(right_option, size=2).ljust(menu_width)
        
        # Centrer la ligne du menu
        menu_line = f"|{left_option}|{right_option}|"
        print(Fore.WHITE + center_text(menu_line, console_width))
    
    # Afficher la bordure inférieure du menu
    print(Fore.WHITE + center_text(border_line, console_width))

def set_title(title):
    if os.name == 'nt':
        ctypes.windll.kernel32.SetConsoleTitleW(title)
    else:
        sys.stdout.write(f"\x1b]2;{title}\x07")

def main():
    set_title("AnGel | by HamzaGSopp")
    install_dependencies()
    clear_console()
    check_for_update()
    clear_console()
    display_menu()
    os.system("pause")

if __name__ == "__main__":
    main()
