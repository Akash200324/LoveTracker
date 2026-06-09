with open('tracker/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

import re

# Add to dashboard_snap_upload
if 'def dashboard_snap_upload' in content:
    content = content.replace(
        "return JsonResponse({'status': 'success'})",
        "notify_partner_background(get_partner(request.user, couple), f\"{request.user.name or request.user.username} added a memory!\", \"Check out the new memory in the gallery.\", \"/dashboard/#memories\")\n    return JsonResponse({'status': 'success'})"
    )

with open('tracker/views.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("Added push trigger to dashboard_snap_upload")
