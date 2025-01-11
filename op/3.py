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

def spam_webhook(webhook):
    gradient_colors = ((255, 105, 180), (0, 0, 255))
    gradient = generate_gradient_line(20, gradient_colors[0], gradient_colors[1])
    webhook_url = webhook
    number_of_messages = input(apply_gradient("Enter Number Of Message:", gradient))
    message = input(apply_gradient("Enter Your Message:", gradient))
   
    try:
        number_of_messages = int(number_of_messages)
    except ValueError:
        print("Le nombre de messages doit être un nombre entier.")
        return

    if not webhook_url.startswith("http"):
        print("Invalid Webhook URL.")
        return

    print(apply_gradient("Sending messages...", gradient))

    for i in range(number_of_messages):
        data = {
            "content": message 
        }
        try:
            response = requests.post(webhook_url, json=data)
            if response.status_code == 204:
                print(f"Message {i + 1} sent successfully!")
            else:
                print(f"Failed to send message {i + 1}. Status code: {response.status_code}")
        except Exception as e:
            print(f"An error occurred: {e}")

            input(apply_gradient("Press Enter to return to the main menu", gradient))
    input(apply_gradient("Press Enter to return to the main menu", gradient))
    clear_console()

def main():
    clear_console()
    gradient_colors = ((255, 105, 180), (0, 0, 255))
    gradient = generate_gradient_line(20, gradient_colors[0], gradient_colors[1])
    webhook = input(apply_gradient("Enter webhook link:", gradient))
    clear_console()
    spam_webhook(webhook)

if __name__ == "__main__":
    main()