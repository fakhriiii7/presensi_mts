from django.contrib import admin
from django.urls import path, include
from presensi.views import CustomLoginView, home
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='/login/'), name='logout'),
    path('', include('presensi.urls')),
]
