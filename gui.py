import customtkinter as ctk
import os

from main import load_passwords, save_passwords, add_password, delete_password, edit_password, search_password, generate_password, check_master_password, format_website_name, view_passwords, MASTER_KEY_FILE
#from main import *

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


#Utility functions
class Utility:
    def bind_enter_key(self, entry, next_widget):
        def handle(event):
            if isinstance(next_widget, ctk.CTkButton):
                next_widget.invoke()
            else:
                next_widget.focus()
        entry.bind("<Return>", handle)
        
    def toggle_password(self, entry, button):
        if entry.cget("show") == "*":
            entry.configure(show="")
            button.configure(text="🙈")
        else:
            entry.configure(show="*")
            button.configure(text="👁")

    def password_field(self, parent, password):
        psw_frame = ctk.CTkFrame(parent, fg_color="transparent")
        psw_frame.pack(anchor="w", padx=15, pady=(2,10))
        
        psw_entry = ctk.CTkEntry(psw_frame, show="*")
        psw_entry.insert(0, password)
        psw_entry.configure(state="readonly")
        psw_entry.pack(side="left")
        
        toggle_btn = ctk.CTkButton(psw_frame, text="👁", width=30, command=lambda: None)
        toggle_btn.configure(command=lambda e=psw_entry, b=toggle_btn: self.toggle_password(e, b))
        toggle_btn.pack(side="left", padx=5)
        
        return psw_entry


class LoginWindow(ctk.CTk, Utility):
    def __init__(self):
        super().__init__()
        
        self.title("Login")
        self.geometry("400x300")
        if not os.path.exists(MASTER_KEY_FILE):
            self.label = ctk.CTkLabel(self, text="Crea una Master Password")
            testo_button = "Crea"
        else:
            self.label = ctk.CTkLabel(self, text="Inserisci la Master Password")
            testo_button = "Accedi"
        
        self.label.pack(pady=20)
        psw_frame = ctk.CTkFrame(self, fg_color="transparent")
        psw_frame.pack(pady=10)

        self.password_entry = ctk.CTkEntry(psw_frame, show="*")
        self.password_entry.pack(side="left", padx=5)
        self.after(500, lambda: (self.focus_force(), self.password_entry.focus_set()))  # Focus automatico sull'entry

        self.toggle_button = ctk.CTkButton(psw_frame, text="👁", width=30,
            command=lambda: self.toggle_password(self.password_entry, self.toggle_button))
        self.toggle_button.pack(side="left")
        
        self.login_button = ctk.CTkButton(self, text=testo_button, command=self.check_password)
        self.login_button.pack(pady=10)
        
        self.bind_enter_key(self.password_entry, self.login_button)

    def check_password(self):
        try:
            password = self.password_entry.get()
            if check_master_password(password):
                self.destroy()
                app = App()
                app.mainloop()
            else:
                ctk.CTkLabel(self, text="Password errata!").pack(pady=10)
        except Exception as e:
            ctk.CTkLabel(self, text="Errore durante il controllo della password!").pack(pady=10)
            return


class App(ctk.CTk, Utility):
    def __init__(self):
        super().__init__()
        
        self.title("Password Manager GUI")
        self.geometry("900x650")
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0, fg_color="#1a1a2e")
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.pack_propagate(False)
        
        self.main_area = ctk.CTkFrame(self, corner_radius=0)
        self.main_area.grid(row=0, column=1, sticky="nsew")
        
        
        self.sidebar_title = ctk.CTkLabel(self.sidebar, text="🔐 Password Manager",)
        self.sidebar_title.pack(pady=20, padx=10)

        
        #Pulsanti della sidebar
        
        #Home
        self.sidebar_button1 = ctk.CTkButton(self.sidebar, text="Home", command=self.show_home)
        self.sidebar_button1.pack(pady=10, padx=10)

        #Aggiungi Password
        self.sidebar_button2 = ctk.CTkButton(self.sidebar, text="Aggiungi Password", command=self.add_password)
        self.sidebar_button2.pack(pady=10, padx=10)
        
        #Elimina Password
        self.sidebar_button3 = ctk.CTkButton(self.sidebar, text="Elimina Password", command=self.del_password)
        self.sidebar_button3.pack(pady=10, padx=10)
        
        #Modifica Password  
        self.sidebar_button4 = ctk.CTkButton(self.sidebar, text="Modifica Password", command=self.modify_password)
        self.sidebar_button4.pack(pady=10, padx=10)
        
        #Cerca Password
        self.sidebar_button5 = ctk.CTkButton(self.sidebar, text="Cerca Password", command=self.find_password)
        self.sidebar_button5.pack(pady=10, padx=10)
        
        #Visualizza Passwords
        self.sidebar_button6 = ctk.CTkButton(self.sidebar, text="Visualizza Passwords", command=self.show_passwords)
        self.sidebar_button6.pack(pady=10, padx=10)
        
        #Genera Password
        self.sidebar_button7 = ctk.CTkButton(self.sidebar, text="Genera Password", command=self.show_generate_password)
        self.sidebar_button7.pack(pady=10, padx=10)
        
        #Chiudi App
        self.sidebar_button8 = ctk.CTkButton(self.sidebar, text="Esci", command=self.exit)
        self.sidebar_button8.pack(pady=10, padx=10)


    #Funzioni per i pulsanti della sidebar
    def show_home(self):
        for widget in self.main_area.winfo_children():
            widget.destroy()
        home_label = ctk.CTkLabel(self.main_area, text="Welcome to the Password Manager!")
        home_label.pack(pady=20)
        
    def add_password(self):
        for widget in self.main_area.winfo_children():
            widget.destroy()
        
        ctk.CTkLabel(self.main_area, text="Aggiungi Password").pack(pady=20)
        
        form_frame = ctk.CTkFrame(self.main_area, fg_color="transparent")
        form_frame.pack(expand=True)
        
        self.aggiungi_sito = ctk.CTkEntry(form_frame, placeholder_text="Sito", width=250)
        self.aggiungi_sito.pack(pady=10, padx=10, anchor="w")
        
        self.aggiungi_sito.focus_set()
        
        self.aggiungi_username = ctk.CTkEntry(form_frame, placeholder_text="Username", width=250)
        self.aggiungi_username.pack(pady=10, padx=10, anchor="w")
        
        psw_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        psw_frame.pack(pady=10, anchor="w")
        
        self.aggiungi_password = ctk.CTkEntry(psw_frame, placeholder_text="Password", show="*", width=250)
        self.aggiungi_password.pack(side="left", padx=5)
        
        self.toggle_aggiungi_password = ctk.CTkButton(psw_frame, text="👁", width=30,
            command=lambda: self.toggle_password(self.aggiungi_password, self.toggle_aggiungi_password))
        self.toggle_aggiungi_password.pack(side="left")

        self.salva_button = ctk.CTkButton(form_frame, text="Salva", command=self.save_password, width=284)
        self.salva_button.pack(pady=10, padx=10, anchor="w")
        
        self.bind_enter_key(self.aggiungi_sito, self.aggiungi_username)
        self.bind_enter_key(self.aggiungi_username, self.aggiungi_password)
        self.bind_enter_key(self.aggiungi_password, self.salva_button)
        
        
        
    def save_password(self):
        try:
            sito = self.aggiungi_sito.get()
            username = self.aggiungi_username.get()
            password = self.aggiungi_password.get()
            
            if sito and username and password:
                add_password(sito, username, password)
                ctk.CTkLabel(self.main_area, text="✅ Password salvata!").pack(pady=10)
            else:
                ctk.CTkLabel(self.main_area, text="⚠️ Compila tutti i campi!").pack(pady=10)
        except Exception as e:
            ctk.CTkLabel(self.main_area, text="⚠️ Errore nel salvataggio della password!").pack(pady=10)
            return

    def del_password(self):
        for widget in self.main_area.winfo_children():
            widget.destroy()
        delete_password_label = ctk.CTkLabel(self.main_area, text="Elimina Password")
        delete_password_label.pack(pady=20)
        
        form_frame = ctk.CTkFrame(self.main_area, fg_color="transparent")
        form_frame.pack(expand=True)
        
        self.elimina_sito = ctk.CTkEntry(form_frame, placeholder_text="Sito da eliminare", width=250)
        self.elimina_sito.pack(pady=10, padx=10, anchor="w")
        self.elimina_sito.focus_set()
        
        self.elimina_button = ctk.CTkButton(form_frame, text="Elimina", command=self.do_delete, width=284, fg_color="#ff4d4d", hover_color="#ff1a1a")
        self.elimina_button.pack(pady=10, padx=10, anchor="w")
        self.bind_enter_key(self.elimina_sito, self.elimina_button) 
        
    def do_delete(self):
        try:
            sito = format_website_name(self.elimina_sito.get())

            passwords = load_passwords()
            
            if sito in passwords:
                delete_password(sito)
                ctk.CTkLabel(self.main_area, text="✅ Password eliminata!").pack(pady=10)
            else:
                ctk.CTkLabel(self.main_area, text="⚠️ Sito non trovato!").pack(pady=10)
        except Exception as e:
            ctk.CTkLabel(self.main_area, text="⚠️ Errore nell'eliminazione della password!").pack(pady=10)
            return

    def modify_password(self):
        for widget in self.main_area.winfo_children():
            widget.destroy()
        edit_password_label = ctk.CTkLabel(self.main_area, text="Modifica Credenziali")
        edit_password_label.pack(pady=20)
    
        form_frame = ctk.CTkFrame(self.main_area, fg_color="transparent")
        form_frame.pack(expand=True)
        
        self.modifica_sito = ctk.CTkEntry(form_frame, placeholder_text="Sito da modificare", width=250)
        self.modifica_sito.pack(pady=10, padx=10, anchor="w")
        self.modifica_sito.focus_set()
        
        self.modifica_username = ctk.CTkEntry(form_frame, placeholder_text="Nuovo Username (opzionale)", width=250)
        self.modifica_username.pack(pady=10, padx=10, anchor="w")
        
        psw_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        psw_frame.pack(pady=10, anchor="w")
        
        self.modifica_password = ctk.CTkEntry(psw_frame, placeholder_text="Nuova Password (opzionale)", show="*", width=250)
        self.modifica_password.pack(pady=10, padx=10, side="left")
        
        self.toggle_modifica_password = ctk.CTkButton(psw_frame, text="👁", width=30,
            command=lambda: self.toggle_password(self.modifica_password, self.toggle_modifica_password))    
        self.toggle_modifica_password.pack(pady=10, padx=10, side="left")
        
        self.modifica_button = ctk.CTkButton(form_frame, text="Modifica", command=self.do_modify, width=284, fg_color="#4a90e2", hover_color="#1DA724")
        self.modifica_button.pack(pady=10, padx=10, anchor="w")
        
        self.bind_enter_key(self.modifica_sito, self.modifica_username)
        self.bind_enter_key(self.modifica_username, self.modifica_password)
        self.bind_enter_key(self.modifica_password, self.modifica_button)
        
    def do_modify(self):
        try:
            sito = format_website_name(self.modifica_sito.get())

            new_username = self.modifica_username.get()
            new_password = self.modifica_password.get()
            
            if edit_password(sito, new_username, new_password):
                ctk.CTkLabel(self.main_area, text="✅ Credenziali modificate!").pack(pady=10)
            else:
                ctk.CTkLabel(self.main_area, text="⚠️ Sito non trovato!").pack(pady=10)
        except Exception as e:
            ctk.CTkLabel(self.main_area, text="⚠️ Errore nella modifica delle credenziali!").pack(pady=10)
            return
            

    def find_password(self):
        for widget in self.main_area.winfo_children():
            widget.destroy()
        find_password_label = ctk.CTkLabel(self.main_area, text="Cerca Password")
        find_password_label.pack(pady=20)
        
        self.form_frame = ctk.CTkFrame(self.main_area, fg_color="transparent")
        self.form_frame.pack(expand=True)
        
        self.cerca_sito = ctk.CTkEntry(self.form_frame, placeholder_text="Sito da cercare", width=250)
        self.cerca_sito.pack(pady=10, padx=10, anchor="w")
        self.cerca_sito.focus_set()
        
        self.cerca_button = ctk.CTkButton(self.form_frame, text="Cerca", command=self.do_search, width=284)
        self.cerca_button.pack(pady=10, padx=10, anchor="w")
        self.bind_enter_key(self.cerca_sito, self.cerca_button)
        
    def do_search(self):
        try:
            sito = format_website_name(self.cerca_sito.get())
            passwords = load_passwords()
            
            if sito in passwords:
                credenziali = passwords[sito]
                card = ctk.CTkFrame(self.form_frame, fg_color="#2b2b2b", corner_radius=10, border_width=2, border_color="#4a4a4a")
                card.pack(pady=10, padx=20, fill="x")
                ctk.CTkLabel(card, text=f"🌐 {sito}", font=("Arial", 14, "bold")).pack(anchor="w", padx=15, pady=(10,2))
                ctk.CTkLabel(card, text=f"👤 {credenziali['username']}").pack(anchor="w", padx=15, pady=2)
                self.password_field(card, credenziali['password'])
            else:
                ctk.CTkLabel(self.form_frame, text="⚠️ Sito non trovato!").pack(pady=10)
        except Exception as e:
            ctk.CTkLabel(self.form_frame, text="⚠️ Errore nella ricerca della password!").pack(pady=10)
            return

    def show_passwords(self):
        for widget in self.main_area.winfo_children():
            widget.destroy()
        show_passwords_label = ctk.CTkLabel(self.main_area, text="Password Salvate")
        show_passwords_label.pack(pady=20)
        
        self.scroll_frame = ctk.CTkScrollableFrame(self.main_area)
        self.scroll_frame.pack(fill="both", expand=True, pady=10, padx=10)
        passwords = load_passwords()
        if not passwords:
            ctk.CTkLabel(self.scroll_frame, text="Nessuna password salvata.").pack(pady=10)
        else:
            for website, credenziali in passwords.items():
                card = ctk.CTkFrame(self.scroll_frame, corner_radius=10, fg_color="#2b2b2b")
                card.pack(pady=5, padx=10, fill="x")

                ctk.CTkLabel(card, text=f"🌐 {website}", font=("Arial", 14, "bold")).pack(anchor="w", padx=15, pady=(10,2))
                ctk.CTkLabel(card, text=f"👤 {credenziali['username']}").pack(anchor="w", padx=15, pady=2)
                self.password_field(card, credenziali['password'])
        
    def show_generate_password(self):
        for widget in self.main_area.winfo_children():
            widget.destroy()
        show_generate_password_label = ctk.CTkLabel(self.main_area, text="Generatore di Password")
        show_generate_password_label.pack(pady=20)
        
        form_frame = ctk.CTkFrame(self.main_area, fg_color="transparent")
        form_frame.pack(expand=True)
        
        self.slider_value = 12
        ctk.CTkSlider(form_frame, from_=4, to=32, number_of_steps=24, command=self.update_password_length).pack(pady=10)
        self.password_length_label = ctk.CTkLabel(form_frame, text="Lunghezza: 12")
        self.password_length_label.pack(pady=5) 
        
        psw_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        psw_frame.pack(pady=10, anchor="w")
        
        self.generated_password_entry = ctk.CTkEntry(psw_frame, width=250)
        self.generated_password_entry.pack(pady=10, padx=10, side="left")
        
        self.toggle_generated_password = ctk.CTkButton(psw_frame, text="👁", width=30,
            command=lambda: self.toggle_password(self.generated_password_entry, self.toggle_generated_password))    
        self.toggle_generated_password.pack(pady=10, padx=10, side="left")
        
        self.generate_button = ctk.CTkButton(form_frame, text="Genera Password", command=self.do_generate_password, width=284, fg_color="#4a90e2", hover_color="#1DA724")
        self.generate_button.pack(pady=10, padx=10, anchor="w")
        
    def update_password_length(self, val):
        self.slider_value = int(val)
        self.password_length_label.configure(text=f"Lunghezza: {int(val)}")
        
    def do_generate_password(self):
        password = generate_password(self.slider_value)
        self.generated_password_entry.configure(state="normal")
        self.generated_password_entry.delete(0, "end")
        self.generated_password_entry.insert(0, password)
        self.generated_password_entry.configure(state="readonly")
        
    def exit(self):
        self.destroy()
        


#Avvio dell'applicazione
if __name__ == "__main__":
    login_window = LoginWindow()
    login_window.mainloop()
    