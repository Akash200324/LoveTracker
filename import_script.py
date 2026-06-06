from tracker.models import Playlist, SongMemory, User
from bs4 import BeautifulSoup
import re

html_path = r"C:\Users\AKASH\.gemini\antigravity-ide\brain\4d80c235-b5c0-434b-8f36-f02396c6e821\.system_generated\steps\1801\content.md"
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')
user = User.objects.first()
from tracker.models import Couple
couple = Couple.objects.first()

playlist = Playlist.objects.create(
    name="New Music Friday India",
    created_by=user,
    couple=couple,
    cover_url="https://i.scdn.co/image/ab67706f000000020b930c48edd584afadf8795c",
    is_external=False,
    platform="spotify"
)

rows = soup.find_all('div', {'data-testid': 'track-row'})
print(f"Found {len(rows)} tracks.")

for row in rows:
    try:
        a_tag = row.find('a', href=re.compile(r'^/track/'))
        if not a_tag: continue
        track_id = a_tag['href'].replace('/track/', '')
        
        title_elem = row.find('p', {'data-encore-id': 'listRowTitle'})
        title = title_elem.text.strip() if title_elem else "Unknown Title"
        
        artist_elem = row.find('p', {'data-encore-id': 'listRowDetails'})
        artist = artist_elem.text.strip() if artist_elem else "Unknown Artist"
        
        img_elem = row.find('img')
        cover_url = img_elem['src'] if img_elem and 'src' in img_elem.attrs else ""
        
        song, created = SongMemory.objects.get_or_create(
            track_id=track_id,
            platform="spotify",
            defaults={
                'title': title,
                'artist': artist,
                'cover_url': cover_url,
                'added_by': user,
                'couple_id': playlist.couple_id if hasattr(playlist, 'couple_id') else 1 # We might need couple_id! Wait, playlist requires couple_id!
            }
        )
        song.playlists.add(playlist)
        print(f"Added: {title} by {artist}")
    except Exception as e:
        print("Error on a row:", e)

print("Done! Created playlist ID:", playlist.id)
