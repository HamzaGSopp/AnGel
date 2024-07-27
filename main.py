import os
import sys
import subprocess
import requests
import ctypes
import webbrowser
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

GITHUB_REPO = "https://api.github.com/repos/HamzaGSopp/AnGel"
GITHUB_URL = "https://github.com/HamzaGSopp/AnGel"
CURRENT_VERSION = "1.0.1"

DEPENDENCIES = ["colorama", "requests", "rich"]

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
    console.print(f"[yellow][ i ][/yellow] Checking for updates...")
    try:
        response = requests.get(GITHUB_REPO + "/releases/latest")
        response.raise_for_status()
        
        # Extraction de la version la plus récente
        data = response.json()
        latest_version = data.get("tag_name", "Version info not available")
        
        # Affichage des informations sur les versions
        console.print(f"[cyan][ i ][/cyan] Current version: [bold]{CURRENT_VERSION}[/bold]")
        console.print(f"[cyan][ i ][/cyan] Latest version: [bold]{latest_version}[/bold]")
        
        if latest_version != CURRENT_VERSION:
            console.print(f"[green][ i ][/green] New version available: [bold]{latest_version}[/bold]")
            webbrowser.open(GITHUB_URL)
        else:
            console.print(f"[green][ i ][/green] No new updates found.")
    except requests.RequestException as e:
        console.print(f"[red][ ! ][/red] Failed to check for updates: [bold]{e}[/bold]")

def display_menu():
    console_width = os.get_terminal_size().columns
    
    # Texte ASCII stylisé
    ascii_art = Text("AnGel", style="bold magenta on white", justify="center")
    ascii_art.append("\nby HamzaGSopp", style="bold green")
    
    # Afficher le texte ASCII
    console.print(ascii_art)
    
    # Créer le menu avec des options en gras
    menu_options = [
        "1. User Info", 
        "2. Guild Info", 
        "3. Webhook Spammer", 
        "4. soon", 
        "5. soon", 
        "6. Exit"
    ]
    
    # Afficher le menu dans un panneau
    menu_text = ""
    for i in range(len(menu_options)):
        menu_text += f"[bold]{menu_options[i]}[/bold]\n"
    
    panel = Panel(menu_text, title="Menu", title_align="center", expand=False, padding=(1, 2))
    
    # Afficher le panneau du menu
    console.print(panel)

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
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
