import os
import subprocess
import ctypes
import time
import sys

CURRENT_ENV = "~"

def print_with_delay(text):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.05)  # Adjust speed of printing
    print()

def write_title():
    print("▄▄▄  ▄▄▄ . ▌ ▐·▄▄▄ .▄▄▄  .▄▄ ·")
    print("▀▄ █·▀▄.▀·▪█·█▌▀▄.▀·▀▄ █·▐█ ▀.")
    print("▐▀▀▄ ▐▀▀▪▄▐█▐█•▐▀▀▪▄▐▀▀▄ ▄▀▀▀█▄")
    print("▐█•█▌▐█▄▄▌ ███ ▐█▄▄▌▐█•█▌▐█▄▪▐█")
    print(".▀  ▀ ▀▀▀ . ▀   ▀▀▀ .▀  ▀ ▀▀▀▀  ")
    print("V1.0")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def trigger_bsod():
    ntdll = ctypes.windll.ntdll
    response = ctypes.c_ulong()
    ntdll.NtRaiseHardError(
        0xC000007B,
        0,
        0,
        0,
        6,
        ctypes.byref(response))
if __name__ == "__main__":
    if ctypes.windll.shell32.IsUserAnAdmin():
        trigger_bsod()
    else:
        print("Cette commande doit être exécuté en tant qu'administrateur.")

def mode_jeu():
    print("[1] Activer le mode jeu\n[2] Désactiver le mode jeu")
    choix = input("Choix : ")
    value = "True" if choix == "1" else "False"
    os.system(f'powershell "New-ItemProperty -Path \'HKCU:\\Software\\Microsoft\\GameBar\' -Name AllowAutoGameMode -Value {value} -PropertyType DWORD -Force"')

def changer_plan_alimentation():
    print("[1] Haute performance\n[2] Équilibré\n[3] Économie d'énergie")
    choix = input("Choix : ")
    plans = {
        "1": "8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c",  # Haute perf
        "2": "381b4222-f694-41f0-9685-ff5bb260df2e",  # Équilibré
        "3": "a1841308-3541-4fab-bc81-f71556f20b4a"   # Économie
    }
    if choix in plans:
        os.system(f"powercfg /setactive {plans[choix]}")
        print("Plan d’alimentation appliqué.")
    else:
        print("Choix invalide.")

COMMANDS = {
    "exit": "Quitte le shell",
    "crash": "Tue l'explorateur Windows",
    "bsod": "Fait Bluescreen le Pc",
    "shutdown": "Éteint le PC",
    "down": "Interface graphique de shutdown réseau",
    "down [ip]": "Éteint un PC distant",
    "c [cmd]": "Exécute une commande shell",
    "term": "Ouvre un nouveau terminal",
    " [texte]": "Copie le texte dans le presse-papier",
    "credit": "Affiche les crédits",
    "ls": "Liste les fichiers du dossier actuel",
    "mrt": "Lance le nettoyage Microsoft",
    "pwd": "Affiche le chemin actuel",
    "clear": "Efface l'écran",
    "wallpaper": "Change le fond d'écran",
    "gamemode": "Active/désactive le mode jeu",
    "whoami": "Affiche l'utilisateur actuel",
    "hostname": "Affiche le nom de la machine",
    "name [nom]": "Change le nom de l'environnement",
    "history": "Affiche l'historique",
    "del history": "Supprime l'historique",
    "changealim": "Changer le mode d'alimentation",
    "edit [fichier]": "Ouvre un fichier dans Notepad",
    "loadenv": "Charge un environnement",
    "loadenv [env]": "Charge un environnement spécifique",
    "testenv": "Affiche l'environnement courant",
    "update": "Vérifie les mises à jour",
    "cd": "Affiche le dossier actuel",
    "cd [dossier]": "Change de dossier",
    "python [script]": "Exécute un script Python",
    "jar [fichier]": "Exécute un fichier Jar",
    "github": "Ouvre github.com dans le navigateur",
    "clone [url]": "Clone un repo git",
    "touch": "Crée un fichier vide newfile.txt",
    "mkdir [dossier]": "Crée un dossier",
    "rmdir [dossier]": "Supprime un dossier vide",
    "rm [fichier]": "Supprime un fichier",
    "mv [src] [dest]": "Renomme un fichier/dossier",
    "cp [src] [dest]": "Copie un fichier",
    "date": "Affiche la date actuelle",
    "time": "Affiche l'heure actuelle",
    "uptime": "Affiche le temps système",
    "users": "Liste les utilisateurs locaux",
    "processes": "Liste les processus en cours",
    "kill [process]": "Tue un processus",
    "echo [texte]": "Affiche un texte",
    "ipconfig": "Affiche la config réseau",
    "ifconfig": "Affiche la config réseau détaillée",
    "ipv4": "Affiche uniquement IPv4",
    "ipv6": "Affiche uniquement IPv6",
    "myip": "Affiche l'IP publique",
    "ipgen": "Génère une IP aléatoire",
    "ipgen [nombre]": "Génère plusieurs IPs aléatoires",
    "iplink": "Affiche les interfaces réseau",
    "ping": "Ping Google",
    "ping [ip]": "Ping une adresse IP",
    "send": "Envoie des paquets ping personnalisés",
    "traceip [ip]": "Trace route avancée",
    "tracert": "Trace route vers Google",
    "tracert [ip]": "Trace route vers une IP",
    "exec [programme]": "Lance un programme",
    "delwinhud": "Désactive le mode test signing Windows",
    "netstat": "Affiche les connexions réseau",
    "arp": "Affiche la table ARP",
    "restart": "Redémarre le shell",
}

def show_help():
    print("Liste des commandes disponibles :")
    for cmd, desc in COMMANDS.items():
        print(f"{cmd:20} - {desc}")

def wallpaper():
    chemin = input("Cehamin de l'image: ")
    ctypes.windll.user32.SystemParametersInfoW(20, 0, chemin, 3)

def execute_command(command):
    if command == "":
        print_with_delay("'help' for see all commands")
        return
    if command == "help":
        show_help()
    if command == "exit":
        sys.exit()
    if command == "crash":
        subprocess.run(["taskkill", "/f", "/im", "explorer.exe"])
    if command == "bsod":
        trigger_bsod()
    if command == "shutdown":
        subprocess.run(["shutdown", "/s", "/t", "0"])
    if command.startswith("down "):
        print_with_delay(f"Sending shutdown to: {command[5:]}")
        subprocess.run(["shutdown", "/s", "/m", f"\\\\{command[5:]}", "/t", "0", "/c"])
    if command == "down":
        subprocess.run(["shutdown", "/i"])
    if command.startswith("c "):
        subprocess.run(command[2:], shell=True)
    if command == "term":
        subprocess.run(["cmd", "/c", "start"])
    if command.startswith(" "):
        subprocess.run(f"echo {command[1:]} | clip", shell=True)
        print_with_delay(f"'{command[1:]}' copied")
    if command == "credit":
        display_credit()
    if command == "ls":
        subprocess.run("dir /b", shell=True)
    if command == "gamemode":
        mode_jeu()
    if command == "mrt":
        subprocess.run("start C:\\Windows\\System32\\MRT.exe", shell=True)
    if command == "pwd":
        print_with_delay(os.getcwd())
    if command == "clear":
        clear_screen()
        write_title()
    if command == "whoami":
        subprocess.run(["whoami"])
    if command == "hostname":
        subprocess.run(["hostname"])
    if command.startswith("name "):
        global CURRENT_ENV
        CURRENT_ENV = command[5:]
    if command == "history":
        with open(os.path.join(os.getenv("temp"), "history.txt"), "r") as file:
            print(file.read())
    if command == "del history":
        os.remove(os.path.join(os.getenv("temp"), "history.txt"))
        print_with_delay("History has been removed")
    if command == "changealim":
        changer_plan_alimentation()
    if command == "maxalim":
        os.system('powercfg -duplicatescheme e9a42b02-d5df-448d-aa00-03f14749eb61')
    if command.startswith("edit "):
        subprocess.run(f"notepad {command[5:]}")
    if command == "loadenv":
        load_env()
    if command.startswith("loadenv "):
        load_specific_env(command[8:])
    if command == "testenv":
        print_with_delay(f"Current environment: {CURRENT_ENV}")
    if command == "update":
        check_update()
    if command == "cd":
        subprocess.run("cd", shell=True)
    if command.startswith("cd "):
        os.chdir(command[3:])
    if command.startswith("python "):
        subprocess.run(command[7:], shell=True)
    if command.startswith("jar "):
        subprocess.run(command[4:], shell=True)
    if command == "github":
        subprocess.run(["start", "https://github.com/"])
    if command.startswith("clone "):
        subprocess.run(f"git clone {command[6:]}")
    if command == "touch":
        with open("newfile.txt", "w"):
            pass
    if command.startswith("mkdir "):
        os.makedirs(command[6:])
    if command.startswith("rmdir "):
        os.rmdir(command[6:])
    if command.startswith("rm "):
        os.remove(command[3:])
    if command.startswith("mv "):
        src, dest = command[3:].split(" ")
        os.rename(src, dest)
    if command.startswith("cp "):
        src, dest = command[3:].split(" ")
        subprocess.run(f"copy {src} {dest}", shell=True)
    if command == "date":
        subprocess.run("date /t", shell=True)
    if command == "time":
        subprocess.run("time /t", shell=True)
    if command == "uptime":
        subprocess.run("systeminfo | find \"Temps systeme\"", shell=True)
    if command == "users":
        subprocess.run("net user", shell=True)
    if command == "processes":
        subprocess.run("tasklist", shell=True)
    if command == "wallpaper":
        wallpaper()
    if command.startswith("kill "):
        subprocess.run(f"taskkill /F /IM {command[5:]}")
    if command.startswith("echo "):
        print_with_delay(command[5:])
    if command == "ipconfig":
        subprocess.run("ipconfig", shell=True)
    if command == "ifconfig":
        subprocess.run("ipconfig /all", shell=True)
    if command == "ipv4":
        subprocess.run("ipconfig | findstr /i \"IPv4\"", shell=True)
    if command == "ipv6":
        subprocess.run("ipconfig | findstr /i \"IPv6\"", shell=True)
    if command == "myip":
        subprocess.run("powershell -Command \"(Invoke-WebRequest -Uri 'https://api.ipify.org').Content\"")
    if command == "ipgen":
        ip_generator()
    if command.startswith("ipgen "):
        count = int(command[6:])
        ip_generator(count)
    if command == "iplink":
        subprocess.run("netsh interface show interface", shell=True)
    if command == "ping":
        subprocess.run("ping 8.8.8.8", shell=True)
    if command.startswith("ping "):
        subprocess.run(f"ping {command[5:]}", shell=True)
    if command == "send":
        send_packets()
    if command.startswith("traceip "):
        subprocess.run(f"pathping {command[8:]}", shell=True)
    if command == "tracert":
        subprocess.run("tracert 8.8.8.8", shell=True)
    if command.startswith("tracert "):
        subprocess.run(f"tracert {command[8:]}", shell=True)
    if command.startswith("exec "):
        subprocess.run(f"start \"\" {command[5:]}", shell=True)
        print_with_delay(f"'{command[5:]}' launched")
    if command == "delwinhud":
        os.system('bcdedit -set TESTSIGNING OFF')
    if command == "netstat":
        subprocess.run("netstat -an", shell=True)
    if command == "arp":
        subprocess.run("arp -a", shell=True)
    if command == "restart":
        main()

def display_credit():
    print_with_delay("Credit :")
    print_with_delay("Revers, Made by NascaR")
    print_with_delay("360 code lines")
    print_with_delay("Thanks for using")
    print_with_delay("Have fun :)")

def load_env():
    print_with_delay("===============================")
    print_with_delay("=== Environment Management ===")
    print_with_delay("===============================")
    print_with_delay("1. Pentest Environment")
    print_with_delay("2. Development Environment")
    print_with_delay("3. Network Environment")
    print_with_delay("0. Back to Main Menu")
    choice = input("Select an environment: ")

    if choice == "1":
        load_specific_env("pentest")
    elif choice == "2":
        load_specific_env("dev")
    elif choice == "3":
        load_specific_env("network")
    elif choice == "0":
        main()

def load_specific_env(env_name):
    global CURRENT_ENV
    env_file = f".envs/{env_name}.bat"
    subprocess.run(f"call {env_file}", shell=True)
    CURRENT_ENV = env_name
    print_with_delay(f"Environment loaded: {env_name}")

def ip_generator(count=1):
    print_with_delay("----------------------------------------")
    for _ in range(count):
        ip = f"{os.urandom(1)[0] % 256}.{os.urandom(1)[0] % 256}.{os.urandom(1)[0] % 256}.{os.urandom(1)[0] % 256}"
        print_with_delay(ip)
    print_with_delay("Generation complete!")

def send_packets():
    target = input("Enter the target IP address or domain: ")
    size = input("Enter the packet size (in bytes 0-65500 max): ")
    count = input("Enter the number of packets to send: ")

    print_with_delay(f"Send {count} packets of {size} octets for {target}...")
    subprocess.run(f"ping {target} -l {size} -n {count}", shell=True)

def main():
    write_title()
    while True:
        current_env = CURRENT_ENV
        command = input(f"┌──({current_env})-[~]\n└─$ ")
        execute_command(command)

if __name__ == "__main__":
    main()
