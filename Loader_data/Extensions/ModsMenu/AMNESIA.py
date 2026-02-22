import customtkinter as ctk
from tkinter import PhotoImage
import tkinter.ttk as ttk
import os
import sys
import ctypes


# Aller dans le dossier du script
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Couleur personnalisée
VIOLET = "#B480FF"
REDLIGHT = "#d44242"

# Thèmes de base
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Titre du cmd
os.system('title Console')

# Welcome message
def show_error_message(title, message):
    ctypes.windll.user32.MessageBoxW(0, message, title, 0x30)  # 0x10 correspond à l'icône d'erreur

# Exemple d'utilisation
show_error_message("Welcome", "This Software is made by NascaR! Have Fun!")

# Fenêtre principale
app = ctk.CTk()
app.geometry("900x600")
app.title("AMNESIA - Mod Menu")
try:
    logo_img = PhotoImage(file="assets/logo.png")  # Remplace "path_to_your_logo.png" par le chemin de ton fichier PNG
    app.iconphoto(True, logo_img)
except Exception as e:
    print(f"Erreur lors du chargement de l'icône PNG : {e}")

# Fonction pour changer le thème
def toggle_theme():
    mode = ctk.get_appearance_mode()
    new_mode = "light" if mode == "dark" else "dark"
    ctk.set_appearance_mode(new_mode)

# === SIDEBAR ===
sidebar = ctk.CTkFrame(app, width=160, corner_radius=0)
sidebar.pack(side="left", fill="y")

logo = ctk.CTkLabel(sidebar, text="⚡ AMNESIA", font=("Arial", 22, "bold"), text_color=VIOLET)
logo.pack(pady=40)

def show_frame(name):
    for frame in frames.values():
        frame.pack_forget()
    frames[name].pack(fill="both", expand=True, padx=20, pady=20)

# Boutons de navigation
ctk.CTkButton(sidebar, text="🎯 Aim", command=lambda: show_frame("aim"), fg_color="transparent", text_color=VIOLET, hover_color="#222").pack(pady=10)
ctk.CTkButton(sidebar, text="👀 ESP", command=lambda: show_frame("esp"), fg_color="transparent", text_color=VIOLET, hover_color="#222").pack(pady=10)
ctk.CTkButton(sidebar, text="🔫 Weapons", command=lambda: show_frame("weapons"), fg_color="transparent", text_color=VIOLET, hover_color="#222").pack(pady=10)
ctk.CTkButton(sidebar, text="🚗 Vehicule", command=lambda: show_frame("car"), fg_color="transparent", text_color=VIOLET, hover_color="#222").pack(pady=10)
ctk.CTkButton(sidebar, text="🏃 Player", command=lambda: show_frame("player"), fg_color="transparent", text_color=VIOLET, hover_color="#222").pack(pady=10)
ctk.CTkButton(sidebar, text="📦​ Inventory", command=lambda: show_frame("inventory"), fg_color="transparent", text_color=VIOLET, hover_color="#222").pack(pady=10)
ctk.CTkButton(sidebar, text="⚙️ Settings", command=lambda: show_frame("settings"), fg_color="transparent", text_color=VIOLET, hover_color="#222").pack(pady=10)

# === MAIN PANEL ===
main_panel = ctk.CTkFrame(app)
main_panel.pack(side="left", fill="both", expand=True)

# Dictionnaire des onglets
frames = {
    "aim": ctk.CTkFrame(main_panel),
    "esp": ctk.CTkFrame(main_panel),
    "weapons": ctk.CTkFrame(main_panel),
    "car": ctk.CTkFrame(main_panel),
    "player": ctk.CTkFrame(main_panel),
    "inventory": ctk.CTkFrame(main_panel),
    "settings": ctk.CTkFrame(main_panel),
}


# === ONGLET AIM ===
ctk.CTkLabel(frames["aim"], text="🎯 Aim Settings", font=("Arial", 22, "bold"), text_color=VIOLET).pack(pady=10)


def toggle_Aimbot():
    if aimbot_switch.get() == 1:
        print("✅ Aimbot activé")
    else:
        print("❌ Aimbot désactivé")

aimbot_switch = ctk.CTkSwitch(frames["aim"], text="Aimbot", switch_height=20, switch_width=40, progress_color=VIOLET, command=toggle_Aimbot)
aimbot_switch.pack(pady=10)



# 👉 Déclarer la fonction d'abord !
def on_aim(val):
    aim_value.configure(text=f"{round(val,1)}x")

ctk.CTkLabel(frames["aim"], text="Aim Smooth").pack()
ctk.CTkSlider(frames["aim"], from_=1, to=10, command=on_aim, progress_color=VIOLET).pack(pady=10)
aim_value = ctk.CTkLabel(frames["aim"], text="1x", text_color=VIOLET)
aim_value.pack()

# === ONGLET ESP ===
ctk.CTkLabel(frames["esp"], text="👀 ESP Settings", font=("Arial", 22, "bold"), text_color=VIOLET).pack(pady=10)

def toggle_Wallhack():
    if Wallhack_switch.get() == 1:
        print("✅ WallHack activé")
    else:
        print("❌ WallHack désactivé")

Wallhack_switch = ctk.CTkSwitch(frames["esp"], text="WallHack", switch_height=20, switch_width=40, progress_color=VIOLET, command=toggle_Wallhack)
Wallhack_switch.pack(pady=10)


# === ONGLET WEAPONS ===
ctk.CTkLabel(frames["weapons"], text="🔫 Weapons Settings", font=("Arial", 22, "bold"), text_color=VIOLET).pack(pady=10)

def give_weapon():
    print("🔫 Give weapon:", weapon_menu.get())

def toggle_No_Recoil():
    if no_recoil_switch.get() == 1:
        print("✅ No Recoil activé")
    else:
        print("❌ No Recoil désactivé")

no_recoil_switch = ctk.CTkSwitch(frames["weapons"], text="No Recoil", switch_height=20, switch_width=40, progress_color=VIOLET, command=toggle_No_Recoil)
no_recoil_switch.pack(pady=10)




def toggle_Unlimited_Ammo():
    if unlimited_ammo_switch.get() == 1:
        print("✅ Unlimited Ammo activé")
    else:
        print("❌ Unlimited Ammo désactivé")

unlimited_ammo_switch = ctk.CTkSwitch(frames["weapons"], text="Unlimited Ammo", switch_height=20, switch_width=40, progress_color=VIOLET, command=toggle_Unlimited_Ammo)
unlimited_ammo_switch.pack(pady=10)



valid_weapons = ["Uzi", "Shotgun", "Toilet Brush"]

def validate_weapon_choice(event=None):
    choice = weapon_menu.get()
    if choice not in valid_weapons:
        weapon_menu.set(valid_weapons[0])

weapon_menu = ctk.CTkComboBox(
    master=frames["weapons"],
    values=valid_weapons,
    button_color=VIOLET,
    dropdown_fg_color=VIOLET,
    dropdown_text_color="white",
    dropdown_hover_color="#7b2cbf",  # Plus foncé pour le survol
    text_color="white",
    fg_color="#3c096c",  # Couleur du champ principal
    border_color=VIOLET,
    border_width=2
)
weapon_menu.pack(pady=10)
weapon_menu.bind("<FocusOut>", validate_weapon_choice)
weapon_menu.set(valid_weapons[0])  # Valeur par défaut




ctk.CTkButton(frames["weapons"], text="🔫 Give Weapon", fg_color=VIOLET, hover_color="#9b5de5", command=give_weapon).pack(pady=20)



# === ONGLET VEHICULE ===
ctk.CTkLabel(frames["car"], text="🚗 Car Mods", font=("Arial", 22, "bold"), text_color=VIOLET).pack(pady=10)

def toggle_nogravity():
    if nogravity_switch.get() == 1:
        print("✅ Nogravity activé")
    else:
        print("❌ Nogravity désactivé")

nogravity_switch = ctk.CTkSwitch(frames["car"], text="Nogravity", progress_color=VIOLET, command=toggle_nogravity)
nogravity_switch.pack(pady=10)


# 👉 Déclarer la fonction d'abord !
def on_carspeed(val):
    carspeed_value.configure(text=f"{round(val,1)}x")

ctk.CTkLabel(frames["car"], text="Car Speed").pack()
ctk.CTkSlider(frames["car"], from_=1, to=10, command=on_carspeed, progress_color=VIOLET).pack(pady=10)
carspeed_value = ctk.CTkLabel(frames["car"], text="1x", text_color=VIOLET)
carspeed_value.pack()


# === ONGLET PLAYER ===
ctk.CTkLabel(frames["player"], text="🏃 Player Mods", font=("Arial", 22, "bold"), text_color=VIOLET).pack(pady=10)

def toggle_god_mode():
    if god_mode_switch.get() == 1:
        print("✅ God Mode activé")
    else:
        print("❌ God Mode désactivé")

def on_speed(val):
    speed_value.configure(text=f"{round(val,1)}x")

god_mode_switch = ctk.CTkSwitch(frames["player"], text="God Mode", progress_color=VIOLET, command=toggle_god_mode)
god_mode_switch.pack(pady=10)

ctk.CTkLabel(frames["player"], text="Speed").pack()
ctk.CTkSlider(frames["player"], from_=1, to=10, command=on_speed, progress_color=VIOLET).pack(pady=10)
speed_value = ctk.CTkLabel(frames["player"], text="1x", text_color=VIOLET)
speed_value.pack()

def toggle_noclip():
    if noclip_switch.get() == 1:
        print("✅ Noclip activé")
    else:
        print("❌ Noclip désactivé")

noclip_switch = ctk.CTkSwitch(frames["player"], text="Noclip", progress_color=VIOLET, command=toggle_noclip)
noclip_switch.pack(pady=10)

# === ONGLET INVENTORY ===
ctk.CTkLabel(frames["inventory"], text="💰 Money", font=("Arial", 22, "bold"), text_color=VIOLET).pack(pady=10)

def toggle_Infinite_Money():
    if infinite_money_switch.get() == 1:
        print("✅ Infinite Money activé")
    else:
        print("❌ Infinite Money désactivé")

infinite_money_switch = ctk.CTkSwitch(frames["inventory"], text="Infinite Money", switch_height=20, switch_width=40, progress_color=VIOLET, command=toggle_Infinite_Money)
infinite_money_switch.pack(pady=10)



def on_money(val):
    money_value.configure(text=f"{round(val,1)}x")

ctk.CTkLabel(frames["inventory"], text="Money").pack()
ctk.CTkSlider(frames["inventory"], from_=0, to=9999, command=on_money, progress_color=VIOLET).pack(pady=10)
money_value = ctk.CTkLabel(frames["inventory"], text="0$", text_color=VIOLET)
money_value.pack()

ctk.CTkLabel(frames["inventory"], text="💼 Inventory Contain", font=("Arial", 22, "bold"), text_color=VIOLET).pack(pady=10)

def clear_inventory():
    print("🗑️ Inventaire vidé.")

ctk.CTkButton(frames["inventory"], text="🗑️ Clear Inventory", command=clear_inventory, fg_color=VIOLET, hover_color="#9b5de5").pack(pady=10)

def give_object():
    print("🏹 Give object:", object_menu.get())

valid_objects = ["Meat", "Drinks", "Grenade"]

def validate_object_choice(event=None):
    choice = object_menu.get()
    if choice not in valid_objects:
        object_menu.set(valid_objects[0])

object_menu = ctk.CTkComboBox(
    master=frames["inventory"],
    values=valid_objects,
    button_color=VIOLET,
    dropdown_fg_color=VIOLET,
    dropdown_text_color="white",
    dropdown_hover_color="#7b2cbf",  # Plus foncé pour le survol
    text_color="white",
    fg_color="#3c096c",  # Couleur du champ principal
    border_color=VIOLET,
    border_width=2
)
object_menu.pack(pady=10)
object_menu.bind("<FocusOut>", validate_object_choice)
object_menu.set(valid_objects[0])  # Valeur par défaut




ctk.CTkButton(frames["inventory"], text="🏹 Give Object", fg_color=VIOLET, hover_color="#9b5de5", command=give_object).pack(pady=20)




def give_all():
    print("🌀 Inventaire Remplie.")

ctk.CTkButton(frames["inventory"], text="🌀 Give All [RISK]", command=give_all, fg_color=VIOLET, hover_color="#9b5de5").pack(pady=10)


# === ONGLET SETTINGS ===
ctk.CTkLabel(frames["settings"], text="⚙️ Settings", font=("Arial", 22, "bold"), text_color=VIOLET).pack(pady=10)

theme_toggle = ctk.CTkSwitch(frames["settings"], text="Light / Dark Mode", command=toggle_theme, progress_color=VIOLET)
theme_toggle.pack(pady=20)

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("🧹 Terminal nettoyé.")

ctk.CTkButton(frames["settings"], text="🧹 Clear Terminal", command=clear_terminal, fg_color=VIOLET, hover_color="#9b5de5").pack(pady=10)

def exit_terminal():
    sys.exit()

ctk.CTkButton(frames["settings"], text="✈️ Quit", command=exit_terminal, fg_color=REDLIGHT, hover_color="#9b5de5").pack(pady=10)

# Lancement initial
show_frame("weapons")
app.mainloop()
