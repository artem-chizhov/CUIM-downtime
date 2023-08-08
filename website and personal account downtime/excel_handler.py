import openpyxl
import os


def check_file_excel():
    if os.path.isfile(
            './Site.xlsx') is False and os.path.isfile('./LK.xlsx') is False:
        return False
    else:
        return True


def func_cell_clear(var_excel):
    for count in range(43200):
        var_excel[f'A{count+2}'] = None
        var_excel[f'E{count+2}'] = None
        var_excel[f'I{count+2}'] = None


def cycle_record(index, data, var_excel):
    for count, val in enumerate(data):
        var_excel[f'{index}{count+2}'] = val


def record_excel(date1, date2, data_list):

    file_excel_site = openpyxl.load_workbook(filename=f'./Site.xlsx')
    result_site = file_excel_site.get_sheet_by_name("Итог")
    data_site = file_excel_site.get_sheet_by_name("Данные")
    func_cell_clear(data_site)
    cycle_record(index='A', data=data_list['msk_site'], var_excel=data_site)
    cycle_record(index='E', data=data_list['spb_site'], var_excel=data_site)
    cycle_record(index='I', data=data_list['ural_site'], var_excel=data_site)
    result_site['B1447'] = date1[-8:]
    result_site['B1448'] = date2[-8:]
    file_excel_site.save(f'Site.xlsx')

    file_excel_lk = openpyxl.load_workbook(filename=f'./LK.xlsx')
    result_lk = file_excel_lk.get_sheet_by_name("Итог")
    data_lk = file_excel_lk.get_sheet_by_name("Данные")
    func_cell_clear(data_lk)
    cycle_record(index='A', data=data_list['msk_lk'], var_excel=data_lk)
    cycle_record(index='E', data=data_list['spb_lk'], var_excel=data_lk)
    cycle_record(index='I', data=data_list['ural_lk'], var_excel=data_lk)
    result_lk['B1447'] = date1[-8:]
    result_lk['B1448'] = date2[-8:]
    file_excel_lk.save(f'LK.xlsx')
