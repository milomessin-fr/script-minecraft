import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import shutil
import os
import json
import time

class MinescriptManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Minescript Manager")
        self.root.geometry("750x750")
        self.root.resizable(True, True)
        
        # Variables
        self.destination_path = tk.StringVar()
        self.script_path = tk.StringVar()
        
        # Style
        bg_color = "#2b2b2b"
        fg_color = "#ffffff"
        button_color = "#4a9eff"
        
        self.root.configure(bg=bg_color)
        
        # Titre
        title = tk.Label(root, text="🎮 Minescript Manager", 
                        font=("Arial", 16, "bold"), 
                        bg=bg_color, fg=fg_color)
        title.pack(pady=15)
        
        # Frame pour le dossier de destination
        dest_frame = tk.Frame(root, bg=bg_color)
        dest_frame.pack(pady=8, padx=20, fill="x")
        
        tk.Label(dest_frame, text="Dossier Minescript:", 
                bg=bg_color, fg=fg_color, font=("Arial", 10, "bold")).pack(anchor="w")
        
        dest_entry_frame = tk.Frame(dest_frame, bg=bg_color)
        dest_entry_frame.pack(fill="x", pady=5)
        
        tk.Entry(dest_entry_frame, textvariable=self.destination_path, 
                font=("Arial", 9), width=60).pack(side="left", padx=(0, 10))
        
        tk.Button(dest_entry_frame, text="📁 Parcourir", 
                 command=self.select_destination, 
                 bg=button_color, fg=fg_color, 
                 font=("Arial", 9), cursor="hand2").pack(side="left")
        
        # Frame pour le script source
        script_frame = tk.Frame(root, bg=bg_color)
        script_frame.pack(pady=8, padx=20, fill="x")
        
        tk.Label(script_frame, text="Script à copier:", 
                bg=bg_color, fg=fg_color, font=("Arial", 10, "bold")).pack(anchor="w")
        
        script_entry_frame = tk.Frame(script_frame, bg=bg_color)
        script_entry_frame.pack(fill="x", pady=5)
        
        tk.Entry(script_entry_frame, textvariable=self.script_path, 
                font=("Arial", 9), width=60).pack(side="left", padx=(0, 10))
        
        tk.Button(script_entry_frame, text="📄 Parcourir", 
                 command=self.select_script, 
                 bg=button_color, fg=fg_color, 
                 font=("Arial", 9), cursor="hand2").pack(side="left")
        
        # Bouton pour copier
        tk.Button(root, text="🚀 Copier le script", 
             command=self.copy_script, 
             bg="#4caf50", fg=fg_color, 
             font=("Arial", 11, "bold"), 
             cursor="hand2", 
             padx=20, pady=8).pack(pady=10)

        # Separator
        ttk.Separator(root, orient='horizontal').pack(fill='x', padx=20, pady=5)

        # Frame pour la liste des scripts existants
        list_label_frame = tk.Frame(root, bg=bg_color)
        list_label_frame.pack(padx=20, fill="x")
        
        tk.Label(list_label_frame, text="📋 Scripts dans le dossier Minescript:", 
            bg=bg_color, fg=fg_color, font=("Arial", 11, "bold")).pack(side="left")
        
        tk.Button(list_label_frame, text="🔄 Actualiser", 
             command=self.refresh_list, 
             bg=button_color, fg=fg_color, 
             font=("Arial", 9), cursor="hand2").pack(side="right")

        # Frame avec canvas et scrollbar pour la liste de scripts
        list_container = tk.Frame(root, bg=bg_color)
        list_container.pack(padx=20, pady=10, fill="both", expand=True)

        # Canvas avec scrollbar
        self.canvas = tk.Canvas(list_container, bg="#1e1e1e", highlightthickness=0)
        scrollbar = tk.Scrollbar(list_container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#1e1e1e")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Légende
        legend_frame = tk.Frame(root, bg=bg_color)
        legend_frame.pack(padx=20, pady=5, fill="x")
        
        tk.Label(legend_frame, text="🟢 À jour  ", 
                bg=bg_color, fg="#4caf50", font=("Arial", 9)).pack(side="left", padx=5)
        tk.Label(legend_frame, text="🟠 Mise à jour disponible  ", 
                bg=bg_color, fg="#ff9800", font=("Arial", 9)).pack(side="left", padx=5)
        tk.Label(legend_frame, text="🔵 Non suivi  ", 
                bg=bg_color, fg="#2196f3", font=("Arial", 9)).pack(side="left", padx=5)
        tk.Label(legend_frame, text="🔴 Source manquante", 
                bg=bg_color, fg="#f44336", font=("Arial", 9)).pack(side="left", padx=5)

        # Separator avant console
        ttk.Separator(root, orient='horizontal').pack(fill='x', padx=20, pady=10)

        # Console de logs
        console_label_frame = tk.Frame(root, bg=bg_color)
        console_label_frame.pack(padx=20, fill="x")
        
        tk.Label(console_label_frame, text="📝 Console de logs:", 
            bg=bg_color, fg=fg_color, font=("Arial", 11, "bold")).pack(side="left")
        
        tk.Button(console_label_frame, text="🗑️ Effacer", 
             command=self.clear_logs, 
             bg="#f44336", fg=fg_color, 
             font=("Arial", 9), cursor="hand2").pack(side="right")

        # Frame pour la console
        console_frame = tk.Frame(root, bg=bg_color)
        console_frame.pack(padx=20, pady=5, fill="both")

        # Text widget pour les logs avec scrollbar
        log_scroll = tk.Scrollbar(console_frame)
        log_scroll.pack(side="right", fill="y")

        self.log_text = tk.Text(
            console_frame, 
            height=8, 
            bg="#0a0a0a", 
            fg="#00ff00",
            font=("Consolas", 9),
            yscrollcommand=log_scroll.set,
            state="disabled",
            wrap="word"
        )
        self.log_text.pack(side="left", fill="both", expand=True)
        log_scroll.config(command=self.log_text.yview)

        # Tags pour différentes couleurs
        self.log_text.tag_config("info", foreground="#00ff00")
        self.log_text.tag_config("success", foreground="#4caf50")
        self.log_text.tag_config("warning", foreground="#ff9800")
        self.log_text.tag_config("error", foreground="#f44336")
        self.log_text.tag_config("timestamp", foreground="#888888")

        # Config storage
        self.config_path = os.path.join(os.path.expanduser("~"), ".minescript_manager.json")
        self.config = {"destination": "", "mapping": {}}
        self.load_config()
        
        # If config had a destination, populate the field
        if self.config.get("destination"):
            self.destination_path.set(self.config.get("destination"))
        
        # Log de démarrage
        self.log("Application démarrée", "info")
        if self.config.get("destination"):
            self.log(f"Dossier chargé: {self.config.get('destination')}", "info")
        
        self.refresh_list()
    
    def log(self, message, log_type="info"):
        """Ajouter un message dans la console de logs"""
        self.log_text.config(state="normal")
        
        # Timestamp
        timestamp = time.strftime("%H:%M:%S")
        self.log_text.insert("end", f"[{timestamp}] ", "timestamp")
        
        # Message avec couleur selon le type
        self.log_text.insert("end", f"{message}\n", log_type)
        
        self.log_text.config(state="disabled")
        self.log_text.see("end")  # Auto-scroll vers le bas
    
    def clear_logs(self):
        """Effacer tous les logs"""
        self.log_text.config(state="normal")
        self.log_text.delete(1.0, "end")
        self.log_text.config(state="disabled")
        self.log("Logs effacés", "info")
        
    def select_destination(self):
        """Sélectionner le dossier de destination"""
        folder = filedialog.askdirectory(title="Choisir le dossier Minescript")
        if folder:
            self.destination_path.set(folder)
            # save preference and refresh list
            self.config["destination"] = folder
            self.save_config()
            self.log(f"Dossier de destination défini: {folder}", "success")
            self.refresh_list()
    
    def select_script(self):
        """Sélectionner le script Python à copier"""
        file = filedialog.askopenfilename(
            title="Choisir un script Python",
            filetypes=[("Python files", "*.py"), ("All files", "*.*")]
        )
        if file:
            self.script_path.set(file)
            self.log(f"Script sélectionné: {os.path.basename(file)}", "info")
    
    def copy_script(self):
        """Copier le script vers le dossier de destination"""
        dest = self.destination_path.get()
        script = self.script_path.get()
        
        # Vérifications
        if not dest:
            self.log("Erreur: Aucun dossier de destination sélectionné", "error")
            messagebox.showerror("Erreur", "Veuillez sélectionner un dossier de destination!")
            return
        
        if not script:
            self.log("Erreur: Aucun script sélectionné", "error")
            messagebox.showerror("Erreur", "Veuillez sélectionner un script à copier!")
            return
        
        if not os.path.exists(dest):
            self.log(f"Erreur: Le dossier '{dest}' n'existe pas", "error")
            messagebox.showerror("Erreur", "Le dossier de destination n'existe pas!")
            return
        
        if not os.path.exists(script):
            self.log(f"Erreur: Le script '{script}' n'existe pas", "error")
            messagebox.showerror("Erreur", "Le script sélectionné n'existe pas!")
            return
        
        try:
            # Nom du fichier
            script_name = os.path.basename(script)
            destination_file = os.path.join(dest, script_name)
            
            # Vérifier si le fichier existe déjà
            if os.path.exists(destination_file):
                self.log(f"Le fichier '{script_name}' existe déjà, demande de confirmation...", "warning")
                response = messagebox.askyesno(
                    "Fichier existant", 
                    f"Le fichier '{script_name}' existe déjà.\nVoulez-vous le remplacer?"
                )
                if not response:
                    self.log("Copie annulée par l'utilisateur", "warning")
                    return
            
            # Copier le fichier
            self.log(f"Copie de '{script_name}' en cours...", "info")
            shutil.copy2(script, destination_file)

            # Mettre à jour le mapping dans la config
            try:
                src_mtime = os.path.getmtime(script)
            except Exception:
                src_mtime = time.time()
            self.config.setdefault("mapping", {})[script_name] = {
                "source": script,
                "src_mtime": src_mtime
            }
            self.config["destination"] = dest
            self.save_config()
            self.refresh_list()

            self.log(f"✅ Script '{script_name}' copié avec succès!", "success")
            messagebox.showinfo(
                "Succès", 
                f"✅ Script '{script_name}' copié avec succès!"
            )
            
        except Exception as e:
            self.log(f"Erreur lors de la copie: {str(e)}", "error")
            messagebox.showerror("Erreur", f"Erreur lors de la copie:\n{str(e)}")

    def load_config(self):
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        self.config.update(data)
        except Exception:
            # ignore malformed config
            pass

    def save_config(self):
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            messagebox.showwarning("Attention", f"Impossible de sauvegarder la configuration:\n{str(e)}")

    def refresh_list(self):
        """Rafraîchir la liste des scripts avec indicateurs visuels"""
        # Clear existing widgets
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        dest = self.destination_path.get() or self.config.get('destination', '')
        if not dest or not os.path.isdir(dest):
            no_folder_label = tk.Label(
                self.scrollable_frame, 
                text="Aucun dossier sélectionné", 
                bg="#1e1e1e", 
                fg="#888888",
                font=("Arial", 10, "italic")
            )
            no_folder_label.pack(pady=20)
            return
        
        mapping = self.config.get('mapping', {})
        try:
            names = sorted([f for f in os.listdir(dest) if f.endswith('.py')])
        except Exception:
            names = []
        
        if not names:
            no_scripts_label = tk.Label(
                self.scrollable_frame, 
                text="Aucun script Python trouvé dans ce dossier", 
                bg="#1e1e1e", 
                fg="#888888",
                font=("Arial", 10, "italic")
            )
            no_scripts_label.pack(pady=20)
            self.log("Aucun script trouvé dans le dossier", "info")
            return
        
        self.log(f"Liste actualisée: {len(names)} script(s) trouvé(s)", "info")
        needs_update_count = 0
        
        for name in names:
            dest_file = os.path.join(dest, name)
            status = ''
            status_color = ''
            status_icon = ''
            needs_update = False
            
            map_entry = mapping.get(name)
            if map_entry:
                src = map_entry.get('source')
                if src and os.path.exists(src):
                    try:
                        src_m = os.path.getmtime(src)
                        dest_m = os.path.getmtime(dest_file)
                        if src_m > dest_m:
                            status = 'Mise à jour disponible'
                            status_color = '#ff9800'
                            status_icon = '🟠'
                            needs_update = True
                            needs_update_count += 1
                        else:
                            status = 'À jour'
                            status_color = '#4caf50'
                            status_icon = '🟢'
                    except Exception:
                        status = 'Erreur'
                        status_color = '#888888'
                        status_icon = '⚠️'
                else:
                    status = 'Source manquante'
                    status_color = '#f44336'
                    status_icon = '🔴'
            else:
                status = 'Non suivi'
                status_color = '#2196f3'
                status_icon = '🔵'
            
            # Frame pour chaque script
            script_frame = tk.Frame(self.scrollable_frame, bg="#2a2a2a", relief="ridge", bd=1)
            script_frame.pack(fill="x", padx=5, pady=3)
            
            # Info frame (left side)
            info_frame = tk.Frame(script_frame, bg="#2a2a2a")
            info_frame.pack(side="left", fill="x", expand=True, padx=10, pady=8)
            
            # Script name
            name_label = tk.Label(
                info_frame, 
                text=f"{status_icon} {name}", 
                bg="#2a2a2a", 
                fg="#ffffff",
                font=("Arial", 10, "bold"),
                anchor="w"
            )
            name_label.pack(anchor="w")
            
            # Status
            status_label = tk.Label(
                info_frame, 
                text=status, 
                bg="#2a2a2a", 
                fg=status_color,
                font=("Arial", 9),
                anchor="w"
            )
            status_label.pack(anchor="w")
            
            # Source path if tracked
            if map_entry and map_entry.get('source'):
                source_label = tk.Label(
                    info_frame, 
                    text=f"Source: {map_entry['source']}", 
                    bg="#2a2a2a", 
                    fg="#888888",
                    font=("Arial", 8),
                    anchor="w"
                )
                source_label.pack(anchor="w")
            
            # Button frame (right side)
            if needs_update:
                btn_frame = tk.Frame(script_frame, bg="#2a2a2a")
                btn_frame.pack(side="right", padx=10, pady=8)
                
                update_btn = tk.Button(
                    btn_frame,
                    text="⬆️ Mettre à jour",
                    command=lambda n=name: self.update_script(n),
                    bg="#ff9800",
                    fg="#ffffff",
                    font=("Arial", 9, "bold"),
                    cursor="hand2",
                    relief="raised",
                    bd=2
                )
                update_btn.pack()
        
        if needs_update_count > 0:
            self.log(f"⚠️ {needs_update_count} script(s) nécessite(nt) une mise à jour", "warning")

    def update_script(self, script_name):
        """Mettre à jour un script spécifique"""
        mapping = self.config.get('mapping', {})
        entry = mapping.get(script_name)
        dest = self.destination_path.get() or self.config.get('destination', '')
        
        if not dest:
            self.log("Erreur: Dossier de destination non défini", "error")
            messagebox.showerror("Erreur", "Dossier de destination non défini!")
            return
        
        destination_file = os.path.join(dest, script_name)
        
        if not entry or not entry.get('source') or not os.path.exists(entry.get('source')):
            self.log(f"Erreur: Source de '{script_name}' introuvable", "error")
            messagebox.showerror("Erreur", f"Source du script '{script_name}' introuvable.")
            return
        
        try:
            self.log(f"Mise à jour de '{script_name}' en cours...", "info")
            shutil.copy2(entry['source'], destination_file)
            entry['src_mtime'] = os.path.getmtime(entry['source'])
            self.save_config()
            self.refresh_list()
            self.log(f"✅ '{script_name}' mis à jour avec succès!", "success")
            messagebox.showinfo("Succès", f"✔️ '{script_name}' mis à jour avec succès!")
        except Exception as e:
            self.log(f"Erreur lors de la mise à jour de '{script_name}': {str(e)}", "error")
            messagebox.showerror("Erreur", f"Erreur lors de la mise à jour:\n{str(e)}")

def main():
    root = tk.Tk()
    app = MinescriptManager(root)
    root.mainloop()

if __name__ == "__main__":
    main()
