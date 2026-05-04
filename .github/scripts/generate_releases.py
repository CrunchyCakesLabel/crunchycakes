import csv
from html import escape

def get_releases(csv_path):
    releases = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            releases.append({
                'artist': escape(row.get('artist', 'Unknown')),
                'title': escape(row.get('title', 'Untitled')),
                'spotify_url': row.get('spotify_url', '#'),
                'cover_url': row.get('cover_url', '')
            })
    return releases

def build_cards(releases, limit=None):
    if limit:
        releases = releases[:limit]
    cards = []
    for r in releases:
        cover_html = ''
        if r['cover_url']:
            cover_html = f'<img src="{r["cover_url"]}" alt="{r["title"]}">'
        else:
            cover_html = '<span class="placeholder">🎵</span>'
        
        card = f'''
        <div class="release-card">
            <div class="release-cover">
                {cover_html}
            </div>
            <div class="release-info">
                <div class="release-artist">{r["artist"]}</div>
                <div class="release-title">{r["title"]}</div>
                <a href="{r["spotify_url"]}" class="release-link" target="_blank">Listen on Spotify →</a>
            </div>
        </div>'''
        cards.append(card)
    return '\n'.join(cards)

def update_file(filepath, releases, limit=None):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    start = content.find('<!-- RELEASES_PLACEHOLDER -->')
    end = content.find('<!-- END_RELEASES_PLACEHOLDER -->')
    
    if start == -1 or end == -1:
        print(f"❌ Placeholders not found in {filepath}")
        return
    
    new_cards = build_cards(releases, limit)
    new_content = (content[:start] + 
                   '<!-- RELEASES_PLACEHOLDER -->\n' + 
                   new_cards + '\n' + 
                   content[end:])
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ Updated {filepath} (limit={limit if limit else 'all'})")

if __name__ == '__main__':
    releases = get_releases('releases.csv')
    update_file('index.html', releases, limit=4)
    update_file('releases.html', releases)
