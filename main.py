import tkinter as tk
from tkinter import messagebox
import speech_recognition as sr
import pyttsx3
import webcolors  # Pour la gestion des noms de couleurs


class LEDControlApp:
    def __init__(self, root):
        """
        Initialisation de l'application et configuration des paramètres de l'interface utilisateur.

        :param root: Fenêtre principale de l'application tkinter
        """
        self.root = root
        self.root.title("Contrôle des LED avec Reconnaissance Vocale")
        self.root.geometry("500x500")
        self.root.resizable(False, False)
        self.root.config(bg="#34495e")  # Couleur d'arrière-plan de la fenêtre

        # Initialisation du moteur de synthèse vocale
        self.tts_engine = pyttsx3.init()

        # Dictionnaire pour la traduction des noms de couleurs en français vers l'anglais
        self.french_to_english_colors = {
            "rouge": "red",
            "bleu": "blue",
            "vert": "green",
            "verre": "green",  # Gestion des erreurs de reconnaissance
            "vers": "green",
            "noir": "black",
            "blanc": "white",
            "jaune": "yellow",
            "rose": "pink",
            "orange": "orange",
            "violet": "purple",
            "gris": "gray",
            "marron": "brown",
            "magenta": "magenta",
            "bleu ciel": "skyblue",
            "beige": "beige",
        }

        # Configuration de l'interface utilisateur
        self.setup_ui()

    def setup_ui(self):
        """
        Configure les composants de l'interface utilisateur (UI) de l'application.
        """
        # Titre de l'application
        title_label = tk.Label(
            self.root,
            text="Contrôle des LED",
            font=("Arial", 28, "bold"),
            fg="white",
            bg="#34495e"
        )
        title_label.pack(pady=20)

        # Cadre pour afficher la couleur actuelle
        self.color_display = tk.Frame(
            self.root,
            width=300,
            height=150,
            bg="#ecf0f1",  # Couleur initiale
            relief="flat"
        )
        self.color_display.pack(pady=20)

        # Bouton pour démarrer la reconnaissance vocale
        self.voice_button = tk.Button(
            self.root,
            text="🎙️ Démarrer la reconnaissance vocale",
            font=("Arial", 16),
            bg="#1abc9c",  # Couleur du bouton
            fg="white",
            activebackground="#16a085",  # Couleur active
            activeforeground="white",
            cursor="hand2",
            relief="flat",
            command=self.start_voice_recognition
        )
        self.voice_button.pack(pady=20)

        # Label pour afficher des informations à l'utilisateur
        self.info_label = tk.Label(
            self.root,
            text="Appuyez sur le bouton et dites une couleur en français.",
            font=("Arial", 12),
            fg="white",
            bg="#34495e",
            wraplength=400,  # Limite la largeur du texte
            justify="center"
        )
        self.info_label.pack(pady=10)

    def start_voice_recognition(self):
        """
        Démarre la reconnaissance vocale et traite la commande utilisateur.
        """
        # Message vocal pour inviter l'utilisateur à parler
        self.say_text("Veuillez dire une couleur en français.")
        recognizer = sr.Recognizer()

        try:
            with sr.Microphone() as source:
                self.info_label.config(text="🎧 Écoute en cours... Parlez maintenant.")
                recognizer.adjust_for_ambient_noise(source, duration=0.5)  # Ajuste pour le bruit ambiant
                audio = recognizer.listen(source, timeout=5)  # Écoute la commande
                command = recognizer.recognize_google(audio, language='fr-FR')  # Reconnaissance vocale en français
                self.process_command(command.lower())  # Traite la commande en minuscules
        except sr.UnknownValueError:
            messagebox.showerror("Erreur", "Je n'ai pas compris, veuillez réessayer.")
        except sr.RequestError as e:
            messagebox.showerror("Erreur", f"Erreur avec le service vocal : {e}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur est survenue : {e}")

    def process_command(self, command):
        """
        Analyse et traite la commande utilisateur.

        :param command: Texte reconnu par la reconnaissance vocale
        """
        try:
            # Recherche d'une couleur reconnue dans la commande
            color_hex = self.get_color_from_command(command)
            if color_hex:
                self.update_color(color_hex, command)  # Mise à jour de la couleur
                return
        except ValueError:
            pass

        # Message si aucune couleur n'est reconnue
        messagebox.showinfo("Commande inconnue", "Couleur non reconnue. Veuillez essayer à nouveau.")

    def get_color_from_command(self, command):
        """
        Tente d'extraire une couleur reconnue dans une commande utilisateur.

        :param command: Texte de la commande utilisateur
        :return: Code hexadécimal de la couleur si trouvée, sinon lève une exception ValueError
        """
        words = command.split()  # Divise la commande en mots
        for word in words:
            if word in self.french_to_english_colors:  # Vérifie si le mot est une couleur connue
                english_color = self.french_to_english_colors[word]
                try:
                    return webcolors.name_to_hex(english_color)  # Convertit en code hexadécimal
                except ValueError:
                    continue
        raise ValueError("Aucune couleur reconnue dans la commande.")

    def update_color(self, color_hex, color_name):
        """
        Met à jour la couleur affichée et informe l'utilisateur.

        :param color_hex: Code hexadécimal de la couleur
        :param color_name: Nom de la couleur
        """
        self.color_display.config(bg=color_hex)  # Change la couleur du cadre
        self.info_label.config(
            text=f"✅ Couleur actuelle : {color_name.capitalize()}"  # Affiche la couleur sélectionnée
        )
        self.say_text(f"La couleur est maintenant {color_name}")  # Message vocal

    def say_text(self, text):
        """
        Utilise le moteur de synthèse vocale pour lire un texte à haute voix.

        :param text: Texte à lire
        """
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()


# Point d'entrée principal de l'application
if __name__ == "__main__":
    root = tk.Tk()  # Création de la fenêtre principale
    app = LEDControlApp(root)  # Initialisation de l'application
    root.mainloop()  # Lancement de la boucle principale de tkinter
