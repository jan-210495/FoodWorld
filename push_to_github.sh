#!/bin/bash

echo "📦 Committing and pushing changes to GitHub..."

# Ask for a commit message
read -p "Enter your commit message: " commit_message

# Run Git commands
git add .
git commit -m "$commit_message"
git push origin main

echo "✅ Done! Changes pushed to GitHub."
