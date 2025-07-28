from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('demo/rest/api/', include('demo_rest_api.urls')),
]
