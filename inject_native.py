with open('tracker/templates/tracker/dashboard.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

start_idx = -1
end_idx = -1

for i, line in enumerate(lines):
    if '<!-- Add Memory Modal -->' in line:
        start_idx = i
    if start_idx != -1 and i > start_idx and '<!-- Snap Popup Modal -->' in line:
        end_idx = i - 1
        break

if start_idx != -1 and end_idx != -1:
    new_modal_html = """<!-- Add Memory Modal -->
<div class="modal-overlay" id="memoryModal" style="z-index: 1000;">
  <div class="modal" style="padding: 0; overflow: hidden; display: flex; flex-direction: column; max-width: 400px; border-radius: 16px; background: rgba(255,255,255,0.95); backdrop-filter: blur(10px);">
    <!-- Header -->
    <div style="padding: 15px; border-bottom: 1px solid rgba(0,0,0,0.05); display: flex; justify-content: space-between; align-items: center;">
      <h3 style="margin: 0; font-family: 'Playfair Display', serif; font-size: 1.3rem; color: var(--charcoal);">📸 New Snap</h3>
      <button onclick="closeMemoryModal()" style="background: none; border: none; font-size: 1.2rem; cursor: pointer; color: var(--text-muted);">✕</button>
    </div>
    
    <!-- Action Buttons -->
    <div id="viewSelection" style="padding: 30px 20px; display: flex; flex-direction: column; gap: 15px; text-align: center;">
      <button onclick="document.getElementById('nativeCameraInput').click()" style="padding: 18px 20px; border-radius: 12px; background: var(--pink-main); border: none; color: white; width: 100%; cursor: pointer; font-weight: bold; font-size: 1.1rem; box-shadow: 0 4px 15px rgba(255,107,152,0.3); transition: 0.2s;">
        📷 Take Photo
      </button>
      <button onclick="document.getElementById('galleryInput').click()" style="padding: 18px 20px; border-radius: 12px; background: rgba(255,107,152,0.1); border: 2px dashed var(--pink-main); color: var(--pink-main); width: 100%; cursor: pointer; font-weight: bold; font-size: 1.1rem; transition: 0.2s;">
        🖼 Choose from Gallery
      </button>
      
      <!-- Hidden Native Inputs -->
      <input type="file" id="nativeCameraInput" accept="image/*" capture="environment" style="display: none;" onchange="previewNativeSnap(this)" />
      <input type="file" id="galleryInput" accept="image/*" style="display: none;" onchange="previewNativeSnap(this)" />
    </div>

    <!-- Preview View -->
    <div id="viewPreview" style="display: none; padding: 20px; text-align: center; flex-direction: column; gap: 15px;">
      <div style="position: relative;">
        <img id="nativePreviewImg" style="width: 100%; max-height: 300px; object-fit: contain; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);" />
        <button onclick="clearNativeSelection()" style="position: absolute; top: 10px; right: 10px; background: rgba(0,0,0,0.5); color: white; border: none; border-radius: 50%; width: 30px; height: 30px; cursor: pointer;">✕</button>
      </div>
      <textarea id="snapCaption" placeholder="Add a caption..." style="width: 100%; padding: 14px; border-radius: 12px; border: 1px solid rgba(0,0,0,0.1); outline: none; font-family: inherit; resize: none; background: rgba(0,0,0,0.02); color: var(--text-main);" rows="2"></textarea>
      <button onclick="uploadNativeSnap()" class="btn btn-primary" style="width: 100%; justify-content: center; padding: 14px; border-radius: 12px; font-size: 1.1rem; box-shadow: 0 4px 15px rgba(255,107,152,0.3);">Save Memory ✨</button>
    </div>
  </div>
</div>
"""
    lines[start_idx:end_idx+1] = [new_modal_html + "\n\n"]
    
    new_js = """
// ═══════════════════════════════════════════════
// NATIVE CAMERA MODAL JS
// ═══════════════════════════════════════════════
let selectedFile = null;

function openSnapModal(src, el) {
    if (src) return; 
}

function openMemoryModal() {
    document.getElementById('memoryModal').classList.add('open');
    clearNativeSelection();
}

function closeMemoryModal() {
    document.getElementById('memoryModal').classList.remove('open');
    clearNativeSelection();
}

function previewNativeSnap(input) {
    if (input.files && input.files[0]) {
        selectedFile = input.files[0];
        const reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById('nativePreviewImg').src = e.target.result;
            document.getElementById('viewSelection').style.display = 'none';
            document.getElementById('viewPreview').style.display = 'flex';
        }
        reader.readAsDataURL(selectedFile);
    }
}

function clearNativeSelection() {
    selectedFile = null;
    document.getElementById('nativeCameraInput').value = '';
    document.getElementById('galleryInput').value = '';
    document.getElementById('viewSelection').style.display = 'flex';
    document.getElementById('viewPreview').style.display = 'none';
}

function uploadNativeSnap() {
    if (!selectedFile) {
        alert("Please select a photo first.");
        return;
    }
    
    const caption = document.getElementById('snapCaption').value.trim();
    
    const fd = new FormData();
    fd.append('title', caption);
    
    const now = new Date();
    const yyyy = now.getFullYear();
    const mm = String(now.getMonth() + 1).padStart(2, '0');
    const dd = String(now.getDate()).padStart(2, '0');
    fd.append('date', `${yyyy}-${mm}-${dd}`);
    
    fd.append('images', selectedFile);
    fd.append('captions', caption);

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const btn = document.querySelector('button[onclick="uploadNativeSnap()"]');
    const origText = btn.innerHTML;
    btn.innerHTML = 'Saving... ⏳';
    btn.disabled = true;

    fetch('/dashboard/snap/upload/', {
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
            alert("Error saving memory.");
            btn.innerHTML = origText;
            btn.disabled = false;
        }
    })
    .catch(err => {
        console.error(err);
        alert('Upload failed. Check console.');
        btn.innerHTML = origText;
        btn.disabled = false;
    });
}
"""

    # find the LAST </script> tag
    last_script_idx = -1
    for i in range(len(lines)-1, -1, -1):
        if '</script>' in lines[i]:
            last_script_idx = i
            break
            
    if last_script_idx != -1:
        lines.insert(last_script_idx, new_js + "\n")
        with open('tracker/templates/tracker/dashboard.html', 'w', encoding='utf-8') as f:
            f.writelines(lines)
        print("Success")
    else:
        print("Could not find </script>")
else:
    print("Could not find modal HTML bounds")
