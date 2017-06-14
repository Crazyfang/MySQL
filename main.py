#!/usr/bin/python
# -*- coding: UTF-8 -*-

# TODO 添加批量化导出excel功能
# TODO 加界面
# TODO 尝试多进程操作

import MySQLdb
import xlrd
import xlwt
import xlsxwriter


class ReadDataToExcel(object):
    def __init__(self, host='localhost', data_name='root', data_password=None, database='stock'):
        try:
            self.__host = host
            self.__data_name = data_name
            self.__data_password = data_password
            self.__database_name = database
            self.db = None
            self.cursor = None
            self.count = 0
            self.district = []
            self.information = [u'股份经济合作社名称',
                                u'股东姓名',
                                u'性别',
                                u'户主姓名',
                                u'户主身份证号',
                                u'成员身份证号',
                                u'与户主关系',
                                u'股东性质',
                                u'人口股',
                                u'农龄股',
                                u'股份总数',
                                u'行政区编号']

            if not self.__host and self.__data_name and self.__data_password:
                raise ValueError
            self.connect_mysql()
        except ValueError:
            print("数据库参数输入错误，请核查")

    def connect_mysql(self):
        try:
            self.db = MySQLdb.connect(self.__host, self.__data_name, self.__data_password, self.__database_name,
                                      charset='utf8')
            self.cursor = self.db.cursor()
        except Exception:
            print('数据库打开错误，请重新核对参数再次尝试')

    def get_district(self):
        sql = "SELECT DISTINCT(stockmemberinfo.District) FROM stockmemberinfo"
        if self.cursor:
            try:
                # 执行SQL语句
                self.cursor.execute(sql)
                # 获取所有记录列表
                self.district = self.cursor.fetchall()
                print("区号列表为：")
                for i in self.district:
                    print i[0]
            except Exception:
                print("错误：没有获取到区号数据")

    def get_district_data_self(self, district=None):
        if not district:
            for index, area_code in enumerate(self.district):
                if index <= 2:
                    print('区号{}开始获取数据'.format(area_code[0]))
                    self.get_district_data(area_code[0])
                else:
                    pass
        else:
            print('区号{}开始获取数据'.format(district))
            self.get_district_data(district)

    def get_district_data(self, district):
        sql = 'SELECT * FROM stockmemberinfo WHERE stockmemberinfo.District={}'.format(district)
        if self.cursor:
            try:
                self.cursor.execute(sql)
            except Exception:
                print("错误：通过区号获取数据失败")
            self.write_to_excel(self.cursor.fetchall())

    def write_to_excel(self, data):
        try:
            file_path = u'./{}.xlsx'.format(data[0][1])
            files = xlsxwriter.Workbook(file_path)
            table = files.add_worksheet(u'成员信息表')
            for index, item in enumerate(self.information):
                table.write(0, index, item)
            for index_first, data_item_all in enumerate(data):
                for index_second, data_item in enumerate(data_item_all):
                    if index_second != 0:
                        table.write(index_first + 1, index_second - 1, data_item)
                    else:
                        pass
                self.count += 1
            print(file_path + u'写入完成')
        except Exception as e:
            print(e)

    def dispose_operation(self, district=None):
        if district:
            self.get_district_data_self(district)
        else:
            self.get_district()
            self.get_district_data_self()

    def return_total_number(self, district=None):
        count = 0
        if not district:
            self.get_district()
            for index, area_code in enumerate(self.district):
                if index <= 2:
                    sql = 'SELECT count(*) FROM stockmemberinfo WHERE stockmemberinfo.District={}'.format(area_code[0])
                    if self.cursor:
                        try:
                            self.cursor.execute(sql)
                            count += self.cursor.fetchall()[0][0]
                        except Exception:
                            print("错误：通过区号获取数据失败")
                else:
                    pass
        else:
            sql = 'SELECT count(*) FROM stockmemberinfo WHERE stockmemberinfo.District={}'.format(district)
            if self.cursor:
                try:
                    self.cursor.execute(sql)
                    count += self.cursor.fetchall()[0][0]
                except Exception:
                    print("错误：通过区号获取数据失败")
        return count

    def return_total_count(self):
        return self.count

    def close_connection(self):
        self.db.close()


if __name__ == '__main__':
    example = ReadDataToExcel('localhost', 'root', 'fighting', 'stock')
    # example.connect_mysql()
    # example.write_to_excel()
    # example.get_district()
    # example.get_district_data_self()
    # example.get_district_data('0226160172')
    print example.return_total_number('0226160172')
    example.close_connection()
