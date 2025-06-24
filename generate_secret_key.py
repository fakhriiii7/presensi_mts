#!/usr/bin/env python3
"""
Generate Django Secret Key

This script generates a secure secret key for Django production use.
Run this script to generate a new secret key for your PythonAnywhere deployment.
"""

import secrets
import string

def generate_secret_key(length=50):
    """Generate a secure secret key"""
    alphabet = string.ascii_letters + string.digits + string.punctuation
    # Remove characters that might cause issues in environment variables
    alphabet = alphabet.replace('"', '').replace("'", '').replace('\\', '')
    
    secret_key = ''.join(secrets.choice(alphabet) for _ in range(length))
    return secret_key

def main():
    """Main function"""
    print("🔐 Django Secret Key Generator")
    print("=" * 40)
    
    # Generate secret key
    secret_key = generate_secret_key()
    
    print(f"\n✅ Generated Secret Key:")
    print(f"SECRET_KEY={secret_key}")
    
    print(f"\n📝 Copy this to your .env file or PythonAnywhere environment variables:")
    print(f"SECRET_KEY={secret_key}")
    
    print(f"\n⚠️  Important:")
    print(f"- Keep this secret key secure")
    print(f"- Don't share it publicly")
    print(f"- Use different keys for different environments")
    
    # Ask if user wants to save to file
    save_to_file = input(f"\n💾 Save to .env file? (y/n): ").lower().strip()
    
    if save_to_file == 'y':
        try:
            with open('.env', 'w') as f:
                f.write(f"SECRET_KEY={secret_key}\n")
                f.write("DEBUG=False\n")
                f.write("PYTHONANYWHERE_DOMAIN=yourusername.pythonanywhere.com\n")
            print(f"✅ Secret key saved to .env file")
        except Exception as e:
            print(f"❌ Error saving to file: {e}")
    
    print(f"\n🎉 Done! Use this secret key in your PythonAnywhere deployment.")

if __name__ == "__main__":
    main() 