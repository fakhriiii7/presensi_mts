from django.db import models
from django.contrib.auth.models import User
from datetime import date, datetime

class AbstractUser(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('staff', 'Staff'),
        ('guru', 'Guru'),
        ('siswa', 'Siswa'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='abstract_user')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='employee')
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Kelas(models.Model):
    nama = models.CharField(max_length=50)
    wali_kelas = models.ForeignKey(AbstractUser, on_delete=models.CASCADE, related_name='wali_kelas')
    siswa = models.ManyToManyField(AbstractUser, related_name='kelas_siswa')

    def __str__(self):
        return self.nama

        
class MataPelajaran(models.Model):
    nama = models.CharField(max_length=100)
    guru = models.ForeignKey(AbstractUser, on_delete=models.CASCADE, related_name='mapel_guru')
    kelas = models.ManyToManyField(Kelas, related_name='mata_pelajaran')
    
    def __str__(self):
        return self.nama

class Presensi(models.Model):
    STATUS_CHOICES = [
        ('hadir', 'Hadir'),
        ('izin', 'Izin'),
        ('sakit', 'Sakit'),
        ('alpha', 'Alpha'),
    ]
    
    user = models.ForeignKey(AbstractUser, on_delete=models.CASCADE, related_name='presensi')
    tanggal = models.DateField(default=date.today())
    jam_masuk = models.TimeField(default=datetime.now().time())
    jam_pulang = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='hadir')
    keterangan = models.TextField(blank=True, null=True)
    mata_pelajaran = models.ForeignKey(MataPelajaran, on_delete=models.CASCADE, related_name='presensi', blank=True, null=True)
    kelas = models.ForeignKey(Kelas, on_delete=models.CASCADE, related_name='presensi', blank=True, null=True)
    guru = models.ForeignKey(AbstractUser, on_delete=models.CASCADE, blank=True, null=True, related_name='presensi_guru')

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.tanggal} - {self.mata_pelajaran}" 
