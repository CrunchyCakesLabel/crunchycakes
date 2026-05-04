import csv
import json
from html import escape

def generate_release_cards(csv_path):
    cards = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            artist = escape(row.get('artist', ''))
            title = escape(row.get('title', ''))
            spotify_url = row.get('spotify_url', '#')
            cover_url = row.get('cover_url', '')
            
            cover_html = f'<img src="{cover_url}" alt="{title}" style="width: 100%; height: 100%; object-fit: cover;">' if cover_url else '<span class="placeholder">🎵</span>'
            
            card = f'''
            <div class="release-card">
                <div class="release-cover">
                    {cover_html}
                </div>
                <div class="release-info">
                    <div class="release-artist">{artist}</div>
                    <div class="release-title">{title}</div>
                    <a href="{spotify_url}" class="release-link" target="_blank">Listen on Spotify →</a>
                </div>
            </div>
            '''
            cards.append(card)
    
    return '\n'.join(cards)

if __name__ == '__main__':
    cards_html = generate_release_cards('releases.csv')
    
    # Читаем текущий index.html
    with open('index.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Находим секцию с релизами (ищем маркер <!-- RELEASES_PLACEHOLDER -->)
    start_marker = '<!-- RELEASES_PLACEHOLDER -->'
    end_marker = '<!-- END_RELEASES_PLACEHOLDER -->'
    
    if start_marker in html_content and end_marker in html_content:
        new_html = html_content.split(start_marker)[0] + start_marker + '\n' + cards_html + '\n' + html_content.split(end_marker)[1]
        
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(new_html)
        print("✅ Releases updated")
    else:
        print("❌ Placeholders not found in index.html")
