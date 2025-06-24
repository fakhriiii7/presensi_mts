# 🚀 Panduan Deploy ke PythonAnywhere

## Overview
Panduan lengkap untuk mendeploy aplikasi MTs Peradaban Insani ke PythonAnywhere.com

## 📋 Prerequisites
- Akun PythonAnywhere (gratis atau berbayar)
- File project Django yang sudah siap
- Koneksi internet stabil

## 🔧 Langkah-langkah Deployment

### 1. Upload Project ke PythonAnywhere

#### A. Menggunakan Git (Recommended)
```bash
# Di PythonAnywhere Bash Console
cd ~
git clone https://github.com/yourusername/presensi_mts.git
cd presensi_mts
```

#### B. Menggunakan File Upload
1. Buka **Files** tab di PythonAnywhere
2. Upload semua file project ke folder `/home/yourusername/`
3. Extract file jika dalam format zip

### 2. Setup Environment

#### A. Install Dependencies
```bash
# Di PythonAnywhere Bash Console
cd ~/presensi_mts
pip install -r requirements.txt
```

#### B. Setup Environment Variables
```bash
# Buat file .env
nano .env
```

Isi dengan:
```env
SECRET_KEY=your-secret-key-here
DEBUG=False
PYTHONANYWHERE_DOMAIN=yourusername.pythonanywhere.com
```

#### C. Collect Static Files
```bash
python manage.py collectstatic --noinput
```

#### D. Run Migrations
```bash
python manage.py migrate
```

#### E. Create Superuser
```bash
python manage.py createsuperuser
```

### 3. Konfigurasi Web App

#### A. Buat Web App Baru
1. Buka **Web** tab di PythonAnywhere
2. Klik **Add a new web app**
3. Pilih **Manual configuration**
4. Pilih **Python 3.9** atau lebih tinggi

#### B. Set Source Code
- **Source code**: `/home/yourusername/presensi_mts`
- **Working directory**: `/home/yourusername/presensi_mts`

#### C. Set WSGI Configuration
1. Klik link **WSGI configuration file**
2. Ganti isi file dengan:

```python
import os
import sys

# Add your project directory to the Python path
path = '/home/yourusername/presensi_mts'
if path not in sys.path:
    sys.path.append(path)

# Set environment variables
os.environ['DJANGO_SETTINGS_MODULE'] = 'presensi_mts.settings'
os.environ['SECRET_KEY'] = 'your-secret-key-here'
os.environ['DEBUG'] = 'False'
os.environ['PYTHONANYWHERE_DOMAIN'] = 'yourusername.pythonanywhere.com'

# Import Django and get WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

#### D. Set Static Files
1. Kembali ke **Web** tab
2. Scroll ke **Static files**
3. Tambahkan:
   - **URL**: `/static/`
   - **Directory**: `/home/yourusername/presensi_mts/staticfiles`

### 4. Reload Web App
1. Klik **Reload** button di **Web** tab
2. Tunggu beberapa detik
3. Akses website Anda di `yourusername.pythonanywhere.com`

## 🔍 Troubleshooting

### Error 1: ModuleNotFoundError
**Gejala**: `ModuleNotFoundError: No module named 'django'`

**Solusi**:
```bash
# Install dependencies
pip install -r requirements.txt

# Atau install manual
pip install Django==5.2.1
```

### Error 2: Static Files Not Found
**Gejala**: CSS/JS tidak dimuat

**Solusi**:
```bash
# Collect static files
python manage.py collectstatic --noinput

# Pastikan konfigurasi static files benar
```

### Error 3: Database Error
**Gejala**: `no such table` atau database error

**Solusi**:
```bash
# Run migrations
python manage.py migrate

# Jika masih error, reset database
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### Error 4: Permission Denied
**Gejala**: `Permission denied` saat menjalankan command

**Solusi**:
```bash
# Pastikan file executable
chmod +x manage.py

# Atau gunakan python3
python3 manage.py migrate
```

### Error 5: Import Error
**Gejala**: `ImportError` saat reload web app

**Solusi**:
1. Periksa WSGI configuration
2. Pastikan path benar
3. Restart web app

## 📱 Mobile Responsive Setup

### Pastikan Static Files Ter-load
1. Buka browser developer tools
2. Periksa **Network** tab
3. Pastikan file CSS/JS dimuat dengan benar

### Test Mobile Responsive
1. Buka website di mobile device
2. Atau gunakan browser dev tools mobile view
3. Test semua fitur mobile

## 🔒 Security Settings

### Production Settings
```python
# Di settings.py
DEBUG = False
ALLOWED_HOSTS = ['yourusername.pythonanywhere.com']

# Security headers
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
```

### Environment Variables
```bash
# Jangan hardcode secret key
SECRET_KEY=your-actual-secret-key
DEBUG=False
```

## 📊 Monitoring

### Error Logs
1. Buka **Web** tab
2. Klik **Error log**
3. Periksa error messages

### Access Logs
1. Buka **Web** tab
2. Klik **Access log**
3. Monitor traffic

## 🚀 Performance Optimization

### Static Files
```bash
# Compress static files
python manage.py collectstatic --noinput
```

### Database
```bash
# Optimize database
python manage.py dbshell
VACUUM;
```

### Caching
```python
# Add caching in settings.py
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
```

## 📞 Support

### PythonAnywhere Support
- [PythonAnywhere Help](https://help.pythonanywhere.com/)
- [Django on PythonAnywhere](https://help.pythonanywhere.com/pages/Django/)

### Common Issues
1. **Memory Limit**: Upgrade ke akun berbayar
2. **CPU Limit**: Optimize code atau upgrade
3. **Storage Limit**: Hapus file tidak perlu

## ✅ Checklist Deployment

- [ ] Upload project ke PythonAnywhere
- [ ] Install dependencies
- [ ] Setup environment variables
- [ ] Collect static files
- [ ] Run migrations
- [ ] Create superuser
- [ ] Konfigurasi web app
- [ ] Set WSGI configuration
- [ ] Set static files
- [ ] Reload web app
- [ ] Test website
- [ ] Test mobile responsive
- [ ] Setup security
- [ ] Monitor logs

## 🎯 Best Practices

### Development
- Test di local sebelum deploy
- Gunakan version control (Git)
- Backup database secara regular

### Production
- Jangan gunakan DEBUG=True
- Gunakan environment variables
- Monitor error logs
- Backup secara berkala

### Security
- Update dependencies regular
- Gunakan strong secret key
- Monitor access logs
- Setup HTTPS jika memungkinkan

---

**Last Updated**: December 2024
**Version**: 1.0.0
**Compatibility**: PythonAnywhere Free/Paid Plans 