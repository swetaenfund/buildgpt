from django.urls import path
from chat.views import fetch_group_messages, send_message, whatsapp_webhook

urlpatterns = [
    path('api/fetch_messages/', fetch_group_messages, name="fetch_messages"),
    path('api/send_message/', send_message, name="send_message"),
    path('api/webhook/', whatsapp_webhook, name="webhook"),
    # other paths...
]
