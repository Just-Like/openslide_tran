# -*- coding: utf-8 -*-
# @Time    : 2019/11/3 21:57
# @Author  : Just
# @Email   : 1785780475@qq.com
# @File    : ui.py
from tkinter import filedialog
from tkinter import Button
from tkinter import Label
from tkinter import Canvas
from tkinter import Entry
from tkinter import StringVar
from tkinter import CENTER
from Service import Convert
from config import Config
from Utiliy.Utiliy import Utiliy
from functools import partial
from requests_toolbelt import MultipartEncoder
import tkinter
import threading
import os
import filetype
import requests


class UiUtiliy(Utiliy):
    pass


class UI(tkinter.Frame):
    def __init__(self, root):
        tkinter.Frame.__init__(self, root)

        frame_main = tkinter.Frame()
        frame_input = tkinter.Frame(frame_main)
        frame_upload_radiobutton = tkinter.Frame(frame_main)
        self.root = root
        self.x = StringVar()
        self.radiobuttonvar = tkinter.IntVar(value=-1)
        self.convert = Convert.Convert(UiUtiliy)
        self.select_button = Button(self, text='选择玻片', width=100, height=50, command=self.askopenfilename)
        self.tran_finsh_lable = Label(self, text='玻片格式转换完成，正在上传服务器！', width=120, height=50)
        self.input = Entry(frame_input)
        self.input_lable = Label(frame_input, text="病理号: ", width=5, height=5,padx=20)
        self.canvas_progress_bar = Canvas(width=120, height=30)
        self.canvas_progress_bar.place(relx=0.45, rely=0.4, anchor=CENTER)
        self.radiobutton_upload = tkinter.Radiobutton(frame_upload_radiobutton, text='上传服务器', variable=self.radiobuttonvar, value=1)
        self.radiobutton_not_upload = tkinter.Radiobutton(frame_upload_radiobutton, text='不上传服务器', variable=self.radiobuttonvar, value=-1)
        self.lable = Label(self, textvariable=self.x)
        self.input.pack(side="right")
        self.input_lable.pack(side="left")
        self.select_button.pack()
        self.radiobutton_upload.pack(side=tkinter.RIGHT)
        self.radiobutton_not_upload.pack(side=tkinter.RIGHT)
        self.out_rec = None
        self.fill_rec = None
        frame_main.pack()
        frame_input.pack()
        frame_upload_radiobutton.pack()

    def askopenfilename(self):
        input_value = self.input.get()
        if self.radiobuttonvar.get() == 1 and not input_value:
            UiUtiliy.messageError("错误", "请先填写病理号！！")
            return
        ext = list(map(lambda ext: (ext.replace("*.", ''), ext), Config.support_ext))
        path = filedialog.askopenfilename(title='玻片文件', filetypes=ext)
        if os.path.exists(path):
            self.root.title("正在转换中..........")
            self.select_button['text'] = '玻片正在转换中请耐心等待'
            tran_thr = threading.Thread(target=self.tran_ui, args=(path,))
            tran_thr.start()
        else:
            UiUtiliy.messageError("提示", "该文件不存在请重新上传")

    def callback(self, monitor, png_size):
        out_rec = self.canvas_progress_bar.create_rectangle(5, 5, 105, 25, outline="blue", width=1)
        fill_rec = self.canvas_progress_bar.create_rectangle(5, 5, 5, 25, outline="", width=0, fill="blue")
        progress_num = (monitor.bytes_read / png_size) * 100
        progress_str = str(round(progress_num, 2)) + "%"
        print(progress_str)
        self.root.update()
        self.x.set(progress_str)
        self.canvas_progress_bar.coords(fill_rec, (5, 5, 6 + progress_num, 25))
        if self.out_rec is not None:
            self.canvas_progress_bar.delete(self.out_rec)
            self.canvas_progress_bar.delete(self.fill_rec)
        self.out_rec = out_rec
        self.fill_rec = fill_rec

    def tran_ui(self, path):
        self.select_button['text'] = '选择玻片'
        self.root.title(Config.main_win_title)
        self.select_button.pack_forget()
        self.tran_finsh_lable['text'] = "玻片正在转换中请耐心等待............"
        self.tran_finsh_lable.pack()
        input_value = self.input.get()
        kind = filetype.guess(path)
        file_mime = kind.mime
        if file_mime != "image/png":
            png_path = self.convert.tran(path)
        else:
            png_path = path
        if self.radiobuttonvar.get() == 1:
            self.tran_finsh_lable['text'] = "玻片格式转换完成，正在上传服务器！"
            png_size = os.path.getsize(png_path)
            config = UiUtiliy.get_config_object()
            upload_url = config.get('upload', 'url')
            fields = {
                "blcheckno": input_value,
                "file": ("img.png", open(png_path, "rb")),
            }
            multipart_data = MultipartEncoder(fields=fields, boundary='---------------------------7de1ae242c06ca')
            try:
                upload_response = UiUtiliy.upload_by_chunk(multipart_data, upload_url, partial(self.callback, png_size=png_size))
                upload_result = upload_response.json()
                print(upload_result)
                if upload_result:
                    if upload_result['code'] == 0:
                        UiUtiliy.messageInfo("提示", "文件已上传至服务器！！")
                    elif upload_result['code'] < 0:
                        UiUtiliy.messageError("错误", upload_result["msg"])
            except requests.exceptions.ConnectionError:
                UiUtiliy.messageError("错误", "上传服务器失败 请检查网络是否正常")
        self.tran_finsh_lable.pack_forget()
        self.select_button.pack()
        self.input.delete(0, "end")



