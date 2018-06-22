import tkinter
import tkinter.ttk
import threading
import DBGroup as Group

class AdGroupUI(threading.Thread):
    '''管理群组的UI类'''
    def __init__(self, profile):
        super().__init__()
        self.groupid = int(profile[0])
        self.profile = profile
    
    def drawframe2(self):
        '''绘制frame2'''
        self.frame2 = tkinter.LabelFrame(
            self.frame1, borderwidth=1, text='profile', labelanchor='n', bg='MintCream')

        self.id_title = tkinter.Label(self.frame2, width=12, height=1,
                                 text='UsrID:', anchor='w', bg='Mintcream')
        self.name_title = tkinter.Label(
            self.frame2, width=12, height=1, text='UsrName:', anchor='w', bg='Mintcream')
        self.state_title = tkinter.Label(
            self.frame2, width=12, height=1, text='State:', anchor='w', bg='Mintcream')

        self.real_id = tkinter.Label(self.frame2, width=12, height=1,
                                text=self.groupid, anchor='e', bg='Mintcream')
        self.real_name = tkinter.Label(
            self.frame2, width=12, height=1, text=self.profile[1], anchor='e', bg='Mintcream')
        self.real_state = tkinter.Label(
            self.frame2, width=12, height=1, text=str(self.profile[2]), anchor='e', bg='Mintcream')

        self.id_title.grid(row=0, column=0, padx=10, pady=15)
        self.name_title.grid(row=1, column=0, padx=10, pady=15)
        self.state_title.grid(row=3, column=0, padx=10, pady=15)

        self.real_id.grid(row=0, column=1, padx=10, pady=15)
        self.real_name.grid(row=1, column=1, padx=10, pady=15)
        self.real_state.grid(row=3, column=1, padx=10, pady=15)

        self.frame2.grid(row=0, column=0, padx=15, pady=15)

    def banAGroup(self):
        '''封禁一个群组'''
        confirm = tkinter.messagebox.askyesno(
            title='封禁', message='你确定要封禁群 ' + str(self.groupid) + ' 吗?')
        if confirm:
            self.profile = self.profile[:2] + (True,)
            Group.update_profile(self.groupid, self.profile)

            self.real_state.config(text=str(self.profile[2]))
            self.button1.config(state='disable')
            self.button2.config(state='normal')

            tkinter.messagebox.showinfo(
                title='封禁', message='群组 ' + str(self.groupid) + ' 已被封禁，现在该群组不能发言')

    def unbanAGroup(self):
        '''解封一个群组'''
        confirm = tkinter.messagebox.askyesno(
            title='解封', message='你确定要解封群组 ' + str(self.groupid) + ' 吗?')
        if confirm:
            self.profile = self.profile[:2] + (False,)
            Group.update_profile(self.groupid, self.profile)
            self.real_state.config(text=str(self.profile[2]))
            self.button1.config(state='normal')
            self.button2.config(state='disable')

            tkinter.messagebox.showinfo(
                title='解封', message='群组 ' + str(self.groupid) + ' 已解封，现在该群可以发言')

    def drawframe3(self):
        '''绘制frame3'''
        self.frame3 = tkinter.LabelFrame(
            self.frame1, text='operations', labelanchor='n', borderwidth=1, bg='MintCream')

        self.button1 = tkinter.Button(self.frame3, width=12, text='封禁', relief=tkinter.GROOVE, 
                                 cursor='hand2', fg = 'red', bg = 'LavenderBlush', command = self.banAGroup,
                                 state = 'normal' if not self.profile[2] else 'disable')
        self.button2 = tkinter.Button(self.frame3, width=12, text='解封', relief=tkinter.GROOVE,
                                      state='normal' if self.profile[2] else 'disable', cursor='hand2',
                                      command = self.unbanAGroup)

        self.button1.grid(row=0, column=0, padx=62, pady=14)
        self.button2.grid(row=1, column=0, padx=62, pady=14)

        self.frame3.grid(row=1, column=0, padx=15, pady=15)

    def showlist(self, listname):
        '''打印信息列表'''
        win = tkinter.Tk()
        sheet = tkinter.ttk.Treeview(
            win, height=10, show='headings', column=('1', '2'))
        sheet.column('1', width=100, anchor=tkinter.CENTER)
        sheet.column('2', width=100, anchor=tkinter.CENTER)
        sheet.heading('1', text='ID')
        sheet.heading('2', text='name')

        allmem = Group.get_mem(self.profile[0])
        l = []
        if listname == 'members':
            for mem in allmem:
                l.append(mem[:2])
        elif listname == 'ad':
            for mem in allmem:
                if mem[2]:
                    l.append(mem[:2])
        for item in l:
            sheet.insert('', tkinter.END, values=item)

        bar = tkinter.ttk.Scrollbar(
            win, command=sheet.yview, orient=tkinter.VERTICAL)
        sheet.config(yscrollcommand=bar.set)

        sheet.grid(row=0, column=0)
        bar.grid(row=0, column=1, sticky=tkinter.NS)
        win.mainloop()

    def showrecord(self):
        '''打印群聊天记录'''
        win = tkinter.Tk()
        sheet = tkinter.ttk.Treeview(
            win, height=10, show='headings', column=('1', '2', '3', '4'))
        sheet.column('1', width=150, anchor=tkinter.CENTER)
        sheet.column('2', width=50, anchor=tkinter.CENTER)
        sheet.column('3', width=75, anchor=tkinter.CENTER)
        sheet.column('4', width=250, anchor=tkinter.CENTER)
        sheet.heading('1', text='time')
        sheet.heading('2', text='senderid')
        sheet.heading('3', text='sender')
        sheet.heading('4', text='content')

        l = Group.get_record(self.profile[0])
        for item in l:
            sheet.insert('', tkinter.END, values=(item[2], item[1], item[0], item[3]))

        bar = tkinter.ttk.Scrollbar(
            win, command=sheet.yview, orient=tkinter.VERTICAL)
        sheet.config(yscrollcommand=bar.set)

        sheet.grid(row=0, column=0)
        bar.grid(row=0, column=1, sticky=tkinter.NS)
        win.mainloop()

    def drawframe4(self):
        '''绘制frame4'''
        self.frame4 = tkinter.LabelFrame(
            self.frame1, text='Detail', labelanchor='n', borderwidth=1, bg='MintCream')

        self.button3 = tkinter.Button(self.frame4, text='Members', command = lambda:self.showlist('members'), 
                                      relief=tkinter.GROOVE, width=15, cursor = 'hand2')
        self.button4 = tkinter.Button(self.frame4, text='Administrators', command=lambda: self.showlist('ad'),
                                      relief=tkinter.GROOVE, width=15, cursor = 'hand2')
        self.button5 = tkinter.Button(self.frame4, text='Record', command = self.showrecord, 
                                      relief=tkinter.GROOVE, width=15, cursor = 'hand2')

        self.button3.grid(row=0, column=0, padx=60, pady=20)
        self.button4.grid(row=1, column=0, padx=60, pady=20)
        self.button5.grid(row=2, column=0, padx=60, pady=20)

        self.frame4.grid(row=0, column=1, rowspan=2, padx=15, pady=15)

    def run(self):
        '''启动群管理UI'''
        self.root = tkinter.Tk()
        self.frame1 = tkinter.LabelFrame(self.root, text='Group Management', labelanchor='n', font=(
            'calibri', 16), borderwidth=4, height=700, width=1300, bg='MintCream')
        self.drawframe2()
        self.drawframe3()
        self.drawframe4()
        self.frame1.grid()
        self.root.mainloop()
