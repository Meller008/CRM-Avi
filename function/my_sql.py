import configparser
from os import getcwd
import mysql.connector


def sql_settings():
    config = configparser.ConfigParser()
    config.sections()
    config.read(getcwd() + '/setting/settings.ini')
    return (config["sql_connect"]["ip"], config["sql_connect"]["db_name"],
            config["sql_connect"]["name"], config["sql_connect"]["password"])


def sql_conn():
        con_conf = sql_settings()
        try:
            conn = mysql.connector.connect(host=con_conf[0], database=con_conf[1], user=con_conf[2], password=con_conf[3])
            cursor = conn.cursor()
            return conn, cursor

        except mysql.connector.Error as e:
            print(e)


def sql_select(query, parametr):
    co, cu, = sql_conn()
    cu.execute(query, parametr)
    return cu.fetchall()
