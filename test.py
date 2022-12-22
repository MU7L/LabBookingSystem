import datetime

date = '2022-12-20'
# src = [{'n': '1', 'start_time': datetime(2022, 12, 20, 20, 0), 'end_time': datetime(2022, 12, 20, 21, 0)},
#        {'start_time': datetime(2022, 12, 20, 21, 0), 'end_time': datetime(2022, 12, 20, 22, 0)}]
src = [{'lab_no': '0', 'start_time': None, 'end_time': None}, {'lab_no': '1', 'start_time': datetime.datetime(2022, 12, 21, 14, 46, 6), 'end_time': datetime.datetime(2022, 12, 21, 14, 46, 9)}, {'lab_no': '1', 'start_time': datetime.datetime(2022, 12, 21, 17, 1, 32), 'end_time': datetime.datetime(2022, 12, 21, 17, 1, 38)}, {'lab_no': '10', 'start_time': None, 'end_time': None}]
year, month, day = [int(i) for i in date.split('-')]
start = datetime.datetime(year, month, day, 0)
end = datetime.datetime(year, month, day, 23, 59, 59)

rtn = []
ptr = start
lab = ''
for t in src:
    # 新实验室记录
    if t['lab_no'] != lab:
        if lab != '':
            rtn.append({
                'lab_no': lab,
                'start_time': str(ptr.time()),
                'end_time': str(end.time()),
                'status': '空闲'
            })  # 此时上一条lab的记录全部结束
        lab = t['lab_no']
        ptr = start

        # None 记录直接入栈
        if None in t.values():
            rtn.append({
                'lab_no': lab,
                'start_time': str(start.time()),
                'end_time': str(end.time()),
                'status': '空闲'
            })
            continue

    if ptr < t['start_time']:
        rtn.append({
            'lab_no': lab,
            'start_time': str(start.time()),
            'end_time': str(t['start_time'].time()),
            'status': '空闲'
        })
        ptr = t['end_time']

# TODO: 记录结束时两种情况
# 1. 最后一条 None
# 2. 最后一条 datetime
if ptr < end and ptr != start:
    rtn.append({
        'lab_no': lab,
        'start_time': str(ptr.time()),
        'end_time': str(end.time()),
        'status': '空闲'
    })

for r in rtn:
    print(r)


