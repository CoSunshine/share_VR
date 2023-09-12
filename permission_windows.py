from pyaxmlparser import APK
import os
import shutil

def check_commands_exist(commands):
    for cmd in commands:
        if shutil.which(cmd) is None:
            print(f"Error: {cmd} command not found.")
            return False
    return True

def sanitize_filename(filename):
    return filename.translate(str.maketrans({" ": "_", "/": "_", "\\": "_", ":": "_", ".": "_"}))

def get_per_from_apk(apk_path):
    output_folder = "./tmp"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)  # Make sure the directory exists

    apk = APK(apk_path)
    permissions = apk.get_permissions()

    sanitized_name = sanitize_filename(apk_path)
    output_file_path = os.path.join(output_folder, f"{sanitized_name}_permissions.txt")

    try:
        with open(output_file_path, 'w', encoding='utf-8') as f:
            for permission in sorted(permissions):
                f.write(f'Permission: {permission}\n')
                print(f'Permission: {permission}')
    except FileNotFoundError as e:
        print(f"File not found error: {e}")

def walk_and_process_apks(start_folder):
    for root, dirs, files in os.walk(start_folder):
        for file in files:
            if file.endswith('.apk'):
                full_path = os.path.join(root, file)
                print(f'Processing APK at {full_path}')
                get_per_from_apk(full_path)

if __name__ == '__main__':
    required_commands = []
    if check_commands_exist(required_commands):
        current_folder = '.'  # Current directory
        walk_and_process_apks(current_folder)
