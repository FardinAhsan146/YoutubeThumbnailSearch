# This script helps me during development to just nuke the two databases and start from scratch 
# .\scripts\clean_databases.ps1

# Remove the chroma directory
Remove-Item -Recurse -Force .\chroma_clip_embeddings\

# Remove the talk_to_youtuber_db.sqlite file
cd database
rm youtuber_db.sqlite
cd ..