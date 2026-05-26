# 🔐 Password Manager – Python

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Active-success)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20Mac-lightgrey)
![Open Source](https://img.shields.io/badge/Open%20Source-Yes-brightgreen)
![Last Commit](https://img.shields.io/github/last-commit/Kindasus-exe/Password-Manager)



## ✨ Funzionalità

- 🔑 Master Password con hash SHA256 e salt randomico
- 🖥️ Interfaccia grafica moderna con CustomTkinter (dark mode)
- 💻 Interfaccia CLI colorata con Colorama
- 📁 Gestione completa — aggiungi, modifica, elimina, cerca password
- 👁️ Mostra/nascondi password con bottone dedicato
- 🔒 Generatore di password sicure con lunghezza personalizzabile
- 🧹 Codice modulare e facilmente estendibile

## 🖥️ Interfaccia grafica (GUI)
Al primo avvio ti verrà chiesto di creare una master password. Agli avvii successivi dovrai inserirla per accedere.
La GUI include:

- Login/Registrazione con master password
- Sidebar di navigazione con tutte le funzioni
- Aggiungi Password — form con campi sito, username e password
- Visualizza Password — lista scrollabile con tutte le credenziali
- Cerca Password — ricerca per nome sito
- Modifica Password — aggiorna username e/o password
- Elimina Password — rimozione credenziali per sito
- Generatore — slider per la lunghezza, password generata istantaneamente


## 💻 Interfaccia CLI
Avvia main.py per usare la versione da terminale:


## 🔐 Come funziona la Master Password

# Primo avvio
1. Il programma chiede di creare una master password
2. Genera un salt casuale con os.urandom(16)
3. Calcola l'hash SHA256 della password
4. Salva password_hash e salt in master.key

# Avvii successivi
1. L’utente inserisce la master password
2. Il programma calcola l’hash
3. Accesso consentito solo se gli hash coincidono
4. Dopo 3 tentativi falliti → uscita

***⚠️  master.key e passwords.json sono esclusi dalla repository tramite .gitignore.***


## Dipendenze

'''
customtkinter
colorama
pillow
'''
