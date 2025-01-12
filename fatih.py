import speech_recognition as sr
import os
import time
from gtts import gTTS
from playsound import playsound
import webbrowser
import wave
import threading
def help():
    speak("Fatih Asistan Komutları:")
    speak("1. 'Uyku' komutu: Uyku moduna geçer.")
    speak("2. 'Çıkış' komutu: Asistanı kapatır.")
    speak("3. 'Selam' veya 'Selamünaleyküm' komutu: Asistana selam verir.")
    speak("4. 'Kapat' komutu: Bilgisayarı kapatır.")
    speak("5. 'İnternete gir' komutu: Chrome tarayıcısını açar.")
    speak("6. 'Yazı yazacağım' komutu: Notepad açar.")
    speak("7. 'Video izleyeceğim' komutu: YouTube'u açar.")
    speak("8. 'Arama yap' komutu: Google üzerinde arama yapar.")
    speak("9. 'İlahi aç' komutu: YouTube'dan ilahi açar.")
    speak("10. 'Yardım' komutu: Komutların listesini gösterir.")


def speak(text):
    audio_path = "response.mp3"

    # Mevcut dosyayı sil (eğer varsa)
    if os.path.exists(audio_path):
        os.remove(audio_path)

    # Yeni dosya oluştur ve sesli yanıtı kaydet
    tts = gTTS(text=text, lang='tr')
    tts.save(audio_path)

    # Dosyayı oynat
    playsound(audio_path)

def save_audio(audio_data, filename="recorded_audio.wav"):
    """
    Verilen audio verisini .wav dosyasına kaydeder.
    """
    with wave.open(filename, "wb") as wav_file:
        wav_file.setnchannels(1)  # Mono kanal
        wav_file.setsampwidth(audio_data.sample_width)
        wav_file.setframerate(audio_data.sample_rate)
        wav_file.writeframes(audio_data.frame_data)

def get_audio_input():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Sizi dinliyorum...")
        # Çevredeki gürültüyü azalt
        recognizer.adjust_for_ambient_noise(source)
        try:
            # Ses kaydını al
            audio = recognizer.listen(source)

            # Ses kaydını kaydet
            save_audio(audio)

            # Google Speech Recognition ile sesi metne çevir
            command = recognizer.recognize_google(audio, language='tr-TR')
            return command

        except sr.UnknownValueError:
            print("Ses anlaşılamadı. Lütfen tekrar edin.")
            speak("Anlaşılamadı, lütfen tekrar edin.")
            return ""
        except sr.RequestError:
            print("Servis hatası. Lütfen internet bağlantınızı kontrol edin.")
            speak("Servis hatası.")
            return ""
        except Exception as e:
            print(f"Bir hata oluştu: {e}")
            speak("Bir hata oluştu. Lütfen tekrar deneyin.")
            return ""

# Uyku moduna geçerken beklemek için fonksiyon
def uyku_modu():
    speak("Uyku moduna geçiyorum. Lütfen süreyi söyleyin.")
    süre_str = input("Süre lütfen (dakika): ")
    try:
        süre = int(süre_str) if süre_str else 0
    except ValueError:
        speak("Geçerli bir süre girmediniz. Lütfen doğru şekilde söyleyin.")
        return  # Geçerli bir süre girmediyse fonksiyonu sonlandır

    speak(f"Uyku moduna geçiyorum. {süre} dakika sonra uyanacağım.")
    time.sleep(süre * 60)  # Verilen süre kadar bekle
    speak("Uyandım, ota60!")  # Süre bitince sesli mesajı ver

# Sürekli dinleme fonksiyonu
def listen_continuously():
    while True:
        command = get_audio_input()
        if "tempo" in command:
            os.system("start chrome.exe https://www.youtube.com/watch?v=lDcby__G9Cs")
            exit()
        if "uyku" in command.lower():
            # Uyku moduna geçmek için çağrılır
            uyku_modu()
        
        elif "çıkış" in command.lower():
            speak("Asistan kapatılıyor.")
            exit()

        elif "selam" in command or "Selamünaleyküm" in command:
            speak("Selam ota60")

        elif "kapat" in command:
            speak("Tamam, iyi günler Ota60!")
            a = input("İşlem yapılmasını ister misiniz? (Evet/Hayır): ")
            if a.lower() == "evet":
                os.system("shutdown /s /f /t 0")
            else:
                continue

        elif "İnternete gir" in command:
            speak("Hemen açılıyor")
            os.system("start chrome.exe")

        elif "yazı yazacağım" in command:
            os.system("start notepad.exe")
            speak("Yazı yazma penceresi açılıyor.")
        
        elif "video izleyeceğim" in command:
            speak("YouTube açılıyor.")
            os.system("start chrome.exe https://www.youtube.com")

        elif "arama yap" in command:
            speak("Ne aramak istersiniz?")
            arama = get_audio_input()
            if arama:
                speak(f"{arama} için arama yapılıyor.")
                # Google'da arama yap
                webbrowser.open(f"https://www.google.com/search?q={arama}")
            else:
                speak("Bir şey anlayamadım, lütfen tekrar deneyin")

        elif "ilahi aç" in command:
            speak("Hemen açılıyor")
            os.system("start chrome.exe https://www.youtube.com/watch?v=lLfjr9V3B5E")

        elif "yardım" in command:
            help()

# Asistanı başlatan fonksiyon
def start_assistant():
    # Sürekli dinleme fonksiyonunu ayrı bir iş parçacığında çalıştır
    listen_thread = threading.Thread(target=listen_continuously)
    listen_thread.daemon = True  # Uygulama kapanınca iş parçacığı da kapanacak
    listen_thread.start()

    # Burada diğer işlemler de yapılabilir
    while True:
        time.sleep(1)  # Ana thread boşta kalır

# Asistanı başlat
start_assistant()
