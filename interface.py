# encoding:utf-8

# TODO 界面继续完善
# TODO 与实际功能结合

from Tkinter import *
import tkFileDialog
import tkMessageBox
from main import ReadDataToExcel


class InterfaceExportData(object):
    def __init__(self):
        self.window = Tk()
        self.window.title('数据库导出系统')
        self.window.iconbitmap('./favicon.ico')

        self.frame = Frame(self.window)
        self.frame.pack()

        self.label_host = Label(self.frame, text='主机').grid(row=0, column=0)
        self.label_name = Label(self.frame, text='账户').grid(row=0, column=2)
        self.label_pass = Label(self.frame, text='密码').grid(row=0, column=4)
        self.label_database = Label(self.frame, text='数据库').grid(row=0, column=6)

        self.entry_host = Entry(self.frame).grid(row=0, column=1)
        self.entry_name = Entry(self.frame).grid(row=0, column=3)
        self.entry_pass = Entry(self.frame).grid(row=0, column=5)
        self.entry_database = Entry(self.frame).grid(row=0, column=7)

        self.label_directory_store = Label(self.frame, text='文件存放文件夹').grid(row=1, column=0)
        self.variable_directory = StringVar()
        self.entry_directory_store = Entry(self.frame, textvariable=self.variable_directory).grid(row=1,
                                                                                                  column=1,
                                                                                                  columnspan=5,
                                                                                                  sticky=E+W)
        self.button_directory_store = Button(self.frame, text='选取文件夹',
                                             command=self.open_directory).grid(row=1,
                                                                               column=6,
                                                                               columnspan=2,
                                                                               sticky=E+W)

        self.window.mainloop()
        # self.handle = ReadDataToExcel()
        # print(self.handle.information)

    def open_directory(self):
        self.variable_directory.set(tkFileDialog.askdirectory())

if __name__ == '__main__':
    interface = InterfaceExportData()
