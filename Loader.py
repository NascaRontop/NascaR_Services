import msvcrt
import requests
import zipfile
import shutil
import pyminizip
from io import BytesIO
import subprocess
import winshell  # pip install winshell
import getpass
import json
import os
import time
import sys
import hashlib
from colorama import init, Fore, Style



init()

REPO_OWNER = "KAMIXlevrai"
REPO_NAME = "Files-NS_services"
BRANCH = "main"  # ou "master" si ton dépôt est sur master
INSTALL_PATH = os.path.join(os.getenv('APPDATA'), "NascaR_Loader")
APP_PATH = INSTALL_PATH

current_color = "07"
dossier_a_supprimer = "%appdata%/NascaR_Loader"
GITHUB_ACCOUNTS_URL = "https://raw.githubusercontent.com/KAMIXlevrai/Account-NS_services/main/accepted_users.json"
WEBHOOK_URL = "https://discord.com/api/webhooks/1389986439361597470/DnhZegvuMylfZKpa1IyHbdP7On8927w-9ncbl8vMCG2NT7rpgg4YZVD1spB8_cblxhty"
MSG_URL = "https://discord.com/api/webhooks/1390032801402847262/ND4438vZ_EdEZFvoAqCpnXOXjecPGbe_My_XdjewESqqvqZgOthyWyO2eohZv62heP_s"
OUVRIR_PATH = os.path.join(APP_PATH, "Loader_data/file_path.json")

def typewriter(text, delay=0.01):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def reinstall_loader():
    if os.path.exists(INSTALL_PATH):
        try:
            typewriter(Fore.RED + "🗑️ Suppression des fichiers du loader..." + Style.RESET_ALL)
            shutil.rmtree(INSTALL_PATH)
            time.sleep(1)
            typewriter(Fore.YELLOW + "🔁 Réinstallation en cours..." + Style.RESET_ALL)
            check_and_install_files()
            typewriter(Fore.GREEN + "✅ Réinstallation terminée !" + Style.RESET_ALL)
        except Exception as e:
            typewriter(Fore.RED + f"❌ Erreur lors de la réinstallation : {e}" + Style.RESET_ALL)
    else:
        typewriter(Fore.YELLOW + "📁 Aucun fichier à supprimer, installation normale..." + Style.RESET_ALL)
        check_and_install_files()

    input("Appuie sur une touche pour continuer...")

def desinstaller_loader():
    appdata_path = os.getenv("APPDATA")  # équivalent à %appdata%
    dossier_a_supprimer = os.path.join(appdata_path, "NascaR_Loader")

    if os.path.exists(dossier_a_supprimer):
        try:
            shutil.rmtree(dossier_a_supprimer)
            typewriter(Fore.WHITE + "✅ " + Fore.GREEN + "Le dossier NascaR_Loader a été supprimé avec succès.")
        except Exception as e:
            typewriter(Fore.WHITE + "❌ " + Fore.RED + f"Erreur lors de la suppression : {e}")
    else:
        typewriter(Fore.WHITE + "❌ " + Fore.RED + "Le dossier NascaR_Loader est introuvable.")

def check_and_install_files():
    required_file = os.path.join(INSTALL_PATH, "Loader_data", "Extensions", "Revers.py")

    if os.path.exists(required_file):
        print("[✓] Fichiers déjà installés.")
        return

    typewriter(Fore.RED + "[!] Fichiers manquants. Téléchargement en cours..." + Style.RESET_ALL)

    try:
        zip_url = f"https://github.com/{REPO_OWNER}/{REPO_NAME}/archive/refs/heads/{BRANCH}.zip"
        response = requests.get(zip_url)
        if response.status_code != 200:
            raise Exception("❌ Échec du téléchargement depuis GitHub.")

        with zipfile.ZipFile(BytesIO(response.content)) as zip_ref:
            zip_ref.extractall("temp_nascar")
            extracted_path = os.path.join("temp_nascar", f"{REPO_NAME}-{BRANCH}")

            if os.path.exists(INSTALL_PATH):
                shutil.rmtree(INSTALL_PATH)
            shutil.move(extracted_path, INSTALL_PATH)
            shutil.rmtree("temp_nascar")

        clear()
        typewriter(Fore.GREEN + "[✅] Fichiers installés avec succès, démarrage..." + Style.RESET_ALL)

    except Exception as e:
        typewriter(Fore.RED + f"[❌] Erreur pendant l'installation : {e}" + Style.RESET_ALL)
        input("Appuie sur une touche pour quitter...")
        sys.exit(1)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def envoyer_message_discord(username):
    message = input("💬 Message à envoyer : ").strip()
    if not message:
        typewriter("⚠️ Message vide, annulation.")
        return

    contenu = f"**{username}** : {message}"

    payload = {
        "content": contenu
    }

    response = requests.post(MSG_URL, json=payload)

    if response.status_code == 204:
        typewriter("✅ Message envoyé avec succès !")
    else:
        typewriter(f"❌ Échec de l'envoi. Code : {response.status_code}")

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def clear_line():
    sys.stdout.write("\r" + " " * 40 + "\r")
    sys.stdout.flush()

def charger_apps():
    if not os.path.exists(OUVRIR_PATH):
        return {}
    with open(OUVRIR_PATH, "r") as f:
        return json.load(f)

def sauvegarder_apps(apps):
    with open(OUVRIR_PATH, "w") as f:
        json.dump(apps, f, indent=4)

def ajouter_app():
    nom = input("📝 Nom de l'application : ").strip()
    chemin = input("📂 Chemin complet du fichier .exe : ").strip()

    # Supprime les guillemets s'ils sont autour du chemin
    if chemin.startswith('"') and chemin.endswith('"'):
        chemin = chemin[1:-1]

    if not os.path.exists(chemin):
        typewriter("❌ Fichier introuvable.")
        return

    apps = charger_apps()
    apps[nom] = chemin
    sauvegarder_apps(apps)
    typewriter(f"✅ {nom} ajouté au menu ouvrir.")

def supprimer_app():
    apps = charger_apps()
    if not apps:
        typewriter("📭 Aucune application à supprimer.")
        return

    print("\nApplications enregistrées :")
    for i, nom in enumerate(apps.keys(), 1):
        print(f"[{i}] {nom}")

    choix = input("\n❌ Numéro à supprimer : ").strip()
    if not choix.isdigit() or int(choix) < 1 or int(choix) > len(apps):
        typewriter("❌ Choix invalide.")
        return

    nom = list(apps.keys())[int(choix)-1]
    del apps[nom]
    sauvegarder_apps(apps)
    typewriter(f"🗑️ {nom} supprimé.")

def fermeture_countdown():
    typewriter(Fore.CYAN + "Au revoir 👋" + Style.RESET_ALL)
    time.sleep(0.5)

    for i in range(3, 0, -1):
        clear_line()
        sys.stdout.write(Fore.YELLOW + f"Fermeture dans {i}..." + Style.RESET_ALL)
        sys.stdout.flush()
        time.sleep(1)

    clear_line()
    sys.stdout.write(Fore.GREEN + "✅ Fermé." + Style.RESET_ALL + "\n")
    sys.stdout.flush()
    time.sleep(0.5)
    sys.exit()

def toggle_startup_shortcut():
    startup_dir = os.path.join(os.getenv('APPDATA'), r'Microsoft\Windows\Start Menu\Programs\Startup')
    shortcut_path = os.path.join(startup_dir, "NascaR_Loader.lnk")

    # Chemin absolu vers l'exécutable ou le script lancé
    target_path = os.path.abspath(sys.argv[0])

    if os.path.exists(shortcut_path):
        os.remove(shortcut_path)
        print("❌ Démarrage auto désactivé (raccourci supprimé).")
    else:
        with winshell.shortcut(shortcut_path) as link:
            link.path = target_path
            link.working_directory = os.path.dirname(target_path)
            link.description = "NascaR Loader"
            link.icon_location = (target_path, 0)
        print("✅ Démarrage auto activé (raccourci créé).")

def repair_network():
    typewriter("🔁 Réinitialisation réseau...")
    os.system("ipconfig /flushdns")
    os.system("ipconfig /release")
    os.system("ipconfig /renew")
    os.system("netsh winsock reset")
    typewriter("✅ Réseau réinitialisé.")
    input("Appuie sur une touche pour continuer...")

def installer_license_winrar():
    source_key = os.path.join(APP_PATH, "Loader_data", "Licenses", "rarreg.key")

    # Dossier par défaut WinRAR
    paths = [
        r"C:\Program Files\WinRAR",
        r"C:\Program Files (x86)\WinRAR"
    ]

    if not os.path.exists(source_key):
        typewriter("❌ Le fichier rarreg.key est introuvable.")
        return

    installed = False
    for path in paths:
        if os.path.exists(path):
            try:
                shutil.copy2(source_key, path)
                typewriter(f"✅ Licence installée dans : {path}")
                installed = True
                break
            except Exception as e:
                typewriter(f"❌ Erreur lors de l'installation dans {path} : {e}")

    if not installed:
        typewriter("⚠️ Dossier WinRAR non trouvé. Assure-toi que WinRAR est bien installé.")

def print_header():
    global current_color
    clear()
    os.system(f"color {current_color}")
    
    # Remplir tout l'écran avec la bonne couleur
    largeur = os.get_terminal_size().columns
    hauteur = os.get_terminal_size().lines
    for _ in range(hauteur):
        print(" " * largeur)

    clear()  # on clear une 2e fois pour effacer ce masque (il fixe la couleur de fond)
    os.system(f"color {current_color}")  # re-force la couleur
    print(Fore.CYAN + Style.BRIGHT + r"""
    _   __                      ____                          _               
   / | / /___ _______________ _/ __ \   ________  ______   __(_)_______  _____
  /  |/ / __ `/ ___/ ___/ __ `/ /_/ /  / ___/ _ \/ ___/ | / / / ___/ _ \/ ___/
 / /|  / /_/ (__  ) /__/ /_/ / _, _/  (__  )  __/ /   | |/ / / /__/  __(__  ) 
/_/ |_/\__,_/____/\___/\__,_/_/ |_|  /____/\___/_/    |___/_/\___/\___/____/
""" + Style.RESET_ALL)

def send_to_discord(username, hashed_password):
    data = {
        "content": f"🔐 Nouvelle demande de compte\n**Username :** {username}\n**Password Hash :** `{hashed_password}`"
    }
    requests.post(WEBHOOK_URL, json=data)
    

def deco():
    typewriter("Déconnexion...")
    time.sleep(1)
    main_menu()

def run_script_in_app(relative_path):
    full_path = os.path.join(APP_PATH, *relative_path.split("/"))
    if os.path.exists(full_path):
        os.system(f'python "{full_path}"')
    else:
        typewriter(f"❌ Script introuvable : {full_path}")
        input("Appuie sur une touche pour continuer...")

def run_file_in_app(relative_path):
    full_path = os.path.join(APP_PATH, *relative_path.split("/"))
    
    if os.path.exists(full_path):
        os.startfile(full_path)  # lance un .exe, .py, .txt, .bat, etc.
    else:
        typewriter(f"❌ Fichier introuvable : {full_path}")
        input("Appuie sur une touche pour continuer...")

def get_all_interfaces():
    try:
        result = subprocess.run(
            ['netsh', 'interface', 'show', 'interface'],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        if result.returncode != 0 or not result.stdout:
            typewriter("❌ Impossible de lire les interfaces réseau.")
            return []

        interfaces = []
        lines = result.stdout.splitlines()
        for line in lines:
            if "Dedicated" in line:
                parts = line.strip().split()
                name = " ".join(parts[3:])  # nom de l'interface
                interfaces.append(name)
        return interfaces

    except Exception as e:
        typewriter(f"Erreur lors de la récupération des interfaces : {e}")
        return []

def disable_network(interface_name):
    cmd = f'netsh interface set interface "{interface_name}" admin=disabled'
    result = subprocess.run(cmd, shell=True)
    if result.returncode == 0:
        print(f"✅ Connexion '{interface_name}' désactivée.")
    else:
        print(f"❌ Erreur lors de la désactivation de '{interface_name}'.")

def enable_network(interface_name):
    cmd = f'netsh interface set interface "{interface_name}" admin=enabled'
    result = subprocess.run(cmd, shell=True)
    if result.returncode == 0:
        print(f"✅ Connexion '{interface_name}' activée.")
    else:
        print(f"❌ Erreur lors de l'activation de '{interface_name}'.")


def zip_dossier_avec_interface():
    os.system("cls" if os.name == "nt" else "clear")
    print("=== Créateur de ZIP sécurisé ===\n")

    # Demande du dossier source
    dossier_source = input("📂 Chemin du dossier à zipper : ").strip().strip('"')
    if not os.path.isdir(dossier_source):
        print("❌ Ce dossier n'existe pas.")
        return

    # Nom du fichier ZIP
    zip_nom = input("📦 Nom du fichier ZIP de sortie (ex: mon_archive.zip) : ").strip()
    if not zip_nom.endswith(".zip"):
        zip_nom += ".zip"
    zip_output = os.path.join(os.getcwd(), zip_nom)

    # Mot de passe
    mot_de_passe = input("🔑 Mot de passe pour protéger l'archive : ").strip()
    if not mot_de_passe:
        print("❌ Mot de passe vide interdit.")
        return

    # Niveau de compression
    try:
        compression = int(input("📉 Niveau de compression (1 = rapide, 9 = maximum) [5 par défaut] : ").strip() or '5')
        if compression < 1 or compression > 9:
            raise ValueError
    except ValueError:
        print("❌ Compression invalide. Utilise un chiffre entre 1 et 9.")
        return

    # Préparation des fichiers
    fichiers = []
    chemins_relatifs = []
    for dossier_racine, _, fichiers_liste in os.walk(dossier_source):
        for fichier in fichiers_liste:
            fichier_complet = os.path.join(dossier_racine, fichier)
            fichiers.append(fichier_complet)
            chemins_relatifs.append(os.path.relpath(fichier_complet, start=dossier_source))

    try:
        pyminizip.compress_multiple(fichiers, chemins_relatifs, zip_output, mot_de_passe, compression)
        print(f"\n✅ Archive créée avec succès : {zip_output}")
    except Exception as e:
        print(f"\n❌ Erreur lors de la compression : {e}")

def zip_folder_contents(source_folder, output_zip):
    if not os.path.exists(source_folder):
        print(f"❌ Dossier introuvable : {source_folder}")
        return

    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for foldername, subfolders, filenames in os.walk(source_folder):
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                # Fichier relatif sans inclure le dossier racine
                arcname = os.path.relpath(file_path, source_folder)
                zipf.write(file_path, arcname)

    print(f"✅ Compression terminée : {output_zip}")

def main_zip():
    clear()
    print_header()
    print("=== Comprésseur ===")
    source = input("📁 Chemin du dossier à compresser : ").strip('"')
    output = input("💾 Nom complet du fichier zip (ex: C:/Users/TonNom/Desktop/monzip.zip) : ").strip('"')

    zip_folder_contents(source, output)
    input("Appuie sur une touche pour Continuer...")
    return

def cleanup_system():
    os.system('del /q/f/s %TEMP%\\*')
    typewriter("✅ Fichiers temporaires supprimés.")

def nettoyer_prefetch():
    chemin = "C:\\Windows\\Prefetch"
    print(f"🧹 Nettoyage de : {chemin}")

    # Supprimer tous les fichiers
    resultat = os.system(f'del /f /s /q "{chemin}\\*"')

    if resultat == 0:
        print("✅ Prefetch vidé.")
    else:
        print("❌ Impossible de nettoyer Prefetch. Lance en admin ?")

def nettoyer_temp():
    chemin = "C:\\Windows\\Temp"
    print(f"🧹 Nettoyage de : {chemin}")

    # Supprimer tous les fichiers
    resultat = os.system(f'del /f /s /q "{chemin}\\*"')

    if resultat == 0:
        print("✅ Prefetch vidé.")
    else:
        print("❌ Impossible de nettoyer Prefetch. Lance en admin ?")

def register():
    print_header()
    print("=== Création de compte ===")
    username = input("🧾 Entrez votre nom d'utilisateur : ")
    password = input("🔑 Entrez votre mot de passe : ")
    hashed_password = hash_password(password)
    send_to_discord(username, hashed_password)
    typewriter("✅ Demande envoyée. En attente de validation...")
    typewriter("\nAppuie sur [échap] pour revenir au menu principal.")
    while True:
        key = msvcrt.getch().decode().lower()
        if key == b'\x1b':
            break  # retour au menu

def extra_menu(username):
    while True:
        print_header()
        print(Fore.YELLOW + "Extra" + Style.RESET_ALL)
        print(Fore.YELLOW + "[1]" + Fore.WHITE + " Créé un dossier sécurisé")
        print(Fore.YELLOW + "[2]" + Fore.WHITE + " Faire un fichier zip")
        print(Fore.YELLOW + "[3]" + Fore.WHITE + " Revenir")
        print("➡️ Appuie sur une touche...")

        touche = msvcrt.getch()
        try:
            touche = touche.decode()
        except:
            touche = ''

        if touche == '1':
            zip_dossier_avec_interface()
        elif touche == '2':
            main_zip()
        elif touche == '3':
            menu(username)
        else:
            typewriter("❌ Choix invalide.")
            input("Appuie sur une touche pour réessayer...")

def menu(username):
    while True:
        print_header()
        print(Fore.YELLOW + f"Bon retour {username}!" + Style.RESET_ALL)
        print(Fore.YELLOW + "[1]" + Fore.WHITE + " Envoyer un message")
        print(Fore.YELLOW + "[2]" + Fore.WHITE + " Options")
        print(Fore.YELLOW + "[3]" + Fore.WHITE + " Applications")
        print(Fore.YELLOW + "[4]" + Fore.WHITE + " Connexions")
        print(Fore.YELLOW + "[5]" + Fore.WHITE + " Extra")
        print(Fore.YELLOW + "[6]" + Fore.WHITE + " Quitter")
        print("➡️ Appuie sur une touche...")

        try:
            touche = msvcrt.getch().decode(errors='ignore')
        except:
            touche = ''

        if touche == '1':
            envoyer_message_discord(username)
            input("Appuie sur une touche pour continuer...")
        elif touche == '2':
            options_menu(username)
        elif touche == '3':
            apps_menu(username)
        elif touche == '4':
            networks_menu(username)
        elif touche == '5':
            extra_menu(username)
        elif touche == '6':
            clear()
            fermeture_countdown()
        else:
            typewriter("❌ Choix invalide.")
            input("Appuie sur une touche pour réessayer...")

def login():
    print_header()
    print("=== Connexion ===")
    username = input("👤 Nom d'utilisateur : ")
    password = input("🔒 Mot de passe : ")
    hashed_password = hash_password(password)

    try:
        r = requests.get(GITHUB_ACCOUNTS_URL)
        if r.status_code != 200:
            typewriter("❌ Impossible de récupérer la base utilisateurs.")
        else:
            users = r.json()
            if username in users and users[username] == hashed_password:
                typewriter(Fore.GREEN + "✅ Connexion réussie : " + Fore.WHITE + f"Bienvenue {username} !" + Style.RESET_ALL)
                os.system(f'title {username}')
                time.sleep(1)
                menu(username)
            else:
                typewriter(Fore.YELLOW + "❌ Identifiants invalides ou compte non accepté." + Style.RESET_ALL)
    except Exception as e:
        typewriter(f"❌ Erreur lors de la connexion : {e}")

    typewriter("\n[?] Appuie sur Échap pour revenir au menu principal.")
    while True:
        key = msvcrt.getch()
        if key == b'\x1b':  # ESC
            break  # retour au menu

def apps_menu(username):
    while True:
        print_header()
        print(Fore.YELLOW + "Applications" + Style.RESET_ALL)
        print(Fore.YELLOW + "[1]" + Fore.WHITE + " Extensions")
        print(Fore.YELLOW + "[2]" + Fore.WHITE + " Cracks")
        print(Fore.YELLOW + "[3]" + Fore.WHITE + " Ouvrir")
        print(Fore.YELLOW + "[4]" + Fore.WHITE + " Revenir")
        print("➡️ Appuie sur une touche...")

        try:
            touche = msvcrt.getch().decode(errors='ignore')
        except:
            touche = ''

        if touche == '1':
            extensions_menu(username)
        elif touche == '2':
            crack_menu(username)
        elif touche == '3':
            ouvrir_menu(username)
        elif touche == '4':
            menu(username)
        else:
            typewriter("❌ Choix invalide.")
            input("Appuie sur une touche pour réessayer...")

def set_dns(interface_name, dns_ip):
    cmd = f'netsh interface ip set dns name="{interface_name}" static {dns_ip} primary'
    result = os.system(cmd)
    if result == 0:
        typewriter(f"✅ DNS de '{interface_name}' changé en {dns_ip}")
    else:
        typewriter(f"❌ Échec du changement DNS pour '{interface_name}'")

def dns_menu():
    interface_name = input("🔌 Entre le nom de ton interface réseau (ex: Wi-Fi, Ethernet) : ").strip()
    dns_ip = input("🌐 Entre l'adresse IP du DNS à appliquer (ex: 8.8.8.8) : ").strip()
    set_dns(interface_name, dns_ip)
    input("Appuie sur une touche pour continuer...")

def networks_menu(username):
    while True:
        print_header()
        print(Fore.YELLOW + "Applications" + Style.RESET_ALL)
        print(Fore.YELLOW + "[1]" + Fore.WHITE + " Désactiver une connexion")
        print(Fore.YELLOW + "[2]" + Fore.WHITE + " Activer une connexion")
        print(Fore.YELLOW + "[3]" + Fore.WHITE + " Changer de DNS")
        print(Fore.YELLOW + "[4]" + Fore.WHITE + " Afficher les réseaux")
        print(Fore.YELLOW + "[5]" + Fore.WHITE + " Réinitialiser le réseau")
        print(Fore.YELLOW + "[6]" + Fore.WHITE + " Revenir")
        print("➡️ Appuie sur une touche...")

        try:
            touche = msvcrt.getch().decode(errors='ignore')
        except:
            touche = ''

        if touche == '1' or touche == '2':
            interfaces = get_all_interfaces()
            if not interfaces:
                typewriter("❌ Aucune interface trouvée.")
                continue

            print("\nInterfaces réseau disponibles :")
            for i, iface in enumerate(interfaces):
                print(f"[{i+1}] {iface}")

            try:
                index = int(input("➡️ Choisis une interface : ")) - 1
                if 0 <= index < len(interfaces):
                    interface_name = interfaces[index]
                    if touche == '1':
                        disable_network(interface_name)
                    else:
                        enable_network(interface_name)
                else:
                    typewriter("❌ Numéro invalide.")
            except ValueError:
                typewriter("❌ Entrée incorrecte.")
            input("Appuie sur une touche pour continuer...")

        elif touche == '3':
            dns_menu()
        elif touche == '4':
            os.system('netsh interface show interface')
            input("Appuie sur une touche pour continuer...")
        elif touche == '5':
            repair_network()
        elif touche == '6':
            return
        else:
            typewriter("❌ Choix invalide.")
            input("Appuie sur une touche pour réessayer...")


def extensions_menu(username):
    while True:
        print_header()
        print(Fore.YELLOW + "Extensions" + Style.RESET_ALL)
        print(Fore.YELLOW + "[1]" + Fore.WHITE + " Steam Achivements")
        print(Fore.YELLOW + "[2]" + Fore.WHITE + " Revers")
        print(Fore.YELLOW + "[3]" + Fore.WHITE + " Amnesia")
        print(Fore.YELLOW + "[4]" + Fore.WHITE + " Revenir")
        print("➡️ Appuie sur une touche...")

        try:
            touche = msvcrt.getch().decode(errors='ignore')
        except:
            touche = ''

        if touche == '1':
            run_file_in_app("Loader_data/Extensions/Steam/Achivements/SAM.Picker.exe")
        elif touche == '2':
            clear()
            run_script_in_app("Loader_data/Extensions/Revers.py")
        elif touche == '3':
            clear()
            run_script_in_app("Loader_data/Extensions/ModsMenu/AMNESIA.py")
        elif touche == '4':
            apps_menu(username)
        else:
            typewriter("❌ Choix invalide.")
            input("Appuie sur une touche pour réessayer...")

def crack_menu(username):
    while True:
        print_header()
        print(Fore.YELLOW + "Applications" + Style.RESET_ALL)
        print(Fore.YELLOW + "[1]" + Fore.WHITE + " Winrar")
        print(Fore.YELLOW + "[2]" + Fore.WHITE + " Windows")
        print(Fore.YELLOW + "[3]" + Fore.WHITE + " Steam DLC")
        print(Fore.YELLOW + "[4]" + Fore.WHITE + " Revenir")
        print("➡️ Appuie sur une touche...")

        try:
            touche = msvcrt.getch().decode(errors='ignore')
        except:
            touche = ''

        if touche == '1':
            installer_license_winrar()
            input("Appuie sur une touche pour continuer...")
        elif touche == '2':
            os.system('bcdedit -set TESTSIGNING OFF')
            typewriter(Fore.GREEN + "[✅] Mode de Test de Windows Désactivé" + Style.RESET_ALL)
            input("Appuie sur une touche pour continuer...")
        elif touche == '3':
            run_file_in_app("Loader_data/Extensions/Steam/DLC/CreamInstaller 5.0.0.exe")
        elif touche == '4':
            return
        else:
            typewriter("❌ Choix invalide.")
            input("Appuie sur une touche pour réessayer...")

def  ouvrir_menu(username):
    while True:
        print_header()
        apps = charger_apps()
        print(Fore.YELLOW + "Applications enregistrées :" + Style.RESET_ALL)
        
        for i, (nom, chemin) in enumerate(apps.items(), 1):
            print(f"{Fore.YELLOW}[{i}]{Fore.WHITE} {nom}")

        offset = len(apps)
        print(Fore.YELLOW + f"[{offset+1}]" + Fore.WHITE + " Ajouter une application")
        print(Fore.YELLOW + f"[{offset+2}]" + Fore.WHITE + " Supprimer une application")
        print(Fore.YELLOW + f"[{offset+3}]" + Fore.WHITE + " Revenir")
        print("➡️ Appuie sur une touche...")

        try:
            touche = msvcrt.getch().decode(errors='ignore')
        except:
            touche = ''

        if touche.isdigit():
            index = int(touche)
            if 1 <= index <= len(apps):
                nom = list(apps.keys())[index - 1]
                os.startfile(apps[nom])
            elif index == len(apps) + 1:
                ajouter_app()
            elif index == len(apps) + 2:
                supprimer_app()
            elif index == len(apps) + 3:
                return
            else:
                typewriter("❌ Choix invalide.")
        else:
            typewriter("❌ Choix invalide.")
        input("Appuie sur une touche pour continuer...")

def menu_color():
    global current_color
    while True:
        print_header()
        print(Fore.YELLOW + "Themes" + Style.RESET_ALL)
        print(Fore.YELLOW + "[1]" + Fore.WHITE + " Noir")
        print(Fore.YELLOW + "[2]" + Fore.WHITE + " Blanc")
        print(Fore.YELLOW + "[3]" + Fore.WHITE + " Bleu")
        print(Fore.YELLOW + "[4]" + Fore.WHITE + " Rouge")
        print(Fore.YELLOW + "[5]" + Fore.WHITE + " Vert")
        print(Fore.YELLOW + "[6]" + Fore.WHITE + " Revenir")
        print("➡️ Appuie sur une touche...")

        try:
            touche = msvcrt.getch().decode(errors='ignore')
        except:
            touche = ''

        if touche == '1':
            current_color = "07"
        elif touche == '2':
            current_color = "70"
        elif touche == '3':
            current_color = "17"
        elif touche == '4':
            current_color = "47"
        elif touche == '5':
            current_color = "27"
        elif touche == '6':
            return  # on quitte la fonction
        else:
            typewriter("❌ Choix invalide.")
            input("Appuie sur une touche pour réessayer...")

        os.system(f"color {current_color}")  # applique la couleur

def options_menu(username):
    while True:
        print_header()
        print(Fore.YELLOW + "Options" + Style.RESET_ALL)
        print(Fore.YELLOW + "[1]" + Fore.WHITE + " Themes")
        print(Fore.YELLOW + "[2]" + Fore.WHITE + " Se déconnecter")
        print(Fore.YELLOW + "[3]" + Fore.WHITE + " Mettre à jour")
        print(Fore.YELLOW + "[4]" + Fore.WHITE + " Réinstaller le Loader")
        print(Fore.YELLOW + "[5]" + Fore.WHITE + " Désinstaller le Loader")
        print(Fore.YELLOW + "[6]" + Fore.WHITE + " Activer/désactiver le démarrage auto")
        print(Fore.YELLOW + "[7]" + Fore.WHITE + " Vidée les fichiers temporaires")
        print(Fore.YELLOW + "[8]" + Fore.WHITE + " Revenir")
        print("➡️ Appuie sur une touche...")

        try:
            touche = msvcrt.getch().decode(errors='ignore')
        except:
            touche = ''

        if touche == '1':
            menu_color()
        elif touche == '2':
            deco()
        elif touche == '3':
            reinstall_loader()
        elif touche == '4':
            os.system('start https://github.com/KAMIXlevrai/Loader-NS_services')
        elif touche == '5':
            desinstaller_loader()
        elif touche == '6':
            toggle_startup_shortcut()
            input("Appuie sur une touche pour continuer...")
        elif touche == '7':
            cleanup_system()
            nettoyer_temp()
            nettoyer_prefetch()
            input("Appuie sur une touche pour continuer...")
        elif touche == '8':
            menu(username)
        else:
            typewriter("❌ Choix invalide.")
            input("Appuie sur une touche pour réessayer...")

def main_menu():
    while True:
        os.system('title NascaR services')
        print_header()
        print(Fore.YELLOW + "Connectez-vous..." + Style.RESET_ALL)
        print(Fore.YELLOW + "[1]" + Fore.WHITE + " Créer un compte")
        print(Fore.YELLOW + "[2]" + Fore.WHITE + " Se connecter")
        print(Fore.YELLOW + "[3]" + Fore.WHITE + " Quitter")
        print("➡️ Appuie sur une touche...")
        print(" ")
        print(Fore.RED + "⚠️" + Fore.RED + " Appuyer sur shift pour utiliser le menu")

        try:
            touche = msvcrt.getch().decode(errors='ignore')
        except:
            touche = ''

        if touche == '1':
            register()
        elif touche == '2':
            login()
        elif touche == '3':
            clear()
            fermeture_countdown()
        else:
            typewriter("❌ Choix invalide.")
            input("Appuie sur une touche pour réessayer...")

if __name__ == "__main__":
    check_and_install_files()
    main_menu()
