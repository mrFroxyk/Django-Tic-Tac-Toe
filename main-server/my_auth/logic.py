import json


# Чтение счетчика из файла
class GlobalIDUserManager(object):
    '''
    Синглтон для менеджмента гостевых id
    '''

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(GlobalIDUserManager, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.global_counter = self.read_counter()

    def get_id_for_new_guest(self):
        self.global_counter += 1
        self.write_counter(self.global_counter)
        return self.global_counter

    @staticmethod
    def read_counter():
        try:
            with open('counter.json', 'r') as file:
                counter_data = json.load(file)
            return counter_data.get('counter', 0)
        except FileNotFoundError:
            return 0

    # Запись счетчика в файл
    @staticmethod
    def write_counter(counter):
        counter_data = {'counter': counter}
        with open('counter.json', 'w') as file:
            json.dump(counter_data, file)
