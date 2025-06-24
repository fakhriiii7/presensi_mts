# 🚀 Deployment Guide - MTs Peradaban Insani

## Overview
Panduan lengkap untuk mendeploy aplikasi Django MTs Peradaban Insani ke PythonAnywhere.com

## 📋 Quick Start

### 1. Generate Secret Key
```bash
python generate_secret_key.py
```

### 2. Setup Project
```bash
python pythonanywhere_setup.py
```

### 3. Follow PythonAnywhere Guide
Lihat file `PYTHONANYWHERE_GUIDE.md` untuk langkah detail

## 🔧 Files yang Diperlukan

### Core Files
- `presensi_mts/settings.py` - Konfigurasi Django
- `presensi_mts/wsgi.py` - WSGI configuration
- `requirements.txt` - Python dependencies
- `manage.py` - Django management

### Deployment Files
- `pythonanywhere_setup.py` - Setup script
- `pythonanywhere_wsgi.py` - WSGI untuk PythonAnywhere
- `generate_secret_key.py` - Generate secret key
- `PYTHONANYWHERE_GUIDE.md` - Panduan lengkap

### Mobile Responsive Files
- `static/css/mobile-responsive.css` - Mobile styles
- `web/partials/mobile-nav.html` - Mobile navigation
- `MOBILE_RESPONSIVE_README.md` - Mobile documentation

## 🚨 Common Issues & Solutions

### Issue 1: ModuleNotFoundError
**Error**: `ModuleNotFoundError: No module named 'django'`

**Solution**:
```bash
# Install dependencies
pip install -r requirements.txt

# Check Python version
python --version

# Make sure you're in the right directory
pwd
ls -la
```

### Issue 2: Static Files Not Loading
**Error**: CSS/JS files not found (404 errors)

**Solution**:
```bash
# Collect static files
python manage.py collectstatic --noinput

# Check static files directory
ls -la staticfiles/

# Verify static files configuration in settings.py
```

### Issue 3: Database Errors
**Error**: `no such table` or database connection issues

**Solution**:
```bash
# Run migrations
python manage.py migrate

# Check database
python manage.py dbshell
.tables
.quit

# If still having issues, reset database
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### Issue 4: Permission Denied
**Error**: `Permission denied` when running commands

**Solution**:
```bash
# Check file permissions
ls -la manage.py

# Make executable if needed
chmod +x manage.py

# Use python3 explicitly
python3 manage.py migrate
```

### Issue 5: Import Errors in WSGI
**Error**: Import errors when reloading web app

**Solution**:
1. Check WSGI configuration file
2. Verify project path is correct
3. Make sure all dependencies are installed
4. Check error logs in PythonAnywhere

## 📱 Mobile Responsive Issues

### Static Files Not Loading on Mobile
1. Check browser developer tools
2. Verify static files are collected
3. Check network tab for 404 errors
4. Ensure mobile CSS is included

### Mobile Navigation Not Working
1. Check JavaScript console for errors
2. Verify Alpine.js is loaded
3. Test touch events
4. Check mobile-specific CSS

## 🔒 Security Checklist

### Before Deployment
- [ ] Generate new secret key
- [ ] Set DEBUG=False
- [ ] Configure ALLOWED_HOSTS
- [ ] Set up environment variables
- [ ] Remove sensitive data from code

### After Deployment
- [ ] Test all functionality
- [ ] Check error logs
- [ ] Monitor access logs
- [ ] Test mobile responsive
- [ ] Verify HTTPS (if available)

## 📊 Monitoring & Maintenance

### Regular Checks
1. **Error Logs**: Check PythonAnywhere error logs weekly
2. **Access Logs**: Monitor traffic patterns
3. **Database**: Check database size and performance
4. **Static Files**: Ensure all files are loading correctly

### Performance Optimization
```bash
# Optimize database
python manage.py dbshell
VACUUM;
ANALYZE;
.quit

# Clear cache (if using)
python manage.py clearcache

# Check static files
python manage.py collectstatic --noinput --clear
```

## 🆘 Emergency Procedures

### Website Down
1. Check PythonAnywhere status page
2. Reload web app
3. Check error logs
4. Restart if necessary

### Database Issues
1. Backup current database
2. Check disk space
3. Run database maintenance
4. Consider database reset if needed

### Static Files Issues
1. Recollect static files
2. Check file permissions
3. Verify static files configuration
4. Clear browser cache

## 📞 Support Resources

### PythonAnywhere Support
- [PythonAnywhere Help](https://help.pythonanywhere.com/)
- [Django on PythonAnywhere](https://help.pythonanywhere.com/pages/Django/)
- [PythonAnywhere Community](https://www.pythonanywhere.com/community/)

### Django Documentation
- [Django Deployment](https://docs.djangoproject.com/en/5.2/howto/deployment/)
- [Django Security](https://docs.djangoproject.com/en/5.2/topics/security/)

### Mobile Responsive
- [Mobile Responsive Guide](MOBILE_RESPONSIVE_README.md)
- [CSS Mobile Best Practices](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Responsive/Mobile_first)

## 🎯 Best Practices

### Development
- Test locally before deploying
- Use version control (Git)
- Keep dependencies updated
- Document changes

### Production
- Never use DEBUG=True in production
- Use environment variables for secrets
- Monitor logs regularly
- Backup data frequently

### Security
- Update dependencies regularly
- Use strong secret keys
- Monitor access patterns
- Implement proper authentication

## 📈 Performance Tips

### Static Files
- Use WhiteNoise for static file serving
- Compress static files
- Use CDN if possible
- Cache static files

### Database
- Use database indexes
- Optimize queries
- Regular maintenance
- Monitor database size

### Code Optimization
- Use Django debug toolbar locally
- Profile slow queries
- Optimize template rendering
- Use caching where appropriate

---

**Last Updated**: December 2024
**Version**: 1.0.0
**Maintainer**: MTs Peradaban Insani Development Team 