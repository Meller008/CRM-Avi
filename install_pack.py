from os import getcwd, path, listdir
import shutil

# modules = ["pyserial", "openpyxl", "pyBarcode", "Pillow", "requests"]

copy_modules = ["certifi", "chardet", "idna", "mysql-connector-python", "num to text",
                "openpyxl", "PIL", "pyBarcode", "pyserial", "requests", "urllib3", "suds", "xmltodict"]
modules_folder = "C:\\Python34\\Lib\\site-packages"


def red(text):
    return "\033[91m" + text + "\033[0m"


def green(text):
    return "\033[92m" + text + "\033[0m"


def yellow(text):
    return "\033[93m" + text + "\033[0m"


# def upgrade_pip():
#     print("Обновлю PIP")
#     subprocess.call("C:\Python34\python -m pip install --upgrade pip", shell=False)
#     print(green("PIP Обновлен"))
#
#     try:
#         import pip._internal as pip
#     except ImportError:
#         pass
#
#
# def search_module_list(modules):
#     no_modules = []
#     installed_packages = pip.get_installed_distributions()
#     installed_packages_list = sorted(["%s" % (i.key,) for i in installed_packages])
#
#     for modul in modules:
#         if modul.lower() in installed_packages_list:
#             print(green("Модуль %s установлен" % modul))
#         else:
#             print(red("Модуль %s не установлен" % modul))
#             no_modules.append(modul)
#
#     return no_modules
#
#
# def install_module(module):
#     print(yellow("Устанавливаю %s" % module))
#     pip.main(["install", module])
#     print(green("Установил %s" % module))


def copy_lib(copy_folder):
    print(yellow("Копирую %s" % copy_folder))
    lib_dir = getcwd() + '\\python_libs\\'
    for file in listdir(lib_dir + copy_folder):
        if path.isdir(lib_dir + copy_folder + "/" + file):
            try:
                shutil.copytree(lib_dir + copy_folder + "\\" + file, modules_folder + "\\" + file)
            except:
                pass
        else:
            try:
                shutil.copy(lib_dir + copy_folder + "\\" + file, modules_folder)
            except PermissionError:
                pass
    print(green("Скопировал %s" % copy_folder))

print(yellow("Сейчас я скопирую пакеты"))
for copy_mod in copy_modules:
    copy_lib(copy_mod)

print(green("Готово"))