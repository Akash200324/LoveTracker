with open('tracker/templates/tracker/dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update CSS
import re

css_old = r"""  \.memory-track-wrapper {
    overflow: hidden;
    border-radius: 20px;
    position: relative;
    cursor: grab;
  }
  \.memory-track-wrapper:active { cursor: grabbing; }

  \.memory-track {
    display: flex;
    gap: 18px;
    animation: scrollMemory 30s linear infinite;
    width: max-content;
    padding-bottom: 8px;
  }
  @keyframes scrollMemory {
    0% { transform: translateX\(0\); }
    100% { transform: translateX\(-50%\); }
  }"""

css_new = """  .memory-track-wrapper {
    overflow-x: auto;
    overflow-y: hidden;
    border-radius: 20px;
    position: relative;
    scroll-behavior: auto;
    -webkit-overflow-scrolling: touch; /* smooth momentum scrolling on iOS */
    scrollbar-width: none; /* Firefox */
  }
  .memory-track-wrapper::-webkit-scrollbar {
    display: none; /* Safari and Chrome */
  }

  .memory-track {
    display: flex;
    gap: 18px;
    width: max-content;
    padding-bottom: 8px;
  }"""

content = re.sub(css_old, css_new, content)

# 2. Add Auto-scroll JS
js_scroll = """
// ═══════════════════════════════════════════════
// AUTO SCROLL MEMORIES
// ═══════════════════════════════════════════════
let scrollReq;
let isHovering = false;

function startAutoScrollMemories() {
  const wrapper = document.querySelector('.memory-track-wrapper');
  if (!wrapper) return;
  
  wrapper.addEventListener('mouseenter', () => isHovering = true);
  wrapper.addEventListener('mouseleave', () => isHovering = false);
  wrapper.addEventListener('touchstart', () => isHovering = true);
  wrapper.addEventListener('touchend', () => {
      setTimeout(() => isHovering = false, 1000);
  });

  function step() {
    if (!isHovering) {
        wrapper.scrollLeft += 1.5; // 1x speed
        if (wrapper.scrollLeft >= (wrapper.scrollWidth - wrapper.clientWidth)) {
            // If reached the end, reset to start or reverse. Let's reset.
            // wrapper.scrollLeft = 0; 
            // Or we just stop. Let's reset for infinite loop effect:
            wrapper.scrollLeft = 0;
        }
    }
    scrollReq = requestAnimationFrame(step);
  }
  
  cancelAnimationFrame(scrollReq);
  scrollReq = requestAnimationFrame(step);
}

// Hook it into renderMemories
const origRenderMemories = renderMemories;
renderMemories = function() {
    origRenderMemories();
    startAutoScrollMemories();
}
"""

if "startAutoScrollMemories()" not in content:
    content = content.replace('// ═══════════════════════════════════════════════\n// NEW CAMERA', js_scroll + '\n// ═══════════════════════════════════════════════\n// NEW CAMERA')

# 3. Add alert to camera catch block
content = content.replace(
    'console.warn("Camera not available: ", err);',
    'console.warn("Camera not available: ", err); alert("Camera access denied or device doesn\'t support it. Note: Camera requires HTTPS or localhost!");'
)

with open('tracker/templates/tracker/dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated dashboard.html successfully.")
