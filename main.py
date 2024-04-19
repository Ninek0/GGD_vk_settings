import requests
import os
import winreg
import string
from sys import argv

def get_available_drives():
    drives = ['%s:' % d for d in string.ascii_uppercase if os.path.exists('%s:' % d)]
    return drives

def find_folder(target_folder):
    drivers = get_available_drives()
    for drive in drivers:
        if os.path.exists(drive):
            for root, dirs, files in os.walk(drive):
                if target_folder in dirs:
                    return os.path.join(root, target_folder)

def set_settings(folder_path=""):
    print(folder_path)
    if not folder_path:
    #Поиск пути до папки с игрой
        folder_name = "Goose Goose Duck"
        folder_path = find_folder(folder_name)
    #Если папка есть то скачиваем файл в папку с игрой
    if folder_path:
        url_download = "https://drive.usercontent.google.com/download?id=1IGENwFzLm8bBEboISadYSNEdxbnjz1fH&export=download&authuser=0&confirm=t&uuid=eb6ddb47-de1b-448c-b241-6b6f14d2afcd&at=APZUnTUrLq2JVznxgbYbXjSJ7FM9%3A1713390017093"
        file = requests.get(url_download, allow_redirects=True)
        open(folder_path + "\\" + "setting.reg", "wb").write(file.content)
        with open(folder_path + "\\" + "setting.reg", 'r+', encoding='utf16') as settings_file:
        #Вносим изменения в реестр
            reg_path  = ""
            attributes = []
            for line in settings_file.readlines():
                line = ''.join(line.split('\n'))
                line.replace('\n', '')
                line.strip()
                if line.startswith('[') and line.endswith(']'):
                    reg_path = line[1:len(line)-1]
                elif line.startswith("\""):
                    attributes.append(line)

            reg_values = reg_path.split('\\')
            # print(reg_values)
            # print('\\'.join(reg_values[1:]))
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, '\\'.join(reg_values[1:]))
            for attribute in attributes:
                start_index = attribute.find('"')
                end_index = attribute.find('"', start_index + 1)
                
                value_name = attribute[start_index + 1:end_index]
                
                value_size = 0
                start_index = attribute.find('=')
                end_index = attribute.find(':')
                if  attribute[start_index + 1:end_index] == 'dword':
                    value_size = winreg.REG_DWORD

                value = int(attribute[attribute.find(':') + 1:], 16)
                winreg.SetValueEx(key, value_name, 0, value_size, value)
            winreg.CloseKey(key)
        print('Скрипт отработал')


if len(argv) == 2:
    game_folder_path = argv[1]
    if os.path.isdir(game_folder_path):
        set_settings(folder_path=game_folder_path)
    else:
        print("Неверно указан путь до папки")
else:
    set_settings()