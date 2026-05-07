import os
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Các thư mục cần xóa
folders_to_delete = [
    os.path.join(BASE_DIR, "../data/chunks"),
    os.path.join(BASE_DIR, "../data/processed"),
    os.path.join(BASE_DIR, "../data/vector_db"),
]

def clear_folder(folder_path):
    if os.path.exists(folder_path):
        print(f"🗑️ Deleting: {folder_path}")
        shutil.rmtree(folder_path)
        os.makedirs(folder_path, exist_ok=True)
        print(f"✅ Recreated empty folder: {folder_path}")
    else:
        print(f"⚠️ Not found: {folder_path}")

if __name__ == "__main__":
    print("=== RESET DATA PIPELINE ===")
    for folder in folders_to_delete:
        clear_folder(folder)
    print("🎯 Done! Data cleaned.")