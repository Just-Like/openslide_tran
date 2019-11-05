# -*- coding: utf-8 -*-
# @Time    : 2019/11/3 21:45
# @Author  : Just
# @Email   : 1785780475@qq.com
# @File    : Utiliy.py

import tkinter
import time
from tkinter import messagebox
from config import Config


class Utiliy:
    @staticmethod
    def messageInfo(title, content):
        messagebox.showinfo(title, content)

    @staticmethod
    def messageError(title, content):
        messagebox.showerror(title, content)

    @staticmethod
    def getMsize(root:tkinter):
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        return Config.main_win_width, Config.main_win_height, (screenwidth - Config.main_win_width) / 2, (screenheight - Config.main_win_height) / 2

    @staticmethod
    def gefName(file_name, file_ext):
        return file_ext+'-'+time.strftime('%Y%m%d-%H%M%S', time.localtime(time.time()))


