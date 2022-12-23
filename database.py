import pymysql
from datetime import datetime

from global_manager import user


class MySQLHelper:
    def __init__(self):
        self.conn = pymysql.connect(
            host='localhost',
            port=3306,
            db='labbooking',
            user='root',
            password='root'
        )
        self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)

    def run(self, sql):
        # SELECT 返回查询结果
        if 'SELECT' in sql:
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        # 其他返回操作结果
        else:
            try:
                self.cursor.execute(sql)
                self.conn.commit()
                return True
            except:
                self.conn.rollback()
                return False

    def close(self):
        self.cursor.close()
        self.conn.close()

    # login ------------------------------------------------------------------------------------------------------

    def check_login(self, username, password):
        sql = '''SELECT name, password
        FROM teacher
        WHERE no = '{}';'''.format(username)
        res = self.run(sql)[0]
        # return res
        if res is not None:
            if password == res['password']:
                user['no'] = username
                user['name'] = res['name']
                return True, '登录成功'
            else:
                return False, '用户名或密码错误'
        else:
            return False, '未找到该用户'

    def check_login_test(self, test):
        if test == 0:
            user['no'] = '0'
            user['name'] = 'admin'
            return True, '登录成功'
        else:
            user['no'] = '1'
            user['name'] = '从永年'
            return True, '登录成功'

    # insert -----------------------------------------------------------------------------------------------------
    # TODO: insert 合理性检查
    def admin_insert(self, table, **data):
        sql = ''
        if table == 'teacher':
            sql = '''INSERT INTO teacher
(no, name, phone, department, password)
VALUES
('{}','{}','{}','{}','12345');'''.format(data['no'], data['name'], data['phone'], data['department'])
        elif table == 'lab':
            sql = '''INSERT INTO lab
(no, name, capacity, info, photo)
VALUES
('{}','{}','{}','{}','{}');'''.format(data['no'], data['name'], data['capacity'], data['info'], data['photo'])
        elif table == 'device':
            sql = '''INSERT INTO device
(no, name, lab_no)
VALUES
('{}','{}','{}');'''.format(data['no'], data['name'], data['lab_no'])
        elif table == 'booking':
            sql = '''INSERT INTO booking
(teacher_no, lab_no, start_time, end_time, user)
VALUES
('{}','{}','{}','{}','{}');'''.format(data['teacher_no'], data['lab_no'], data['start_time'], data['end_time'],
                                      data['user'])
        return self.run(sql)

    # select ---------------------------------------------------------------------------------------------------

    # 通过教师编号或教师名查询该教师某一时间段内的预定记录
    def admin_select_1(self, option, value):
        # option = 'no' / 'name'
        # value = '1000x' / 'name'
        sql = '''SELECT teacher.name as teacher_name, lab.no as lab_no, booking.start_time, booking.end_time, booking.user
FROM booking
JOIN teacher ON booking.teacher_no = teacher.no
JOIN lab ON booking.lab_no = lab.no
WHERE teacher.{} = '{}';'''.format(option, value)
        return self.run(sql)

    # 通过实验室号及日期查询本实验室当天场地已预定时间段
    def admin_select_2(self, lab_no, date):
        # lab_no = '0'
        # date = '2022-12-20'
        sql = '''SELECT start_time, end_time FROM booking
WHERE lab_no = '{}' AND DATE(start_time) = '{}';'''.format(lab_no, date)
        tmp = self.run(sql)
        # TODO：将预约记录转为全天状态记录
        year, month, day = [int(i) for i in date.split('-')]
        start = datetime(year, month, day, 0)  # 00:00:00
        end = datetime(year, month, day, 23, 59, 59)  # 23:59:59
        rtn = []
        ptr = start
        for t in tmp:
            if ptr < t['start_time']:
                rtn.append({
                    'start_time': str(start.time()),
                    'end_time': str(t['start_time'].time()),
                    'status': '空闲'
                })
            rtn.append({
                'start_time': str(t['start_time'].time()),
                'end_time': str(t['end_time'].time()),
                'state': '已预约'
            })
            ptr = t['end_time']
        if ptr < end:
            rtn.append({
                'start_time': str(ptr.time()),
                'end_time': str(end.time()),
                'status': '空闲'
            })
        return rtn

    # 通过设备号查询设备所在实验室
    def admin_select_3(self, device_no):
        sql = '''SELECT device.no as device_no, device.name as device_name, lab.no as lab_no
FROM device
JOIN lab ON device.lab_no = lab.no
WHERE device.no = '{}';'''.format(device_no)
        return self.run(sql)

    # 按照年月日查询所有实验室的空闲时间段
    def admin_select_4(self, date):
        # 全部预约记录 当天没有记录的为 None
        sql = '''SELECT lab.no as lab_no, selected.start_time, selected.end_time
FROM lab
LEFT JOIN (SELECT lab_no, start_time, end_time
    FROM booking
    WHERE DATE(start_time) = '{}' AND DATE(end_time) = '{}') as selected
ON lab.no = selected.lab_no
ORDER BY lab_no, start_time;'''.format(date, date)
        tmp = self.run(sql)
        # TODO: tmp 是一个混杂了 None 记录与有预约记录的字典 没有转换为所需结果
        return tmp

    # update --------------------------------------------------------------------------------------------------

    def admin_update(self, table, no, **data):
        sql = 'UPDATE {} SET '.format(table)
        for key, value in data.items():
            sql += "{} = '{}', ".format(key, value)
        sql = sql.rstrip(', ')
        sql += " WHERE no = '{}';".format(no)
        return self.run(sql)

    # delete --------------------------------------------------------------------------------------------------

    # 按照设备号/教师编号/实验室号删除信息
    def admin_delete(self, table, no):
        sql = '''DELETE FROM {}
WHERE no='{}';'''.format(table, no)
        return self.run(sql)

    # 按日期删除某教师某实验室的预约记录
    def admin_delete_4(self, date, teacher_no):
        sql = '''DELETE FROM booking
WHERE DATE(start_time) = '{}' AND teacher_no = '{}';'''.format(date, teacher_no)
        return self.run(sql)

    # 按照年份删除实验室预约记录
    def admin_delete_5(self, year):
        sql = '''DELETE FROM booking
WHERE YEAR(start_time) = '{}' OR YEAR(end_time) = '{}';'''.format(year, year)
        return self.run(sql)

    # 信息统计 统计各实验室被预约的总时长
    def admin_stats(self):
        sql = 'SELECT SUM(TIMESTAMPDIFF(MINUTE,start_time,end_time)) as sum_minutes FROM booking;'
        res = self.run(sql)[0]['sum_minutes']
        months = 0
        years = 0
        if res is not None:
            months = round(res / 60 / 30, 1)  # 按一个月30天
            years = round(months / 12, 1)
        return months, years


db = MySQLHelper()

if __name__ == '__main__':
    # sql = 'SELECT SUM(TIMESTAMPDIFF(MINUTE,start_time,end_time)) as sum_minutes FROM booking;'
    # t = db.run(sql)[0]['sum_minutes']
    t = db.admin_stats()
    print(t)
