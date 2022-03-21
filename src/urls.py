from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('student/', include("student.urls")), 
    path('teacher/', include('teacher.urls')), 
    path('quiz/', include('quiz.urls')),
]


# To serve the media files
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
