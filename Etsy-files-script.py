import os
import re
from operator import itemgetter
import zipfile

main_list = []

def create_list_and_rename_files(folder_dir, given_name = ''):
    folder = os.listdir(f'/{folder_dir}')
    given_name_num = 1
    for file in folder:
        if given_name == '':
            new_name = re.sub(r'-min', '', file)
        elif given_name != '':
            new_name = re.sub(r'.*\.', f'{given_name}-{given_name_num}.', file)
            given_name_num += 1
        path_name = f'/{folder_dir}/{file}'
        path_new_name = f'/{folder_dir}/{new_name}'
        os.rename(path_name, path_new_name)
        file_size = os.path.getsize(path_new_name)
        main_list.append([file_size, new_name])


def create_zips(archive_name, etsy_shop_name, folder_dir, *args):
    num = 1
    for new_list in args:
        if new_list != []:
            print(f'[+] Archive {num} created')
            new_zip = zipfile.ZipFile(f'/{folder_dir}/{archive_name}-{etsy_shop_name}-{num}.zip', 'w', zipfile.ZIP_DEFLATED)
            for item in new_list:
                new_zip.write(os.path.join(f'/{folder_dir}', item[1]), arcname=item[1])  # делаем относительный путь к файлу
            new_zip.close()
            num += 1


def create_lists(archive_name, etsy_shop_name, folder_dir):
    new_list1, new_list2, new_list3, new_list4, new_list5 = [], [], [], [], []
    local_size1, local_size2, local_size3, local_size4, local_size5 = 0, 0, 0, 0, 0
    total_size = 0
    max_zip_size = 20971520

    for item in main_list:
        if total_size < max_zip_size:
            new_list1.append(item)
            total_size += item[0]
            local_size1 += item[0]
            if local_size1 > max_zip_size:
                new_list2.append(new_list1[-1])
                local_size1 -= new_list1[-1][0]
                local_size2 += new_list1[-1][0]
                del new_list1[-1]

        elif total_size < max_zip_size + max_zip_size:
            new_list2.append(item)
            total_size += item[0]
            local_size2 += item[0]
            if local_size2 > max_zip_size:
                new_list3.append(new_list2[-1])
                local_size2 -= new_list2[-1][0]
                local_size3 += new_list2[-1][0]
                del new_list2[-1]

        elif total_size < max_zip_size + max_zip_size + max_zip_size:
            new_list3.append(item)
            total_size += item[0]
            local_size3 += item[0]
            if local_size3 > max_zip_size:
                new_list4.append(new_list3[-1])
                local_size3 -= new_list3[-1][0]
                local_size4 += new_list3[-1][0]
                del new_list3[-1]

        elif total_size < max_zip_size + max_zip_size + max_zip_size + max_zip_size:
            new_list4.append(item)
            total_size += item[0]
            local_size4 += item[0]
            if local_size4 > max_zip_size:
                new_list5.append(new_list4[-1])
                local_size4 -= new_list4[-1][0]
                del new_list4[-1]

        elif total_size > max_zip_size + max_zip_size + max_zip_size + max_zip_size:
            new_list5.append(item)
            total_size += item[0]

    create_zips(archive_name, etsy_shop_name, folder_dir, new_list1, new_list2, new_list3, new_list4, new_list5)


def start_program():
    print('[!] WELCOME [!]\nETSY rename and archive files')
    print('--------------------------------------------------------')

    print('[!] Please enter the folder link')
    print('[!] test dir => user/lihon/Desktop/images')
    folder_dir = input('folder dir => ')
    print('[!] Delete "-min" in file names\n 1 - yes\n 2 - no')
    min_del = int(input('delete "-min" ? => '))

    if min_del == 1:
        create_list_and_rename_files(folder_dir)
        print('[!] "-min" deleted')
    else:
        print('[!] Action skipped')

    print('--------------------------------------------------------')

    print('[!] Complete rename all files ? \n 1 - yes\n 2 - no')
    compl_rename = int(input('Complete rename ? => '))

    if compl_rename == 1:
        given_name = input('[!] Enter new files name "Watercolor-gold-frames" => ')
        create_list_and_rename_files(folder_dir, given_name)
        print('[!] Fiels renamed')
    else:
        print('[!] Action skipped')

    print('--------------------------------------------------------')

    main_list.sort(key=itemgetter(0), reverse=True)   #сортировка списка по размеру файлов

    print('[!] Archive files ? \n 1 - yes\n 2 - no')
    create_arch = int(input('Archive files ? => '))

    if create_arch == 1:
        if min_del != 1 and compl_rename != 1:
            create_list_and_rename_files(folder_dir)

        print('[!] Enter archive names')
        print('[!] test archive name => Watercolor-frames')
        archive_name = input('archive name => ')
        print('[!] Enter Etsy shop name')
        print('[!] test Etsy shop name => BEEART')
        etsy_shop_name = input('etsy shop name => ')
        create_lists(archive_name, etsy_shop_name, folder_dir)
        print('[!] Archives created')
    else:
        print('[!] Action skipped')

    print('--------------------------------------------------------')
    print('[!] Program completed')


start_program()