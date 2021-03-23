from os.path import isdir, join, splitext, getsize
from os import remove, listdir, curdir
from shutil import rmtree
from tkinter.simpledialog import askstring
from tkinter.filedialog import askdirectory
import tkinter as tk
import tkinter.scrolledtext
import re

filetypes = []  #指定要删除的文件后缀名类型
filefolders = []  #指定要删除的文件夹名称

def clear():  #清空滚动文本框内容
    outText.delete("0.0", "end")

def OpenF():  #打开文件夹按钮响应函数
    askdir = askdirectory()
    if askdir:
        EntryFolderPath.delete("0", "end")
        EntryFolderPath.insert("0",askdir)

def click():
    if SearchFilesVar.get() or SearchFoldersVar.get():  #如果有选中正则文件与文件夹的话弹出警告框
        s = askstring('Warning', prompt='正则表达式删除文件有风险，请先正则搜索文件是否有不想删除的！\n确认删除请输YES：', initialvalue='YES or NO?')
        if s != 'YES':
            return
    directory = EntryFolderPath.get()  #获取输入的文件夹路径
    global filetypes  #声明全局变量filetypes(文件后缀名)
    filetypes = EntryFilesPath.get().split(',')  #获取输入的文件后缀名生成list并赋给filetypes
    global filefolders  #声明全局变量filefolders(文件夹名)
    filefolders = EntryDelFolderPath.get().split(',')  #获取输入的文件夹生成list并赋给filefolders
    if directory == '':  #默认为当前文件夹
        directory = curdir
    delector(directory)  #调用delector函数删除文件与文件夹

def CppClick():  #删除C++调试文件checkbox的按钮绑定事件
    if CppVar.get():
        EntryDelFolderPath.delete("0", "end")  #先清空Entry内容
        EntryFilesPath.delete("0", "end")
        EntryDelFolderPath.insert("0",'Debug')  #C++调试后生成Debug文件夹
        EntryFilesPath.insert("0",'.ncb,.suo')  #C++调试后生成.ncb与.suo后缀文件
    else:
        EntryDelFolderPath.delete("0", "end") 
        EntryFilesPath.delete("0", "end") 

def delector(directory):
    if not isdir(directory):  #如果文件夹找不到(或格式错误)的话就提示文件夹输入错误输入错误并返回
        outText.insert(1.0,"文件夹输入错误！\n")
        return
    for fname in listdir(directory):  #迭代文件夹里的文件及文件夹
        temp = join(directory, fname)  #把迭代的文件或文件夹加入路径
        if isdir(temp):  #如果此文件或文件夹是文件夹
            if folderVar.get() and not listdir(temp):  #判断folder的checkbox有无选上,选上的话删除空文件夹
                delFolder(temp)
            elif fname in filefolders:  #判断该文件夹是否在filefolders里,是则删除此文件夹
                delFolder(temp)
            elif SearchFoldersVar.get() and search(fname):  #判断正则搜索文件夹的checkbox有无选上并正则匹配文件夹，匹配上删除
                delFolder(temp)
            else:
                delector(temp)  #递归调用delector(进入该文件夹内执行删除)
        elif splitext(temp)[-1] in filetypes:  #判断该文件后缀名是否在filetypes里,是则删除此文件
            delFiles(temp)
        elif SearchFilesVar.get() and search(fname):  #判断正则搜索文件的checkbox有无选上并正则匹配该文件，匹配上删除
            delFiles(temp)
        elif filesVar.get() and getsize(temp) == 0:  #判断files的checkbox有无选上,选上的话删除空文件
            delFiles(temp)

def PatternSearch():
    directory = EntryFolderPath.get()  #获取输入的文件夹路径
    if directory == '':  #默认为当前文件夹
        directory = curdir
    PatternSearchCore(directory)  #调用delector函数删除文件与文件夹

def PatternSearchCore(directory):
    if not isdir(directory):  #如果文件夹找不到(或格式错误)的话就提示文件夹输入错误输入错误并返回
        outText.insert(1.0,"文件夹输入错误！\n")
        return
    for fname in listdir(directory):  #迭代文件夹里的文件及文件夹
        temp = join(directory, fname)  #把迭代的文件或文件夹加入路径
        if isdir(temp):  #如果此文件或文件夹是文件夹
            if SearchFoldersVar.get() and search(fname):
                outText.insert(1.0,temp+" Searched.\n")
            else:
                PatternSearchCore(temp)  #递归调用PatternSearchCore(进入该文件夹内执行正则匹配)
        elif SearchFilesVar.get() and search(fname):
            outText.insert(1.0,temp+" Searched.\n")

def search(name):  #正则匹配搜索，匹配成功返回True
    pattern = EntrySearch.get()
    if re.match(pattern,name):
        return True

def delFiles(FileName):
    remove(FileName)
    outText.insert(1.0,FileName+" deleted.\n")

def delFolder(FolderName):
    rmtree(FolderName)
    outText.insert(1.0,FolderName+" deleted.\n")

root = tk.Tk()
filesVar = tk.IntVar(0)  #files的checkbox有无选上的标志
folderVar = tk.IntVar(0)  #folder的checkbox有无选上的标志
CppVar = tk.IntVar(0)  #Cpp的checkbox有无选上的标志
SearchFilesVar = tk.IntVar(0)  #正则搜索文件的checkbox有无选上的标志
SearchFoldersVar = tk.IntVar(0)  #正则搜索文件夹的checkbox有无选上的标志
root.title('Python小程序之删除特定文件与文件夹')
root.geometry('500x500')
lbFolderPath = tk.Label(root,text='请输入文件夹路径(默认当前文件夹)：')
lbFolderPath.place(relx=0.1,rely=0.05)
EntryFolderPath = tk.Entry(root)
EntryFolderPath.place(relx=0.1,rely=0.10,relwidth=0.8)
BtnOpenF = tk.Button(root,text="选择文件夹",command=OpenF)  #按钮控件绑定OpenF函数
BtnOpenF.place(relx=0.70,rely=0.05,relwidth=0.2,relheight=0.05)
lbFilesPath = tk.Label(root,text='请输入需删除文件的后缀名(例:.exe,.txt[删除多个用“,”隔开])：')
lbFilesPath.place(relx=0.1,rely=0.15)
EntryFilesPath = tk.Entry(root)
EntryFilesPath.place(relx=0.1,rely=0.20,relwidth=0.8)
lbDelFolderPath = tk.Label(root,text='请输入需删除的文件夹名(删除多个用“,”隔开)：')
lbDelFolderPath.place(relx=0.1,rely=0.25)
EntryDelFolderPath = tk.Entry(root)
EntryDelFolderPath.place(relx=0.1,rely=0.30,relwidth=0.8)
lbSearch = tk.Label(root,text='正则表达式：')
lbSearch.place(relx=0.1,rely=0.35,relwidth=0.2)
EntrySearch = tk.Entry(root)
EntrySearch.place(relx=0.3,rely=0.35,relwidth=0.6)
ChkBtnEmptyFolder = tk.Checkbutton(root,text='删除空文件夹',variable = folderVar,onvalue = 1,offvalue = 0)  #ChkBtnEmptyFolder绑定了folderVar值对象，选中时为1反之0
ChkBtnEmptyFolder.place(relx=0.10,rely=0.40)
ChkBtnEmptyFiles = tk.Checkbutton(root,text='删除空文件',variable = filesVar,onvalue = 1,offvalue = 0)
ChkBtnEmptyFiles.place(relx=0.35,rely=0.40)
ChkBtnCpp = tk.Checkbutton(root,text='删除C++调试文件',variable = CppVar,onvalue = 1,offvalue = 0,command=CppClick)  #Checkbox控件绑定CppClick函数
ChkBtnCpp.place(relx=0.6,rely=0.40)
ChkBtnSearchFiles = tk.Checkbutton(root,text='正则匹配文件',variable = SearchFilesVar,onvalue = 1,offvalue = 0)
ChkBtnSearchFiles.place(relx=0.2,rely=0.45)
ChkBtnSearchFolders = tk.Checkbutton(root,text='正则匹配文件夹',variable = SearchFoldersVar,onvalue = 1,offvalue = 0)
ChkBtnSearchFolders.place(relx=0.5,rely=0.45)
BtnDel = tk.Button(root,text="删除",command=click)  #按钮控件绑定click函数
BtnDel.place(relx=0.10,rely=0.50,relwidth=0.25)
BtnClear = tk.Button(root,text="清空文本",command=clear)  #按钮控件绑定clear函数
BtnClear.place(relx=0.4,rely=0.50,relwidth=0.2)
BtnSearch = tk.Button(root,text="正则搜索",command=PatternSearch)  #按钮控件绑定PatternSearch函数
BtnSearch.place(relx=0.65,rely=0.50,relwidth=0.25)
outText = tk.scrolledtext.ScrolledText(root, wrap=tk.WORD)  # wrap=tk.WORD   这个值表示在行的末尾如果有一个单词跨行，会将该单词放到下一行显示,比如输入hello，he在第一行的行尾,llo在第二行的行首, 这时如果wrap=tk.WORD，则表示会将 hello 这个单词挪到下一行行首显示, wrap默认的值为tk.CHAR
outText.place(relx=0.1,rely=0.60,relwidth=0.8,relheight=0.35)

root.mainloop()
