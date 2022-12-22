# 调用
# import global_manager as gm

# user 当前登录用户
# name: default为未登录 admin为管理员 其他值为登录用户
# 对 db 读写
# 对 gui 只读
user = {
    'no': '0',
    'name': 'default'
}

# gui root
root = 0

# TODO: 设置项可以独立出来
# login page 大小
size1 = (450, 300)
size2 = (600, 400)


def set_size(op):
    size = ()
    if op == 'size1':
        size = size1
    else:
        size = size2
    return '{}x{}'.format(size[0], size[1])
