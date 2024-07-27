import os
import sys
import subprocess
import requests
import ctypes
import webbrowser
from colorama import init, Fore, Style

init(autoreset=True)

GITHUB_REPO = "https://api.github.com/repos/HamzaGSopp/AnGel"
GITHUB_URL = "https://github.com/HamzaGSopp/AnGel"
CURRENT_VERSION = "1.0.8"

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
        
        data = response.json()
        latest_version = data.get("tag_name", "Version info not available")
        
        print(f"{Fore.CYAN}[ i ] Current version: {CURRENT_VERSION}")
        print(f"{Fore.CYAN}[ i ] Latest version: {latest_version}")
        
        if latest_version != CURRENT_VERSION:
            print(f"{Fore.GREEN}[ i ] New version available: {latest_version}")
            webbrowser.open(GITHUB_URL)
            os.system("pause")
            sys.exit()
        else:
            print(f"{Fore.GREEN}[ i ] No new updates found.")
    except requests.RequestException as e:
        print(f"{Fore.RED}[ ! ] Failed to check for updates: {e}")

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

def center_text(text, width):
    return text.center(width)

def bold_text(text):
    return f"{Fore.WHITE}{Style.BRIGHT}{text}{Style.RESET_ALL}"

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
    
    gradient_colors = ((255, 105, 180), (0, 0, 255))
    gradient = generate_gradient_line(console_width, gradient_colors[0], gradient_colors[1])
    
    ascii_lines = ascii_art.split('\n')
    for line in ascii_lines:
        centered_line = center_text(line, console_width)
        colored_line = apply_gradient(centered_line, gradient)
        print(colored_line)
    
    print(bold_text(center_text("AnGel by HamzaGSopp", console_width)))
    print("\n\n")
    
    menu_options = [
        "1. User Info", 
        "2. Guild Info", 
        "3. Webhook Spammer", 
        "4. soon", 
        "5. soon",
        "6. soon", 
        "7. soon",
        "8. soon",
        "9. Exit"
    ]
    
    option_width = 35
    num_columns = 3
    
    num_rows = (len(menu_options) + num_columns - 1) // num_columns
    
    menu_lines = ['' for _ in range(num_rows)]
    for i in range(num_rows):
        for j in range(num_columns):
            index = i + j * num_rows
            if index < len(menu_options):
                menu_lines[i] += menu_options[index].ljust(option_width)
            else:
                menu_lines[i] += ' ' * option_width
    
    max_width = max(len(line) for line in menu_lines)
    
    border_top = "╭" + "─" * (max_width + 2) + "╮"
    border_bottom = "╰" + "─" * (max_width + 2) + "╯"
    
    menu_width = max_width + 2
    total_console_width = os.get_terminal_size().columns
    padding = (total_console_width - menu_width) // 2
    
    print(Fore.WHITE + ' ' * padding + border_top)
    for line in menu_lines:
        print(Fore.WHITE + ' ' * padding + "│ " + line.strip().ljust(max_width) + " │")
    print(Fore.WHITE + ' ' * padding + border_bottom)

def set_title(title):
    if os.name == 'nt':
        ctypes.windll.kernel32.SetConsoleTitleW(title)
    else:
        sys.stdout.write(f"\x1b]2;{title}\x07")

def execute_option_1():
    clear_console()
    subprocess.call([sys.executable, "op/1.py"])
    clear_console()
    display_menu()

def main():
    set_title("AnGel | by HamzaGSopp")
    install_dependencies()
    clear_console()
    check_for_update()
    clear_console()
    display_menu()
    
    gradient_colors_input = ((255, 105, 180), (0, 0, 255))
    gradient_input = generate_gradient_line(20, gradient_colors_input[0], gradient_colors_input[1])
    
    print()
    while True:
        try:
            gradient_text = apply_gradient("Enter a number: ", gradient_input)
            choice = input(gradient_text)
            if choice.isdigit():
                if int(choice) == 9:
                    print("Exiting the program...")
                    sys.exit()
                elif int(choice) == 1:
                    execute_option_1()
                elif 1 <= int(choice) <= 8:
                    print(f"You selected option {choice}.")
                    # Ajoutez le code pour chaque option ici
                else:
                    print("Invalid choice. Please enter a number between 1 and 9.")
            else:
                print("Invalid input. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

if __name__ == "__main__":
    main()
