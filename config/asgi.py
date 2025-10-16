import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter
# from channels.auth import AuthMiddlewareStack
# from django.urls import re_path
# from channels.routing import URLRouter

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    # "websocket": AuthMiddlewareStack(
    #     URLRouter([
    #         # re_path(r"^ws/somepath/$", YourConsumer.as_asgi()),
    #     ])
    # ),
})
