#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Ui_mw import *
import re
from dowload_dplayer import loop_download

import sys
import os

__author__ = "chenyansu"

class Run():
    """
    后端与UI结合
    可以使用qt设计师随意更改ui样式,但是不能更改相关组件名称。
    """

    def __init__(self):
        # ScrapydTools.__init__(self, baseUrl=baseUrl)
        super().__init__()
        self.s_r_counter = 0
        self.message = "欢迎使用小王霸下载器，如有疑问请联系aschenyansu@foxmail.com" # 显示在主窗口的信息
        self.open_ui()
        self.Ui_register()
        self.close_ui()

    def open_ui(self):
        """ 打开Ui绘制 """
        self.app = QtWidgets.QApplication(sys.argv)
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        self.MainWindow.show()

    def close_ui(self):
        """ 关闭Ui绘制 """
        sys.exit(self.app.exec_())

    def Ui_register(self):
        """ 交互式Ui注册 """
        self.show_message() # 注册显示器
        self.button_register() # 注册按钮
        pass

    def show_message(self):
        """ 注册显示器 """
        self.ui.display_textBrowser.setText(self.message)

    def button_register(self):
        """ 按钮注册 """
        self.ui.add_task_pushButton.clicked.connect(self.add_task_pushButton_func)
        self.ui.quick_insert_pushButton.clicked.connect(self.quick_insert_pushButton_func)
        self.ui.analyse_url_pushButton.clicked.connect(self.analyse_url_pushButton_func)
        self.ui.add_history_pushButton.clicked.connect(self.add_history_pushButton_func)
        self.ui.clean_history_pushButton.clicked.connect(self.clean_history_pushButton_func)
        self.ui.delete_a_history_pushButton.clicked.connect(self.delete_a_history_pushButton_func)
        self.ui.clear_display_pushButton.clicked.connect(self.clear_display_pushButton_func)


    def add_task_pushButton_func(self):
        """ 添加任务按钮"""
        base_url = self.ui.base_url_lineEdit.text()
        prefix = ""
        postfix = self.ui.postfix_lineEdit.text()
        amount = int(self.ui.amount_lineEdit.text())
        out = self.ui.name_lineEdit.text()
        finish = int(self.ui.finish_num_lineEdit.text())
        if self.add_task_check(base_url, out, amount, finish, postfix) == False:
            print("错误，请重新输入")
            return -1
        # 执行命令
        self.run_on_cmd(base_url, out, amount, finish, postfix)
        # 添加历史任务进入下拉栏
        self.add_history_to_combox(base_url, out, amount, finish, postfix)
        # 显示信息
        url = base_url + str(amount) + postfix
        self.ui.display_textBrowser.append('["{}", "{}"]'.format(url, out))
        # 取消提示
        self.ui.warning_label.setText("")
        self.ui.warning_label.setStyleSheet("background-color:transparent;")
        self.ui.finish_num_lineEdit.setStyleSheet("background-color:rgb(255,255,255);")
        # 恢复状态
        self.back()

    def back(self):
        """ 清除除了下拉列表外的数据"""
        self.ui.url_lineEdit.setText("")
        self.ui.quick_insert_lineEdit.setText("")
        self.ui.base_url_lineEdit.setText("")
        self.ui.amount_lineEdit.setText("1")
        self.ui.finish_num_lineEdit.setText("-1")
        self.ui.name_lineEdit.setText("")


    def run_on_cmd(self, base_url, out, amount, finish, postfix):
        """ 在cmd执行命令"""
        os.system('start cmd /k "python dowload_dplayer.py {} {} {} {} {}"'.format(base_url, out, amount, finish, postfix))
        # os.system('start cmd ')


    def analyse_url(self, url):
        """ 将url拆分为base_url， 后缀名，总数"""
        postfix = os.path.splitext(url)[-1]
        a = os.path.splitext(url)[0]
        amount_str = re.findall("\d{3}", a)[-1]
        base_url = a[0:len(a)-len(amount_str)]
        return postfix, base_url, amount_str

    def quick_insert_pushButton_func(self):
        """ 快速插入下添加任务按钮以字典形式传递参数"""
        if self.quick_insert_check(self.ui.quick_insert_lineEdit.text()) == False:
            return -1
        args = eval(self.ui.quick_insert_lineEdit.text())
        self.quick_insert(args)
        # 增加提示颜色
        self.warning_finish_num()

    def quick_insert(self, args):
        """ 解析"""
        # 填入postfix, base_url, amount
        url = args[0]
        self.auto_write(url)
        # 填入影片名
        self.ui.name_lineEdit.setText(args[1])

    def auto_write(self, url):
        """ 将analyse_url结果填入相应输入框"""
        postfix, base_url, amount = self.analyse_url(url)
        self.ui.postfix_lineEdit.setText(postfix)
        self.ui.base_url_lineEdit.setText(base_url)
        self.ui.amount_lineEdit.setText(amount)


    def analyse_url_pushButton_func(self):
        """ 分析按钮"""
        url = self.ui.url_lineEdit.text()
        self.auto_write(url)


    def add_history_to_combox(self, base_url, out, amount, finish, postfix):
        """ 添加历史任务到历史任务下拉框"""
        url = base_url + str(amount) + postfix
        args = '["{}", "{}"]'.format(url, out)
        # 去重加入
        exist = 0
        for i in range(self.ui.history_comboBox.count()):
            if args == self.ui.history_comboBox.itemText(i):
                exist = 1
        if exist == 0:
            self.ui.history_comboBox.addItem(args)

    def add_history_pushButton_func(self):
        """ 导入历史记录"""
        args = eval(self.ui.history_comboBox.currentText())
        # print(args)
        self.quick_insert(args)
        # 增加提示颜色
        self.warning_finish_num()


    def clean_history_pushButton_func(self):
        """ 清除所有记录 """
        self.ui.history_comboBox.clear()

    def delete_a_history_pushButton_func(self):
        """ 删除当前历史记录"""
        currentIndex = self.ui.history_comboBox.currentIndex()
        self.ui.history_comboBox.removeItem(currentIndex)

    def warning_finish_num(self):
        # 提示
        self.ui.warning_label.setText("注意修改完成任务数")
        self.ui.warning_label.setStyleSheet("background-color:rgb(255,0,0);" )
        self.ui.finish_num_lineEdit.setStyleSheet("background-color:rgb(255,0,0);")

    def clear_display_pushButton_func(self):
        """ 清除显示窗口"""
        self.ui.display_textBrowser.clear()
        self.back()

    ####################
    #输入检验函数#
    ####################
    def analyse_url_check(self):
        pass

    def quick_insert_check(self, args):
        """ 检验快速插入"""
        try:
            args = eval(args)
        except:
            self.ui.display_textBrowser.append("快速插入的不是一个列表")
            return False
        if type(args) is not list:
            self.ui.display_textBrowser.append("快速插入的不是一个列表")
            return False
        if len(args) < 2:
            self.ui.display_textBrowser.append("快速插入列表长度过短")
            return False

    def add_task_check(self, base_url, out, amount, finish, postfix):
        """ 检验添加任务按钮"""
        if not base_url:
            self.ui.display_textBrowser.append("缺失base_url")
            return False
        if not out:
            self.ui.display_textBrowser.append("缺失保存名称")
            return False
        if int(finish) > int(amount):
            self.ui.display_textBrowser.append("已完成数大于总数")
            return False



if __name__ == "__main__":
    a = Run()