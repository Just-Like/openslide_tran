# -*- coding: utf-8 -*-
# @Time    : 2019/11/3 21:57
# @Author  : Just
# @Email   : 1785780475@qq.com
# @File    : ui.py
from tkinter import filedialog
from Service import Convert
from config import Config
import tkinter


class UI(tkinter.Frame):
    def __init__(self, root):
        self.root = root
        self.convert = Convert.Convert()
        tkinter.Frame.__init__(self, root)
        tkinter.Button(self, text='选择玻片',width=100,height=50, command=self.askopenfilename).pack()

    def askopenfilename(self):
        ext = list(map(lambda ext: (ext.replace("*.", ''), ext), Config.support_ext))

        path = filedialog.askopenfilename(title='玻片文件', filetypes=ext)
        if not path:
            return
        self.root.title("正在转换中..........")
        self.convert.tran(path)


