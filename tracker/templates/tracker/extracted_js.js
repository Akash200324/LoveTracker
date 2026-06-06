
  // Safe data building
  let songs = [
    {% for s in songs %}
    {
      id: {{ s.id }},
      title: "{{ s.title|escapejs }}",
      artist: "{{ s.artist|escapejs }}",
      platform: "{{ s.platform|escapejs }}",
      track_id: "{{ s.track_id|escapejs }}",
      date: "{{ s.date_added|date:'M d, Y' }}",
      cover_url: "{{ s.cover_url|escapejs }}",
      playlist_ids: [ {% for p in s.playlists.all %}{{ p.id }},{% endfor %} ]
    },
    {% endfor %}
  ];

  let playlists = [
    {% for p in playlists %}
    {
      id: {{ p.id }},
      name: "{{ p.name|escapejs }}",
      created_by: ("{{ p.created_by.first_name|default:p.created_by.username|escapejs }}").split('@')[0],
      cover_url: "{{ p.cover_url|escapejs }}",
      is_external: {{ p.is_external|yesno:"true,false" }},
      platform: "{{ p.platform|escapejs }}",
      external_id: "{{ p.external_id|escapejs }}"
    },
    {% endfor %}
  ];

  let currentPlaylistId = null;
  let currentView = 'home';

  window.onload = () => {
    const el = document.getElementById('navUsername');
    if(el) el.textContent = el.textContent.split('@')[0];

    renderSidebarPlaylists();
    renderHome();
    updatePlaylistSelects();
  };

  function handleScroll() {
    const nav = document.getElementById('topNav');
    if (document.getElementById('mainView').scrollTop > 20) {
      nav.classList.add('top-nav-scrolled');
    } else {
      nav.classList.remove('top-nav-scrolled');
    }
  }

  function showToast(msg, type='success') {
    const t = document.getElementById('toast');
    t.textContent = msg;
    t.className = 'toast show ' + type;
    setTimeout(() => t.classList.remove('show'), 4000);
  }

  function openModal(id) { document.getElementById(id).classList.add('open'); }
  function closeModal(id) { document.getElementById(id).classList.remove('open'); }

  function showHome() {
    currentView = 'home';
    currentPlaylistId = null;
    document.getElementById('viewHome').style.display = 'block';
    document.getElementById('viewPlaylist').style.display = 'none';
    document.getElementById('viewSearch').style.display = 'none';
    document.getElementById('searchInput').value = '';
    
    // Update active nav
    document.querySelectorAll('.sb-item').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.sb-item')[1].classList.add('active'); // Home is 2nd

    renderHome();
  }

  function goBack() { showHome(); }

  function renderSidebarPlaylists() {
    const sb = document.getElementById('sidebarPlaylists');
    sb.innerHTML = '';
    playlists.forEach(p => {
      const el = document.createElement('div');
      el.className = 'pl-item';
      el.onclick = () => showPlaylist(p.id);
      el.innerHTML = `
        <span style="flex:1; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">${p.name}</span>
        <button class="sb-pl-del" onclick="event.stopPropagation(); deleteCurrentPlaylist(${p.id})" title="Delete Playlist">
          <svg viewBox="0 0 24 24" width="16" fill="currentColor"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/></svg>
        </button>
      `;
      sb.appendChild(el);
    });
  }

  function updatePlaylistSelects() {
    const sel = document.getElementById('inpSongPlaylist');
    sel.innerHTML = '<option value="">-- No Playlist --</option>';
    playlists.forEach(p => {
      const opt = document.createElement('option');
      opt.value = p.id;
      opt.textContent = p.name;
      sel.appendChild(opt);
    });
  }

  function renderHome() {
    const grid = document.getElementById('playlistsGrid');
    grid.innerHTML = '';
    playlists.forEach(p => {
      const card = document.createElement('div');
      card.className = 'pl-card';
      card.onclick = () => showPlaylist(p.id);
      card.innerHTML = `
        <button class="btn-card-del" onclick="event.stopPropagation(); deleteCurrentPlaylist(${p.id})" title="Delete Playlist">
          <svg viewBox="0 0 24 24" width="18" fill="currentColor"><path d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zm2.46-7.12l1.41-1.41L12 12.59l2.12-2.12 1.41 1.41L13.41 14l2.12 2.12-1.41 1.41L12 15.41l-2.12 2.12-1.41-1.41L10.59 14l-2.13-2.12zM15.5 4l-1-1h-5l-1 1H5v2h14V4z"/></svg>
        </button>
        <div class="pl-card-img" style="${p.cover_url ? `background: url('${p.cover_url}') center/cover no-repeat;` : `background: linear-gradient(135deg, #1DB954, #121212);`}"></div>
        <div class="pl-card-title">${p.name}</div>
        <div class="pl-card-sub">By ${p.created_by}</div>
      `;
      grid.appendChild(card);
    });

    const sGrid = document.getElementById('allSongsGrid');
    sGrid.innerHTML = '';
    songs.slice(0, 10).forEach(s => {
      const card = document.createElement('div');
      card.className = 'pl-card';
      card.onclick = () => playSong(s);
      card.innerHTML = `
        <button class="btn-card-del" onclick="event.stopPropagation(); deleteSong(${s.id})" title="Delete Song">
          <svg viewBox="0 0 24 24" width="18" fill="currentColor"><path d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zm2.46-7.12l1.41-1.41L12 12.59l2.12-2.12 1.41 1.41L13.41 14l2.12 2.12-1.41 1.41L12 15.41l-2.12 2.12-1.41-1.41L10.59 14l-2.13-2.12zM15.5 4l-1-1h-5l-1 1H5v2h14V4z"/></svg>
        </button>
        <div class="pl-card-img" style="${s.cover_url ? `background: url('${s.cover_url}') center/cover no-repeat;` : `background: linear-gradient(135deg, #9b5de5, #121212);`}"></div>
        <div class="pl-card-title">${s.title || 'Unknown Track'}</div>
        <div class="pl-card-sub">${s.artist || s.platform}</div>
      `;
      sGrid.appendChild(card);
    });
  }

  function showPlaylist(id) {
    currentView = 'playlist';
    currentPlaylistId = id;
    document.getElementById('viewHome').style.display = 'none';
    document.getElementById('viewSearch').style.display = 'none';
    document.getElementById('viewPlaylist').style.display = 'block';

    document.querySelectorAll('.sb-item').forEach(el => el.classList.remove('active'));

    const p = playlists.find(x => x.id === id);
    if (!p) return;

    document.getElementById('plHeroTitle').textContent = p.name;
    const img = document.getElementById('plHeroImg');
    if (p.cover_url) {
      img.style.background = `url('${p.cover_url}') center/cover no-repeat`;
    } else {
      img.style.background = `linear-gradient(135deg, #1DB954, #121212)`;
    }

    const tb = document.getElementById('songsTbody');
    const tbParent = tb.parentElement;
    tb.innerHTML = '';
    
    if (p.is_external) {
      document.getElementById('plHeroMeta').textContent = `By ${p.created_by} • External Playlist`;
      tbParent.style.display = 'none';
      document.getElementById('noSongsMsg').style.display = 'none';
      
      const wrap = document.getElementById('playerWrap');
      if (p.platform === 'spotify') {
        wrap.innerHTML = `<iframe src="https://open.spotify.com/embed/playlist/${p.external_id}?utm_source=generator" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"></iframe>`;
      } else if (p.platform === 'youtube') {
        wrap.innerHTML = `<iframe src="https://www.youtube.com/embed/videoseries?list=${p.external_id}" allow="autoplay; encrypted-media" allowfullscreen></iframe>`;
      }
      return;
    }

    tbParent.style.display = 'table';
    const plSongs = songs.filter(s => s.playlist_ids.includes(id));
    document.getElementById('plHeroMeta').textContent = `By ${p.created_by} • ${plSongs.length} songs`;
    
    document.getElementById('btnDeletePlaylist').style.display = 'inline-block';
    
    if (plSongs.length === 0) {
      document.getElementById('noSongsMsg').style.display = 'block';
    } else {
      document.getElementById('noSongsMsg').style.display = 'none';
      plSongs.forEach((s, idx) => {
        const tr = document.createElement('tr');
        tr.className = 'song-row';
        tr.onclick = (e) => { if(e.target.tagName !== 'BUTTON') playSong(s); };
        tr.innerHTML = `
          <td>
            <div class="song-index">${idx+1}</div>
            <div class="song-play"><svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg></div>
          </td>
          <td>
            <div class="song-cell-title">
              <div class="song-thumb" style="${s.cover_url ? `background: url('${s.cover_url}') center/cover no-repeat;` : `background: linear-gradient(45deg, #1DB954, #121212);`}"></div>
              <div class="song-info">
                <span class="song-name">${s.title || 'Unknown Title'}</span>
                <span class="song-artist">${s.artist || s.platform}</span>
              </div>
            </div>
          </td>
          <td>${s.date}</td>
          <td><button class="btn-cancel" style="padding: 4px 8px; font-size: 12px;" onclick="deleteSong(${s.id})">Remove</button></td>
        `;
        tb.appendChild(tr);
      });
    }
  }

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
        tr.className = 'song-row';
        tr.onclick = (e) => { if(e.target.tagName !== 'BUTTON') playSong(s); };
        tr.innerHTML = `
          <td>
            <div class="song-index">${idx+1}</div>
            <div class="song-play"><svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg></div>
          </td>
          <td>
            <div class="song-cell-title">
              <div class="song-thumb" style="${s.cover_url ? `background: url('${s.cover_url}') center/cover no-repeat;` : `background: linear-gradient(45deg, #1DB954, #121212);`}"></div>
              <div class="song-info">
                <span class="song-name">${s.title || 'Unknown Title'}</span>
                <span class="song-artist">${s.artist || s.platform}</span>
              </div>
            </div>
          </td>
          <td>${s.date}</td>
          <td><button class="btn-cancel" style="padding: 4px 8px; font-size: 12px;" onclick="deleteSong(${s.id})">Remove</button></td>
        `;
        tb.appendChild(tr);
      });
    }
  }

  function playSong(s) {
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
    }
  }

  function getCSRF() {
    return document.cookie.split('; ').find(row => row.startsWith('csrftoken='))?.split('=')[1] || '';
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
    document.getElementById('btnAddSongSubmit').style.background = 'var(--green)';
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
      showToast('Song already exists!', 'warning');
      document.getElementById('addSongTitle').textContent = 'Song already in tracker!';
      const btn = document.getElementById('btnAddSongSubmit');
      btn.textContent = 'Add anyway to this Playlist?';
      btn.style.background = '#f59e0b'; // orange
      document.getElementById('inpForceAdd').value = 'true';
      return;
    }

    if(data.status === 'success') {
      if (data.type === 'playlist') {
        playlists.push({
          id: data.id,
          name: data.name,
          created_by: 'You',
          cover_url: data.cover_url,
          is_external: true,
          platform: data.platform,
          external_id: data.external_id
        });
        showToast('Playlist imported successfully!');
        renderSidebarPlaylists();
        updatePlaylistSelects();
        closeModal('modalAddSong');
        if(currentView === 'home') renderHome();
      } else {
        let existing = songs.find(x => x.id === data.id);
        if(existing) {
          if(pl_id && !existing.playlist_ids.includes(parseInt(pl_id))) {
            existing.playlist_ids.push(parseInt(pl_id));
          }
        } else {
          songs.unshift({
            id: data.id,
            title: data.title,
            artist: data.artist,
            platform: data.platform,
            track_id: data.track_id,
            date: data.date,
            cover_url: data.cover_url,
            playlist_ids: pl_id ? [parseInt(pl_id)] : []
          });
        }

        closeModal('modalAddSong');
        showToast('Song added successfully!');
        
        // Update UI
        if(currentView === 'playlist' && parseInt(pl_id) === currentPlaylistId) {
          showPlaylist(currentPlaylistId);
        } else if(currentView === 'home') {
          renderHome();
        } else if(currentView === 'search') {
          handleSearch();
        }
      }
    } else {
      showToast(data.message || 'Error adding song', 'error');
    }
  }

