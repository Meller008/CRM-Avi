import configparser
from os import getcwd
import mysql.connector


def sql_settings():
    config = configparser.ConfigParser()
    config.sections()
    config.read(getcwd() + '/setting/settings_lan.ini')
    # config.read("C:/Users/cs007/Desktop/CRM-Avi/setting/settings_lan.ini")
    return (config["sql_connect"]["ip"], config["sql_connect"]["db_name"],
            config["sql_connect"]["name"], config["sql_connect"]["password"])


def sql_conn():
    con_conf = sql_settings()
    try:
        conn = mysql.connector.connect(host=con_conf[0], database=con_conf[1], user=con_conf[2], password=con_conf[3])
        cursor = conn.cursor()
        return conn, cursor

    except mysql.connector.Error as error:
        print(error)
        return error


def sql_select(query, parametr=tuple()):
    try:
        connect, cursor, = sql_conn()
        cursor.execute(query, parametr)
        result = cursor.fetchall()
        cursor.close()
        connect.close()
        return result

    except mysql.connector.Error as error:
        print(error)
        connect.rollback()
        cursor.close()
        connect.close()
        return error


def sql_change(query, parametr=tuple()):
    try:
        connect, cursor, = sql_conn()
        cursor.execute(query, parametr)
        result = "нет ID"
        if cursor.lastrowid:
            result = str(cursor.lastrowid)
        connect.commit()
        cursor.close()
        connect.close()
        return result

    except mysql.connector.Error as error:
        print(error)
        connect.rollback()
        cursor.close()
        connect.close()
        return error


def sql_many(query, parametr=tuple()):
    try:
        connect, cursor, = sql_conn()
        cursor.executemany(query, parametr)
        result = "нет ID"
        if cursor.lastrowid:
            result = str(cursor.lastrowid)
        connect.commit()
        cursor.close()
        connect.close()
        return result

    except mysql.connector.Error as error:
        print(error)
        connect.rollback()
        cursor.close()
        connect.close()
        return error


def sql_start_transaction():
    try:
        connect, cursor, = sql_conn()
        connect.start_transaction(isolation_level='REPEATABLE READ')
        cursor.close()
        print("SQL - Транзакция начата")
        return connect

    except mysql.connector.Error as error:
        print("SQL - Ошибка открытия транзакции")
        print(error)
        connect.rollback()
        cursor.close()
        connect.close()
        return error


def sql_select_transaction(connect, query, parametr=tuple()):
    try:
        cursor = connect.cursor()
        cursor.execute(query, parametr)
        result = cursor.fetchall()
        cursor.close()
        print("SQL - Получил информацию")
        return result

    except mysql.connector.Error as error:
        print("SQL - Ошибка при получении информации")
        print(error)
        sql_rollback_transaction(connect)
        return error


def sql_change_transaction(connect, query, parametr=tuple()):
    try:
        cursor = connect.cursor()
        cursor.execute(query, parametr)
        result = "нет ID"
        if cursor.lastrowid:
            result = str(cursor.lastrowid)
        cursor.close()
        print("SQL - Изменения прошли")
        return result

    except mysql.connector.Error as error:
        print("SQL - Ошибка при изменении")
        print(error)
        sql_rollback_transaction(connect)
        return error


def sql_many_transaction(connect, query, parametr=tuple()):
    try:
        cursor = connect.cursor()
        cursor.executemany(query, parametr)
        result = "нет ID"
        if cursor.lastrowid:
            result = str(cursor.lastrowid)
        cursor.close()
        return result

    except mysql.connector.Error as error:
        print("SQL - Ошибка при изменении")
        print(error)
        sql_rollback_transaction(connect)
        return error


def sql_commit_transaction(connect):
    try:
        connect.commit()
        connect.close()
        print("SQL - Транзакция закомичена")
        return True

    except mysql.connector.Error as error:
        print("SQL - Ошибка закомичивании транзакции")
        print(error)
        return error


def sql_rollback_transaction(connect):
    try:
        connect.rollback()
        connect.close()
        print("SQL - Транзакция откачена")
        return True

    except mysql.connector.Error as error:
        print("SQL - Ошибка при откате транзакции")
        print(error)
        return error
