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



def get_dir_tree(current_dir, to_ignore:(tuple, list)=('__pycache__',) ):
    dir_cont = os.listdir(current_dir)

    dir_dict = {
        'path': current_dir,
        'dirs': {},
        'files': {}

    }

    for i in dir_cont:
        if i in to_ignore:
            continue

        fullpath = os.path.join(current_dir, i).replace("\\", "/")
        # print(fullpath)

        if os.path.isfile(fullpath):
            dir_dict['files'][i] = fullpath

        elif os.path.isdir(fullpath):
            dir_dict['dirs'][i] = get_dir_tree(fullpath)


    return dir_dict