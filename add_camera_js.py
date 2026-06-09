import re

with open('tracker/templates/tracker/dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

camera_js = """
// ═══════════════════════════════════════════════
// NEW CAMERA MODAL JS
// ═══════════════════════════════════════════════
let currentStream = null;
let currentSnapBlob = null;

function openSnapModal(src, el) {
    if (src) {
        // This is for viewing an existing memory, which is already handled somewhere else or we can handle it here
        // If it's the new snap button, src is undefined
        return;
    }
}

function openMemoryModal() {
    document.getElementById('memoryModal').classList.add('open');
    switchSnapTab('camera');
}

function closeMemoryModal() {
    document.getElementById('memoryModal').classList.remove('open');
    stopSnapCamera();
    clearGallerySelection();
}

function switchSnapTab(tab) {
    const tabCam = document.getElementById('tabCamera');
    const tabGal = document.getElementById('tabGallery');
    const viewCam = document.getElementById('viewCamera');
    const viewGal = document.getElementById('viewGallery');

    if (tab === 'camera') {
        tabCam.style.borderBottomColor = 'var(--pink-main)';
        tabCam.style.color = 'var(--text-main)';
        tabGal.style.borderBottomColor = 'transparent';
        tabGal.style.color = 'var(--text-muted)';
        
        viewCam.style.display = 'flex';
        viewGal.style.display = 'none';
        
        startSnapCamera();
    } else {
        tabGal.style.borderBottomColor = 'var(--pink-main)';
        tabGal.style.color = 'var(--text-main)';
        tabCam.style.borderBottomColor = 'transparent';
        tabCam.style.color = 'var(--text-muted)';
        
        viewGal.style.display = 'block';
        viewCam.style.display = 'none';
        
        stopSnapCamera();
    }
}

function startSnapCamera() {
    const video = document.getElementById('cameraVideo');
    const controls = document.getElementById('cameraControls');
    const postControls = document.getElementById('postCaptureControls');
    const canvas = document.getElementById('cameraCanvas');
    
    video.style.display = 'block';
    canvas.style.display = 'none';
    controls.style.display = 'flex';
    postControls.style.display = 'none';
    currentSnapBlob = null;

    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } })
        .then(stream => {
            currentStream = stream;
            video.srcObject = stream;
        })
        .catch(err => {
            console.warn("Camera not available: ", err);
            alert("Camera access denied or device doesn't support it. Note: Camera requires HTTPS or localhost!");
            switchSnapTab('gallery');
        });
    } else {
        alert("Camera API not supported by this browser.");
        switchSnapTab('gallery');
    }
}

function stopSnapCamera() {
    if (currentStream) {
        currentStream.getTracks().forEach(track => track.stop());
        currentStream = null;
    }
}

function captureSnap() {
    const video = document.getElementById('cameraVideo');
    const canvas = document.getElementById('cameraCanvas');
    const controls = document.getElementById('cameraControls');
    const postControls = document.getElementById('postCaptureControls');
    
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext('2d').drawImage(video, 0, 0);
    
    video.style.display = 'none';
    canvas.style.display = 'block';
    controls.style.display = 'none';
    postControls.style.display = 'block';
    
    canvas.toBlob(blob => {
        currentSnapBlob = blob;
    }, 'image/jpeg', 0.85);
    
    stopSnapCamera();
}

function retakeSnap() {
    startSnapCamera();
}

let galleryFile = null;
function previewGallerySnap(input) {
    if (input.files && input.files[0]) {
        galleryFile = input.files[0];
        const reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById('galleryPreview').src = e.target.result;
            document.getElementById('galleryPreviewContainer').style.display = 'block';
            document.getElementById('gallerySelectBtn').style.display = 'none';
        }
        reader.readAsDataURL(galleryFile);
    }
}

function clearGallerySelection() {
    galleryFile = null;
    document.getElementById('galleryInput').value = '';
    document.getElementById('galleryPreviewContainer').style.display = 'none';
    document.getElementById('gallerySelectBtn').style.display = 'block';
}

function uploadSnapMemory() {
    const caption = document.getElementById('snapCaption').value.trim();
    const isCamera = document.getElementById('viewCamera').style.display !== 'none';
    
    const fd = new FormData();
    fd.append('title', caption); // use caption as title
    
    const now = new Date();
    const yyyy = now.getFullYear();
    const mm = String(now.getMonth() + 1).padStart(2, '0');
    const dd = String(now.getDate()).padStart(2, '0');
    fd.append('date', `${yyyy}-${mm}-${dd}`);
    
    if (isCamera && currentSnapBlob) {
        fd.append('images', currentSnapBlob, 'snap.jpg');
        fd.append('captions', caption);
    } else if (!isCamera && galleryFile) {
        fd.append('images', galleryFile);
        fd.append('captions', caption);
    } else {
        alert("Please take a photo or select one from the gallery.");
        return;
    }

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
    const btn = document.querySelector('button[onclick="uploadSnapMemory()"]');
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

if "function startSnapCamera()" not in content:
    content = content.replace('// ═══════════════════════════════════════════════\n// NEW CAMERA MODAL JS\n// ═══════════════════════════════════════════════', '')
    content = content.replace('</script>', camera_js + '\n</script>')
    with open('tracker/templates/tracker/dashboard.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Injected camera JS successfully")
else:
    print("Already exists")
