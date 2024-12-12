import tkinter as tk  # Importation de la bibliothèque tkinter pour créer l'interface graphique
from tkinter import messagebox  # Pour afficher des boîtes de dialogue d'erreur ou d'information
import speech_recognition as sr  # Pour la reconnaissance vocale
import pyttsx3  # Pour la synthèse vocale (text-to-speech)


class LEDControlApp:
    def __init__(self, root):
        """
        Initialisation de l'application et configuration des paramètres de l'interface utilisateur.

        :param root: Fenêtre principale de l'application tkinter
        """
        self.root = root
        self.root.title("Contrôle des LED avec Reconnaissance Vocale")  # Définir le titre de la fenêtre
        self.root.geometry("500x500")  # Définir les dimensions de la fenêtre
        self.root.resizable(False, False)  # Empêcher le redimensionnement de la fenêtre
        self.root.config(bg="#34495e")  # Définir une couleur de fond

        # Initialisation du moteur de synthèse vocale
        self.tts_engine = pyttsx3.init()

        # Dictionnaire des couleurs disponibles avec leurs noms et codes hexadécimaux
        self.color_map = {
            "rouge": "#e74c3c",

            "bleu": "#3498db",
            "noir": "#000000"
        }

        # Configuration de l'interface utilisateur
        self.setup_ui()

    def setup_ui(self):
        """
        Configure et crée les éléments de l'interface utilisateur (widgets).
        """
        # Titre principal affiché en haut de la fenêtre
        title_label = tk.Label(
            self.root,
            text="Contrôle des LED",
            font=("Arial", 28, "bold"),  # Police et taille du texte
            fg="white",  # Couleur du texte
            bg="#34495e"  # Couleur de fond de l'étiquette
        )
        title_label.pack(pady=20)  # Ajout d'un espace vertical autour du titre

        # Cadre utilisé pour afficher la couleur sélectionnée par l'utilisateur
        self.color_display = tk.Frame(
            self.root,
            width=300,
            height=150,
            bg="#ecf0f1",  # Couleur initiale (grise)
            relief="flat"
        )
        self.color_display.pack(pady=20)

        # Bouton permettant de démarrer la reconnaissance vocale
        self.voice_button = tk.Button(
            self.root,
            text="🎙️ Démarrer la reconnaissance vocale",
            font=("Arial", 16),  # Police et taille du texte
            bg="#1abc9c",  # Couleur de fond du bouton
            fg="white",  # Couleur du texte du bouton
            activebackground="#16a085",  # Couleur du bouton lorsqu'il est activé
            activeforeground="white",  # Couleur du texte lorsque le bouton est activé
            cursor="hand2",  # Change le curseur en une main survolant le bouton
            relief="flat",  # Style visuel du bouton
            command=self.start_voice_recognition  # Lier au clic la fonction de reconnaissance vocale
        )
        self.voice_button.pack(pady=20)

        # Étiquette d'information pour donner des instructions à l'utilisateur
        self.info_label = tk.Label(
            self.root,
            text="Appuyez sur le bouton et dites une couleur : rouge, vert ou bleu.",
            font=("Arial", 12),  # Police et taille du texte
            fg="white",  # Couleur du texte
            bg="#34495e",  # Couleur de fond
            wraplength=400,  # Limite la largeur du texte
            justify="center"  # Aligne le texte au centre
        )
        self.info_label.pack(pady=10)

    def start_voice_recognition(self):
        """
        Démarre la reconnaissance vocale pour écouter une commande de couleur.
        L'utilisateur doit dire une couleur parmi celles disponibles (rouge, vert, bleu).
        """
        # Informer l'utilisateur qu'il peut parler
        self.say_text("Veuillez dire une couleur : rouge, noire ou bleu .")
        recognizer = sr.Recognizer()  # Initialiser l'objet de reconnaissance vocale

        try:
            # Activer le microphone pour écouter la commande
            with sr.Microphone() as source:
                self.info_label.config(text="🎧 Écoute en cours... Parlez maintenant.")  # Mettre à jour l'interface
                recognizer.adjust_for_ambient_noise(source, duration=0.5)  # Ajuster le seuil pour le bruit ambiant
                audio = recognizer.listen(source, timeout=5)  # Écouter pendant 5 secondes maximum
                command = recognizer.recognize_google(audio, language='fr-FR')  # Reconnaître la commande en français
                self.process_command(command.lower())  # Traiter la commande reconnue
        except sr.UnknownValueError:
            # Afficher un message si la commande n'est pas comprise
            messagebox.showerror("Erreur", "Je n'ai pas compris, veuillez réessayer.")
        except sr.RequestError as e:
            # Afficher un message si le service vocal rencontre une erreur
            messagebox.showerror("Erreur", f"Erreur avec le service vocal : {e}")
        except Exception as e:
            # Afficher un message pour toute autre erreur
            messagebox.showerror("Erreur", f"Une erreur est survenue : {e}")

    def process_command(self, command):
        """
        Analyse et traite la commande vocale reçue.
        Si la commande contient une couleur connue, met à jour l'affichage de la couleur.

        :param command: Texte reconnu par la reconnaissance vocale
        """
        for color, hex_color in self.color_map.items():
            if color in command:  # Vérifie si une couleur connue est mentionnée dans la commande
                self.update_color(hex_color, color)  # Mettre à jour l'affichage avec la couleur correspondante
                return
        # Si aucune couleur n'est reconnue, informer l'utilisateur
        messagebox.showinfo("Commande inconnue", "Couleur non reconnue. Veuillez dire rouge, vert ou bleu.")

    def update_color(self, color_hex, color_name):
        """
        Met à jour la couleur affichée dans l'interface et informe l'utilisateur.

        :param color_hex: Code hexadécimal de la couleur à afficher
        :param color_name: Nom de la couleur
        """
        self.color_display.config(bg=color_hex)  # Mettre à jour la couleur du cadre
        self.info_label.config(
            text=f"✅ Couleur actuelle : {color_name.capitalize()}")  # Mettre à jour le texte d'information
        self.say_text(f"La couleur est maintenant {color_name}")  # Annoncer la couleur sélectionnée

    def say_text(self, text):
        """
        Utilise la synthèse vocale pour parler à l'utilisateur.

        :param text: Texte à prononcer
        """
        self.tts_engine.say(text)  # Ajouter le texte à la file d'attente de la synthèse vocale
        self.tts_engine.runAndWait()  # Démarrer la synthèse vocale


# Point d'entrée de l'application
if __name__ == "__main__":
    root = tk.Tk()  # Créer la fenêtre principale
    app = LEDControlApp(root)  # Instancier l'application
    root.mainloop()  # Lancer la boucle principale de l'interface
