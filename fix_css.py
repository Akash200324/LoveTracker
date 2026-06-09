with open('tracker/templates/tracker/dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix CSS variables
content = content.replace('var(--pink-main)', '#ff4d6d')
content = content.replace('var(--charcoal)', '#2d3436')
content = content.replace('var(--text-muted)', '#636e72')
content = content.replace('var(--text-main)', '#2d3436')

# Fix hidden inputs
content = content.replace('style="display: none;" onchange="previewNativeSnap(this)"', 'style="opacity:0; position:absolute; width:0; height:0; z-index:-1;" onchange="previewNativeSnap(this)"')

with open('tracker/templates/tracker/dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('Fixed CSS and visibility')
