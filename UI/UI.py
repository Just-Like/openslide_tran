# -*- coding: utf-8 -*-
# @Time    : 2019/11/3 21:57
# @Author  : Just
# @Email   : 1785780475@qq.com
# @File    : ui.py
from tkinter import filedialog
from tkinter import Button
from Service import Convert
from config import Config
from Utiliy.Utiliy import Utiliy
import tkinter
import threading
import os


class UI(tkinter.Frame):
    def __init__(self, root):
        tkinter.Frame.__init__(self, root)

        self.root = root
        self.convert = Convert.Convert()
        self.select_button = Button(self, text='选择玻片', width=100, height=50, command=self.askopenfilename)
        self.select_button.pack()

    def askopenfilename(self):
        ext = list(map(lambda ext: (ext.replace("*.", ''), ext), Config.support_ext))
        path = filedialog.askopenfilename(title='玻片文件', filetypes=ext)
        if os.path.exists(path):
            self.root.title("正在转换中..........")
            self.select_button['text'] = '玻片正在转换中请耐心等待'
            tran_thr = threading.Thread(target=self.tran_ui, args=(path,))
            tran_thr.start()
        else:
            Utiliy.messageError("提示", "该文件不存在请重新上传")

    def tran_ui(self, path):
        self.convert.tran(path)
        self.select_button['text'] = '选择玻片'
        self.root.title(Config.main_win_title)
        png_path = os.getcwd() + '\\pngs'
        os.startfile(png_path)


