import os
import tempfile
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
from playsound import playsound
import customtkinter as ctk
from threading import Thread
import time

# Optimized recognizer settings for faster response
recognizer = sr.Recognizer()
recognizer.pause_threshold = 1.0  # Faster response time
recognizer.energy_threshold = 3000  # Better for noisy environments
recognizer.dynamic_energy_threshold = True
recognizer.operation_timeout = 2  # Timeout after 2 seconds of silence

# Updated language mapping with correct codes
language_mapping = {
    'türkçe': ('tr', 'tr-TR'),
    'ingilizce': ('en', 'en-US'),
    'almanca': ('de', 'de-DE'),
    'fransızca': ('fr', 'fr-FR'),
    'korece': ('ko', 'ko-KR'),
    'japonca': ('ja', 'ja-JP'),
    'çince': ('zh-cn', 'zh-CN'),  # Fixed Chinese language code
    'rusça': ('ru', 'ru-RU'),
    'danca': ('da', 'da-DK')
}

class SpeechiTranslatorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.after(100, self.initialize_app)

    def initialize_app(self):
        # App settings
        self.title("Speechi Pro")
        self.geometry("900x700")
        self.resizable(False, False)
        
        # Variables
        self.mode = "Otomatik"
        self.src_lang = "türkçe"
        self.dst_lang = "ingilizce"
        self.full_conversation_src = []
        self.full_conversation_dst = []
        self.listening = False
        self.processing = False
        
        # UI Components
        self.create_widgets()
        
        # Ask for languages in automatic mode
        if self.mode == "Otomatik":
            Thread(target=self.ask_for_languages, daemon=True).start()

    def create_widgets(self):
        # Title
        self.title_label = ctk.CTkLabel(self, text="Speechi PRO", font=("Segoe UI", 28, "bold"))
        self.title_label.pack(pady=15)

        # Mode selector
        self.mode_selector = ctk.CTkSegmentedButton(self, values=["Otomatik", "Manuel"], command=self.change_mode)
        self.mode_selector.set("Otomatik")
        self.mode_selector.pack(pady=5)

        # Language selection
        self.lang_card = ctk.CTkFrame(self, corner_radius=10)
        self.lang_card.pack(pady=5, padx=20, fill="x")

        # Source language (left)
        self.src_lang_box = ctk.CTkComboBox(self.lang_card, values=list(language_mapping.keys()))
        self.src_lang_box.pack(side="left", padx=10, pady=10, expand=True, fill="x")

        # Destination language (right)
        self.dst_lang_box = ctk.CTkComboBox(self.lang_card, values=list(language_mapping.keys()))
        self.dst_lang_box.pack(side="right", padx=10, pady=10, expand=True, fill="x")

        # Mic button (only enabled in Manuel mode)
        self.mic_card = ctk.CTkFrame(self, corner_radius=10)
        self.mic_card.pack(pady=5, padx=20, fill="x")

        self.listen_button = ctk.CTkButton(
            self.mic_card, 
            text="Konuşmaya Başla", 
            font=("Segoe UI", 16), 
            command=self.start_listening_thread
        )
        self.listen_button.pack(pady=10)
        self.listen_button.configure(state="disabled")

        # Current translation frame
        self.current_translation_frame = ctk.CTkFrame(self, corner_radius=10)
        self.current_translation_frame.pack(pady=5, padx=20, fill="both", expand=True)

        # Source text (left)
        self.src_text_label = ctk.CTkLabel(self.current_translation_frame, text="Kaynak Metin", font=("Segoe UI", 12, "bold"))
        self.src_text_label.pack(anchor="w", padx=10, pady=(10,0))
        self.src_text = ctk.CTkTextbox(self.current_translation_frame, height=100)
        self.src_text.pack(side="left", padx=10, pady=10, expand=True, fill="both")

        # Translated text (right)
        self.dst_text_label = ctk.CTkLabel(self.current_translation_frame, text="Çeviri", font=("Segoe UI", 12, "bold"))
        self.dst_text_label.pack(anchor="w", padx=10, pady=(10,0))
        self.dst_text = ctk.CTkTextbox(self.current_translation_frame, height=100)
        self.dst_text.pack(side="right", padx=10, pady=10, expand=True, fill="both")

        # Full conversation history
        self.history_frame = ctk.CTkFrame(self, corner_radius=10)
        self.history_frame.pack(pady=5, padx=20, fill="both", expand=True)

        # Full source conversation (left)
        self.full_src_label = ctk.CTkLabel(self.history_frame, text="Tüm Kaynak Konuşma", font=("Segoe UI", 12, "bold"))
        self.full_src_label.pack(anchor="w", padx=10, pady=(10,0))
        self.full_src_text = ctk.CTkTextbox(self.history_frame, height=150)
        self.full_src_text.pack(side="left", padx=10, pady=10, expand=True, fill="both")

        # Full translated conversation (right)
        self.full_dst_label = ctk.CTkLabel(self.history_frame, text="Tüm Çeviri", font=("Segoe UI", 12, "bold"))
        self.full_dst_label.pack(anchor="w", padx=10, pady=(10,0))
        self.full_dst_text = ctk.CTkTextbox(self.history_frame, height=150)
        self.full_dst_text.pack(side="right", padx=10, pady=10, expand=True, fill="both")

    def ask_for_languages(self):
        self.src_text.delete("1.0", "end")
        self.src_text.insert("1.0", "Lütfen kaynak ve hedef dilleri söyleyin (örn: 'Türkçe Japonca')")
        
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.listen(source, timeout=3, phrase_time_limit=4)
                text = recognizer.recognize_google(audio, language='tr-TR').lower()
                
                if "dil değiştir" in text:
                    self.ask_for_languages()
                    return
                
                languages = text.split()
                if len(languages) >= 2:
                    src = self.find_best_language_match(languages[0])
                    dst = self.find_best_language_match(languages[1])
                    
                    if src and dst:
                        self.src_lang = src
                        self.dst_lang = dst
                        self.src_lang_box.set(src)
                        self.dst_lang_box.set(dst)
                        self.start_listening_thread()
                        return
                
                # If not understood, ask again
                self.ask_for_languages()
                
        except (sr.WaitTimeoutError, sr.UnknownValueError):
            # Default to Turkish-English if no input
            self.set_default_languages()
        except Exception as e:
            print(f"Error in language detection: {e}")
            self.set_default_languages()

    def find_best_language_match(self, input_text):
        # Find the best matching language from user input
        for lang in language_mapping:
            if lang.startswith(input_text[:3]):  # Check first 3 characters for match
                return lang
        return None

    def set_default_languages(self):
        self.src_lang = "türkçe"
        self.dst_lang = "ingilizce"
        self.src_lang_box.set(self.src_lang)
        self.dst_lang_box.set(self.dst_lang)
        self.start_listening_thread()

    def change_mode(self, value):
        self.mode = value
        if self.mode == "Manuel":
            self.src_lang_box.configure(state="normal")
            self.dst_lang_box.configure(state="normal")
            self.listen_button.configure(state="normal")
            if self.listening:
                self.listening = False
        else:
            self.src_lang_box.configure(state="disabled")
            self.dst_lang_box.configure(state="disabled")
            self.listen_button.configure(state="disabled")
            self.start_listening_thread()

    def start_listening_thread(self):
        if not self.listening:
            self.listening = True
            Thread(target=self.listen_loop, daemon=True).start()

    def listen_loop(self):
        while self.listening and self.mode == "Otomatik" and not self.processing:
            self.listen_once()
            time.sleep(2)  # 2-second pause between sentences
        
        # In Manuel mode, just listen once when button pressed
        if self.mode == "Manuel":
            self.listen_once()

    def listen_once(self):
        if self.processing:
            return
            
        self.processing = True
        src = self.src_lang_box.get().lower()
        dst = self.dst_lang_box.get().lower()
        
        if src not in language_mapping or dst not in language_mapping:
            self.processing = False
            return
            
        src_code, src_recog_code = language_mapping[src]
        dst_code, _ = language_mapping[dst]
        
        try:
            with sr.Microphone() as source:
                self.src_text.delete("1.0", "end")
                self.src_text.insert("1.0", "Dinleniyor...")
                
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.listen(source, timeout=2, phrase_time_limit=8)
                text = recognizer.recognize_google(audio, language=src_recog_code)
                
                if text.lower() == "dil değiştir":
                    self.ask_for_languages()
                    self.processing = False
                    return
                
                # Update UI with source text
                self.src_text.delete("1.0", "end")
                self.src_text.insert("1.0", text)
                self.full_conversation_src.append(text)
                self.full_src_text.insert("end", text + "\n")
                self.full_src_text.see("end")
                
                # Translate (with retry logic for Chinese)
                translated = ""
                retries = 3
                while retries > 0:
                    try:
                        translator = Translator()
                        translated = translator.translate(text, src=src_code, dest=dst_code).text
                        break
                    except Exception as e:
                        retries -= 1
                        if retries == 0:
                            translated = f"Çeviri hatası: {str(e)}"
                        time.sleep(0.5)
                
                # Update UI with translation
                self.dst_text.delete("1.0", "end")
                self.dst_text.insert("1.0", translated)
                self.full_conversation_dst.append(translated)
                self.full_dst_text.insert("end", translated + "\n")
                self.full_dst_text.see("end")
                
                # Speak translation
                self.speak_text(translated, dst_code)
                
        except sr.WaitTimeoutError:
            pass
        except sr.UnknownValueError:
            self.src_text.delete("1.0", "end")
            self.src_text.insert("1.0", "Anlaşılamadı, tekrar deneyin")
        except Exception as e:
            print(f"Error in listening: {e}")
            self.src_text.delete("1.0", "end")
            self.src_text.insert("1.0", f"Hata: {str(e)}")
        finally:
            self.processing = False

    def speak_text(self, text, lang_code):
        try:
            # Special handling for Chinese
            if lang_code.startswith('zh'):
                lang_code = 'zh'  # Use generic Chinese code for TTS
                
            tts = gTTS(text=text, lang=lang_code)
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
                temp_path = f.name
            tts.save(temp_path)
            playsound(temp_path)
            os.remove(temp_path)
        except Exception as e:
            print(f"TTS error: {e}")

if __name__ == "__main__":
    app = SpeechiTranslatorApp()
    app.mainloop()
