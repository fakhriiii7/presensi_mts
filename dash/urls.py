"""
URL configuration for dash project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf import settings
from presensi import views
from django.conf.urls.static import static

urlpatterns = (
    [
        path('admin/', admin.site.urls),
        path('', views.home, name='home'),
        path('absensi', views.home, name='absensi_guru'),
        path('rekap/guru', views.rekap_presensi, name='rekap_presensi'),
        path('presensi/guru', views.presensi_guru, name='presensi_guru'),
        path('get-siswa-kelas/', views.get_siswa_kelas, name='get_siswa_kelas'),
        path('submit-presensi/', views.submit_presensi, name='submit_presensi'),
        path('presensi/guru', views.presensi_guru, name='presensi_guru'),
        path('export-presensi/', views.export_presensi, name='export_presensi'),
        path('get-presensi-period/', views.get_presensi_period, name='get_presensi_period'),
        path('login/', views.login, name='login'),
        path('logout/', views.logout, name='logout'),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
