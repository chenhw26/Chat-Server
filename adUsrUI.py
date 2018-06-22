import tkinter
import tkinter.messagebox
import tkinter.ttk
import threading
import sqlite3
import DBUsr as Usr

class AdUsrUI(threading.Thread):
    '''管理单个用户的UI类'''
    def __init__(self, profile):
        super().__init__()
        self.usrid = str(profile[0])
        self.profile = profile
        
    def drawframe2(self):
        '''绘制frame2'''
        self.frame2 = tkinter.LabelFrame(
            self.frame1, borderwidth = 1, text = 'profile', labelanchor = 'n', bg = 'MintCream')

        self.id_title = tkinter.Label(
            self.frame2, width = 12, height = 1, text = 'UsrID:', anchor = 'w', bg = 'Mintcream')
        self.name_title = tkinter.Label(
            self.frame2, width = 12, height = 1, text = 'UsrName:', anchor = 'w', bg = 'Mintcream')
        self.psw_title = tkinter.Label(
            self.frame2, width=12, height=1, text='PassWord:', anchor='w', bg='Mintcream')
        self.state_title = tkinter.Label(
            self.frame2, width = 12, height = 1, text = 'State:', anchor = 'w', bg = 'Mintcream')

        self.real_id = tkinter.Label(
            self.frame2, width=12, height=1, text=str(self.profile[0]), anchor='e', bg='Mintcream')
        self.real_name = tkinter.Label(
            self.frame2, width=12, height=1, text=self.profile[1], anchor='e', bg='Mintcream')
        self.real_psw = tkinter.Label(
            self.frame2, width=12, height=1, text=self.profile[2], anchor='e', bg='Mintcream')
        self.real_state = tkinter.Label(
            self.frame2, width=12, height=1, text=str(self.profile[3]), anchor='e', bg='Mintcream')

        self.id_title.grid(row = 0, column = 0, padx = 10, pady = 15)
        self.name_title.grid(row=1, column=0, padx = 10, pady = 15)
        self.psw_title.grid(row=2, column=0, padx = 10, pady = 15)
        self.state_title.grid(row=3, column=0, padx=10, pady=15)

        self.real_id.grid(row = 0, column = 1, padx = 10, pady = 15)
        self.real_name.grid(row = 1, column = 1, padx = 10, pady = 15)
        self.real_psw.grid(row = 2, column = 1, padx = 10, pady = 15)
        self.real_state.grid(row=3, column=1, padx=10, pady=15)

        self.frame2.grid(row=0, column=0, padx=15, pady=15)

    def banAUsr(self):
        '''封禁一个用户'''
        confirm = tkinter.messagebox.askyesno(title = '封禁', message='你确定要封禁用户 ' + self.usrid + ' 吗?')
        if confirm:
            self.profile = self.profile[:3] + (True,)
            Usr.update_profile(self.profile, self.usrid)
            
            self.real_state.config(text = str(self.profile[3]))
            self.button1.config(state = 'disable')
            self.button2.config(state = 'normal')
            
            tkinter.messagebox.showinfo(title = '封禁', message='用户 ' + self.usrid + ' 已被封禁，现在该账户不能登录')

    def unbanAUsr(self):
        '''解封一个用户'''
        confirm = tkinter.messagebox.askyesno(
            title='解封', message='你确定要解封用户 ' + self.usrid + ' 吗?')
        if confirm:
            self.profile = self.profile[:3] + (False,)
            Usr.update_profile(self.profile, self.usrid)

            self.real_state.config(text=str(self.profile[3]))
            self.button1.config(state='normal')
            self.button2.config(state='disable')

            tkinter.messagebox.showinfo(title='解封', message='用户 ' + self.usrid + ' 已解封，现在该账户可以重新登录')

    def drawframe3(self):
        '''绘制frame3'''
        self.frame3 = tkinter.LabelFrame(
            self.frame1, text = 'operations', labelanchor = 'n', borderwidth = 1, bg = 'MintCream')

        self.button1 = tkinter.Button(self.frame3, width=12, text='封禁', relief=tkinter.GROOVE, fg='red', bg='LavenderBlush', 
                                      state='normal' if not self.profile[3] else 'disable', cursor='hand2', command=self.banAUsr)
        self.button2 = tkinter.Button(self.frame3, width=12, text='解封', relief=tkinter.GROOVE, 
                                      state='normal' if self.profile[3] else 'disable', cursor='hand2', command = self.unbanAUsr)

        self.button1.grid(row = 0, column = 0, padx = 62, pady = 14)
        self.button2.grid(row = 1, column = 0, padx = 62, pady = 14)

        self.frame3.grid(row=1, column=0, padx=15, pady=15)

    def showlist(self, listname):
        '''打印信息列表'''
        win = tkinter.Tk()
        sheet = tkinter.ttk.Treeview(win, height=10, show = 'headings', column = ('1', '2'))
        sheet.column('1', width=100, anchor = tkinter.CENTER)
        sheet.column('2', width=100, anchor=tkinter.CENTER)
        sheet.heading('1', text='ID')
        sheet.heading('2', text='name')

        if listname == 'friends':
            l = Usr.get_friends(self.profile[0])
        elif listname == 'groups':
            l = Usr.get_groups(self.profile[0])
        elif listname == 'black':
            l = Usr.get_black(self.profile[0])

        for item in l.items():
            sheet.insert('', tkinter.END, values = item)

        bar = tkinter.ttk.Scrollbar(
            win, command=sheet.yview, orient=tkinter.VERTICAL)
        sheet.config(yscrollcommand=bar.set)

        sheet.grid(row=0, column=0)
        bar.grid(row=0, column=1, sticky=tkinter.NS)
        win.mainloop()

    def showmoment(self):
        '''打印所有说说'''
        win = tkinter.Tk()
        sheet = tkinter.ttk.Treeview(win, height=10, show='headings', column=('1', '2'))
        sheet.column('1', width=200, anchor=tkinter.CENTER)
        sheet.column('2', width=200, anchor=tkinter.CENTER)
        sheet.heading('1', text='time')
        sheet.heading('2', text='content')

        l = Usr.get_moments(self.profile[0])
        for item in l.values():
            sheet.insert('', tkinter.END, values = item)

        bar = tkinter.ttk.Scrollbar(
            win, command=sheet.yview, orient=tkinter.VERTICAL)
        sheet.config(yscrollcommand=bar.set)

        sheet.grid(row=0, column=0)
        bar.grid(row=0, column=1, sticky=tkinter.NS)
        win.mainloop()

    def showrecord(self):
        '''显示用户所有聊天记录'''
        win = tkinter.Tk()
        sheet = tkinter.ttk.Treeview(win, height=10, show='headings', column=('1', '2', '3', '4'))
        sheet.column('1', width=150, anchor = tkinter.CENTER)
        sheet.column('2', width=75, anchor = tkinter.CENTER)        
        sheet.column('3', width=75, anchor = tkinter.CENTER)
        sheet.column('4', width=250, anchor = tkinter.CENTER)
        sheet.heading('1', text='time')
        sheet.heading('2', text='sender')
        sheet.heading('3', text='receiver')
        sheet.heading('4', text='content')

        allfriens = Usr.get_friends(self.profile[0])
        for friends in allfriens.keys():
            l = Usr.get_record(self.profile[0], friends)
            for item in l:
                sheet.insert('', tkinter.END, values = (item[2], item[1], item[2], item[3]))

        bar = tkinter.ttk.Scrollbar(
            win, command=sheet.yview, orient=tkinter.VERTICAL)
        sheet.config(yscrollcommand=bar.set)

        sheet.grid(row=0, column=0)
        bar.grid(row=0, column=1, sticky=tkinter.NS)
        win.mainloop()

    def drawframe4(self):
        '''绘制frame4'''
        self.frame4 = tkinter.LabelFrame(self.frame1, text = 'Detail', labelanchor = 'n', borderwidth = 1, bg = 'MintCream')

        self.button3 = tkinter.Button(self.frame4, text = 'Friends', relief = tkinter.GROOVE, 
                                      width = 15, cursor = 'hand2', command = lambda:self.showlist('friends'))
        self.button4 = tkinter.Button(self.frame4, text = 'Black', relief = tkinter.GROOVE, 
                                      width=15, cursor='hand2', command=lambda: self.showlist('black'))
        self.button5 = tkinter.Button(self.frame4, text='Groups', relief=tkinter.GROOVE, 
                                      width = 15, cursor = 'hand2', command = lambda:self.showlist('groups'))
        self.button6 = tkinter.Button(self.frame4, text='Moments', relief=tkinter.GROOVE, 
                                      width = 15, cursor = 'hand2', command = self.showmoment)
        self.button7 = tkinter.Button(self.frame4, text='Record', relief=tkinter.GROOVE, 
                                      width=15, cursor = 'hand2', command = self.showrecord)

        self.button3.grid(row = 0, column = 0, padx = 60, pady = 20)
        self.button4.grid(row = 1, column = 0, padx = 60, pady = 20)
        self.button5.grid(row = 2, column = 0, padx = 60, pady = 20)
        self.button6.grid(row = 3, column = 0, padx = 60, pady = 20)
        self.button7.grid(row = 4, column = 0, padx = 60, pady = 20)

        self.frame4.grid(row=0, column=1, rowspan=2, padx=15, pady=15)

    def run(self):
        '''启动管理用户UI'''
        self.root = tkinter.Tk()
        self.frame1 = tkinter.LabelFrame(self.root, text='User Management', labelanchor='n',
                                    font = ('calibri', 16), borderwidth = 4, height = 700, 
                                    width = 1300, bg = 'MintCream')
        self.drawframe2()
        self.drawframe3()
        self.drawframe4()
        self.frame1.grid()
        self.root.mainloop()
