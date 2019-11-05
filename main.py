# -*- coding: utf-8 -*-
# @Time    : 2019/11/3 22:08
# @Author  : Just
# @Email   : 1785780475@qq.com
# @File    : main.py
import tkinter
from UI.UI import UI
from Utiliy.Utiliy import Utiliy
from config import Config

if __name__ == '__main__':
    root = tkinter.Tk()
    root.title(Config.main_win_title)
    root.update_idletasks()
    root.withdraw()
    root.geometry('%dx%d+%d+%d' % (Utiliy.getMsize(root)))
    root.deiconify()
    root.update()
    UI(root).pack()
    root.mainloop()
