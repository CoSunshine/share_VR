import profile
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options, FirefoxProfile
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

from xml.dom.minidom import parseString
import os, csv
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


def get_permission_level():
    url = 'https://developer.android.com/reference/android/Manifest.permission'
    profile_path = r'/Users/liuhuo/Library/Application Support/Firefox/Profiles/1hywajcr.default'
    profile = FirefoxProfile(profile_path)
    serv = Service(r'/Users/liuhuo/Documents/Code/google_third_party/tools/geckodriver')

    firefox_capabilities = DesiredCapabilities.FIREFOX
    firefox_capabilities['marionette'] = True


    driver = Firefox(capabilities=firefox_capabilities, service=serv, firefox_profile=profile)
    
    driver.get(url)
    time.sleep(10)

    danger_perms, normal_perm, restricted_perms = [], [], []

    elems = driver.find_elements(by='xpath', value="//div[@data-version-added]")

    for ele in elems:
        id_ele = ele.find_element(by='xpath', value=".//h3")
        id = id_ele.get_attribute('id')
        ps = ele.find_elements(by='xpath', value=".//p")
        dangerous, normal, restricted = False, False, False
        
        for p in ps:
            if 'Protection level: dangerous' in p.text:
                dangerous = True
            if 'Protection level: normal' in p.text:
                normal = True
        if dangerous:
            danger_perms.append(id)
    return danger_perms


def analyze_dangerous_perm(folder):
    danger_perms = open('danger_perms.txt', 'r').readlines()
    fs = os.listdir(folder)

    per_dis = dict() 
    per_details = dict()
    per_type = dict()

    for p_t in danger_perms:
        per_type[p_t] = 0

    for f in fs:
        count = 0
        perms = open(folder + '/' + f, 'r').readlines()
        
        per_details[f] = []

        for p in perms:

            for danger_p in danger_perms:
                if danger_p in p:
                    count += 1
                    per_type[danger_p] += 1
                    per_details[f].append(danger_p.replace('\n', ''))

        if count == 0:
            continue

        per_dis[f] = count
    
    for p_t in per_type:
        if per_type[p_t] == 0:
            continue
        print(p_t.replace('\n', ''), per_type[p_t])

    val_dic = dict()
    for key in per_dis:
        val = per_dis[key]

        if val not in val_dic:
            val_dic[val] = 0
        
        val_dic[val] += 1
    
    # for key in sorted(val_dic.keys()):
    #     print(key, val_dic[key])
    
    return per_details, val_dic


def declared_permissions_pico(file, folder):
    danger_perm_details, val_dic = analyze_dangerous_perm(folder)
    print(folder, val_dic)
    chinese_english = {
        '相机': ['CAMERA'],
        '麦克风': ['RECORD_AUDIO', 'READ_MEDIA_AUDIO'],
        '存储空间': ['READ_EXTERNAL_STORAGE', 'WRITE_EXTERNAL_STORAGE'],
        '位置信息': [
            'ACCESS_BACKGROUND_LOCATION',
            'ACCESS_COARSE_LOCATION',
            'ACCESS_FINE_LOCATION',
            'ACCESS_MEDIA_LOCATION',
        ],
        'null': [],
    }
    perm_dict = set()
    with open(file, 'r') as f:
        csvreader = csv.DictReader(f, delimiter=',')
        for row in csvreader:
            name = row['name']
            perms = row['权限'].replace('权限：', '').split(', ')
            not_declared = []
            # print(row['name'], row['权限'])
            for key in danger_perm_details:
                if name in key:
                    declared_english_perms = []
                    for perm in perms:
                        declared_english_perms.extend(chinese_english[perm])
                    # print(danger_perm_details[key], declared_english_perms)

                    
                    for perm in danger_perm_details[key]:
                        if perm not in declared_english_perms:
                            not_declared.append(perm)
            if len(not_declared) > 0:
                print(name, not_declared)
                # print(danger_perm_details[key], perms)

            for perm in perms:
                perm_dict.add(perm)

    print(perm_dict)


def declared_permissions_oculus():
    folder = "permissions_oculus"
    _, val_dic = analyze_dangerous_perm(folder)
    print(val_dic)

if __name__ == '__main__':
    # folder = 'permissions_pico'
    # # folder = 'share_VR/result'
    # analyze_dangerous_perm(folder)
    #     . In total, we collect
    # 898 .apk, including 455 from Oculus and 443 from Pico

    ## pico requested dangerous perm: 
    ## {1: 82, 3: 108, 2: 154, 4: 36, 5: 12, 6: 4} 
    ## key: the number of requested dangerous perm, value: service number
    ## oculus requested dangerous perm:
    ## {1: 17, 2: 139, 3: 74, 4: 7, 7: 1}


    file = 'pico_csvs/all.csv'
    declared_permissions_pico(file, "permissions_pico")

    declared_permissions_oculus()