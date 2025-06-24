#!/usr/bin/env python3
"""
PythonAnywhere Setup Script for MTs Peradaban Insani

This script helps configure your Django project for PythonAnywhere hosting.
Run this script after uploading your project to PythonAnywhere.
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during {description}:")
        print(f"   Command: {command}")
        print(f"   Error: {e.stderr}")
        return None

def setup_pythonanywhere():
    """Main setup function"""
    print("🚀 PythonAnywhere Setup for MTs Peradaban Insani")
    print("=" * 50)
    
    # Get current directory
    current_dir = Path.cwd()
    print(f"📁 Current directory: {current_dir}")
    
    # Check if we're in the right directory
    if not (current_dir / 'manage.py').exists():
        print("❌ Error: manage.py not found. Please run this script from your project root directory.")
        return False
    
    # 1. Install requirements
    print("\n📦 Installing Python requirements...")
    result = run_command("pip install -r requirements.txt", "Installing requirements")
    if not result:
        return False
    
    # 2. Collect static files
    print("\n📁 Collecting static files...")
    result = run_command("python manage.py collectstatic --noinput", "Collecting static files")
    if not result:
        return False
    
    # 3. Run migrations
    print("\n🗄️ Running database migrations...")
    result = run_command("python manage.py migrate", "Running migrations")
    if not result:
        return False
    
    # 4. Create superuser (optional)
    print("\n👤 Creating superuser (optional)...")
    create_superuser = input("Do you want to create a superuser? (y/n): ").lower().strip()
    if create_superuser == 'y':
        run_command("python manage.py createsuperuser", "Creating superuser")
    
    # 5. Check configuration
    print("\n🔍 Checking configuration...")
    result = run_command("python manage.py check --deploy", "Checking deployment configuration")
    if not result:
        print("⚠️ Warning: Some deployment issues found. Check the output above.")
    
    print("\n✅ Setup completed!")
    print("\n📋 Next steps:")
    print("1. Go to your PythonAnywhere dashboard")
    print("2. Navigate to 'Web' tab")
    print("3. Add a new web app")
    print("4. Choose 'Manual configuration'")
    print("5. Choose Python 3.9 or higher")
    print("6. Set your source code directory to your project folder")
    print("7. Set your WSGI configuration file to: presensi_mts/wsgi.py")
    print("8. Set your static files URL to: /static/")
    print("9. Set your static files directory to: /home/yourusername/yourproject/staticfiles")
    print("10. Reload your web app")
    
    return True

def create_env_file():
    """Create a .env file template"""
    env_content = """# Environment variables for PythonAnywhere
# Replace these values with your actual settings

# Django settings
SECRET_KEY=your-secret-key-here
DEBUG=False
PYTHONANYWHERE_DOMAIN=yourusername.pythonanywhere.com

# Database settings (if using external database)
# DATABASE_URL=your-database-url-here

# Email settings (if needed)
# EMAIL_HOST=smtp.gmail.com
# EMAIL_PORT=587
# EMAIL_USE_TLS=True
# EMAIL_HOST_USER=your-email@gmail.com
# EMAIL_HOST_PASSWORD=your-app-password
"""
    
    env_file = Path('.env')
    if not env_file.exists():
        with open(env_file, 'w') as f:
            f.write(env_content)
        print("📝 Created .env file template. Please update it with your actual values.")
    else:
        print("📝 .env file already exists.")

if __name__ == "__main__":
    try:
        # Create .env file template
        create_env_file()
        
        # Run setup
        success = setup_pythonanywhere()
        
        if success:
            print("\n🎉 Setup completed successfully!")
            print("Your Django project is now ready for PythonAnywhere hosting.")
        else:
            print("\n❌ Setup failed. Please check the errors above and try again.")
            
    except KeyboardInterrupt:
        print("\n\n⏹️ Setup interrupted by user.")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1) 