from qiniu import Auth, put_file, etag
import os
from hashlib import md5
import qiniu.config
from upload_settings import bucket_name,domain,access_key,secret_key
from tkinter import Label, Entry, Button, RIGHT, LEFT, BOTTOM, TOP, Tk, Listbox, filedialog,Menu
from tkinter.ttk import Combobox
import tkinter as tk
import time

# 上传
def upload():
    global route, upload_list, completed_list,LB_LEFT,LB_RIGHT,tips_text,comboxlist
    # 需要填写你的 Access Key 和 Secret Key
    # 构建鉴权对象
    q = Auth(access_key, secret_key)  # 上传后保存的文件名
    key = route.get()
    upload_list_file = upload_list.get()
    bucket = comboxlist.get()
    for localfile in list(LB_LEFT.get(0,last=tk.END)):
        tips_text.set('正在上传'+localfile+'...')
        name,end = os.path.basename(localfile).split('.')
        print(name,end)
        m = md5(name.encode(encoding='utf-8')).hexdigest()
        real_name = key + time.strftime("%Y-%m-%d_%H-%M", time.localtime())  + '_' + m + '.' + end
        print(real_name)
        # 生成上传 Token，可以指定过期时间等
        token = q.upload_token(bucket, real_name, 3600)
        # 上传文件,返回状态
        ret, info = put_file(token, real_name, localfile)
        if ret['key'] == real_name and ret['hash'] == etag(localfile):
            LB_RIGHT.insert('end',domain+real_name)
    tips_text.set('全部上传完成!')

# 选择文件
def select_file():
    localfile = filedialog.askopenfilenames(title='选择上传文件')
    global LB_LEFT
    for file_name in localfile:
        LB_LEFT.insert('end', file_name)


top = Tk()
# key的值
route = tk.StringVar()
# 上传文件的列表
upload_list = tk.StringVar()
# 已上传完成的列表
completed_list = tk.StringVar()
# 下拉框自带的文本
comvalue=tk.StringVar()
# 提示字符串
tips_text = tk.StringVar()
tips_text.set('还没开始!')
top.title('上传文件')
top.geometry('950x650')

route.set('upload/imgages/')
L1 = Label(top, text="附加文件前缀:").place(x=335, y=30)
E1 = Entry(top, textvariable=route).place(x=450, y=30)
L2 = Label(top, text="需要上传的文件:").place(x=5, y=73)
L3 = Label(top, text="已上传的文件:").place(x=525, y=73)
L3 = Label(top, text="目标空间:").place(x=5, y=30)

# 左右ListBox
LB_LEFT = Listbox(top, listvariable=upload_list, selectmode="extended", height=20, width=43)
LB_RIGHT = Listbox(top, listvariable=completed_list, selectmode="browse", height=20, width=43)
LB_LEFT.place(x=5,y=100)
LB_RIGHT.place(x=525,y=100)

# 左列表横滚动条
scrollbar_LEFT = tk.Scrollbar(top,orient=tk.HORIZONTAL)
scrollbar_LEFT.place(x=5,y=524,width=390)
scrollbar_LEFT.config(command = LB_LEFT.xview )
LB_LEFT.config(xscrollcommand = scrollbar_LEFT.set)

# 右列表横滚动条
scrollbar_RIGHT = tk.Scrollbar(top,orient=tk.HORIZONTAL)
scrollbar_RIGHT.place(x=525,y=524,width=390)
scrollbar_RIGHT.config(command = LB_RIGHT.xview )
LB_RIGHT.config(xscrollcommand = scrollbar_RIGHT.set)

# 目标空间下拉框
comboxlist = Combobox(top,textvariable=comvalue)
comboxlist.place(x=85,y=30)
comboxlist['values'] = bucket_name
comboxlist.current(0)

button = Button(top, text='选择文件', command=select_file).place(x=650, y=20)
button = Button(top, text='全部上传', command=upload).place(x=427, y=300)
# 提示文本
tips = Label(top,bg='green',width=40,textvariable=tips_text).place(x=250,y=560)

# 右键菜单
class section:
    # def onPaste(self):
    #     try:
    #         self.text = root.clipboard_get()
    #     except TclError:
    #         pass
    #     show.set(str(self.text))

    def onCopy(self):
        self.text = LB_RIGHT.get(tk.ACTIVE)
        top.clipboard_append(self.text)

    # def onCut(self):
    #     self.onCopy()
    #     try:
    #         Entry.delete('sel.first', 'sel.last')
    #     except TclError:
    #         pass

section = section()
menu = Menu(top, tearoff=0)
menu.add_command(label="复制", command=section.onCopy)
menu.add_separator()
def popupmenu(event):
    menu.post(event.x_root, event.y_root)

# Mac系统
LB_RIGHT.bind("<Button-2>", popupmenu)

# Win系统
# LB_RIGHT.bind("<Button-3>", popupmenu)

top.mainloop()