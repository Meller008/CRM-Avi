from os import remove, getcwd


def del_temp_file(name):
    remove(getcwd() + '/temp/%s' % name)
