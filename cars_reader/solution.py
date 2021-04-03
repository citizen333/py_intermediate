import csv

def isint(value):
    try:
        int(value)
        return True
    except:
        return False

def isfloat(value):
    try:
        float(value)
        return True
    except:
        return False

class CarBase:
    
    photo_exts = ('.jpg', '.jpeg', '.png', '.gif')
    car_types = ('car', 'truck', 'spec_machine')
    
    def __init__(self, brand, photo_file_name, carrying):
        self._car_type = None
        self._photo_file_name = photo_file_name
        self.brand = brand
        self.carrying = float(carrying)
    
    car_type = property()
    
    @car_type.getter
    def car_type(self):
        return self._car_type
    
    @car_type.setter
    def car_type(self, value):
        if value in self.car_types:
            self._car_type = value
        else:
            raise ValueError('incorrect value of car_type')
        
    photo_file_name = property()
    
    @photo_file_name.getter
    def photo_file_name(self):
        return self._photo_file_name
    
    @photo_file_name.setter
    def photo_file_name(self, value):
        if value.endswith(self.photo_exts):
            self._photo_file_name = value
        else:
            raise ValueError('incorrect photo extesion')
            
    def get_photo_file_ext(self):
        ext = self._photo_file_name.split('.')[-1]
        return '.' + ext


class Car(CarBase):
    def __init__(self, brand, photo_file_name, carrying,\
        passenger_seats_count):
        super().__init__(brand, photo_file_name, carrying)
        self.car_type = 'car'
        self.passenger_seats_count = int(passenger_seats_count)


class Truck(CarBase):
    def __init__(self, brand, photo_file_name, carrying, body_whl):
        super().__init__(brand, photo_file_name, carrying)
        self.car_type = 'truck'
        try:
            body_whl_list = body_whl.split('x')
            can_split_whl = True
        except:
            can_split_whl = False
        valid_whl_format = can_split_whl and (len(body_whl_list) == 3)\
            and isfloat(body_whl_list[0]) and isfloat(body_whl_list[1])\
            and isfloat(body_whl_list[2])
        if valid_whl_format:
            self.body_length = float(body_whl_list[0])
            self.body_width = float(body_whl_list[1])
            self.body_height = float(body_whl_list[2])
        else:
            self.body_length = 0.0
            self.body_width = 0.0
            self.body_height = 0.0
    
    def get_body_volume(self):
        return self.body_length * self.body_width * self.body_height


class SpecMachine(CarBase):
    def __init__(self, brand, photo_file_name, carrying, extra):
        super().__init__(brand, photo_file_name, carrying)
        self.car_type = 'spec_machine'
        self.extra =extra


def validate_row(row):
    valid_len = len(row) == 7
    if not valid_len:
        return False
    valid_car_type = row[0] in CarBase.car_types
    valid_brand = len(row[1]) > 0 and not row[1].isspace()
    valid_photo_ext = row[3].endswith(CarBase.photo_exts) and\
        len(row[3].split('.')[0]) > 0
    valid_carring = isint(row[5]) or isfloat(row[5])
    return valid_len and valid_brand and valid_car_type and\
        valid_photo_ext and valid_carring

def get_car_list(csv_filename):
    car_list = []
    with open(csv_filename) as csv_fd:
        reader = csv.reader(csv_fd, delimiter=';')
        next(reader)  # пропускаем заголовок
        for row in reader:
            valid_row = validate_row(row)
            if not valid_row:
                continue
            if row[0] == 'car':
                if row[2].isdigit():
                    car_list.append(Car(row[1], row[3], row[5], row[2]))
            elif row[0] == 'truck':
                car_list.append(Truck(row[1], row[3], row[5], row[4]))
            elif row[0] == 'spec_machine':
                if len(row[6]) > 0:
                    car_list.append(SpecMachine(row[1], row[3], row[5], row[6]))
    return car_list
