class User:
    id = ""
    login = ""
    privilege = ""


class Auth:
    _instance = None

    def __init__(self):
        # some initialization
        self._id = 1
        pass

    def getInstance(self):
        if self._instance is None:
            self._instance = "123"
            print(1)
        print(0)
        return self._instance