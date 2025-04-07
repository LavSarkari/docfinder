#!/bin/bash
# DoctorFinder deployment script for AlwaysData
# Run this script from your local project directory to deploy to AlwaysData

echo "===== DoctorFinder Deployment to AlwaysData ====="
echo "This script will upload your project to AlwaysData and execute the deployment process."
echo ""

# SSH connection details
SSH_HOST="ssh-lavsarkari.alwaysdata.net"
SSH_USER="lavsarkari"
REMOTE_DIR="/home/lavsarkari/www/doctorfinder"

echo "Creating remote directory structure..."
ssh $SSH_USER@$SSH_HOST "mkdir -p $REMOTE_DIR"

echo ""
echo "Uploading project files..."
# Using rsync to upload only necessary files (avoiding venv, .git, etc.)
rsync -av --progress \
    --exclude='.git/' \
    --exclude='venv/' \
    --exclude='.venv/' \
    --exclude='__pycache__/' \
    --exclude='*.pyc' \
    --exclude='db.sqlite3' \
    --exclude='.env' \
    --exclude='media/uploads/' \
    ./ $SSH_USER@$SSH_HOST:$REMOTE_DIR/

echo ""
echo "Setting file permissions..."
ssh $SSH_USER@$SSH_HOST "chmod +x $REMOTE_DIR/deploy.py"
ssh $SSH_USER@$SSH_HOST "chmod +x $REMOTE_DIR/test_email.py"
ssh $SSH_USER@$SSH_HOST "chmod +x $REMOTE_DIR/wsgi.py"

echo ""
echo "Running the deployment script..."
ssh -t $SSH_USER@$SSH_HOST "cd $REMOTE_DIR && python deploy.py"

echo ""
echo "===== Deployment process completed ====="
echo "Your DoctorFinder application should now be available at: https://lavsarkari.alwaysdata.net"
echo "Access the admin panel at: https://lavsarkari.alwaysdata.net/admin/"
echo "Access webmail at: https://webmail.alwaysdata.com/" 