from pyaxmlparser import APK
import os
import shutil
import patoolib
from pyunpack import Archive
from rarfile import RarFile

import timeit



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


    try:
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
    except:
        print('error happened while processing the apk file')

def is_rar_with_passwd(name):
    if True:
        pass
    return

def process_rar_file(root, file):
    full_path = os.path.join(root, file)
    apk_unzip_folder = 'apk_unzip_folder'

    if not os.path.exists(apk_unzip_folder):
        os.makedirs(apk_unzip_folder)  # Make sure the directory exists
    
    # start_time = timeit.default_timer()
    try:
        patoolib.extract_archive(full_path, outdir=apk_unzip_folder, verbosity=1)
        # with RarFile(full_path, 'r') as myrar:
        #     myrar.extractall(path=apk_unzip_folder, pwd='vrmoo.cn')

        # Archive(full_path).extractall(apk_unzip_folder, password='vrmoo.cn')
        print('extraction successfully')


    except Exception as e:
        print(f'extraction error occurred: {e}')
        return

    un_zipped_folder = os.path.join(apk_unzip_folder, file.replace('.rar', ''))
    if os.path.exists(un_zipped_folder) == False:
        un_zipped_folder = apk_unzip_folder
    
    files = os.listdir(un_zipped_folder)

    for f in files:
        if f.endswith('.apk'):
            full_path = os.path.join(un_zipped_folder, f)
            print(f'Processing APK at {full_path}')
            get_per_from_apk(full_path)
    
    ## delete the unzipped folder
    shutil.rmtree(un_zipped_folder)
    print(f"Folder '{un_zipped_folder}' deleted successfully.")


    return

def walk_and_process_apks(start_folder):
    for root, dirs, files in os.walk(start_folder):
        for file in files:
            if file.endswith('.apk'):
                full_path = os.path.join(root, file)
                print(f'Processing APK at {full_path}')
                get_per_from_apk(full_path)
            if file.endswith('.rar'):
                process_rar_file(root, file)
                


if __name__ == '__main__':
    required_commands = []
    if check_commands_exist(required_commands):
        current_folder = 'VR'  # Current directory
        walk_and_process_apks(current_folder)