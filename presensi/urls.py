from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile_siswa, name='profile_siswa'),
    path('presensi-guru/', views.presensi_guru, name='presensi_guru'),
    path('get-siswa-kelas/', views.get_siswa_kelas, name='get_siswa_kelas'),
    path('submit-presensi/', views.submit_presensi, name='submit_presensi'),
    path('riwayat/', views.riwayat_siswa, name='riwayat_siswa'),
] 