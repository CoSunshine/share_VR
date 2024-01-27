import os
def filter_android_permissions(lines):
    filtered = []
    for l in lines:
        if "android.permission." in l or "com.android." in l or "android." in l:
            continue
        if 'oculus' not in l or 'pico' not in l:
            continue
        filtered.append(l.strip())
    return filtered

def analyze_permissions(folder):
    fs = os.listdir(folder)
    for f in fs:
        f_p = os.path.join(folder, f)
        lines = open(f_p, 'r').readlines()
        filtered = filter_android_permissions(lines)
        if len(filtered) > 0:
            print('################################')
            print('\n'.join(filtered))

if __name__ == '__main__':
    folder = "permissions_oculus"
    folder = "permissions_pico"
    analyze_permissions(folder)
