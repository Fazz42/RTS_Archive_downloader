import requests
from bs4 import BeautifulSoup
import yt_dlp
import os

# URL de la page web
base_url = "https://www.rts.ch/services/archives/?q=best%20of&sort=publicationDate&minYear=2015&maxYear=2025&media=audio&programs=Dicodeurs&page=8"

# Créer un dossier pour sauvegarder les fichiers
output_folder = "downloads"
os.makedirs(output_folder, exist_ok=True)

# Fonction pour extraire les liens et les dates depuis la page
def get_audio_links_and_dates(url):
    response = requests.get(url)
    response.raise_for_status()  # Vérifie les erreurs HTTP
    soup = BeautifulSoup(response.text, 'html.parser')

    # Chercher les éléments contenant les liens audio et les dates
    program_links = soup.select('a[href*="/play/radio/redirect/detail/"]')
    date_elements = soup.select('time')

    # Vérifier que le nombre de dates correspond au nombre de liens
    if len(program_links) != len(date_elements):
        print("Mismatch between number of links and dates.")
        return []

    # Extraire les URLs et les dates
    audio_data = []
    for link, date in zip(program_links, date_elements):
        audio_url = link['href']
        full_url = "https://www.rts.ch" + audio_url
        date_text = date.get('datetime', '').split('T')[0]  # Format YYYY-MM-DD
        audio_data.append((full_url, date_text))

    return audio_data

# Fonction pour télécharger l'audio
def download_audio(link, date, output_folder):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{output_folder}/{date}.%(ext)s',
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
    except Exception as e:
        print(f"Erreur lors du téléchargement de {link} : {e}")

# Récupérer les données des audios depuis la page
audio_links_and_dates = get_audio_links_and_dates(base_url)

# Télécharger chaque fichier audio
for audio_link, date in audio_links_and_dates:
    print(f"Téléchargement de l'audio pour la date {date} depuis {audio_link}...")
    download_audio(audio_link, date, output_folder)

print("Téléchargement terminé !")
