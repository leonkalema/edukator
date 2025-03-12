#!/bin/bash

# Script to remove sensitive data from Git repository

echo "Cleaning repository of sensitive data..."

# Create backup of .env file
cp .env .env.backup

# Create a clean .env file without sensitive data
cat > .env << EOL
# API Keys (add your keys here but don't commit this file)
OPENAI_API_KEY=
T2A_API_KEY=
T2A_GROUP_ID=
PORT=8201
EOL

echo "Created clean .env file. Original saved as .env.backup"
echo "Now run the following Git commands to fix your history:"
echo ""
echo "git add .env .gitignore .env.example"
echo "git commit --amend --no-edit"
echo "git push -f origin main"
echo ""
echo "IMPORTANT: After pushing, restore your API keys to .env from .env.backup"
echo "Remember to NEVER commit .env files with real API keys"
