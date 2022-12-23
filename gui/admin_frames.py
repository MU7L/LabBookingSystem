import tkinter as tk
import tkinter.messagebox as tkm
from tkinter import ttk

import global_manager as gm
from database import db, datetime_check


# insert ----------------------------------------------------------------------------------------------------------

# 录入教师信息
class InsertTeacherFrame(tk.Frame):
    def __init__(self):
        super().__init__(gm.root)
        tk.Label(self, text='[ 录入教师信息 ]').pack()

        # data
        self.data_no = tk.StringVar()
        self.data_name = tk.StringVar()
        self.data_phone = tk.StringVar()
        self.data_department = tk.StringVar()

        label_no = tk.Label(self, text='教师编号：')
        entry_no = tk.Entry(self, textvariable=self.data_no)
        label_name = tk.Label(self, text='教师姓名：')
        entry_name = tk.Entry(self, textvariable=self.data_name)
        label_phone = tk.Label(self, text='联系电话：')
        entry_phone = tk.Entry(self, textvariable=self.data_phone)
        label_department = tk.Label(self, text='所属教研室：')
        entry_department = tk.Entry(self, textvariable=self.data_department)
        btn_logon = tk.Button(self, text='录入', command=lambda: self.btn_logon_click())

        label_no.pack()
        entry_no.pack()
        label_name.pack()
        entry_name.pack()
        label_phone.pack()
        entry_phone.pack()
        label_department.pack()
        entry_department.pack()
        btn_logon.pack()

    def btn_logon_click(self):
        no = self.data_no.get()
        name = self.data_name.get()
        phone = self.data_phone.get()
        department = self.data_department.get()
        if db.admin_insert('teacher', no=no, name=name, phone=phone, department=department):
            tkm.showinfo(title='录入成功', message='{}[{}] 录入成功'.format(name, no))
        else:
            tkm.askretrycancel(title='录入失败', message='检查教师编号是否有误')


# 录入实验室信息
class InsertLabFrame(tk.Frame):
    def __init__(self):
        super().__init__(gm.root)
        tk.Label(self, text='[ 录入实验室信息 ]').pack()

        # data
        self.data_no = tk.StringVar()
        self.data_name = tk.StringVar()
        self.data_capacity = tk.IntVar()
        self.data_info = tk.StringVar()
        self.data_photo = tk.StringVar()

        label_no = tk.Label(self, text='实验室编号：')
        entry_no = tk.Entry(self, textvariable=self.data_no)
        label_name = tk.Label(self, text='实验室名：')
        entry_name = tk.Entry(self, textvariable=self.data_name)
        label_capacity = tk.Label(self, text='实验室容量：')
        entry_capacity = tk.Entry(self, textvariable=self.data_capacity)
        label_info = tk.Label(self, text='实验室用途：')
        entry_info = tk.Entry(self, textvariable=self.data_info)
        label_photo = tk.Label(self, text='实验室照片(文件路径)：')
        entry_photo = tk.Entry(self, textvariable=self.data_photo)
        btn_logon = tk.Button(self, text='录入', command=lambda: self.btn_logon_click())

        label_no.pack()
        entry_no.pack()
        label_name.pack()
        entry_name.pack()
        label_capacity.pack()
        entry_capacity.pack()
        label_info.pack()
        entry_info.pack()
        label_photo.pack()
        entry_photo.pack()
        btn_logon.pack()

    def btn_logon_click(self):
        no = self.data_no.get()
        name = self.data_name.get()
        capacity = self.data_capacity.get()
        info = self.data_info.get()
        photo = self.data_photo.get()
        if db.admin_insert('lab', no=no, name=name, capacity=capacity, info=info, photo=photo):
            tkm.showinfo(title='录入成功', message='{}[{}] 录入成功'.format(name, no))
        else:
            tkm.askretrycancel(title='录入失败', message='检查实验室编号是否有误')


# 录入设备信息
class InsertDeviceFrame(tk.Frame):
    def __init__(self):
        super().__init__(gm.root)
        tk.Label(self, text='[ 录入设备信息 ]').pack()

        # data
        self.data_no = tk.StringVar()
        self.data_name = tk.StringVar()
        self.data_lab_no = tk.StringVar()

        label_no = tk.Label(self, text='设备编号：')
        entry_no = tk.Entry(self, textvariable=self.data_no)
        label_name = tk.Label(self, text='设备名：')
        entry_name = tk.Entry(self, textvariable=self.data_name)
        label_lab_no = tk.Label(self, text='设备所属实验室编号：')
        entry_lab_no = tk.Entry(self, textvariable=self.data_lab_no)
        btn_logon = tk.Button(self, text='录入', command=lambda: self.btn_logon_click())

        label_no.pack()
        entry_no.pack()
        label_name.pack()
        entry_name.pack()
        label_lab_no.pack()
        entry_lab_no.pack()
        btn_logon.pack()

    def btn_logon_click(self):
        no = self.data_no.get()
        name = self.data_name.get()
        lab_no = self.data_lab_no.get()
        if db.admin_insert('device', no=no, name=name, lab_no=lab_no):
            tkm.showinfo(title='录入成功', message='{}[{}] 录入成功'.format(name, no))
        else:
            # TODO: 返回db异常
            msg = '''录入失败原因可能是：
1. 已有该设备编号
2. 没找到对应实验室编号'''
            tkm.askretrycancel(title='录入失败', message=msg)


# 录入预约记录
class InsertBookingFrame(tk.Frame):
    def __init__(self):
        super().__init__(gm.root)
        tk.Label(self, text='[ 录入预约记录 ]').pack()
        tk.Label(self, text='预约时间限定为 8:00-22:00').pack()

        # data
        self.data_teacher_no = tk.StringVar()
        self.data_lab_no = tk.StringVar()
        self.data_start_time = tk.StringVar()
        self.data_start_time.set('yyyy-mm-dd hh:mm')
        self.data_end_time = tk.StringVar()
        self.data_end_time.set('yyyy-mm-dd hh:mm')
        self.data_user = tk.StringVar()

        label_teacher_no = tk.Label(self, text='教师编号：')
        entry_teacher_no = tk.Entry(self, textvariable=self.data_teacher_no)
        label_lab_no = tk.Label(self, text='实验室编号：')
        entry_lab_no = tk.Entry(self, textvariable=self.data_lab_no)
        label_start_time = tk.Label(self, text='预约起始时间：')
        entry_start_time = tk.Entry(self, textvariable=self.data_start_time)
        label_end_time = tk.Label(self, text='预约结束时间：')
        entry_end_time = tk.Entry(self, textvariable=self.data_end_time)
        label_user = tk.Label(self, text='预约使用人：')
        entry_user = tk.Entry(self, textvariable=self.data_user)
        btn_logon = tk.Button(self, text='录入', command=lambda: self.btn_logon_click())

        label_teacher_no.pack()
        entry_teacher_no.pack()
        label_lab_no.pack()
        entry_lab_no.pack()
        label_start_time.pack()
        entry_start_time.pack()
        label_end_time.pack()
        entry_end_time.pack()
        label_user.pack()
        entry_user.pack()
        btn_logon.pack()

    def btn_logon_click(self):
        teacher_no = self.data_teacher_no.get()
        lab_no = self.data_lab_no.get()
        start_time = self.data_start_time.get() + ':00'
        check_start_time = datetime_check(start_time)
        end_time = self.data_end_time.get() + ':00'
        check_end_time = datetime_check(end_time)
        user = self.data_user.get()
        if check_start_time['format'] and check_end_time['format']:
            tkm.askretrycancel(title='录入失败', message='时间格式不正确。请检查格式是否为 yyyy-mm-dd hh:mm')
            return
        if check_start_time['range'] and check_end_time['range']:
            tkm.askretrycancel(title='录入失败', message='超出预约时间段。预约时间限定为 8:00-22:00')
            return
        if db.admin_insert('booking', teacher_no=teacher_no, lab_no=lab_no, start_time=start_time, end_time=end_time,
                           user=user):
            tkm.showinfo(title='录入成功', message='{}-{} @{} 录入成功'.format(teacher_no, lab_no, start_time))
        else:
            msg = '''录入失败原因可能是：
1. 教师编号/实验室编号不存在
2. 起始/结束时间格式不正确'''
            tkm.askretrycancel(title='录入失败', message='msg')


# select ----------------------------------------------------------------------------------------------------------

# 通过教师编号或教师名查询该教师某一时间段内的预定记录
class SelectBookingFrame(tk.Frame):
    def __init__(self):
        super().__init__(gm.root)
        tk.Label(self, text='[ 查询预订记录 ]').pack()

        # 输入
        self.str_value = tk.StringVar()
        self.str_option = tk.StringVar()
        self.str_option.set('no')

        label_option = tk.Label(self, text='查找方式：')
        radio1 = tk.Radiobutton(self, text='按教师编号', variable=self.str_option, value='no')
        radio1.select()
        radio2 = tk.Radiobutton(self, text='按教师姓名', variable=self.str_option, value='name')
        label_value = tk.Label(self, text="查找内容：")
        entry_value = tk.Entry(self, textvariable=self.str_value)
        btn_select = tk.Button(self, text="查找/刷新", command=lambda: self.load_table())

        label_option.pack()
        radio1.pack()
        radio2.pack()
        label_value.pack()
        entry_value.pack()
        btn_select.pack()

        # 输出
        self.columns = ('teacher_name', 'lab_no', 'start_time', 'end_time', 'user')
        columns_show = ('预订教师', '预订实验室', '开始时间', '结束时间', '使用人')
        self.table = ttk.Treeview(self, show='headings', columns=self.columns)
        col_width = int(gm.size2[0] / len(self.columns)) - 5
        for i in range(len(self.columns)):
            self.table.column(self.columns[i], width=col_width, anchor='center')
            self.table.heading(self.columns[i], text=columns_show[i])
        self.table.pack()
        self.load_table()

    def load_table(self):
        # old data
        for _ in map(self.table.delete, self.table.get_children('')):
            pass
        # new data
        option = self.str_option.get()
        value = self.str_value.get()
        res = [{c: 'None' for c in self.columns}]
        if '' not in (option, value):
            res = db.admin_select_1(option, value)
        for r in res:
            self.table.insert('', 'end', values=tuple(r.values()))


# 通过实验室号及日期查询本实验室当天场地已预定时间段
class SelectLabFrame1(tk.Frame):
    def __init__(self):
        super().__init__(gm.root)
        tk.Label(self, text='[ 查询实验室闲忙 ]').pack()

        # 输入
        self.str_lab_no = tk.StringVar()
        self.str_date = tk.StringVar()
        self.str_date.set('yyyy-mm-dd')

        label_lab_no = tk.Label(self, text='实验室编号')
        entry_lab_no = tk.Entry(self, textvariable=self.str_lab_no)
        label_date = tk.Label(self, text="查询预约日期：")
        entry_date = tk.Entry(self, textvariable=self.str_date)
        btn_select = tk.Button(self, text="查找/刷新", command=lambda: self.load_table())

        label_lab_no.pack()
        entry_lab_no.pack()
        label_date.pack()
        entry_date.pack()
        btn_select.pack()

        # 输出
        self.columns = ('start_time', 'end_time', 'state')
        columns_show = ('开始时间', '结束时间', '实验室状态')
        self.table = ttk.Treeview(self, show='headings', columns=self.columns)
        col_width = int(gm.size2[0] / len(self.columns)) - 5
        for i in range(len(self.columns)):
            self.table.column(self.columns[i], width=col_width, anchor='center')
            self.table.heading(self.columns[i], text=columns_show[i])
        self.load_table()
        self.table.pack()

    def load_table(self):
        # old data
        for _ in map(self.table.delete, self.table.get_children('')):
            pass
        # new data
        lab_no = self.str_lab_no.get()
        date = self.str_date.get()
        res = [{c: 'None' for c in self.columns}]
        if lab_no != '' and datetime_check(date+' 00:00:00')['format']:
            res = db.admin_select_2(lab_no, date)
        for r in res:
            self.table.insert('', 'end', values=tuple(r.values()))


# 通过设备号查询设备所在实验室
class SelectDeviceFrame(tk.Frame):
    def __init__(self):
        super().__init__(gm.root)
        tk.Label(self, text='[ 查询设备记录 ]').pack()

        # 输入
        self.str_no = tk.StringVar()

        label_no = tk.Label(self, text='设备编号')
        entry_no = tk.Entry(self, textvariable=self.str_no)
        btn_select = tk.Button(self, text="查找/刷新", command=lambda: self.load_table())

        label_no.pack()
        entry_no.pack()
        btn_select.pack()

        # 输出
        self.columns = ('device_no', 'device_name', 'lab_no')
        columns_show = ('设备编号', '设备名', '实验室编号')
        self.table = ttk.Treeview(self, show='headings', columns=self.columns)
        col_width = int(gm.size2[0] / len(self.columns)) - 5
        for i in range(len(self.columns)):
            self.table.column(self.columns[i], width=col_width, anchor='center')
            self.table.heading(self.columns[i], text=columns_show[i])
        self.load_table()
        self.table.pack()

    def load_table(self):
        # old data
        for _ in map(self.table.delete, self.table.get_children('')):
            pass
        # new data
        no = self.str_no.get()
        res = [{c: 'None' for c in self.columns}]
        if no != '':
            res = db.admin_select_3(no)
        for r in res:
            self.table.insert('', 'end', values=tuple(r.values()))


# 按照年月日查询所有实验室的空闲时间段
class SelectLabFrame2(tk.Frame):
    def __init__(self):
        super().__init__(gm.root)
        tk.Label(self, text='[ 查询所有实验室空闲 ]').pack()

        # 输入
        self.str_date = tk.StringVar()
        self.str_date.set('yyyy-mm-dd')

        label_date = tk.Label(self, text="查询预约日期：")
        entry_date = tk.Entry(self, textvariable=self.str_date)
        btn_select = tk.Button(self, text="查找/刷新", command=lambda: self.load_table())

        label_date.pack()
        entry_date.pack()
        btn_select.pack()

        # 输出
        self.columns = ('lab_no', 'start_time', 'end_time')
        columns_show = ('实验室编号', '开始时间', '结束时间')
        self.table = ttk.Treeview(self, show='headings', columns=self.columns)
        col_width = int(gm.size2[0] / len(self.columns)) - 5
        for i in range(len(self.columns)):
            self.table.column(self.columns[i], width=col_width, anchor='center')
            self.table.heading(self.columns[i], text=columns_show[i])
        self.table.pack()
        self.load_table()

    def load_table(self):
        # old data
        for _ in map(self.table.delete, self.table.get_children('')):
            pass
        # new data
        date = self.str_date.get()
        res = [{c: 'None' for c in self.columns}]
        if datetime_check(date+' 00:00:00')['format']:
            res = db.admin_select_4(date)
        for r in res:
            self.table.insert('', 'end', values=tuple(r.values()))


# update ----------------------------------------------------------------------------------------------------------

# 修改教师信息
class UpdateTeacherFrame(tk.Frame):
    def __init__(self):
        super().__init__(gm.root)
        tk.Label(self, text='[ 修改教师信息 ]').pack()

        # data
        self.data_no = tk.StringVar()
        self.data_name = tk.StringVar()
        self.data_phone = tk.StringVar()
        self.data_department = tk.StringVar()
        self.data_password = tk.StringVar()

        label_no = tk.Label(self, text='教师编号：')
        entry_no = tk.Entry(self, textvariable=self.data_no)
        label_name = tk.Label(self, text='修改教师姓名：')
        entry_name = tk.Entry(self, textvariable=self.data_name)
        label_phone = tk.Label(self, text='修改联系电话：')
        entry_phone = tk.Entry(self, textvariable=self.data_phone)
        label_department = tk.Label(self, text='修改所属教研室：')
        entry_department = tk.Entry(self, textvariable=self.data_department)
        label_password = tk.Label(self, text='修改密码：')
        entry_password = tk.Entry(self, textvariable=self.data_password, show='*')
        btn_update = tk.Button(self, text='修改', command=lambda: self.btn_update_click())

        label_no.pack()
        entry_no.pack()
        label_name.pack()
        entry_name.pack()
        label_phone.pack()
        entry_phone.pack()
        label_department.pack()
        entry_department.pack()
        label_password.pack()
        entry_password.pack()
        btn_update.pack()

    def btn_update_click(self):
        no = self.data_no.get()
        name = self.data_name.get()
        phone = self.data_phone.get()
        department = self.data_department.get()
        password = self.data_password.get()
        if db.admin_update('teacher', no, name=name, phone=phone, department=department, password=password):
            tkm.showinfo(title='修改成功', message='{}[{}] 修改成功'.format(name, no))
        else:
            tkm.askretrycancel(title='修改失败', message='请检查教师编号是否存在')


# 修改实验室信息
class UpdateLabFrame(tk.Frame):
    def __init__(self):
        super().__init__(gm.root)
        tk.Label(self, text='[ 修改实验室信息 ]').pack()

        # data
        self.data_no = tk.StringVar()
        self.data_name = tk.StringVar()
        self.data_capacity = tk.IntVar()
        self.data_info = tk.StringVar()
        self.data_photo = tk.StringVar()

        label_no = tk.Label(self, text='实验室编号：')
        entry_no = tk.Entry(self, textvariable=self.data_no)
        label_name = tk.Label(self, text='修改实验室名：')
        entry_name = tk.Entry(self, textvariable=self.data_name)
        label_capacity = tk.Label(self, text='修改实验室容量：')
        entry_capacity = tk.Entry(self, textvariable=self.data_capacity)
        label_info = tk.Label(self, text='修改实验室用途：')
        entry_info = tk.Entry(self, textvariable=self.data_info)
        label_photo = tk.Label(self, text='修改实验室照片(文件路径)：')
        entry_photo = tk.Entry(self, textvariable=self.data_photo)
        btn_update = tk.Button(self, text='修改', command=lambda: self.btn_update_click())

        label_no.pack()
        entry_no.pack()
        label_name.pack()
        entry_name.pack()
        label_capacity.pack()
        entry_capacity.pack()
        label_info.pack()
        entry_info.pack()
        label_photo.pack()
        entry_photo.pack()
        btn_update.pack()

    def btn_update_click(self):
        no = self.data_no.get()
        name = self.data_name.get()
        capacity = self.data_capacity.get()
        info = self.data_info.get()
        photo = self.data_photo.get()
        if db.admin_update('lab', no, name=name, capacity=capacity, info=info, photo=photo):
            tkm.showinfo(title='修改成功', message='{}[{}] 修改成功'.format(name, no))
        else:
            tkm.askretrycancel(title='修改失败', message='请检查实验室编号是否存在')


# 修改设备信息
class UpdateDeviceFrame(tk.Frame):
    def __init__(self):
        super().__init__(gm.root)
        tk.Label(self, text='[ 修改设备信息 ]').pack()

        # data
        self.data_no = tk.StringVar()
        self.data_name = tk.StringVar()
        self.data_lab_no = tk.StringVar()

        label_no = tk.Label(self, text='设备编号：')
        entry_no = tk.Entry(self, textvariable=self.data_no)
        label_name = tk.Label(self, text='修改设备名：')
        entry_name = tk.Entry(self, textvariable=self.data_name)
        label_lab_no = tk.Label(self, text='修改设备所属实验室编号：')
        entry_lab_no = tk.Entry(self, textvariable=self.data_lab_no)
        btn_update = tk.Button(self, text='修改', command=lambda: self.btn_update_click())

        label_no.pack()
        entry_no.pack()
        label_name.pack()
        entry_name.pack()
        label_lab_no.pack()
        entry_lab_no.pack()
        btn_update.pack()

    def btn_update_click(self):
        no = self.data_no.get()
        name = self.data_name.get()
        lab_no = self.data_lab_no.get()
        if db.admin_update('device', no, name=name, lab_no=lab_no):
            tkm.showinfo(title='修改成功', message='{}[{}] 修改成功'.format(name, no))
        else:
            msg = '''修改失败原因可能为：
1. 设备编号不存在
2. 实验室号不存在'''
            tkm.askretrycancel(title='修改失败', message=msg)


# delete ----------------------------------------------------------------------------------------------------------

# 删除教师信息
class DeleteTeacherFrame(tk.Frame):
    def __init__(self):
        super().__init__(gm.root)
        tk.Label(self, text='[ 删除教师信息 ]').pack()

        self.no = tk.StringVar()
        label = tk.Label(self, text='待删除教师编号')
        entry = tk.Entry(self, textvariable=self.no)
        btn = tk.Button(self, text='删除', command=lambda: self.delete())

        label.pack()
        entry.pack()
        btn.pack()

    def delete(self):
        no = self.no.get()
        if tkm.askokcancel(title='删除', message='是否删除教师 [{}]'.format(no)):
            if db.admin_delete('teacher', no):
                tkm.showinfo(title='删除成功', message='教师 [{}] 已删除'.format(no))
            else:
                # TODO: 返回db异常
                msg = '''删除失败原因可能为：
1. 该教师仍有预约记录，不可删除
2. 该教师不存在'''
                tkm.askretrycancel(title='删除失败', message=msg)


# 删除实验室信息
class DeleteLabFrame(tk.Frame):
    def __init__(self):
        super().__init__(gm.root)
        tk.Label(self, text='[ 删除实验室信息 ]').pack()

        self.no = tk.StringVar()
        label = tk.Label(self, text='待删除实验室编号')
        entry = tk.Entry(self, textvariable=self.no)
        btn = tk.Button(self, text='删除', command=lambda: self.delete())

        label.pack()
        entry.pack()
        btn.pack()

    def delete(self):
        no = self.no.get()
        if tkm.askokcancel(title='删除', message='是否删除实验室[{}]'.format(no)):
            if db.admin_delete('lab', no):
                tkm.showinfo(title='删除成功', message='实验室 [{}] 已删除'.format(no))
            else:
                # TODO: 返回db异常
                msg = '''删除失败原因可能为：
1. 该实验室仍有预约记录，不可删除
2. 该实验室不存在'''
                tkm.askretrycancel(title='删除失败', message=msg)


# 删除设备信息
class DeleteDeviceFrame(tk.Frame):
    def __init__(self):
        super().__init__(gm.root)
        tk.Label(self, text='[ 删除设备信息 ]').pack()

        self.no = tk.StringVar()
        label = tk.Label(self, text='待删除设备编号')
        entry = tk.Entry(self, textvariable=self.no)
        btn = tk.Button(self, text='删除', command=lambda: self.delete())

        label.pack()
        entry.pack()
        btn.pack()

    def delete(self):
        no = self.no.get()
        if tkm.askokcancel(title='删除', message='是否删除设备 [{}]'.format(no)):
            if db.admin_delete('device', no):
                tkm.showinfo(title='删除成功', message='设备 [{}] 已删除'.format(no))
            else:
                # TODO: 返回db异常
                msg = '''删除失败原因可能为：
1. 该设备仍有预约记录，不可删除
2. 该设备不存在'''
                tkm.askretrycancel(title='删除失败', message=msg)


# 删除预约记录(按教师)
class DeleteBookingFrame1(tk.Frame):
    def __init__(self):
        super().__init__(gm.root)
        tk.Label(self, text='[ 删除预约记录 ]').pack()

        self.data_date = tk.StringVar()
        self.data_date.set('yyyy-mm-dd')
        self.data_no = tk.StringVar()
        label_date = tk.Label(self, text='待删除记录日期：')
        entry_date = tk.Entry(self, textvariable=self.data_date)
        label_no = tk.Label(self, text='预约教师编号：')
        entry_no = tk.Entry(self, textvariable=self.data_no)
        btn = tk.Button(self, text='删除', command=lambda: self.delete())

        label_date.pack()
        entry_date.pack()
        label_no.pack()
        entry_no.pack()
        btn.pack()

    def delete(self):
        date = self.data_date.get()
        if not datetime_check(date+' 00:00:00')['format']:
            tkm.askretrycancel(title='删除失败', message='时间格式有误')
            return
        no = self.data_no.get()
        if tkm.askokcancel(title='删除', message='是否删除该记录'):
            if db.admin_delete_4(date, no):
                tkm.showinfo(title='删除成功', message='预约记录已删除')
            else:
                # TODO: 返回db异常
                tkm.askretrycancel(title='删除失败', message='该记录不存在')


# 删除预约记录(按年)
class DeleteBookingFrame2(tk.Frame):
    def __init__(self):
        super().__init__(gm.root)
        tk.Label(self, text='[ 删除预约记录 ]').pack()

        self.year = tk.StringVar()
        label = tk.Label(self, text='待删除记录年份：')
        entry = tk.Entry(self, textvariable=self.year)
        btn = tk.Button(self, text='删除', command=lambda: self.delete())

        label.pack()
        entry.pack()
        btn.pack()

    def delete(self):
        year = self.year.get()
        if not year.isdigit():
            tkm.showinfo(title='删除失败', message='年份格式有误')
        if tkm.askokcancel(title='删除', message='是否删除该年所有记录'):
            if db.admin_delete_5(year):
                tkm.showinfo(title='删除成功', message='预约记录已删除')
            else:
                tkm.askretrycancel(title='删除失败', message='记录不存在')


# stats ----------------------------------------------------------------------------------------------------------

# 信息统计
class StatsFrame(tk.Frame):
    def __init__(self):
        super().__init__(gm.root)
        tk.Label(self, text='[ 信息统计 ]').pack()

        self.data_years = tk.IntVar()
        self.data_months = tk.IntVar()
        label_title_year = tk.Label(self, text='各实验室被预约总时长 (年)')
        label_data_year = tk.Label(self, textvariable=self.data_years)
        label_title_month = tk.Label(self, text='各实验室被预约总时长 (月)')
        label_data_month = tk.Label(self, textvariable=self.data_months)
        btn_flash = tk.Button(self, text='刷新', command=lambda: self.load_data())

        label_title_year.pack()
        label_data_year.pack()
        label_title_month.pack()
        label_data_month.pack()
        btn_flash.pack()

        self.load_data()

    def load_data(self):
        months, years = db.admin_stats()
        self.data_years.set(years)
        self.data_months.set(months)
