with open('tracker/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

import_statement = 'from .utils import send_push_message\n'
if import_statement not in content:
    content = content.replace('from .models import (', import_statement + 'from .models import (')

import_sys = 'import threading\n'
if import_sys not in content:
    content = content.replace('from .utils import send_push_message\n', 'from .utils import send_push_message\nimport threading\n')

helper = '''
def notify_partner_background(partner, title, body, url):
    if not partner: return
    def _send():
        subs = partner.push_subscriptions.all()
        for sub in subs:
            send_push_message(sub, title, body, url)
    threading.Thread(target=_send).start()
'''

if 'def notify_partner_background' not in content:
    content = content.replace('def get_partner(user, couple):', helper + '\n\ndef get_partner(user, couple):')

if 'notify_partner_background' not in content.split('messages.success(request, \'Mood log saved!\')')[0]:
    content = content.replace(
        'messages.success(request, \'Mood log saved!\')',
        'notify_partner_background(get_partner(request.user, get_couple(request.user)), f"{request.user.name or request.user.username} updated their mood!", "Tap to check on them.", "/yourmoodtracker/")\n            messages.success(request, \'Mood log saved!\')'
    )

with open('tracker/views.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('Patched views')
