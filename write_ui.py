import os

html = """{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>Our Music — HiWow Style</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet"/>
<style>
:root {
  --bg-main: #1A1A24;
  --bg-sidebar: #13111C;
  --bg-card: #222030;
  --bg-card-hover: #2D2A3D;
  --accent: #FFD700;
  --accent-hover: #e6c200;
  --text-main: #ffffff;
  --text-muted: #8E8A9F;
  --border: rgba(255,255,255,0.05);
  --font: 'Inter', sans-serif;
  --left-sidebar-w: 240px;
  --right-sidebar-w: 320px;
  --player-h: 100px;
}

*,*::before,*::after { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: var(--font); background: var(--bg-main); color: var(--text-main); height: 100vh; overflow: hidden; display: flex; flex-direction: column; }
button { background: none; border: none; cursor: pointer; color: inherit; font-family: inherit; }
a { text-decoration: none; color: inherit; }
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.2); }

/* --- APP LAYOUT --- */
.app-wrapper { display: grid; grid-template-columns: var(--left-sidebar-w) 1fr var(--right-sidebar-w); flex: 1; height: calc(100vh - var(--player-h)); overflow: hidden; }

/* --- LEFT SIDEBAR --- */
.left-sidebar { background: var(--bg-sidebar); border-right: 1px solid var(--border); padding: 32px 0; display: flex; flex-direction: column; overflow-y: auto; }
.logo-container { display: flex; align-items: center; gap: 12px; padding: 0 32px; margin-bottom: 40px; }
.logo-icon { width: 36px; height: 36px; border-radius: 50%; border: 2px solid var(--accent); display: flex; align-items: center; justify-content: center; color: var(--accent); font-weight: 800; font-size: 18px; }
.logo-text { font-size: 20px; font-weight: 800; letter-spacing: 0.5px; }

.nav-section { margin-bottom: 32px; }
.nav-item { display: flex; align-items: center; gap: 16px; padding: 12px 32px; color: var(--text-muted); font-weight: 600; font-size: 14px; transition: 0.2s; position: relative; cursor: pointer; }
.nav-item svg { width: 20px; height: 20px; fill: currentColor; }
.nav-item:hover { color: var(--text-main); }
.nav-item.active { color: var(--text-main); }
.nav-item.active::before { content: ''; position: absolute; left: 0; top: 50%; transform: translateY(-50%); width: 4px; height: 20px; background: var(--accent); border-radius: 0 4px 4px 0; }
.nav-item.active svg { fill: var(--accent); }

.nav-title { padding: 0 32px; font-size: 14px; font-weight: 700; color: var(--text-main); margin-bottom: 16px; margin-top: 16px; }

/* --- MAIN CONTENT --- */
.main-content { padding: 32px 48px; overflow-y: auto; position: relative; }
.search-container { position: relative; max-width: 400px; margin-bottom: 40px; }
.search-container input { width: 100%; background: var(--bg-card); border: 1px solid transparent; color: var(--text-main); padding: 12px 20px 12px 48px; border-radius: 8px; font-family: var(--font); font-size: 14px; outline: none; transition: 0.2s; }
.search-container input:focus { border-color: rgba(255,215,0,0.5); }
.search-container svg { position: absolute; left: 16px; top: 50%; transform: translateY(-50%); width: 18px; height: 18px; fill: var(--text-muted); }

/* Hero Banner */
.hero-banner { width: 100%; height: 280px; border-radius: 12px; background: linear-gradient(135deg, #c31432, #240b36); position: relative; overflow: hidden; margin-bottom: 40px; display: flex; align-items: center; padding: 48px; box-shadow: 0 20px 40px rgba(0,0,0,0.3); }
.hero-content { position: relative; z-index: 2; max-width: 50%; }
.hero-title { font-size: 48px; font-weight: 900; line-height: 1.1; margin-bottom: 16px; text-shadow: 0 4px 12px rgba(0,0,0,0.3); }
.hero-subtitle { font-size: 14px; color: rgba(255,255,255,0.8); line-height: 1.5; }

/* Section Grid */
.section-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.section-title { font-size: 18px; font-weight: 700; }
.section-more { color: var(--text-muted); font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; cursor: pointer; transition: 0.2s; }
.section-more:hover { color: var(--text-main); }

.grid-albums { display: grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap: 24px; margin-bottom: 48px; }
.album-card { background: var(--bg-card); padding: 12px; border-radius: 8px; cursor: pointer; transition: 0.3s; position: relative; }
.album-card:hover { background: var(--bg-card-hover); transform: translateY(-4px); }
.album-img { width: 100%; aspect-ratio: 1; object-fit: cover; border-radius: 4px; margin-bottom: 12px; box-shadow: 0 8px 16px rgba(0,0,0,0.2); }
.album-title { font-size: 14px; font-weight: 600; margin-bottom: 4px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.album-sub { font-size: 12px; color: var(--text-muted); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.btn-card-del { position: absolute; top: 16px; right: 16px; background: rgba(0,0,0,0.7); color: white; width: 28px; height: 28px; border-radius: 50%; display: flex; align-items: center; justify-content: center; opacity: 0; transition: 0.2s; z-index: 10; }
.album-card:hover .btn-card-del { opacity: 1; }
.btn-card-del:hover { background: #e91429; }

.grid-artists { display: flex; gap: 24px; overflow-x: auto; padding-bottom: 16px; margin-bottom: 48px; }
.artist-card { display: flex; flex-direction: column; align-items: center; gap: 12px; cursor: pointer; transition: 0.2s; min-width: 100px; }
.artist-card:hover { transform: translateY(-4px); }
.artist-img { width: 90px; height: 90px; border-radius: 50%; object-fit: cover; box-shadow: 0 8px 16px rgba(0,0,0,0.3); border: 2px solid transparent; transition: 0.2s; }
.artist-card:hover .artist-img { border-color: var(--accent); }
.artist-name { font-size: 13px; font-weight: 600; text-align: center; }

/* Playlist View */
.view-playlist { display: none; }
.playlist-header { display: flex; align-items: flex-end; gap: 32px; margin-bottom: 40px; }
.pl-cover { width: 200px; height: 200px; border-radius: 8px; object-fit: cover; box-shadow: 0 12px 32px rgba(0,0,0,0.4); }
.pl-info { flex: 1; }
.pl-type { font-size: 12px; font-weight: 700; color: var(--accent); text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px; }
.pl-title { font-size: 48px; font-weight: 900; line-height: 1.1; margin-bottom: 12px; }
.pl-meta { font-size: 14px; color: var(--text-muted); }
.pl-actions { display: flex; gap: 16px; margin-top: 24px; }
.btn-primary { background: var(--accent); color: #000; font-weight: 700; padding: 10px 24px; border-radius: 500px; font-size: 14px; transition: 0.2s; }
.btn-primary:hover { background: var(--accent-hover); transform: scale(1.05); }
.btn-secondary { background: var(--bg-card); color: var(--text-main); font-weight: 600; padding: 10px 24px; border-radius: 500px; font-size: 14px; transition: 0.2s; border: 1px solid var(--border); }
.btn-secondary:hover { background: var(--bg-card-hover); border-color: var(--text-muted); }

.table-songs { width: 100%; border-collapse: collapse; }
.table-songs th { text-align: left; padding: 12px 16px; color: var(--text-muted); font-size: 12px; font-weight: 600; text-transform: uppercase; border-bottom: 1px solid var(--border); }
.table-songs td { padding: 12px 16px; border-bottom: 1px solid var(--border); transition: 0.2s; }
.table-songs tr:hover td { background: rgba(255,255,255,0.02); }
.table-songs tr { cursor: pointer; }

/* --- RIGHT SIDEBAR --- */
.right-sidebar { background: var(--bg-sidebar); border-left: 1px solid var(--border); padding: 32px 24px; display: flex; flex-direction: column; overflow-y: auto; }
.user-bar { display: flex; align-items: center; justify-content: space-between; margin-bottom: 40px; }
.user-info { display: flex; align-items: center; gap: 12px; }
.user-avatar { width: 40px; height: 40px; border-radius: 50%; background: var(--bg-card); display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 16px; }
.user-name { font-size: 14px; font-weight: 600; }
.user-sub { font-size: 11px; color: var(--text-muted); }
.btn-icon { width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: var(--text-muted); transition: 0.2s; }
.btn-icon:hover { color: var(--text-main); background: rgba(255,255,255,0.1); }

.weekly-list { margin-bottom: 40px; }
.wl-item { display: flex; align-items: center; padding: 8px 12px; border-radius: 4px; cursor: pointer; transition: 0.2s; margin-bottom: 4px; }
.wl-item:hover { background: rgba(255,255,255,0.05); }
.wl-item.active { background: var(--accent); color: #000; }
.wl-item.active .wl-num, .wl-item.active .wl-sub { color: #000; }
.wl-num { width: 24px; font-size: 12px; font-weight: 600; color: var(--text-muted); }
.wl-title { flex: 1; font-size: 13px; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.wl-play { width: 20px; display: flex; align-items: center; justify-content: flex-end; opacity: 0; transition: 0.2s; }
.wl-item:hover .wl-play, .wl-item.active .wl-play { opacity: 1; }
.wl-play svg { width: 14px; height: 14px; fill: currentColor; }

.sales-support { margin-bottom: 24px; }
.ss-card { display: flex; align-items: center; gap: 12px; background: var(--bg-card); padding: 12px; border-radius: 8px; margin-bottom: 8px; transition: 0.2s; cursor: pointer; }
.ss-card:hover { background: var(--bg-card-hover); transform: translateX(-4px); }
.ss-img { width: 48px; height: 48px; border-radius: 4px; object-fit: cover; }
.ss-info { flex: 1; }
.ss-title { font-size: 13px; font-weight: 600; margin-bottom: 4px; }
.ss-sub { font-size: 11px; color: var(--text-muted); }

/* --- PLAYER BAR --- */
.player-bar { height: var(--player-h); background: #15131C; border-top: 1px solid var(--border); display: flex; align-items: center; padding: 0 32px; z-index: 500; }
.player-container { width: 100%; max-width: 600px; height: 80px; margin: 0 auto; border-radius: 12px; overflow: hidden; background: #000; box-shadow: 0 4px 12px rgba(0,0,0,0.5); }
.player-container iframe { width: 100%; height: 100%; border: none; }
.empty-player { width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; color: var(--text-muted); font-size: 13px; font-weight: 500; }

/* Modals */
.modal-ov { position: fixed; inset: 0; background: rgba(0,0,0,0.8); backdrop-filter: blur(8px); display: none; align-items: center; justify-content: center; z-index: 9999; opacity: 0; transition: opacity 0.3s; }
.modal-ov.open { display: flex; animation: fadeIn 0.3s forwards; }
.modal-box { background: var(--bg-sidebar); border: 1px solid var(--border); padding: 32px; border-radius: 16px; width: 100%; max-width: 480px; box-shadow: 0 20px 40px rgba(0,0,0,0.5); transform: translateY(20px); opacity: 0; transition: 0.4s cubic-bezier(0.16, 1, 0.3, 1); }
.modal-ov.open .modal-box { transform: translateY(0); opacity: 1; border-top: 2px solid var(--accent); }
@keyframes fadeIn { to { opacity: 1; } }

.modal-title { font-size: 24px; font-weight: 800; margin-bottom: 24px; text-align: center; }
.form-group { margin-bottom: 20px; }
.form-group label { display: block; font-size: 12px; font-weight: 700; color: var(--text-muted); margin-bottom: 8px; text-transform: uppercase; letter-spacing: 1px; }
.form-group input, .form-group select { width: 100%; background: var(--bg-card); border: 1px solid var(--border); color: var(--text-main); padding: 14px 16px; border-radius: 8px; font-family: var(--font); font-size: 14px; outline: none; transition: 0.2s; }
.form-group input:focus, .form-group select:focus { border-color: var(--accent); }
.modal-actions { display: flex; justify-content: flex-end; gap: 12px; margin-top: 32px; }

/* Toast */
.toast { position: fixed; bottom: 120px; left: 50%; transform: translateX(-50%) translateY(20px); background: var(--accent); color: #000; padding: 12px 24px; border-radius: 8px; font-weight: 600; font-size: 14px; opacity: 0; pointer-events: none; transition: 0.3s; z-index: 10000; box-shadow: 0 8px 24px rgba(255, 215, 0, 0.3); }
.toast.show { opacity: 1; transform: translateX(-50%) translateY(0); pointer-events: auto; }
.toast.error { background: #E22134; color: #fff; box-shadow: 0 8px 24px rgba(226, 33, 52, 0.4); }

.no-msg { color: var(--text-muted); font-size: 14px; text-align: center; padding: 40px; border: 1px dashed var(--border); border-radius: 8px; }
</style>
</head>
<body>

<div class="app-wrapper">
  <!-- LEFT SIDEBAR -->
  <aside class="left-sidebar">
    <div class="logo-container">
      <div class="logo-icon">H</div>
      <div class="logo-text">HIWOW<br/><span style="font-size:10px; color:var(--text-muted); font-weight:600;">studio</span></div>
    </div>

    <div class="nav-section">
      <div class="nav-item active" onclick="showHome()">
        <svg viewBox="0 0 24 24"><path d="M12 3l9 7v11a1 1 0 01-1 1h-5v-6H9v6H4a1 1 0 01-1-1v-11l9-7z"/></svg>
        Music
      </div>
      <div class="nav-item" onclick="document.getElementById('searchInput').focus()">
        <svg viewBox="0 0 24 24"><path d="M15.5 14h-.79l-.28-.27A6.471 6.471 0 0016 9.5 6.5 6.5 0 109.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/></svg>
        Find
      </div>
      <div class="nav-item" onclick="openAddSongModal()">
        <svg viewBox="0 0 24 24"><path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/></svg>
        Singer
      </div>
      <div class="nav-item" onclick="openCreatePlaylistModal()">
        <svg viewBox="0 0 24 24"><path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/></svg>
        Collection
      </div>
    </div>

    <div class="nav-title">Song list</div>
    <div class="nav-section" id="sidebarPlaylists">
      <!-- injected -->
    </div>
  </aside>

  <!-- MAIN CONTENT -->
  <main class="main-content">
    <div class="search-container">
      <svg viewBox="0 0 24 24"><path d="M15.5 14h-.79l-.28-.27A6.471 6.471 0 0016 9.5 6.5 6.5 0 109.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/></svg>
      <input type="text" id="searchInput" placeholder="Search" oninput="handleSearch()"/>
    </div>

    <!-- HOME VIEW -->
    <div id="viewHome">
      <div class="hero-banner">
        <div class="hero-content">
          <div class="hero-title">OZUNA<br/>& MORE!</div>
          <div class="hero-subtitle">2024 Music Trends<br/>Exclusive Backstage<br/>Portraits of Top Artists</div>
        </div>
      </div>

      <div class="section-header">
        <div class="section-title">Recommended album</div>
        <div class="section-more" onclick="openCreatePlaylistModal()">Create</div>
      </div>
      <div class="grid-albums" id="playlistsGrid">
        <!-- injected -->
      </div>

      <div class="section-header">
        <div class="section-title">Recommended artist</div>
        <div class="section-more">More</div>
      </div>
      <div class="grid-artists" id="artistsGrid">
        <!-- injected -->
      </div>
      
      <div class="section-header">
        <div class="section-title">All Songs</div>
        <div class="section-more" onclick="openAddSongModal()">Add</div>
      </div>
      <div class="grid-albums" id="allSongsGrid">
        <!-- injected -->
      </div>
    </div>

    <!-- PLAYLIST VIEW -->
    <div id="viewPlaylist" class="view-playlist">
      <div class="playlist-header">
        <img id="plHeroImg" src="" class="pl-cover" alt="Cover"/>
        <div class="pl-info">
          <div class="pl-type" id="plHeroType">PLAYLIST</div>
          <div class="pl-title" id="plHeroTitle">Playlist Name</div>
          <div class="pl-meta" id="plHeroMeta">Details</div>
          <div class="pl-actions">
            <button class="btn-primary" onclick="playAll()">Play All</button>
            <button class="btn-secondary" id="btnAddSongBtn" onclick="openAddSongModal()">Add Song</button>
            <button class="btn-secondary" id="btnDeletePlaylist" onclick="deleteCurrentPlaylist()">Delete Playlist</button>
            <button class="btn-secondary" onclick="showHome()">Back</button>
          </div>
        </div>
      </div>
      
      <div id="noSongsMsg" class="no-msg" style="display:none;">This playlist is empty. Add some songs!</div>
      
      <table class="table-songs" id="songsTableWrap">
        <thead>
          <tr>
            <th width="40">#</th>
            <th>Title</th>
            <th>Date Added</th>
            <th width="80"></th>
          </tr>
        </thead>
        <tbody id="songsTbody">
          <!-- injected -->
        </tbody>
      </table>
    </div>

    <!-- SEARCH VIEW -->
    <div id="viewSearch" class="view-playlist">
      <div class="section-header" style="margin-top: 24px;">
        <div class="section-title">Search Results</div>
        <div class="section-more" onclick="document.getElementById('searchInput').value=''; handleSearch();">Clear</div>
      </div>
      <div id="noSearchMsg" class="no-msg" style="display:none;">No results found.</div>
      <table class="table-songs">
        <tbody id="searchTbody"></tbody>
      </table>
    </div>

  </main>

  <!-- RIGHT SIDEBAR -->
  <aside class="right-sidebar">
    <div class="user-bar">
      <div class="user-info">
        <div class="user-avatar">{{ request.user.first_name|default:request.user.username|make_list|first|upper }}</div>
        <div>
          <div class="user-name">{{ request.user.first_name|default:request.user.username }}</div>
          <div class="user-sub">No Introduction</div>
        </div>
      </div>
      <a href="{% url 'dashboard' %}" class="btn-icon" title="Dashboard">
        <svg viewBox="0 0 24 24"><path d="M3 13h8V3H3v10zm0 8h8v-6H3v6zm10 0h8V11h-8v10zm0-18v6h8V3h-8z"/></svg>
      </a>
    </div>

    <div class="section-title" style="font-size: 14px; margin-bottom: 16px;">Weekly list</div>
    <div class="weekly-list" id="weeklyList">
      <!-- injected -->
    </div>

    <div class="section-title" style="font-size: 14px; margin-bottom: 16px;">Sales support</div>
    <div class="sales-support" id="salesSupport">
      <!-- injected -->
    </div>
  </aside>
</div>

<!-- PLAYER BAR -->
<div class="player-bar">
  <div class="player-container" id="playerWrap">
    <div class="empty-player">Select a song to play</div>
  </div>
</div>

<!-- MODALS -->
<div class="modal-ov" id="modalAddSong" onclick="if(event.target===this) closeModal('modalAddSong')">
  <div class="modal-box">
    <div class="modal-title" id="addSongTitle">Add Song or Playlist</div>
    <div class="form-group">
      <label>Spotify / YouTube Link</label>
      <input type="text" id="inpSongLink" placeholder="Paste track or playlist link..."/>
    </div>
    <div class="form-group">
      <label>Add to Playlist (Optional)</label>
      <select id="inpSongPlaylist">
        <option value="">-- None (Save to All Songs) --</option>
      </select>
    </div>
    <input type="hidden" id="inpForceAdd" value="false"/>
    <div class="modal-actions">
      <button class="btn-cancel" onclick="closeModal('modalAddSong')">Cancel</button>
      <button class="btn-submit" id="btnAddSongSubmit" onclick="submitAddSong()">Add</button>
    </div>
  </div>
</div>

<div class="modal-ov" id="modalCreatePl" onclick="if(event.target===this) closeModal('modalCreatePl')">
  <div class="modal-box">
    <div class="modal-title">Create Playlist</div>
    <div class="form-group">
      <label>Playlist Name</label>
      <input type="text" id="inpPlName" placeholder="e.g. Chill Vibes"/>
    </div>
    <div class="modal-actions">
      <button class="btn-cancel" onclick="closeModal('modalCreatePl')">Cancel</button>
      <button class="btn-submit" onclick="submitCreatePlaylist()">Create</button>
    </div>
  </div>
</div>

<div class="toast" id="toast"></div>

<!-- INJECT EXTRACTED JS HERE -->
<script>
"""

with open('c:\\Users\\AKASH\\PycharmProjects\\coupleapp\\couple_tracker\\tracker\\templates\\tracker\\extracted_js.js', 'r', encoding='utf-8') as f:
    js_content = f.read()

html += js_content
html += """</script>
</body>
</html>
"""

# Now we need to modify the extracted JS to match the new DOM elements and logic!
# Instead of doing complex string replacements in python, I'll write the JS rewrite logic manually here.
# Actually, I can just write the modified JS entirely.

js_rewrite = '''
  let songs = [];
  let playlists = [];
  let currentPlaylistId = null;
  let currentView = 'home';
  let activeSongId = null;

  document.addEventListener('DOMContentLoaded', () => {
    fetchData();
  });

  async function fetchData() {
    // In a real app, you'd fetch from an API. We'll use the existing template injection.
    songs = [
      {% for s in songs %}
      {
        id: {{ s.id }},
        title: "{{ s.title|escapejs }}",
        artist: "{{ s.artist|escapejs }}",
        platform: "{{ s.platform }}",
        track_id: "{{ s.track_id }}",
        cover_url: "{{ s.cover_url|escapejs }}",
        date: "{{ s.date_added|date:'M d, Y' }}",
        playlist_ids: [{% for p in s.playlists.all %}{{ p.id }},{% endfor %}]
      },
      {% endfor %}
    ];

    playlists = [
      {% for p in playlists %}
      {
        id: {{ p.id }},
        name: "{{ p.name|escapejs }}",
        cover_url: "{{ p.cover_url|escapejs }}",
        created_by: "{{ p.created_by.first_name|default:p.created_by.username|escapejs }}",
        is_external: {{ p.is_external|yesno:"true,false" }},
        platform: "{{ p.platform|default:'' }}",
        external_id: "{{ p.external_id|default:'' }}"
      },
      {% endfor %}
    ];

    renderSidebarPlaylists();
    updatePlaylistSelects();
    renderHome();
    renderRightSidebar();
  }

  function renderSidebarPlaylists() {
    const sb = document.getElementById('sidebarPlaylists');
    sb.innerHTML = '';
    playlists.forEach(p => {
      const el = document.createElement('div');
      el.className = 'nav-item';
      el.innerHTML = `
        <span style="color:var(--text-muted); font-weight:800; margin-right:8px;">-</span>
        <span style="flex:1; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">${p.name}</span>
      `;
      el.onclick = () => showPlaylist(p.id);
      sb.appendChild(el);
    });
  }

  function updatePlaylistSelects() {
    const sel = document.getElementById('inpSongPlaylist');
    sel.innerHTML = '<option value="">-- None (Save to All Songs) --</option>';
    playlists.filter(p => !p.is_external).forEach(p => {
      const opt = document.createElement('option');
      opt.value = p.id;
      opt.textContent = p.name;
      sel.appendChild(opt);
    });
  }

  function renderRightSidebar() {
    // Weekly List
    const wl = document.getElementById('weeklyList');
    wl.innerHTML = '';
    const topSongs = songs.slice(0, 6);
    topSongs.forEach((s, idx) => {
      const el = document.createElement('div');
      el.className = 'wl-item' + (activeSongId === s.id ? ' active' : '');
      el.onclick = () => playSong(s);
      el.innerHTML = `
        <div class="wl-num">${idx + 1}</div>
        <div class="wl-title">${s.title || s.artist} - <span style="font-weight:400;">${s.artist || s.platform}</span></div>
        <div class="wl-play"><svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg></div>
      `;
      wl.appendChild(el);
    });

    // Sales Support / Recent Playlists
    const ss = document.getElementById('salesSupport');
    ss.innerHTML = '';
    const topPls = playlists.slice(0, 4);
    topPls.forEach(p => {
      const el = document.createElement('div');
      el.className = 'ss-card';
      el.onclick = () => showPlaylist(p.id);
      el.innerHTML = `
        <img src="${p.cover_url || 'https://ui-avatars.com/api/?name=' + encodeURIComponent(p.name) + '&background=random'}" class="ss-img"/>
        <div class="ss-info">
          <div class="ss-title">${p.name}</div>
          <div class="ss-sub">${p.created_by}</div>
        </div>
      `;
      ss.appendChild(el);
    });
  }

  function renderHome() {
    currentView = 'home';
    currentPlaylistId = null;
    document.getElementById('viewPlaylist').style.display = 'none';
    document.getElementById('viewSearch').style.display = 'none';
    document.getElementById('viewHome').style.display = 'block';

    // Playlists Grid
    const pGrid = document.getElementById('playlistsGrid');
    pGrid.innerHTML = '';
    playlists.forEach(p => {
      const card = document.createElement('div');
      card.className = 'album-card';
      card.onclick = () => showPlaylist(p.id);
      card.innerHTML = `
        <button class="btn-card-del" onclick="event.stopPropagation(); deleteCurrentPlaylist(${p.id})" title="Delete">
          <svg viewBox="0 0 24 24" width="16" fill="currentColor"><path d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zm2.46-7.12l1.41-1.41L12 12.59l2.12-2.12 1.41 1.41L13.41 14l2.12 2.12-1.41 1.41L12 15.41l-2.12 2.12-1.41-1.41L10.59 14l-2.13-2.12zM15.5 4l-1-1h-5l-1 1H5v2h14V4z"/></svg>
        </button>
        <img class="album-img" src="${p.cover_url || 'https://ui-avatars.com/api/?name=' + encodeURIComponent(p.name) + '&background=1C192B&color=fff&size=200'}"/>
        <div class="album-title">${p.name}</div>
        <div class="album-sub">${p.created_by}</div>
      `;
      pGrid.appendChild(card);
    });

    // All Songs Grid
    const sGrid = document.getElementById('allSongsGrid');
    sGrid.innerHTML = '';
    songs.forEach(s => {
      const card = document.createElement('div');
      card.className = 'album-card';
      card.onclick = () => playSong(s);
      card.innerHTML = `
        <button class="btn-card-del" onclick="event.stopPropagation(); deleteSong(${s.id})" title="Delete">
          <svg viewBox="0 0 24 24" width="16" fill="currentColor"><path d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zm2.46-7.12l1.41-1.41L12 12.59l2.12-2.12 1.41 1.41L13.41 14l2.12 2.12-1.41 1.41L12 15.41l-2.12 2.12-1.41-1.41L10.59 14l-2.13-2.12zM15.5 4l-1-1h-5l-1 1H5v2h14V4z"/></svg>
        </button>
        <img class="album-img" src="${s.cover_url || 'https://ui-avatars.com/api/?name=' + encodeURIComponent(s.title || 'U') + '&background=222030&color=fff&size=200'}"/>
        <div class="album-title">${s.title || 'Unknown Track'}</div>
        <div class="album-sub">${s.artist || s.platform}</div>
      `;
      sGrid.appendChild(card);
    });

    // Artists Grid
    const aGrid = document.getElementById('artistsGrid');
    aGrid.innerHTML = '';
    const artistNames = [...new Set(songs.map(s => s.artist).filter(a => a && a !== 'Unknown Artist'))];
    artistNames.forEach(a => {
      const card = document.createElement('div');
      card.className = 'artist-card';
      card.innerHTML = `
        <img class="artist-img" src="https://ui-avatars.com/api/?name=${encodeURIComponent(a)}&background=random&color=fff&size=150"/>
        <div class="artist-name">${a}</div>
      `;
      aGrid.appendChild(card);
    });
  }

  function showPlaylist(id) {
    currentView = 'playlist';
    currentPlaylistId = id;
    document.getElementById('viewHome').style.display = 'none';
    document.getElementById('viewSearch').style.display = 'none';
    document.getElementById('viewPlaylist').style.display = 'block';

    const p = playlists.find(x => x.id === id);
    if(!p) return;

    document.getElementById('plHeroImg').src = p.cover_url || 'https://ui-avatars.com/api/?name=' + encodeURIComponent(p.name) + '&background=1C192B&color=fff&size=400';
    document.getElementById('plHeroTitle').textContent = p.name;
    document.getElementById('plHeroType').textContent = p.is_external ? 'EXTERNAL PLAYLIST' : 'PLAYLIST';
    
    const tbParent = document.getElementById('songsTableWrap');
    const tb = document.getElementById('songsTbody');
    tb.innerHTML = '';
    
    if (p.is_external) {
      document.getElementById('plHeroMeta').textContent = `By ${p.created_by} • External Playlist`;
      tbParent.style.display = 'none';
      document.getElementById('noSongsMsg').style.display = 'none';
      document.getElementById('btnAddSongBtn').style.display = 'none';
      
      const wrap = document.getElementById('playerWrap');
      if (p.platform === 'spotify') {
        wrap.innerHTML = `<iframe src="https://open.spotify.com/embed/playlist/${p.external_id}?utm_source=generator" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"></iframe>`;
      } else if (p.platform === 'youtube') {
        wrap.innerHTML = `<iframe src="https://www.youtube.com/embed/videoseries?list=${p.external_id}" allow="autoplay; encrypted-media" allowfullscreen></iframe>`;
      }
      return;
    }

    document.getElementById('btnAddSongBtn').style.display = 'inline-block';
    tbParent.style.display = 'table';
    const plSongs = songs.filter(s => s.playlist_ids.includes(id));
    document.getElementById('plHeroMeta').textContent = `By ${p.created_by} • ${plSongs.length} songs`;
    
    if (plSongs.length === 0) {
      document.getElementById('noSongsMsg').style.display = 'block';
      tbParent.style.display = 'none';
    } else {
      document.getElementById('noSongsMsg').style.display = 'none';
      tbParent.style.display = 'table';
      plSongs.forEach((s, idx) => {
        const tr = document.createElement('tr');
        tr.onclick = (e) => { if(e.target.tagName !== 'BUTTON' && !e.target.closest('button')) playSong(s); };
        tr.innerHTML = `
          <td>${idx+1}</td>
          <td>
            <div style="display:flex; align-items:center; gap:12px;">
              <img src="${s.cover_url || 'https://ui-avatars.com/api/?name=U&background=222030&color=fff'}" style="width:40px; height:40px; border-radius:4px; object-fit:cover;"/>
              <div>
                <div style="font-size:14px; font-weight:600; color:var(--text-main);">${s.title || 'Unknown Title'}</div>
                <div style="font-size:12px; color:var(--text-muted);">${s.artist || s.platform}</div>
              </div>
            </div>
          </td>
          <td>${s.date}</td>
          <td><button class="btn-card-del" style="position:static; opacity:1; width:auto; height:auto; padding:6px 12px; border-radius:4px; font-size:12px;" onclick="deleteSong(${s.id})">Remove</button></td>
        `;
        tb.appendChild(tr);
      });
    }
  }

  function playSong(s) {
    activeSongId = s.id;
    renderRightSidebar(); // Update highlight
    const wrap = document.getElementById('playerWrap');
    let embedType = 'track';
    let tId = s.track_id;
    if (tId.startsWith('playlist:')) {
      embedType = 'playlist';
      tId = tId.replace('playlist:', '');
    }

    if (s.platform === 'spotify') {
      wrap.innerHTML = `<iframe src="https://open.spotify.com/embed/${embedType}/${tId}?utm_source=generator" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"></iframe>`;
    } else if (s.platform === 'youtube') {
      if (embedType === 'playlist') {
        wrap.innerHTML = `<iframe src="https://www.youtube.com/embed/videoseries?list=${tId}" allow="autoplay; encrypted-media" allowfullscreen></iframe>`;
      } else {
        wrap.innerHTML = `<iframe src="https://www.youtube.com/embed/${tId}?autoplay=1" allow="autoplay; encrypted-media" allowfullscreen></iframe>`;
      }
    } else {
      wrap.innerHTML = `<div class="empty-player">Cannot play this link format.</div>`;
    }
  }

  function playAll() {
    if(!currentPlaylistId) return;
    const plSongs = songs.filter(s => s.playlist_ids.includes(currentPlaylistId));
    if(plSongs.length > 0) playSong(plSongs[0]);
  }

  function showHome() { renderHome(); }

  // SEARCH
  function handleSearch() {
    const q = document.getElementById('searchInput').value.toLowerCase();
    if (!q) {
      if (currentPlaylistId) showPlaylist(currentPlaylistId);
      else showHome();
      return;
    }
    
    document.getElementById('viewHome').style.display = 'none';
    document.getElementById('viewPlaylist').style.display = 'none';
    document.getElementById('viewSearch').style.display = 'block';

    const res = songs.filter(s => (s.title && s.title.toLowerCase().includes(q)) || (s.artist && s.artist.toLowerCase().includes(q)) || (s.platform && s.platform.toLowerCase().includes(q)));
    
    const tb = document.getElementById('searchTbody');
    tb.innerHTML = '';
    
    if (res.length === 0) {
      document.getElementById('noSearchMsg').style.display = 'block';
    } else {
      document.getElementById('noSearchMsg').style.display = 'none';
      res.forEach((s, idx) => {
        const tr = document.createElement('tr');
        tr.onclick = (e) => { if(e.target.tagName !== 'BUTTON' && !e.target.closest('button')) playSong(s); };
        tr.innerHTML = `
          <td>${idx+1}</td>
          <td>
            <div style="display:flex; align-items:center; gap:12px;">
              <img src="${s.cover_url || 'https://ui-avatars.com/api/?name=U&background=222030&color=fff'}" style="width:40px; height:40px; border-radius:4px; object-fit:cover;"/>
              <div>
                <div style="font-size:14px; font-weight:600; color:var(--text-main);">${s.title || 'Unknown Title'}</div>
                <div style="font-size:12px; color:var(--text-muted);">${s.artist || s.platform}</div>
              </div>
            </div>
          </td>
          <td>${s.date}</td>
          <td><button class="btn-card-del" style="position:static; opacity:1; width:auto; height:auto; padding:6px 12px; border-radius:4px; font-size:12px;" onclick="deleteSong(${s.id})">Remove</button></td>
        `;
        tb.appendChild(tr);
      });
    }
  }

  // DELETE
  async function deleteSong(id) {
    if(!confirm('Delete this song?')) return;
    const r = await fetch(`/songs/delete/${id}/`, {
      method: 'POST',
      headers: { 'X-CSRFToken': getCSRF(), 'X-Requested-With': 'XMLHttpRequest' }
    });
    if(r.ok) {
      songs = songs.filter(s => s.id !== id);
      if(currentView === 'playlist') showPlaylist(currentPlaylistId);
      else if(currentView === 'search') handleSearch();
      else showHome();
      renderRightSidebar();
      showToast('Song deleted');
    }
  }

  async function deleteCurrentPlaylist(id = null) {
    const targetId = id || currentPlaylistId;
    if(!targetId) return;
    if(!confirm('Delete this entire playlist?')) return;
    const r = await fetch(`/songs/playlist/delete/${targetId}/`, {
      method: 'POST',
      headers: { 'X-CSRFToken': getCSRF(), 'X-Requested-With': 'XMLHttpRequest' }
    });
    if(r.ok) {
      playlists = playlists.filter(p => p.id !== targetId);
      if(currentView === 'playlist' && currentPlaylistId === targetId) showHome();
      else if(currentView === 'home') renderHome();
      showToast('Playlist deleted');
      renderSidebarPlaylists();
      updatePlaylistSelects();
      renderRightSidebar();
    }
  }

  // MODALS
  function getCSRF() {
    return document.cookie.split('; ').find(row => row.startsWith('csrftoken='))?.split('=')[1] || '';
  }

  function openModal(id) {
    const m = document.getElementById(id);
    m.style.display = 'flex';
    setTimeout(() => m.classList.add('open'), 10);
  }
  function closeModal(id) {
    const m = document.getElementById(id);
    m.classList.remove('open');
    setTimeout(() => m.style.display = 'none', 300);
  }

  function openCreatePlaylistModal() {
    document.getElementById('inpPlName').value = '';
    openModal('modalCreatePl');
  }

  async function submitCreatePlaylist() {
    const name = document.getElementById('inpPlName').value.trim();
    if(!name) return;
    
    const fd = new FormData();
    fd.append('name', name);

    const r = await fetch('{% url "create_playlist" %}', {
      method: 'POST',
      headers: { 'X-CSRFToken': getCSRF() },
      body: fd
    });
    const data = await r.json();
    if(data.status === 'success') {
      playlists.push({id: data.id, name: data.name, created_by: 'You'});
      renderSidebarPlaylists();
      updatePlaylistSelects();
      if(currentView === 'home') renderHome();
      renderRightSidebar();
      closeModal('modalCreatePl');
      showToast('Playlist created!');
    }
  }

  function openAddSongModal(forcePlId = null, isFromSearch = false) {
    document.getElementById('inpSongLink').value = '';
    document.getElementById('inpForceAdd').value = 'false';
    const sel = document.getElementById('inpSongPlaylist');
    
    if (forcePlId) {
      sel.value = forcePlId;
    } else if (currentPlaylistId && !isFromSearch) {
      sel.value = currentPlaylistId;
    } else {
      sel.value = '';
    }
    
    document.getElementById('btnAddSongSubmit').textContent = 'Add';
    document.getElementById('addSongTitle').textContent = 'Add Song or Playlist';
    openModal('modalAddSong');
  }

  async function submitAddSong() {
    const link = document.getElementById('inpSongLink').value.trim();
    const pl_id = document.getElementById('inpSongPlaylist').value;
    const force = document.getElementById('inpForceAdd').value === 'true';

    if(!link) return;

    const payload = {
      link: link,
      playlist_id: pl_id || null,
      force_add: force
    };

    const r = await fetch('{% url "add_song_api" %}', {
      method: 'POST',
      headers: { 'X-CSRFToken': getCSRF(), 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await r.json();
    
    if(data.status === 'exists') {
      showToast(data.message, 'warning');
      document.getElementById('inpForceAdd').value = 'true';
      document.getElementById('btnAddSongSubmit').textContent = 'Add Anyway';
      return;
    }

    if(data.status === 'error') {
      showToast(data.message || 'Failed to add', 'error');
      return;
    }

    if(data.status === 'success') {
      if(data.type === 'playlist') {
        playlists.push({
          id: data.id,
          name: data.name,
          cover_url: data.cover_url,
          created_by: 'You',
          is_external: true,
          platform: data.platform,
          external_id: data.external_id
        });
        renderSidebarPlaylists();
      } else {
        const newS = {
          id: data.id,
          title: data.title,
          artist: data.artist,
          platform: data.platform,
          track_id: data.track_id,
          cover_url: data.cover_url,
          date: data.date,
          playlist_ids: pl_id ? [parseInt(pl_id)] : []
        };
        const exists = songs.find(x => x.id === data.id);
        if(!exists) songs.unshift(newS);
        else if(pl_id && !exists.playlist_ids.includes(parseInt(pl_id))) exists.playlist_ids.push(parseInt(pl_id));
      }
      
      closeModal('modalAddSong');
      showToast('Added successfully!');
      
      if(currentView === 'home') renderHome();
      else if(currentView === 'playlist') showPlaylist(currentPlaylistId);
      
      renderRightSidebar();
    }
  }

  // TOAST
  let toastTimeout;
  function showToast(msg, type='success') {
    const t = document.getElementById('toast');
    t.textContent = msg;
    t.className = 'toast show ' + type;
    clearTimeout(toastTimeout);
    toastTimeout = setTimeout(() => t.classList.remove('show'), 3000);
  }
'''

with open('c:\\Users\\AKASH\\PycharmProjects\\coupleapp\\couple_tracker\\scratch_writer.py', 'w', encoding='utf-8') as f:
    f.write(f"""
import sys
html = {repr(html)}
js = {repr(js_rewrite)}

final_content = html.split('<script>')[0] + '<script>\\n' + js + '\\n</script>\\n</body>\\n</html>'

with open('c:\\\\Users\\\\AKASH\\\\PycharmProjects\\\\coupleapp\\\\couple_tracker\\\\tracker\\\\templates\\\\tracker\\\\song_tracker.html', 'w', encoding='utf-8') as out:
    out.write(final_content)
print("Done writing.")
""")
