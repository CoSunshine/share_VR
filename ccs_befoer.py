import os
def filter_android_permissions(lines):
    filtered = []
    for l in lines:
        if "android.permission." in l or "com.android." in l or "android." in l:
            continue
        if 'oculus' not in l and 'pico' not in l:
            continue
        filtered.append(l.strip())
    return filtered

def analyze_permissions(folder):
    fs = os.listdir(folder)
    service_features = dict()
    for f in fs:
        f_p = os.path.join(folder, f)
        lines = open(f_p, 'r').readlines()
        filtered = filter_android_permissions(lines)
        if len(filtered) > 0:
            print('################################ ', f)
            print('\n'.join(filtered))
            service_features[f] = filtered
    return service_features

def sort_dict(orginial):
    sorted_dict = dict(sorted(orginial.items(), key=lambda items: items[1], reverse=True))
    return sorted_dict

def analyze_distribution(folder):
    service_features = analyze_permissions(folder)
    feature_requested_times = dict()
    for serv in service_features:
        features = service_features[serv]
        for f in features:
            if f not in feature_requested_times:
                feature_requested_times[f] = 0
            feature_requested_times[f] += 1
    print('################################')

    sorted_dict = dict(sorted(feature_requested_times.items(), key=lambda items: items[1], reverse=True))
    for f in sorted_dict:
        print(f, sorted_dict[f])

    return

def analyze_service_distribution(folder):
    service_features = analyze_permissions(folder)
    service_requested_times = dict()

    for serv in service_features:
        number = len(service_features[serv])
        if number not in service_requested_times:
            service_requested_times[number] = 0
        service_requested_times[number] += 1
    
    sorted = sort_dict(service_requested_times)
    for f in sorted:
        print(f, sorted[f])

    return

if __name__ == '__main__':
    folder = "permissions_oculus"
    folder = "permissions_pico"
    analyze_permissions(folder)
    # # analyze_distribution(folder)
    # analyze_service_distribution(folder)
