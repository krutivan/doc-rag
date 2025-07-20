import glob
import os
from src.services.index.index_service import IndexService

def upload_file_to_index(file_path):
    print(f"Indexing file: {file_path}")
    try:
        num_chunks = IndexService.index(file_path)
        print(f"✅ Success: {num_chunks} chunks indexed for '{file_path}'.")
    except Exception as e:
        print(f"❌ Failed to index '{file_path}': {str(e)}")

if __name__ == "__main__":
    knowledge_folder = "data/knowledge"
    md_files = glob.glob(os.path.join(knowledge_folder, "*.md"))
    if not md_files:
        print("No markdown files found in knowledge folder.")
    for file_path in md_files:
        upload_file_to_index(file_path)
