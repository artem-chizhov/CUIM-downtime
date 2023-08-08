import tkinter as tk
from tkinter import BooleanVar, Checkbutton
from tkinter import messagebox
from scrap_zabbix import start_receiving
from txt_file_processing import record_to_txt, del_txt_all
from time_calc import slicing_time, corector
from tkinter import BOTH
from test_connection import check_all
from excel_handler import record_excel, check_file_excel
import dotenv
import os


class Tab_view():

    def __init__(self, form_tab) -> None:
        self.simple_site = ''
        self.simple_lk = ''
        self.form_tab = form_tab
        self.lbl_head = tk.Label(
            self.form_tab,
            text="Формирование данных",
            font=(
                "Arial Bold",
                12))
        self.lbl_head.grid(column=0, row=0, columnspan=3, ipadx=80, pady=10)

        self.lbl_d1 = tk.Label(
            self.form_tab, text="Диапазон 1", font=(
                "Arial Bold", 11))
        self.lbl_d1.grid(column=0, row=1, columnspan=3)
        self.lbl_q1 = tk.Label(
            self.form_tab,
            text="DD / MM / YYYY / HH / MM / SS",
            font=(
                "Arial Bold",
                8))
        self.lbl_q1.grid(column=0, row=2, columnspan=3)
        self.input_time_one = DateEntry(
            self.form_tab, font=(
                'Helvetica', 12, tk.NORMAL))
        self.input_time_one.grid(column=0, row=3, columnspan=3)

        self.lbl_d2 = tk.Label(
            self.form_tab, text="Диапазон 2", font=(
                "Arial Bold", 11))
        self.lbl_d2.grid(column=0, row=4, columnspan=3)
        self.lbl_q1 = tk.Label(
            self.form_tab,
            text="DD / MM / YYYY / HH / MM / SS",
            font=(
                "Arial Bold",
                8))
        self.lbl_q1.grid(column=0, row=5, columnspan=3)
        self.input_time_two = DateEntry(
            self.form_tab, font=(
                'Helvetica', 12, tk.NORMAL))
        self.input_time_two.grid(column=0, row=6, columnspan=3)

        self.btn = tk.Button(
            self.form_tab,
            text="Сформировать",
            command=self.click_button)
        self.btn.grid(
            column=0,
            row=7,
            columnspan=2,
            ipadx=80,
            pady=10,
            padx=35)

        self.var_check_txt = BooleanVar()
        self.var_check_txt.set(0)
        self.chek_txt = Checkbutton(self.form_tab, text="Выгрузить в txt",
                                    variable=self.var_check_txt,
                                    onvalue=1, offvalue=0,
                                    command='')
        self.chek_txt.grid(
            column=0,
            row=8,
            columnspan=5,
            ipadx=65,
            pady=3,
            padx=10)

        self.var_check_excel = BooleanVar()
        self.var_check_excel.set(0)
        self.chek_excel = Checkbutton(self.form_tab, text="Выгрузить в excel",
                                      variable=self.var_check_excel,
                                      onvalue=1, offvalue=0,
                                      command='')
        self.chek_excel.grid(
            column=0,
            row=9,
            columnspan=5,
            ipadx=65,
            pady=3,
            padx=10)

        self.lbl_end = tk.Label(
            self.form_tab,
            text="!Перед запуском необходимо закрыть файлы Excel!",
            font=(
                "Arial Bold",
                10),
            background='#FA8072')
        self.lbl_end.grid(column=0, row=10, columnspan=5)

    def err_show(self, text_error):
        messagebox.showerror("Ошибка", text_error)
        return

    def message_show(self, text_message):
        messagebox.showinfo("Уведомление", text_message)
        return

    def click_button(self):
        self.result_test_dict = check_all()
        for k, v in self.result_test_dict.items():
            if v[0] is False:
                self.err_show(
                    f'Conntection error:\nurl: {k}\nstatus code: {v[1]}\nerror: {v[2]}')
                return

        del_txt_all()
        self.v_excel = self.var_check_excel.get()
        self.v_txt = self.var_check_txt.get()
        self.res1 = self.input_time_one.get()
        self.res2 = self.input_time_two.get()
        self.result_list = corector(self.res1, self.res2)
        self.slicing_time_list = slicing_time(
            date_one=self.result_list[0],
            date_two=self.result_list[1])

        if self.slicing_time_list is False:
            self.err_show('!ошибка диапазона!')
            return

        self.finish_data_dict = start_receiving(self.slicing_time_list)

        if self.v_txt is True and self.v_excel is True:
            if check_file_excel() is False:
                self.err_show(
                    '''!Ошибка целостности!\nДля работы скрипта необходимы файлы:\nSite.xlsx и LK.xlsx\nШаблон на ВИКИ.''')
            record_to_txt(self.finish_data_dict)
            record_excel(data_list=self.finish_data_dict,
                         date1=self.result_list[0],
                         date2=self.result_list[1])
            self.message_show('Выгружено.')
            return

        elif self.v_txt is True:
            record_to_txt(self.finish_data_dict)
            self.message_show('Выгружено.')
            return

        elif self.v_excel is True:
            if check_file_excel() is False:
                self.err_show(
                    '''!Ошибка целостности!\nДля работы скрипта необходимы файлы:\nSite.xlsx и LK.xlsx\nШаблон на ВИКИ.''')
            record_excel(data_list=self.finish_data_dict,
                         date1=self.result_list[0],
                         date2=self.result_list[1])
            record_excel(data_list=self.finish_data_dict,
                         date1=self.result_list[0],
                         date2=self.result_list[1])
            self.message_show('Выгружено.')
            return
        else:
            self.err_show("Не выбран вариант выгрузки.")
            return


class Tab_readme():

    def __init__(self, form_tab) -> None:
        self.form_tab = form_tab
        self.lbl_head = tk.Label(self.form_tab, text="""
        Скрипт "режет" диапазоны времени по 12 часов\n
        Идет на заббикс, забирает данные\n
        Вставляет данные в excel файлы\n
        Перед вставкой затирает ячейки в файлах\n
        Заполняемые поля в excel:\n
        Итог - B1447, B1448\n
        Данные - столбцы A,E,I начиная с 2-й строки до 43200\n
        Файлы необходимые в корневой дирректории:\n
        Site.xlsx, LK.xlsx, .env (файл переменных окружения)
        """, font=("Arial Bold", 8))
        self.lbl_head.grid(column=0, row=0, columnspan=2, padx=5)


class Tab_setup():

    def __init__(self, form_tab) -> None:

        self.form_tab = form_tab
        self.lbl_zbx_log_msk = tk.Label(
            self.form_tab, text="Логин к Zabbix MSK", font=(
                "Arial Bold", 10))
        self.lbl_zbx_log_msk.grid(column=0, row=0, padx=10, pady=4)
        self.in_zbx_log_msk = tk.Entry(self.form_tab, width=10)
        self.in_zbx_log_msk.grid(column=0, row=1, padx=10, pady=4)

        self.lbl_zbx_log_spb = tk.Label(
            self.form_tab, text="Логин к Zabbix SPB", font=(
                "Arial Bold", 10))
        self.lbl_zbx_log_spb.grid(column=0, row=2, padx=10, pady=4)
        self.in_zbx_log_spb = tk.Entry(self.form_tab, width=10)
        self.in_zbx_log_spb.grid(column=0, row=3, padx=10, pady=4)

        self.lbl_zbx_log_ural = tk.Label(
            self.form_tab, text="Логин к Zabbix URAL", font=(
                "Arial Bold", 10))
        self.lbl_zbx_log_ural.grid(column=0, row=4, padx=10, pady=4)
        self.in_zbx_log_ural = tk.Entry(self.form_tab, width=10)
        self.in_zbx_log_ural.grid(column=0, row=5, padx=10, pady=4)

        self.lbl_zbx_pas_msk = tk.Label(
            self.form_tab, text="Пароль к Zabbix MSK", font=(
                "Arial Bold", 10))
        self.lbl_zbx_pas_msk.grid(column=1, row=0, padx=10, pady=4)
        self.in_zbx_pas_msk = tk.Entry(self.form_tab, width=10)
        self.in_zbx_pas_msk.grid(column=1, row=1, padx=10, pady=4)

        self.lbl_zbx_pas_spb = tk.Label(
            self.form_tab, text="Пароль к Zabbix SPB", font=(
                "Arial Bold", 10))
        self.lbl_zbx_pas_spb.grid(column=1, row=2, padx=10, pady=4)
        self.in_zbx_pas_spb = tk.Entry(self.form_tab, width=10)
        self.in_zbx_pas_spb.grid(column=1, row=3, padx=10, pady=4)

        self.lbl_zbx_pas_ural = tk.Label(
            self.form_tab, text="Пароль к Zabbix URAL", font=(
                "Arial Bold", 10))
        self.lbl_zbx_pas_ural.grid(column=1, row=4, padx=10, pady=4)
        self.in_zbx_pas_ural = tk.Entry(self.form_tab, width=10)
        self.in_zbx_pas_ural.grid(column=1, row=5, padx=10, pady=4)

        self.btn = tk.Button(
            self.form_tab,
            text="Изменить",
            command=self.click_button_set)
        self.btn.grid(column=0, row=8, columnspan=2, ipadx=70, padx=4, pady=4)
        self.form_tab.columnconfigure(index=1, weight=1)
        self.form_tab.columnconfigure(index=2, weight=1)
        self.form_tab.rowconfigure(index=8, weight=1)

    def click_button_set(self):

        for k, v in {
            'LOGIN_MSK': self.in_zbx_log_msk.get(),
            'LOGIN_SPB': self.in_zbx_log_spb.get(),
            'LOGIN_URAL': self.in_zbx_log_ural.get(),
            'PASSWORD_MSK': self.in_zbx_pas_msk.get(),
            'PASSWORD_SPB': self.in_zbx_pas_spb.get(),
                'PASSWORD_URAL': self.in_zbx_pas_ural.get()}.items():
            if v != '':
                dotenv_file = dotenv.find_dotenv()
                dotenv.load_dotenv(dotenv_file)
                os.environ[k] = v
                dotenv.set_key(dotenv_file, k, os.environ[k])


class Tab_setup_url():

    def __init__(self, form_tab) -> None:

        self.form_tab = form_tab
        self.lbl_zbx_url_msk = tk.Label(
            self.form_tab, text="Ссылка на zabbix MSK", font=(
                "Arial Bold", 10))
        self.lbl_zbx_url_msk.grid(column=0, row=0, padx=10, pady=4)
        self.in_zbx_url_msk = tk.Entry(self.form_tab, width=50)
        self.in_zbx_url_msk.grid(column=0, row=1, padx=10, pady=4)

        self.lbl_zbx_url_spb = tk.Label(
            self.form_tab, text="Ссылка на zabbix SPB", font=(
                "Arial Bold", 10))
        self.lbl_zbx_url_spb.grid(column=0, row=2, padx=10, pady=4)
        self.in_zbx_url_spb = tk.Entry(self.form_tab, width=50)
        self.in_zbx_url_spb.grid(column=0, row=3, padx=10, pady=4)

        self.lbl_zbx_url_ural = tk.Label(
            self.form_tab, text="Ссылка на zabbix URAL", font=(
                "Arial Bold", 10))
        self.lbl_zbx_url_ural.grid(column=0, row=4, padx=10, pady=4)
        self.in_zbx_url_ural = tk.Entry(self.form_tab, width=50)
        self.in_zbx_url_ural.grid(column=0, row=5, padx=10, pady=4)

        self.btn = tk.Button(
            self.form_tab,
            text="Изменить",
            command=self.click_button_set)
        self.btn.grid(column=0, row=8, columnspan=3, ipadx=70, padx=4, pady=4)
        self.form_tab.columnconfigure(index=1, weight=1)
        self.form_tab.columnconfigure(index=2, weight=1)
        self.form_tab.rowconfigure(index=8, weight=1)

    def click_button_set(self):

        for k, v in {
            'URL_MSK': self.in_zbx_url_msk.get(),
            'URL_SPB': self.in_zbx_url_spb.get(),
                'URL_URAL': self.in_zbx_url_ural.get(), }.items():
            if v != '':
                dotenv_file = dotenv.find_dotenv()
                dotenv.load_dotenv(dotenv_file)
                os.environ[k] = v
                dotenv.set_key(dotenv_file, k, os.environ[k])


class DateEntry(tk.Frame):
    def __init__(self, master, frame_look={}, **look):
        args = dict(relief=tk.SUNKEN, border=1)
        args.update(frame_look)
        tk.Frame.__init__(self, master, **args)

        self.entry_1 = tk.Entry(self, width=2, **args)
        self.label_1 = tk.Label(self, text='/', **args)
        self.entry_2 = tk.Entry(self, width=2, **args)
        self.label_2 = tk.Label(self, text='/', **args)
        self.entry_3 = tk.Entry(self, width=4, **args)
        self.label_3 = tk.Label(self, text='/', **args)
        self.entry_4 = tk.Entry(self, width=2, **args)
        self.label_4 = tk.Label(self, text='/', **args)
        self.entry_5 = tk.Entry(self, width=2, **args)
        self.label_5 = tk.Label(self, text='/', **args)
        self.entry_6 = tk.Entry(self, width=2, **args)

        self.entry_1.pack(side=tk.LEFT)
        self.label_1.pack(side=tk.LEFT)
        self.entry_2.pack(side=tk.LEFT)
        self.label_2.pack(side=tk.LEFT)
        self.entry_3.pack(side=tk.LEFT)
        self.label_3.pack(side=tk.LEFT)
        self.entry_4.pack(side=tk.LEFT)
        self.label_4.pack(side=tk.LEFT)
        self.entry_5.pack(side=tk.LEFT)
        self.label_5.pack(side=tk.LEFT)
        self.entry_6.pack(side=tk.LEFT)

        self.entries = [
            self.entry_1,
            self.entry_2,
            self.entry_3,
            self.entry_4,
            self.entry_5,
            self.entry_6]

        self.entry_1.bind('<KeyRelease>', lambda e: self._check(0, 2))
        self.entry_2.bind('<KeyRelease>', lambda e: self._check(1, 2))
        self.entry_3.bind('<KeyRelease>', lambda e: self._check(2, 4))
        self.entry_4.bind('<KeyRelease>', lambda e: self._check(3, 2))
        self.entry_5.bind('<KeyRelease>', lambda e: self._check(4, 2))
        self.entry_6.bind('<KeyRelease>', lambda e: self._check(5, 2))

    def _backspace(self, entry):
        cont = entry.get()
        entry.delete(0, tk.END)
        entry.insert(0, cont[:-1])

    def _check(self, index, size):
        entry = self.entries[index]
        next_index = index + 1
        next_entry = self.entries[next_index] if next_index < len(
            self.entries) else None
        data = entry.get()

        if len(data) > size or not data.isdigit():
            self._backspace(entry)
        if len(data) >= size and next_entry:
            next_entry.focus()

    def get(self):
        return [e.get() for e in self.entries]
