"""
DjangoEmail URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from mainApp.views import EmailAPI
from django.urls import path
import logging

logger = logging.getLogger('notification')

def log_request_with_correlation_id(view):
    """
    Decorator to log requests with Correlation ID at the URL level.
    """
    def wrapper(request, *args, **kwargs):
        correlation_id = getattr(request, 'correlation_id', 'N/A')
        logger.info(f'Request received: {request.method} {request.path}',
                    extra={'correlation_id': correlation_id})
        return view(request, *args, **kwargs)
    return wrapper

urlpatterns = [
    path('admin/', admin.site.urls),
    path('send-email', log_request_with_correlation_id(EmailAPI.as_view()), name='send-email'),
]
"""
ex get request: GET /send-email?subject=Meeting&text=The%20meeting%20is%20on%202024-12-20%209:00AM&recipient_list=ndemssie762@gmail.com

HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "msg": "Email scheduled to be sent at 2024-12-20 08:50:00."
}
"""
