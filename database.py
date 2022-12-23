import pymysql
from datetime import datetime, time

from global_manager import user


def convert_busy_empty(date, origin_data, booked):
    year, month, day = [int(i) for i in date.split('-')]
    start = datetime(year, month, day, 8, 0)  # yyyy-mm-dd 8:00:00
    end = datetime(year, month, day, 22, 0)  # yyyy-mm-dd 22:00:00
    rtn = []
    ptr = start
    for t in origin_data:
        if ptr < t['start_time']:
            rtn.append({
                'start_time': str(ptr.time()),
                'end_time': str(t['start_time'].time()),
                'status': '空闲'
            })
        if booked:
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
            user['no'] = '10000'
            user['name'] = 'admin'
            return True, '登录成功'
        else:
            user['no'] = '10001'
            user['name'] = '教师a'
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
        # lab_no = 'G101'
        # date = '2022-12-23'
        sql = '''SELECT start_time, end_time FROM booking
WHERE lab_no = '{}' AND DATE(start_time) = '{}'
ORDER BY start_time;'''.format(lab_no, date)
        tmp = self.run(sql)
        # return tmp
        return convert_busy_empty(date, tmp, True)

    # 通过设备号查询设备所在实验室
    def admin_select_3(self, device_no):
        sql = '''SELECT device.no as device_no, device.name as device_name, lab.no as lab_no
FROM device
JOIN lab ON device.lab_no = lab.no
WHERE device.no = '{}';'''.format(device_no)
        return self.run(sql)

    # 按照年月日查询所有实验室的空闲时间段
    def admin_select_4(self, date):
        # date = '2022-12-23'
        # 全部预约记录 当天没有记录的为 None
        sql = '''SELECT lab.no as lab_no, selected.start_time, selected.end_time
FROM lab
LEFT JOIN (SELECT lab_no, start_time, end_time
    FROM booking
    WHERE DATE(start_time) = '{}' AND DATE(end_time) = '{}') as selected
ON lab.no = selected.lab_no
ORDER BY lab_no, start_time;'''.format(date, date)
        tmp = self.run(sql)
        # return tmp
        lab_no = ''
        rtn = []  # 最终结果
        tmp_data = []  # 暂存各个实验室的记录
        for t in tmp:
            # 新的实验室记录
            if t['lab_no'] != lab_no:
                # 处理上一实验室记录
                if lab_no != '':
                    tmp_res = convert_busy_empty(date, tmp_data, False)
                    for tr in tmp_res:
                        rtn.append({
                            'lab_no': lab_no,
                            'start_time': tr['start_time'],
                            'end_time': tr['end_time'],
                        })
                # 置零 记录下一实验室
                lab_no = t['lab_no']
                tmp_data = []
            # 上一个实验室的记录 None记录不入栈tmp_data
            if t['start_time'] is not None and t['end_time'] is not None:
                tmp_data.append(t)
            else:
                tmp_res = convert_busy_empty(date, [], False)[0]
                rtn.append({
                    'lab_no': lab_no,
                    'start_time': tmp_res['start_time'],
                    'end_time': tmp_res['end_time'],
                })
        return rtn

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


def datetime_check(str_datetime):
    # date = 'yyyy-mm-dd hh:mm:ss'
    set_date, set_time = str_datetime.split(' ')
    dates = set_date.split('-')
    times = set_time.split(':')
    for s in dates + times:
        if not s.isdigit():
            return {
                'format': False,
                'range': False
            }
    dt = datetime(int(dates[0]), int(dates[1]), int(dates[2]), int(times[0]), int(times[1]), int(times[2]))
    early = time(8, 0)
    late = time(22, 0)
    return {
        'format': True,
        'range': early < dt.time() < late and dt > datetime.now()
    }


if __name__ == '__main__':
    # res = db.admin_select_2('G101', '2022-12-23')
    res = db.admin_select_4('2022-12-23')
    # res = convert_busy_empty('2022-12-23', [], False)
    for r in res:
        print(r)
    db.close()
