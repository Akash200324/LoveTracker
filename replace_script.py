import sys

with open('tracker/templates/tracker/dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_func = """function uploadNativeSnap() {
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
    }).catch(err => {
        console.error(err);
        alert("Network error.");
        btn.innerHTML = origText;
        btn.disabled = false;
    });
}"""

new_func = """function compressImage(file, maxWidth, maxHeight, quality, callback) {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = function(event) {
        const img = new Image();
        img.src = event.target.result;
        img.onload = function() {
            let width = img.width;
            let height = img.height;
            if (width > height) {
                if (width > maxWidth) {
                    height *= maxWidth / width;
                    width = maxWidth;
                }
            } else {
                if (height > maxHeight) {
                    width *= maxHeight / height;
                    height = maxHeight;
                }
            }
            const canvas = document.createElement('canvas');
            canvas.width = width;
            canvas.height = height;
            const ctx = canvas.getContext('2d');
            ctx.drawImage(img, 0, 0, width, height);
            canvas.toBlob(function(blob) {
                callback(blob);
            }, 'image/jpeg', quality);
        };
    };
}

function uploadNativeSnap() {
    if (!selectedFile) {
        alert("Please select a photo first.");
        return;
    }
    
    const caption = document.getElementById('snapCaption').value.trim();
    const btn = document.querySelector('button[onclick="uploadNativeSnap()"]') || document.querySelector('.snap-upload-btn');
    const origText = btn ? btn.innerHTML : 'Save';
    if(btn) {
        btn.innerHTML = 'Optimizing... ⏳';
        btn.disabled = true;
    }

    compressImage(selectedFile, 1200, 1200, 0.8, function(compressedBlob) {
        const fd = new FormData();
        fd.append('title', caption);
        
        const now = new Date();
        const yyyy = now.getFullYear();
        const mm = String(now.getMonth() + 1).padStart(2, '0');
        const dd = String(now.getDate()).padStart(2, '0');
        fd.append('date', `${yyyy}-${mm}-${dd}`);
        
        fd.append('images', compressedBlob, selectedFile.name || 'snap.jpg');
        fd.append('captions', caption);

        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        if(btn) btn.innerHTML = 'Uploading... 🚀';

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
                if(btn) { btn.innerHTML = origText; btn.disabled = false; }
            }
        }).catch(err => {
            console.error(err);
            alert("Network error.");
            if(btn) { btn.innerHTML = origText; btn.disabled = false; }
        });
    });
}"""

if old_func in content:
    content = content.replace(old_func, new_func)
    with open('tracker/templates/tracker/dashboard.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Successfully replaced.")
else:
    print("Did not find old function in dashboard.html. It might be slightly different.")
