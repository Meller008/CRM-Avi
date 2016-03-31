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


def sql_select(query, parametr=tuple()):
    connect, cursor, = sql_conn()
    cursor.execute(query, parametr)
    result = cursor.fetchall()
    cursor.close()
    connect.close()
    return result


def sql_change(query, parametr=tuple()):
    connect, cursor, = sql_conn()
    cursor.execute(query, parametr)
    result = "нет ID"
    if cursor.lastrowid:
        result = str(cursor.lastrowid)
    connect.commit()
    cursor.close()
    connect.close()
    return result
