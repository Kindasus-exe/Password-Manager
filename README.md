# 🔐 Password Manager – Python

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Active-success)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20Mac-lightgrey)
![Open Source](https://img.shields.io/badge/Open%20Source-Yes-brightgreen)
![Last Commit](https://img.shields.io/github/last-commit/Kindasus-exe/Password-Manager)



## ✨ Funzionalità principali
- 🔑 Master Password con hash SHA256
- 🧂 Salt randomico per maggiore sicurezza
- 🗝️ File master.key generato automaticamente
- 📁 Gestione password (aggiungi, modifica, elimina, cerca)
- 🔒 Generatore di password sicure
- 🎨 Interfaccia colorata con Colorama
- 🧹 Codice pulito e facilmente estendibile



## 🔐 Come funziona la Master Password

# Primo avvio
Il programma chiede di creare una master password

Genera un salt casuale

Calcola l’hash SHA256 della password

Salva password_hash e salt in master.key

# Avvii successivi
L’utente inserisce la master password
Il programma calcola l’hash
Lo confronta con quello salvato
Dopo 3 tentativi falliti → uscita

''' ⚠️  master.key e passwords.json sono esclusi dalla repository tramite .gitignore. '''
