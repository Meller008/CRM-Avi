from function import my_sql


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class User(metaclass=Singleton):
    def __init__(self):
        self.__id = None
        self.__f_name = None
        self.__l_name = None
        self.__position_id = None
        self.__position_name = None

    def id(self):
        return self.__id

    def position_name(self):
        return self.__position_name

    def set_id(self, id):
        query = """SELECT staff_worker_info.Id, staff_worker_info.First_Name, staff_worker_info.Last_Name, staff_position.Id, staff_position.Name
                      FROM staff_worker_info LEFT JOIN staff_position ON staff_worker_info.Position_Id = staff_position.Id
                      WHERE staff_worker_info.Id = %s"""
        sql_info = my_sql.sql_select(query, (id, ))
        if "mysql.connector.errors" in str(type(sql_info)):
            raise RuntimeError("Не смог получить операции артикула")

        self.__id = sql_info[0][0]
        self.__f_name = sql_info[0][1]
        self.__l_name = sql_info[0][2]
        self.__position_id = sql_info[0][3]
        self.__position_name = sql_info[0][4]

