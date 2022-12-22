import tkinter as tk

from database import db
import global_manager as gm
import gui.admin_frames as frames


class AdminPage:
    def __init__(self):
        # root
        gm.root.title('实验室预约系统 - 管理员')
        gm.root.geometry(gm.set_size('size2'))

        # 菜单栏
        bar = tk.Menu(gm.root)

        menu_insert = tk.Menu(bar, tearoff=False)
        menu_insert.add_command(label='录入教师信息', command=lambda: self.cmd_to_frame(0))    # InsertTeacherFrame
        menu_insert.add_command(label='录入实验室信息', command=lambda: self.cmd_to_frame(1))  # InsertLabFrame
        menu_insert.add_command(label='录入设备信息', command=lambda: self.cmd_to_frame(2))    # InsertDeviceFrame
        menu_insert.add_command(label='录入预约记录', command=lambda: self.cmd_to_frame(3))    # InsertBookingFrame
        bar.add_cascade(label="信息录入", menu=menu_insert)

        menu_select = tk.Menu(bar, tearoff=False)
        menu_select.add_command(label='查询预订记录', command=lambda: self.cmd_to_frame(4))        # SelectBookingFrame
        menu_select.add_command(label='查询实验室闲忙', command=lambda: self.cmd_to_frame(5))  # SelectLabFrame1
        menu_select.add_command(label='查询设备记录', command=lambda: self.cmd_to_frame(6))        # SelectDeviceFrame
        menu_select.add_command(label='查询所有实验室空闲', command=lambda: self.cmd_to_frame(7))  # SelectLabFrame2
        bar.add_cascade(label="信息查询", menu=menu_select)

        menu_update = tk.Menu(bar, tearoff=False)
        menu_update.add_command(label='修改教师信息', command=lambda: self.cmd_to_frame(8))    # UpdateTeacherFrame
        menu_update.add_command(label='修改实验室信息', command=lambda: self.cmd_to_frame(9))  # UpdateLabFrame
        menu_update.add_command(label='修改设备信息', command=lambda: self.cmd_to_frame(10))    # UpdateDeviceFrame
        bar.add_cascade(label="信息修改", menu=menu_update)

        menu_delete = tk.Menu(bar, tearoff=False)
        menu_delete.add_command(label='删除教师信息', command=lambda: self.cmd_to_frame(11))          # DeleteTeacherFrame
        menu_delete.add_command(label='删除实验室信息', command=lambda: self.cmd_to_frame(12))          # DeleteLabFrame
        menu_delete.add_command(label='删除设备信息', command=lambda: self.cmd_to_frame(13))          # DeleteDeviceFrame
        menu_delete.add_command(label='删除预约记录(按教师)', command=lambda: self.cmd_to_frame(14))  # DeleteBookingFrame1
        menu_delete.add_command(label='删除预约记录(按年)', command=lambda: self.cmd_to_frame(15))    # DeleteBookingFrame2
        bar.add_cascade(label="信息删除", menu=menu_delete)

        bar.add_command(label="信息统计", command=lambda: self.cmd_to_frame(16))  # StatsFrame

        gm.root.config(menu=bar)

        # frames
        self.frames = [
            frames.InsertTeacherFrame(),
            frames.InsertLabFrame(),
            frames.InsertDeviceFrame(),
            frames.InsertBookingFrame(),
            frames.SelectBookingFrame(),
            frames.SelectLabFrame1(),
            frames.SelectDeviceFrame(),
            frames.SelectLabFrame2(),
            frames.UpdateTeacherFrame(),
            frames.UpdateLabFrame(),
            frames.UpdateDeviceFrame(),
            frames.DeleteTeacherFrame(),
            frames.DeleteLabFrame(),
            frames.DeleteDeviceFrame(),
            frames.DeleteBookingFrame1(),
            frames.DeleteBookingFrame2(),
            frames.StatsFrame(),
        ]
        self.frame_now = -1  # 没有 frame 时设置为 -1

    # frames 切换
    def cmd_to_frame(self, f):
        if self.frame_now != -1:
            self.frames[self.frame_now].pack_forget()
        self.frame_now = f
        self.frames[f].pack()


if __name__ == '__main__':
    user = {
        'no': '0',
        'name': 'admin'
    }
    gm.root = tk.Tk()
    AdminPage()
    gm.root.mainloop()
    db.close()
