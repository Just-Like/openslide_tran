# -*- coding: utf-8 -*-
# @Time    : 2019/11/3 21:57
# @Author  : Just
# @Email   : 1785780475@qq.com
# @File    : ui.py
from gevent import monkey
monkey.patch_socket()
import gevent
from tkinter import filedialog
from tkinter import Button
from tkinter import Label
from tkinter import Canvas
from multiprocessing import Process
from tkinter import StringVar
from tkinter import NW,CENTER
from Service import Convert
from config import Config
from Utiliy.Utiliy import Utiliy
import tkinter
import threading
import requests
import time
import os


class UI(tkinter.Frame):
    def __init__(self, root):
        tkinter.Frame.__init__(self, root)

        self.root = root
        self.convert = Convert.Convert()
        self.select_button = Button(self, text='选择玻片', width=100, height=50, command=self.askopenfilename)
        self.tran_finsh_lable = Label(self, text='玻片格式转换完成，准备上传至服务器！', width=100, height=50)
        self.canvas_progress_bar = Canvas(width=100, height=20)
        self.canvas_progress_bar.place(relx=0.45, rely=0.4, anchor=CENTER)
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
        png_path = self.convert.tran(path)
        self.select_button['text'] = '选择玻片'
        self.root.title(Config.main_win_title)
        self.select_button.pack_forget()
        self.tran_finsh_lable.pack()
        upload_response = Utiliy.upload_by_chunk(png_path)
        if upload_response.json():
            if upload_response.json()['msg'] == 'success':
                Utiliy.messageInfo("提示", "文件已上传至服务器！！")
                self.tran_finsh_lable.pack_forget()
                self.select_button.pack()


