from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('logs/', include('log_receiver.urls')),  # Include the URLs from the log_receiver app
]
