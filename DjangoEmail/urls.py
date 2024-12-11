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
from django.urls import path
from mainApp.views import EmailAPI
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('send-email', EmailAPI.as_view(), name='send-email'),
]
#ex get request  http://127.0.0.1:8000/send-email?subject=Meeting%20Reminder&text=The%20meeting%20is%20set%20for%208:46PM&recipient_list=ndemssie762@gmail.com,nathandemssie@gmail.com"""
"""
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "msg": "Email scheduled to be sent at 2024-12-11 20:36:00."
}
"""
