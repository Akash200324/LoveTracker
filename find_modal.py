with open('tracker/templates/tracker/dashboard.html', 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        if 'id="snapModal"' in line:
            print(f"{i}: {line.strip()}")
