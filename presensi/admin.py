from django.contrib import admin
from .models import AbstractUser, Kelas, MataPelajaran, Presensi
from django import forms

@admin.register(AbstractUser)
class AbstractUserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'role', 'user')
    list_filter = ('role',)
    search_fields = ('first_name', 'last_name', 'user__username')

class KelasAdminForm(forms.ModelForm):
    class Meta:
        model = Kelas
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Batasi pilihan siswa hanya untuk role='siswa'
        self.fields['siswa'].queryset = AbstractUser.objects.filter(role='siswa')
        # Opsional: Batasi wali kelas hanya untuk role selain siswa
        self.fields['wali_kelas'].queryset = AbstractUser.objects.exclude(role='siswa')

@admin.register(Kelas)
class KelasAdmin(admin.ModelAdmin):
    form = KelasAdminForm
    list_display = ('nama', 'wali_kelas')
    search_fields = ('nama',)
    filter_horizontal = ('siswa',)

@admin.register(MataPelajaran)
class MataPelajaranAdmin(admin.ModelAdmin):
    list_display = ('nama', 'guru')
    search_fields = ('nama', 'guru__first_name')
    filter_horizontal = ('kelas',)

@admin.register(Presensi)
class PresensiAdmin(admin.ModelAdmin):
    list_display = ('user', 'tanggal', 'jam_masuk', 'jam_pulang', 'status', 'mata_pelajaran', 'kelas', 'guru')
    list_filter = ('status', 'tanggal', 'mata_pelajaran', 'kelas')
    search_fields = ('user__first_name', 'user__last_name', 'mata_pelajaran__nama', 'kelas__nama')
    date_hierarchy = 'tanggal'
