from xml.dom.minidom import parseString
import os
# Documentation on Permissions in AndroidManifest.xml
# https://developer.android.com/guide/topics/manifest/manifest-intro#perms


def fetch_permissions():
    data = '' # string data from file
    with open('AndroidManifest.xml_dump', 'r') as f:
        data = f.read()

    dom = parseString(data) # parse file contents to xml dom
    nodes = dom.getElementsByTagName('uses-permission') # xml nodes named "uses-permission"
    nodes+= dom.getElementsByTagName('uses-permission-sdk-23') # xml nodes named "uses-permission-sdk-23"

    permissions = [] # holder for all permissions as we gather them
    # Iterate over all the uses-permission nodes
    for node in nodes:
        permissions += [node.getAttribute("name")] # save permissionName to our list

    # Print sorted list
    for permission in sorted(permissions): # sort permissions and iterate
        print('this is permissions:', permission) # print permission name

def get_manifest_file(folder, filename):
    path = os.path.join(folder, filename)
    command = 'java -jar ClassyShark.jar -export '+ path + ' AndroidManifest.xml'
    os.system(command)
    new_manifest_name = 'xml/' + filename + 'AndroidManifest.xml'
    rename_command = 'mv AndroidManifest.xml_dump ' + new_manifest_name 
    os.system(rename_command)


def unzip_zip(folder, filename):
    return

def loop_all_apk(folder):
    fs = os.listdir(folder)
    for f in fs:
        get_manifest_file(folder, f)
    return

if __name__ == '__main__':
    apks_folder = 'tmp'
    loop_all_apk(apks_folder)