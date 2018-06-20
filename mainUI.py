import tkinter
from tkinter import ttk
import tkinter.messagebox
import time
import adUsrUI
import adGroupUI
import threading
import os
import json

class MainUI(threading.Thread):
    '''显示管理窗口'''
    def __init__(self, onlinesocket, usr_locks, usr_locks_lock, group_locks, group_locks_lock):
        super().__init__()
        self.onlinesocket = onlinesocket
        self.usr_locks = usr_locks
        self.usr_locks_lock = usr_locks_lock
        self.group_locks = group_locks
        self.group_locks_lock = group_locks_lock

    def drawframe4(self):
        '''绘制frame4'''
        self.frame4 = tkinter.Frame(self.frame2, bg = "MintCream")
        self.subtitle1 = tkinter.Label(
        self.frame4, width=20, height=2, text="All Users", font=('calibri', 20), bg="MintCream")
        self.button1 = tkinter.Button(
            self.frame4, text="Refresh", width=6, relief=tkinter.GROOVE, bg='Azure', cursor='hand2', command=self.getUsrSheetItems)
        self.subtitle1.grid(column=0, row=0)
        self.button1.grid(column=1, row=0)
        self.frame4.grid(row=0, pady=10)

    def getUsrSheetItems(self):
        '''更新用户列表'''
        allitems = self.sheet1.get_children()
        for item in allitems:
            self.sheet1.delete(item)

        allUsr = os.listdir('usr')
        for usr in allUsr:
            with open('usr\\' + usr + '\\profile.txt') as fp:
                profile = json.load(fp)
                self.sheet1.insert('', tkinter.END, values = (profile[0], profile[1], profile[3], 
                                                              'yes' if int(usr) in self.onlinesocket else 'no'))

    def drawframe8(self):
        '''绘制frame8'''
        self.frame8 = tkinter.Frame(self.frame2, bg="MintCream")

        self.sheet1 = ttk.Treeview(self.frame8, height=10, show="headings",
                                   column=('1', '2', '3', '4'))
        self.sheet1.column('1', width=87, anchor = tkinter.E)
        self.sheet1.column('2', width=87, anchor = tkinter.E)
        self.sheet1.column('3', width=87, anchor = tkinter.E)
        self.sheet1.column('4', width=87, anchor=tkinter.E)
        self.sheet1.heading('1', text='id')
        self.sheet1.heading('2', text='name')
        self.sheet1.heading('3', text='state')
        self.sheet1.heading('4', text='online')

        self.getUsrSheetItems()

        self.bar1 = ttk.Scrollbar(self.frame8, command=self.sheet1.yview, orient=tkinter.VERTICAL)
        self.sheet1.configure(yscrollcommand=self.bar1.set)

        self.sheet1.grid(row=0, column=0)
        self.bar1.grid(row=0, column=1, sticky=tkinter.NS)
        self.frame8.grid(row=1, pady=10)

    def getUsrDetail(self):
        '''查看一个用户详细信息，启动AdUsrUI类'''
        usrid = self.inputbar1.get()
        try:
            with open('usr\\' + usrid + '\\profile.txt') as fp:
                profile = json.load(fp)
                subUI = adUsrUI.AdUsrUI(profile, self.usr_locks, self.usr_locks_lock)
                subUI.start()
        except:
            tkinter.messagebox.showerror(title='Error', message='UserID:' + usrid + ' doesn\'t exist!')

    def drawframe6(self):
        '''绘制frame6'''
        self.frame6 = tkinter.Frame(self.frame2, bg="MintCream")
        self.inputbar1 = tkinter.Entry(self.frame6, width=30)
        self.inputbar1.insert(0, '输入id以查看详情')
        self.button3 = tkinter.Button(self.frame6, width=6, height=1, text='Enter',
                                 relief=tkinter.GROOVE, bg='Azure', cursor='hand2', 
                                 command = self.getUsrDetail)
        self.inputbar1.grid(row=0, column=0, padx=10, sticky=tkinter.W)
        self.button3.grid(row=0, column=1, padx=10, sticky=tkinter.E)
        self.frame6.grid(row=2, pady=10)

    def drawframe2(self):
        '''绘制frame2'''
        self.frame2 = tkinter.LabelFrame(self.frame1, bg="MintCream", borderwidth=1)
        self.drawframe4()
        self.drawframe8()
        self.drawframe6()
        self.frame2.grid(row=0, column=0, padx=30, pady=30)

    def drawframe5(self):
        '''绘制frame5'''
        self.frame5 = tkinter.Frame(self.frame3, bg="MintCream")

        self.subtitle2 = tkinter.Label(
            self.frame5, width=20, height=2, text="All Groups", font=('calibri', 20), bg="MintCream")
        self.button2 = tkinter.Button(
            self.frame5, text="Refresh", width=6, relief=tkinter.GROOVE, bg='Azure', cursor='hand2', command = self.getGroupSheetItems)
        self.subtitle2.grid(column=0, row=0)
        self.button2.grid(column=1, row=0)
        self.frame5.grid(row=0, pady=10)

    def getGroupSheetItems(self):
        '''更新所有群组列表'''
        allitems = self.sheet2.get_children()
        for item in allitems:
            self.sheet2.delete(item)

        allGroup = os.listdir('group')
        for group in allGroup:
            with open('group\\' + group + '\\profile.txt') as fp:
                profile = json.load(fp)
                self.sheet2.insert('', tkinter.END, values=profile)


    def drawframe9(self):
        '''绘制frame9'''
        self.frame9 = tkinter.Frame(self.frame3, bg="MintCream")

        self.sheet2 = ttk.Treeview(self.frame9, height=10, show="headings",
                                   column=('1', '2', '3'))
        self.sheet2.column('1', width=116, anchor = tkinter.E)
        self.sheet2.column('2', width=116, anchor = tkinter.E)
        self.sheet2.column('3', width=116, anchor=tkinter.E)
        self.sheet2.heading('1', text='id')
        self.sheet2.heading('2', text='name')
        self.sheet2.heading('3', text='state')
        
        self.getGroupSheetItems()

        self.bar2 = ttk.Scrollbar(self.frame9, command=self.sheet2.yview, orient=tkinter.VERTICAL)
        self.sheet2.configure(yscrollcommand=self.bar2.set)

        self.sheet2.grid(row=0, column=0)
        self.bar2.grid(row=0, column=1, sticky=tkinter.NS)
        self.frame9.grid(row=1, pady=10)

    def getGroupDetail(self):
        '''查看群组详细信息，启动adGroupUI类'''
        groupid = self.inputbar2.get()
        try:
            with open('group\\' + groupid + '\\profile.txt') as fp:
                profile = json.load(fp)
                subUI = adGroupUI.AdGroupUI(
                    profile, self.group_locks, self.group_locks_lock)
                subUI.start()
        except:
            tkinter.messagebox.showerror(
                title='Error', message='GroupID:' + groupid + ' doesn\'t exist!')

    def drawframe7(self):
        '''绘制frame7'''
        self.frame7 = tkinter.Frame(self.frame3, bg="MintCream")
        self.inputbar2 = tkinter.Entry(self.frame7, width=30)
        self.inputbar2.insert(0, '输入id以查看详情')
        self.button4 = tkinter.Button(self.frame7, width=6, height=1, text='Enter',
                                 relief=tkinter.GROOVE, bg='Azure', cursor='hand2', 
                                 command = self.getGroupDetail)
        self.inputbar2.grid(row=0, column=0, padx = 10, sticky = tkinter.W)
        self.button4.grid(row=0, column=1, padx=10, sticky=tkinter.E)
        self.frame7.grid(row=2, pady=10)

    def drawframe3(self):
        '''绘制frame3'''
        self.frame3 = tkinter.LabelFrame(self.frame1, bg="MintCream", borderwidth=1)
        self.drawframe5()
        self.drawframe9()
        self.drawframe7()
        self.frame3.grid(row=0, column=1, padx=30, pady = 30)

    def run(self):
        '''启动主管理窗口'''
        self.root = tkinter.Tk()
        self.frame1 = tkinter.LabelFrame(self.root, text='Administrator', labelanchor='n', font=('calibri', 12),
                                    borderwidth = 4, height=700, width=1300, bg='MintCream')
        self.drawframe2()
        self.drawframe3()
        self.frame1.grid()
        self.root.mainloop()
