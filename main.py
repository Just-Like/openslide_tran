# -*- coding: utf-8 -*-
# @Time    : 2019/11/3 22:08
# @Author  : Just
# @Email   : 1785780475@qq.com
# @File    : main.py
import tkinter
from UI.UI import UI
from UI.Cmdexe import Cmdexe
from Utiliy.Utiliy import Utiliy
from config import Config
import sys

if __name__ == '__main__':
    print(len(sys.argv))
    print(str(sys.argv))
    if len(sys.argv) == 1:
        root = tkinter.Tk()
        root.title(Config.main_win_title)
        root.update_idletasks()
        root.withdraw()
        root.geometry('%dx%d+%d+%d' % (Utiliy.getMsize(root)))
        root.deiconify()
        root.update()
        UI(root).pack()
        root.mainloop()
    else:
        blcheckno = sys.argv[1]
        file_path = sys.argv[2]
        print("病理号为："+blcheckno)
        print("玻片路径为："+file_path)
        cmd = Cmdexe(blcheckno, file_path)
        cmd.tran()