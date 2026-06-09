import re

with open('tracker/templates/tracker/dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

new_modal = """<!-- Add Memory Modal -->
<div class="modal-overlay" id="memoryModal" style="z-index: 1000;">
  <div class="modal" style="padding: 0; overflow: hidden; display: flex; flex-direction: column; max-width: 400px; border-radius: 16px; background: rgba(255,255,255,0.95); backdrop-filter: blur(10px);">
    <!-- Header -->
    <div style="padding: 15px; border-bottom: 1px solid rgba(0,0,0,0.05); display: flex; justify-content: space-between; align-items: center;">
      <h3 style="margin: 0; font-family: 'Playfair Display', serif; font-size: 1.3rem; color: var(--charcoal);">📸 New Snap</h3>
      <button onclick="closeMemoryModal()" style="background: none; border: none; font-size: 1.2rem; cursor: pointer; color: var(--text-muted);">✕</button>
    </div>
    
    <!-- Tabs -->
    <div style="display: flex; background: rgba(0,0,0,0.02);">
      <button id="tabCamera" onclick="switchSnapTab('camera')" style="flex: 1; padding: 12px; border: none; background: #fff; font-weight: bold; border-bottom: 2px solid var(--pink-main); cursor: pointer; transition: 0.3s; color: var(--text-main);">Camera</button>
      <button id="tabGallery" onclick="switchSnapTab('gallery')" style="flex: 1; padding: 12px; border: none; background: transparent; font-weight: bold; border-bottom: 2px solid transparent; cursor: pointer; transition: 0.3s; color: var(--text-muted);">Gallery</button>
    </div>

    <!-- Camera View -->
    <div id="viewCamera" style="display: flex; flex-direction: column; position: relative; background: #000;">
      <video id="cameraVideo" autoplay playsinline style="width: 100%; height: 350px; object-fit: cover;"></video>
      <canvas id="cameraCanvas" style="display: none; width: 100%; height: 350px; object-fit: cover;"></canvas>
      
      <!-- Capture Button Container -->
      <div id="cameraControls" style="position: absolute; bottom: 20px; width: 100%; display: flex; justify-content: center;">
        <button onclick="captureSnap()" style="width: 60px; height: 60px; border-radius: 50%; background: rgba(255,255,255,0.3); border: 4px solid #fff; cursor: pointer; box-shadow: 0 4px 15px rgba(0,0,0,0.2); transition: transform 0.2s;" onmousedown="this.style.transform='scale(0.95)'" onmouseup="this.style.transform='scale(1)'"></button>
      </div>

      <!-- Post-Capture Controls -->
      <div id="postCaptureControls" style="display: none; position: absolute; top: 15px; right: 15px;">
        <button onclick="retakeSnap()" style="background: rgba(0,0,0,0.5); color: #fff; border: 1px solid rgba(255,255,255,0.3); padding: 6px 14px; border-radius: 20px; cursor: pointer; font-size: 0.9rem; backdrop-filter: blur(5px);">↺ Retake</button>
      </div>
    </div>

    <!-- Gallery View -->
    <div id="viewGallery" style="display: none; padding: 30px 20px; text-align: center; height: 350px; overflow-y: auto;">
      <div id="galleryPreviewContainer" style="display: none; margin-bottom: 20px; position: relative;">
        <img id="galleryPreview" style="width: 100%; max-height: 250px; object-fit: contain; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);" />
        <button onclick="clearGallerySelection()" style="position: absolute; top: 10px; right: 10px; background: rgba(0,0,0,0.5); color: white; border: none; border-radius: 50%; width: 30px; height: 30px; cursor: pointer;">✕</button>
      </div>
      <button id="gallerySelectBtn" onclick="document.getElementById('galleryInput').click()" style="padding: 15px 20px; border-radius: 12px; background: rgba(255,107,152,0.1); border: 2px dashed var(--pink-main); color: var(--pink-main); width: 100%; cursor: pointer; font-weight: bold; font-size: 1rem; transition: 0.2s;">
        🖼 Select from Device
      </button>
      <input type="file" id="galleryInput" accept="image/*" style="display: none;" onchange="previewGallerySnap(this)" />
    </div>

    <!-- Description & Upload -->
    <div style="padding: 15px; display: flex; flex-direction: column; gap: 12px;">
      <textarea id="snapCaption" placeholder="Add a caption..." style="width: 100%; padding: 14px; border-radius: 12px; border: 1px solid rgba(0,0,0,0.1); outline: none; font-family: inherit; resize: none; background: rgba(0,0,0,0.02); color: var(--text-main);" rows="2"></textarea>
      <button onclick="uploadSnapMemory()" class="btn btn-primary" style="width: 100%; justify-content: center; padding: 14px; border-radius: 12px; font-size: 1.1rem; box-shadow: 0 4px 15px rgba(255,107,152,0.3);">Save Memory ✨</button>
    </div>
  </div>
</div>"""

# Replace old modal
old_modal_pattern = r'<!-- Add Memory Modal -->.*?</div>\s*</div>'
content = re.sub(old_modal_pattern, new_modal, content, flags=re.DOTALL)

# Add JS logic
js_logic = """
// ═══════════════════════════════════════════════
// NEW CAMERA / MEMORY LOGIC
// ═══════════════════════════════════════════════
let snapStream = null;
let capturedSnapBlob = null;
let selectedGalleryFile = null;

function openAddMemoryModal() {
  document.getElementById('memoryModal').classList.add('open');
  document.getElementById('snapCaption').value = '';
  switchSnapTab('camera');
}

function closeMemoryModal() {
  document.getElementById('memoryModal').classList.remove('open');
  stopSnapCamera();
}

function switchSnapTab(tab) {
  const btnCam = document.getElementById('tabCamera');
  const btnGal = document.getElementById('tabGallery');
  const viewCam = document.getElementById('viewCamera');
  const viewGal = document.getElementById('viewGallery');

  if (tab === 'camera') {
    btnCam.style.background = '#fff';
    btnCam.style.borderBottomColor = 'var(--pink-main)';
    btnCam.style.color = 'var(--text-main)';
    btnGal.style.background = 'transparent';
    btnGal.style.borderBottomColor = 'transparent';
    btnGal.style.color = 'var(--text-muted)';
    viewCam.style.display = 'flex';
    viewGal.style.display = 'none';
    startSnapCamera();
  } else {
    btnGal.style.background = '#fff';
    btnGal.style.borderBottomColor = 'var(--pink-main)';
    btnGal.style.color = 'var(--text-main)';
    btnCam.style.background = 'transparent';
    btnCam.style.borderBottomColor = 'transparent';
    btnCam.style.color = 'var(--text-muted)';
    viewGal.style.display = 'block';
    viewCam.style.display = 'none';
    stopSnapCamera();
  }
}

function startSnapCamera() {
  const video = document.getElementById('cameraVideo');
  navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } })
    .then(stream => {
      snapStream = stream;
      video.srcObject = stream;
      video.style.display = 'block';
      document.getElementById('cameraCanvas').style.display = 'none';
      document.getElementById('cameraControls').style.display = 'flex';
      document.getElementById('postCaptureControls').style.display = 'none';
      capturedSnapBlob = null;
    })
    .catch(err => {
      console.warn("Camera not available: ", err);
      // If camera blocked/fails, switch to gallery automatically
      switchSnapTab('gallery');
    });
}

function stopSnapCamera() {
  if (snapStream) {
    snapStream.getTracks().forEach(track => track.stop());
    snapStream = null;
  }
}

function captureSnap() {
  const video = document.getElementById('cameraVideo');
  const canvas = document.getElementById('cameraCanvas');
  const context = canvas.getContext('2d');
  
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  context.drawImage(video, 0, 0, canvas.width, canvas.height);
  
  video.style.display = 'none';
  canvas.style.display = 'block';
  document.getElementById('cameraControls').style.display = 'none';
  document.getElementById('postCaptureControls').style.display = 'block';
  
  canvas.toBlob(blob => {
    capturedSnapBlob = blob;
  }, 'image/jpeg', 0.85);
}

function retakeSnap() {
  document.getElementById('cameraVideo').style.display = 'block';
  document.getElementById('cameraCanvas').style.display = 'none';
  document.getElementById('cameraControls').style.display = 'flex';
  document.getElementById('postCaptureControls').style.display = 'none';
  capturedSnapBlob = null;
}

function previewGallerySnap(input) {
  if (input.files && input.files[0]) {
    selectedGalleryFile = input.files[0];
    const reader = new FileReader();
    reader.onload = function(e) {
      document.getElementById('galleryPreview').src = e.target.result;
      document.getElementById('galleryPreviewContainer').style.display = 'block';
      document.getElementById('gallerySelectBtn').style.display = 'none';
    }
    reader.readAsDataURL(selectedGalleryFile);
  }
}

function clearGallerySelection() {
  selectedGalleryFile = null;
  document.getElementById('galleryInput').value = '';
  document.getElementById('galleryPreviewContainer').style.display = 'none';
  document.getElementById('gallerySelectBtn').style.display = 'block';
}

function uploadSnapMemory() {
  const caption = document.getElementById('snapCaption').value.trim();
  const fd = new FormData();
  fd.append('captions', caption);
  
  const isCamera = document.getElementById('viewCamera').style.display !== 'none';
  
  if (isCamera) {
    if (!capturedSnapBlob) { alert('Please capture a photo first!'); return; }
    fd.append('images', capturedSnapBlob, 'snap.jpg');
  } else {
    if (!selectedGalleryFile) { alert('Please select an image from your device!'); return; }
    fd.append('images', selectedGalleryFile);
  }
  
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  const btn = document.querySelector('#memoryModal .btn-primary');
  const originalText = btn.innerHTML;
  btn.innerHTML = 'Saving... ⏳';
  btn.disabled = true;

  fetch('{% url "dashboard_snap_upload" %}', {
    method: 'POST',
    headers: {
      'X-CSRFToken': csrftoken,
      'X-Requested-With': 'XMLHttpRequest'
    },
    body: fd
  })
  .then(res => res.json())
  .then(data => {
    if (data.status === 'success') {
      location.reload();
    } else {
      alert("Error: " + JSON.stringify(data.errors || data.message || "Unknown error"));
      btn.innerHTML = originalText;
      btn.disabled = false;
    }
  })
  .catch(err => {
    console.error(err);
    alert('Upload failed. Check console.');
    btn.innerHTML = originalText;
    btn.disabled = false;
  });
}
"""

if "function openAddMemoryModal()" not in content:
    content = content.replace('</script>\n</body>', js_logic + '\n</script>\n</body>')

with open('tracker/templates/tracker/dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated dashboard.html")
