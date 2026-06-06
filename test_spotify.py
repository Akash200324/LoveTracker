import requests, re, json
html = requests.get('https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M').text
with open('test_spotify.html', 'w', encoding='utf-8') as f:
    f.write(html)
