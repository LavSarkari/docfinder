#!/usr/bin/env python
"""
DoctorFinder deployment script for AlwaysData
Run this script from your local project directory to deploy to AlwaysData
Works on Windows, macOS, and Linux
"""

import os
import sys
import subprocess
import platform
import time

# SSH connection details
SSH_HOST = "ssh-lavsarkari.alwaysdata.net"
SSH_USER = "lavsarkari"
REMOTE_DIR = "/home/lavsarkari/www/doctorfinder"

def run_command(command, shell=True):
    """Run a shell command and print output"""
    print(f"Running: {command}")
    process = subprocess.Popen(
        command, shell=shell, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        universal_newlines=True
    )
    
    # Print output in real-time
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())
    
    return process.poll()

def main():
    """Main deployment function"""
    print("\n===== DoctorFinder Deployment to AlwaysData =====\n")
    print("This script will upload your project to AlwaysData and execute the deployment process.")
    print("")
    
    # Check if SSH is available
    try:
        run_command("ssh -V")
    except Exception as e:
        print("Error: SSH client not found. Please install OpenSSH client.")
        print("On Windows, you can install it from Optional Features or use Git Bash.")
        sys.exit(1)
    
    # Create remote directory
    print("\nCreating remote directory structure...")
    run_command(f'ssh {SSH_USER}@{SSH_HOST} "mkdir -p {REMOTE_DIR}"')
    
    # Determine the best upload method
    use_rsync = True
    try:
        run_command("rsync --version")
    except Exception:
        use_rsync = False
        print("Rsync not found, will use SCP instead (slower but compatible with Windows).")
    
    # Upload files
    print("\nUploading project files...")
    
    if use_rsync:
        # Using rsync (faster, preserves permissions)
        exclude_args = "--exclude='.git/' --exclude='venv/' --exclude='.venv/' --exclude='__pycache__/' " \
                       "--exclude='*.pyc' --exclude='db.sqlite3' --exclude='.env' --exclude='media/uploads/'"
        
        run_command(f'rsync -av --progress {exclude_args} ./ {SSH_USER}@{SSH_HOST}:{REMOTE_DIR}/')
    else:
        # Using SCP (more compatible with Windows)
        print("Creating a temporary file list for upload...")
        
        # Create a temporary file with all files to upload
        with open('upload_files.txt', 'w') as f:
            for root, dirs, files in os.walk('.'):
                # Skip directories that should be excluded
                dirs[:] = [d for d in dirs if d not in ['.git', 'venv', '.venv', '__pycache__']]
                
                for file in files:
                    if file.endswith('.pyc') or file == 'db.sqlite3' or file == '.env':
                        continue
                        
                    file_path = os.path.join(root, file)
                    # Convert to Unix path format
                    file_path = file_path.replace('\\', '/')
                    f.write(f"{file_path}\n")
        
        # Upload files one by one
        with open('upload_files.txt', 'r') as f:
            files = f.read().splitlines()
            
        total_files = len(files)
        for i, file in enumerate(files, 1):
            # Create the directory structure for this file
            remote_path = f"{REMOTE_DIR}/{file[2:]}"  # Remove './' from the beginning
            remote_dir = os.path.dirname(remote_path)
            run_command(f'ssh {SSH_USER}@{SSH_HOST} "mkdir -p {remote_dir}"')
            
            # Upload the file
            print(f"[{i}/{total_files}] Uploading {file}...")
            run_command(f'scp "{file}" {SSH_USER}@{SSH_HOST}:"{remote_path}"')
        
        # Remove temporary file
        os.remove('upload_files.txt')
    
    # Set permissions
    print("\nSetting file permissions...")
    run_command(f'ssh {SSH_USER}@{SSH_HOST} "chmod +x {REMOTE_DIR}/deploy.py"')
    run_command(f'ssh {SSH_USER}@{SSH_HOST} "chmod +x {REMOTE_DIR}/test_email.py"')
    run_command(f'ssh {SSH_USER}@{SSH_HOST} "chmod +x {REMOTE_DIR}/wsgi.py"')
    
    # Run deployment script
    print("\nRunning the deployment script...")
    run_command(f'ssh -t {SSH_USER}@{SSH_HOST} "cd {REMOTE_DIR} && python deploy.py"')
    
    print("\n===== Deployment process completed =====")
    print("Your DoctorFinder application should now be available at: https://lavsarkari.alwaysdata.net")
    print("Access the admin panel at: https://lavsarkari.alwaysdata.net/admin/")
    print("Access webmail at: https://webmail.alwaysdata.com/")

if __name__ == "__main__":
    main() 