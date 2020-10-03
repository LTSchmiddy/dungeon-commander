import os

def mkdir_if_missing(dir_path: str):
    if not os.path.isdir(dir_path):
        # os.mkdir(dir_path)
        os.makedirs(dir_path)



class classproperty(object):
    def __init__(self, f):
        self.f = classmethod(f)
    def __get__(self, *a):
        return self.f.__get__(*a)()

#
# class moduleproperty(object):
#     def __init__(self, f, *args):
#         self.args = args
#         self.f = f
#
#     def __get__(self):
#         return self.f(*self.args)
#
#     def __call__(self):
#         return self.__get__()


def list_contains(p_filter, p_list):
    for x in p_list:
        if p_filter(x):
            return True
    return False

def list_get(p_filter, p_list):
    for x in p_list:
        if p_filter(x):
            return x
    return None
