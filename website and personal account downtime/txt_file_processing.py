import os


def record_to_txt(data_dict):

    with open('msk_site.txt', 'a+', encoding='utf8') as file:
        for v in data_dict['msk_site']:
            file.writelines(f'{v}\n')

    with open('ural_site.txt', 'a+', encoding='utf8') as file:
        for v in data_dict['ural_site']:
            file.writelines(f'{v}\n')

    with open('spb_site.txt', 'a+', encoding='utf8') as file:
        for v in data_dict['spb_site']:
            file.writelines(f'{v}\n')

    with open('msk_lk.txt', 'a+', encoding='utf8') as file:
        for v in data_dict['msk_lk']:
            file.writelines(f'{v}\n')

    with open('ural_lk.txt', 'a+', encoding='utf8') as file:
        for v in data_dict['ural_lk']:
            file.writelines(f'{v}\n')

    with open('spb_lk.txt', 'a+', encoding='utf8') as file:
        for v in data_dict['spb_lk']:
            file.writelines(f'{v}\n')


def del_txt_all():
    try:
        os.unlink("ural_lk.txt")
        os.unlink("msk_lk.txt")
        os.unlink("spb_lk.txt")
        os.unlink("ural_site.txt")
        os.unlink("msk_site.txt")
        os.unlink("spb_site.txt")
    except BaseException:
        pass
