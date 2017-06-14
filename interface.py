# encoding:utf-8

# TODO 界面继续完善
# TODO 与实际功能结合

from Tkinter import *
import tkFileDialog
import tkMessageBox
from main import ReadDataToExcel
from PIL import ImageTk
import Pmw
from tkMessageBox import showwarning, showinfo
import MySQLdb
import ttk
import time
import threading


class InterfaceExportData(object):
    def __init__(self):
        self.maximum = 0
        self.example = None
        self.window = Tk()
        self.window.title('数据库导出系统')
        self.window.iconbitmap('./favicon.ico')
        self.window.geometry('950x400')

        # Pmw.Note
        self.tabControl = Pmw.NoteBook(self.window)
        self.tabControl.pack(fill=BOTH, expand=YES)

        self.firstPage = self.tabControl.add('数据汇总')
        self.secondPage = self.tabControl.add('数据导入')
        self.frame = Frame(self.firstPage)
        self.frame.pack()

        self.label_host = Label(self.frame, text='主机')
        self.label_host.grid(row=0, column=0)
        self.label_name = Label(self.frame, text='账户')
        self.label_name.grid(row=0, column=2)
        self.label_pass = Label(self.frame, text='密码')
        self.label_pass.grid(row=0, column=4)
        self.label_database = Label(self.frame, text='数据库')
        self.label_database.grid(row=0, column=6)

        self.entry_host = Entry(self.frame)
        self.entry_host.grid(row=0, column=1)
        self.entry_name = Entry(self.frame)
        self.entry_name.grid(row=0, column=3)
        self.entry_pass = Entry(self.frame)
        self.entry_pass.grid(row=0, column=5)
        self.entry_database = Entry(self.frame)
        self.entry_database.grid(row=0, column=7)

        self.label_directory_store = Label(self.frame, text='文件存放文件夹')
        self.label_directory_store.grid(row=1, column=0)
        self.variable_directory = StringVar()
        self.entry_directory_store = Entry(self.frame, textvariable=self.variable_directory)
        self.entry_directory_store.grid(row=1, column=1)
        self.button_directory_store = Button(self.frame, text='选取文件夹',
                                             command=self.open_directory).grid(row=1,
                                                                               column=2,
                                                                               columnspan=2,
                                                                               sticky=E+W)
        self.label_district = Label(self.frame, text='独立处理')
        self.label_district.grid(row=1, column=4)
        self.entry_district = Entry(self.frame)
        self.entry_district.grid(row=1, column=5)

        self.button_process = Button(self.frame, text='开始处理', command=self.process)
        self.button_process.grid(row=2, column=6, columnspan=2, sticky=E+W)

        self.process_bar = ttk.Progressbar(self.frame, maximum=200)
        self.process_bar.grid(row=2, column=0, columnspan=6, sticky=E+W)
        self.window.mainloop()

    def open_directory(self):
        self.variable_directory.set(tkFileDialog.askdirectory())

    def process(self):
        host, name, password, data = self.entry_host.get(), self.entry_name.get(), self.entry_pass.get(), \
                                         self.entry_database.get()
        if not host:
            showwarning(title='警告', message='主机不能为空')
        elif not name:
            showwarning(title='警告', message='账户不能为空')
        elif not password:
            showwarning(title='警告', message='密码不能为空')
        elif not data:
            showwarning(title='警告', message='数据库不能为空')
        else:
            try:
                self.example = ReadDataToExcel(host, name, password, data)
                self.process_bar_handle()
            except Exception as e:
                print(e)

    def process_bar_handle(self):
        number_branches = self.example.return_total_number('0226160192')
        self.process_bar.config(maximum=number_branches)
        thread = threading.Thread(target=self.example.dispose_operation, args=('0226160192',))
        thread.start()
        while 1:
            self.maximum = self.example.return_total_count()
            self.process_bar.config(value=self.maximum)
            self.process_bar.update()

            if self.maximum == number_branches:
                self.example.close_connection()
                showinfo(title='通知', message='任务完成')
                break

if __name__ == '__main__':
    interface = InterfaceExportData()
