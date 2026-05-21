import json
import os
import hashlib
import base64



BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PASSWORD_FILE = os.path.join(BASE_DIR, "passwords.json")
MASTER_KEY_FILE = os.path.join(BASE_DIR, "master.key")

#Colorama per colorare i messaggi in console
from colorama import init, Fore, Style
init(autoreset=True)


#Master password functions

def check_master_password():
    # Se il file non esiste primo avvio
    if not os.path.exists(MASTER_KEY_FILE):
        print(Fore.YELLOW + "Nessuna master password trovata. Creane una ora.")
        master_password = input(Fore.WHITE + "Crea una password master: ")

        # 1. genera salt (bytes)
        salt = os.urandom(16)

        # 2. calcola hash SHA256
        password_hash = hashlib.sha256(master_password.encode()).hexdigest()

        # 3. converti salt in base64
        salt_b64 = base64.b64encode(salt).decode()

        # 4. salva tutto nel file
        data = {
            "password_hash": password_hash,
            "salt": salt_b64
        }

        with open(MASTER_KEY_FILE, "w") as f:
            json.dump(data, f)

        print(Fore.GREEN + "Master password creata con successo.")
        return master_password, salt

    # Se il file esiste verifica password
    else:
        with open(MASTER_KEY_FILE, "r") as f:
            data = json.load(f)

        saved_hash = data["password_hash"]
        salt_b64 = data["salt"]

        # ricostruisci il salt
        salt = base64.b64decode(salt_b64)

        for _ in range(3):
            master_password = input(Fore.WHITE + "Inserisci la password master: ")

            # calcola hash della password inserita
            password_hash = hashlib.sha256(master_password.encode()).hexdigest()

            if password_hash == saved_hash:
                print(Fore.GREEN + "Accesso consentito.")
                return master_password, salt

            print(Fore.RED + "Password errata.")

        print(Fore.RED + "Accesso negato.")
        exit()



# Main functions

def load_passwords():
    if not os.path.exists(PASSWORD_FILE):
        save_passwords({})
        print(Fore.GREEN + "File passwords.json creato con successo.")
        return {}

    try:
        with open(PASSWORD_FILE, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError:
        print(Fore.RED + "File corrotto. Ricreo passwords.json.")
        save_passwords({})
        return {}

def save_passwords(passwords):
    with open(PASSWORD_FILE, "w") as file:
        json.dump(passwords, file, indent=4)
        

def add_password():
    website = format_website_name(input(Fore.WHITE + "Inserisci il nome del sito web: "))
    username= input("Inserisci il nome utente: ")
    password = input("Inserisci la password: ")
    
    
    if website in load_passwords():
        print(Fore.YELLOW + "Sito web già presente. Vuoi sovrascrivere la password? (s/n)")
        scelta = input().lower()
        if scelta != 's':
            print(Fore.RED + "Operazione annullata.")
            return

    passwords = load_passwords()
    
    passwords[website] = {
        "username": username,
        "password": password
    }

    save_passwords(passwords)
    print(Fore.GREEN + "Password salvata con successo.")
    print(f"Sito web: {website}")
    print(f"Nome utente: {username}")
    print(f"Password: {password}")
    
    
    
    
def view_passwords():
    passwords = load_passwords()
    
    if not passwords:
        print(Fore.RED + "Nessuna password salvata.")
        return
    
    print(Fore.LIGHTGREEN_EX + "\n-------- Password salvate: --------")
    for website, credenziali in passwords.items():
        print(f"Sito web: {website}")
        print(f"Nome utente: {credenziali['username']}")
        print(f"Password: {credenziali['password']}")
        print("-" * 20)
        
        
def search_password():
    website= format_website_name(input(Fore.WHITE + "Inserisci il nome del sito web da cercare: "))
    passwords = load_passwords()
    
    if website in passwords:
        credenziali = passwords[website]
        print(Fore.GREEN + "------- Sito web trovato: -------")
        print(Fore.WHITE + f"Sito web: {website}")
        print(Fore.WHITE + f"Nome utente: {credenziali['username']}")
        print(Fore.WHITE + f"Password: {credenziali['password']}")
        print(Fore.GREEN + "--------------")
        
    else:
        print(Fore.RED + "Sito web non trovato.")

def edit_password():
    website = format_website_name(input(Fore.WHITE + "Inserisci il nome del sito web da modificare: "))
    passwords = load_passwords()

    if website in passwords:
        print(f"Sito web: {website}")
        print(f"Nome utente: {passwords[website]['username']}")
        print(f"Password: {passwords[website]['password']}")

        new_username = input("Inserisci il nuovo nome utente (lascia vuoto per non modificare): ")
        new_password = input("Inserisci la nuova password (lascia vuoto per non modificare): ")

        if new_username:
            passwords[website]['username'] = new_username
        if new_password:
            passwords[website]['password'] = new_password

        save_passwords(passwords)
        print(Fore.GREEN + "Password aggiornata con successo.")
    else:
        print(Fore.RED + "Sito web non trovato.")
        

def delete_password():
    website = format_website_name(input(Fore.WHITE + "Inserisci il nome del sito web da eliminare: "))
    passwords = load_passwords()
    if website in passwords:
        del passwords[website]
        save_passwords(passwords)
        print(Fore.GREEN + f"Password eliminata con successo per il sito {website}.")
        


def generate_password():
    import random
    import string
    
    try:
        lunghezza_psw = int(input(Fore.WHITE + "Inserisci la lunghezza della password: "))
    except ValueError:
        print(Fore.RED + "Input non valido. Inserisci un numero. O.o")
        return
    
    while lunghezza_psw < 4 or lunghezza_psw > 32:
        print(Fore.RED + "La lunghezza deve essere compresa tra 4 e 32 caratteri.")
        try:
            lunghezza_psw = int(input(Fore.WHITE + "Inserisci la lunghezza della password: "))
        except ValueError:
            print(Fore.RED + "Input non valido. Inserisci un numero. O.o")
            continue

    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for n in range(lunghezza_psw))
    print(Fore.MAGENTA + f"Password generata: " + Fore.WHITE + f"{password}") 

# UTILITY FUNCTIONS

def format_website_name(website):
    return website.strip().title()




# MENU PRINCIPALE

master_password, salt = check_master_password()  # Verifica o crea la master password
load_passwords()  # Carica le password all'avvio del programma

while True:
    print (f"{Fore.CYAN}\n------ Password Manager ------")
    print(Fore.LIGHTBLUE_EX + "1. Aggiungi password")
    print(Fore.LIGHTBLUE_EX + "2. Visualizza password")
    print(Fore.LIGHTBLUE_EX + "3. Cerca password")
    print(Fore.LIGHTBLUE_EX + "4. Modifica password")
    print(Fore.LIGHTBLUE_EX + "5. Elimina password")
    print(Fore.LIGHTBLUE_EX + "6. Genera password sicura")
    print(Fore.LIGHTBLUE_EX + "7. Esci")
    
    scelta = input(Fore.MAGENTA + "Scegli un'opzione: ")
    
    if scelta == "1":
        add_password()
        
    elif scelta == "2":
        view_passwords()
        
    elif scelta == "3":
        search_password()
        
    elif scelta == "4":
        edit_password()
        
    elif scelta == "5":
        delete_password()
        
    elif scelta == "6":
        generate_password()
        
    elif scelta == "7":
        print(Fore.YELLOW + "Uscita dal Password Manager. Arrivederci!")
        break
    
    else:
        print(Fore.RED + "Opzione non valida. Riprova.")
