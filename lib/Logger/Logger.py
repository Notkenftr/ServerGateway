from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)

def timestamp():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

def Info(message):
    print(f"{Fore.GREEN}[{timestamp()}] [INFO] {Fore.WHITE}{message}")

def Warn(message):
    print(f"{Fore.YELLOW}[{timestamp()}] [WARNING] {Fore.LIGHTYELLOW_EX}{message}")

def Error(message):
    print(f"{Fore.RED}[{timestamp()}] [ERROR] {Fore.LIGHTRED_EX}{message}")

def Debug(message):
    print(f"{Fore.CYAN}[{timestamp()}] [DEBUG] {Fore.LIGHTCYAN_EX}{message}")

def Success(message):
    print(f"{Fore.MAGENTA}[{timestamp()}] [SUCCESS] {Fore.LIGHTMAGENTA_EX}{message}")


