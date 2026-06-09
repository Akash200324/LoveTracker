import json
from django.conf import settings
from pywebpush import webpush, WebPushException

def send_push_message(subscription, title, body, url="/dashboard/"):
    """
    Sends a Web Push Notification to a given PushSubscription.
    subscription: PushSubscription model instance
    """
    try:
        payload = json.dumps({
            "title": title,
            "body": body,
            "url": url,
            "icon": "/static/images/pwa_icon.png"
        })
        
        sub_data = {
            "endpoint": subscription.endpoint,
            "keys": {
                "auth": subscription.auth,
                "p256dh": subscription.p256dh
            }
        }
        
        webpush(
            subscription_info=sub_data,
            data=payload,
            vapid_private_key=settings.VAPID_PRIVATE_KEY,
            vapid_claims={
                "sub": settings.VAPID_ADMIN_EMAIL,
            }
        )
        return True
    except WebPushException as ex:
        print("Web Push Error:", repr(ex))
        # If the subscription is expired or invalid, Mozilla/Google returns 410 or 404
        if ex.response and ex.response.status_code in [404, 410]:
            subscription.delete()
        return False
    except Exception as e:
        print("Push Notification Failed:", str(e))
        return False
