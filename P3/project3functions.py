from pathlib import Path
import project3webapi as p3a
import json
import sys
import math


class CenFile:
    def __init__(self, file_name: str) -> None:
        """Read longitude and latitude values from a given file during initializaion.
        Prints a FORMAT failure message if file is in incorrect format.

        Returns:
            None

        """
        file = _open_file(file_name)
        try:
            self._latitude = float(file[0]['lat'])
            self._longitude = float(file[0]['lon'])
        except:
            _fail(file_name, 'FORMAT')

    def coordinates(self) -> (float, float):
        """Return longitude and latitude values from center file.

        Returns:
            float: longitude and latitude values

        """
        return self._latitude, self._longitude
        
        
class FileAQI:
    def __init__(self, file_name: str) -> None:
        """Read important information from all sensors in given PurpleAir file, and
        Prints a FORMAT failure message if file is in incorrect format.
        Information: PM concentration, time since last report, indoor or outdoor type, longitude, and latitude

        Returns:
            None

        """
        file = _open_file(file_name)
        try:
            self._AQIInfo = []
            for data in file['data']:
                self._AQIInfo.append([data[1],data[4],data[25],data[27],data[28]])
        except:
            _fail(file_name, 'FORMAT')

    def AQIInfo(self) -> [['data']]:
        """Return important information from all sensors

        Return:
            'data': information about AQI sensors

        """
        return self._AQIInfo


class FileReverse:
    def __init__(self, files: [str]) -> None:
        """Read important locational data from all files during start and
        Prints FORMAT failure message if file is in incorrect format
        Data: longitude values, latitude values, display names

        Returns:
            None

        """
        self._reverse_data = []
        for file_name in files:
            file = _open_file(file_name)
            try:
                self._reverse_data.append([[float(file["lat"]),float(file['lon'])],file["display_name"]])
            except:
                _fail(file_name, 'FORMAT')

    def display(self, coordinates: [float,float]) -> str:
        """Return the closest display name to the set of longitude and latitude coordinates

        Returns:
            Str: String of the set of Longitude and Latitude values

        """
        smallest_distance = None
        current_display = ''
        for data in self._reverse_data:
            distance = (data[0][0]-coordinates[0])**2 + (data[0][1]-coordinates[1])**2
            if smallest_distance == None or distance < smallest_distance:
                current_display = data[1]
                smallest_distance = distance
        return current_display


def take_input() -> str:
    """Take input from user and stores it in strings

    Args:
        None

    Returns:
        Str: User inputs for center_str, range_miles, threshold, max_locations, aqi_str, and reverse_str

    """
    center_str = input()
    range_miles = input()
    threshold = input()
    max_locations = input()
    aqi_str = input()
    reverse_str = input()
    return center_str, range_miles, threshold, max_locations, aqi_str, reverse_str


def find_info(center_str: str, range_miles: str, threshold: str, max_locations: str, aqi_str: str, reverse_str: str) -> str:
    """Take information and use webapi to determine locations and information.

    Args:
        center_str: Center location
        range_miles: Range around center
        threshold: AQI minimum
        max_locations: Maximum location count returned
        aqi_str: Type of AQI used
        reverse_str: Nominatim's reverse geocoding

    Returns:
        Str: information on certain locations

    """
    mile_range = int(range_miles.lstrip('RANGE '))
    threshold = int(threshold.lstrip('THRESHOLD '))
    max_locations = int(max_locations.lstrip('MAX '))
    if center_str.startswith('CENTER FILE '):
        center = CenFile(center_str.lstrip('CENTER FILE '))
    elif center_str.startswith('CENTER NOMINATIM '):
        center = p3a.CenAPI(center_str.lstrip('CENTER NOMINATIM '))
    else:
        fail('INPUT FORMAT')
    if aqi_str.startswith('AQI FILE '):
        aqi = FileAQI(aqi_str[9:])
    if aqi_str == 'AQI PURPLEAIR':
        aqi = p3a.APIforAQI()
    if reverse_str.startswith('REVERSE FILES'):
        reverse_data = FileReverse(reverse_str.lstrip('REVERSE FILES ').split())
    elif reverse_str == ('REVERSE NOMINATIM'):
        reverse_data = p3a.APIReverse()
    else:
        fail('INPUT FORMAT')
    return center, mile_range, threshold, max_locations, aqi, reverse_data


def find_data(aqi: 'aqi', center, mile_range) -> list:
    """Find data within AQI and stores it

    Args:
        aqi: aqi information
        center: center location
        mile_range: range around center

    Returns:
        list: list of data

    """
    store_data = []
    for data in aqi.AQIInfo():
        if None not in data:
            if distance(center.coordinates(), [data[3],data[4]]) <= mile_range:
                if data[1] <= 3600:
                    if data[2] == 0:
                        store_data.append([data[0],[data[3],data[4]]])
    return store_data


def print_center(center: 'Center') -> None:
    """Print center location and coordinates

    Args:
        center: center location

    Returns:
        None

    """
    print('CENTER', _format_coordinates(center.coordinates()))


def distance(coordinates1: [float,float], coordinates2: [float,float]) -> float:
    """Find the distance from center location

    Args:
        coordinates1: coordinates of center location
        coordinates2: coordinates of other area

    Returns:
        float: distance from center area

    """
    distance_latitude = math.radians(coordinates1[0] - coordinates2[0])
    distance_longitude = math.radians(coordinates1[1] - coordinates2[1])
    area_latitude = math.radians((coordinates1[0] + coordinates2[0]) / 2)
    distance = math.sqrt((distance_longitude * math.cos(area_latitude))**2 + distance_latitude**2) * 3958.8
    return distance


def print_data(data: ['data'], reverse_data: 'Reverse') -> None:
    """Print data given

    Args:
        data: Data given
        reverse_data: reverse geocoding of data

    Returns:
        none

    """
    print('AQI', str(data[0]) + '\n' + _format_coordinates(data[1]) + '\n' + reverse_data.display(data[1]))


def convert_pm_to_aqi(concentration: int) -> int:
    """Convert 2.5PM to AQI value

    Args:
        concentration: PM Int Value

    Returns:
        int: AQI value

    """
    if concentration < 12.1:
        return round(concentration * 50 / 12)
    elif concentration < 35.5:
        return round((35.4-concentration) / (35.4-12.1) * 51 + (12.1-concentration) / (12.1-35.4) * 100)
    elif concentration < 55.5:
        return round((55.4-concentration) / (55.4-35.5) * 101 + (35.5-concentration) / (35.5-55.4) * 150)
    elif concentration < 150.5:
        return round((150.4-concentration) / (150.4-55.5) * 151 + (55.5-concentration) / (55.5-150.4) * 200)
    elif concentration < 250.5:
        return round((250.4-concentration) / (250.4-150.5) * 201 + (150.5-concentration) / (150.5-250.4) * 250.5)
    elif concentration < 350.5:
        return round((350.4-concentration) / (350.4-250.5) * 301 + (250.5-concentration) / (250.5-350.4) * 400)
    elif concentration < 500.5:
        return round((500.4-concentration) / (500.4-350.5) * 401 + (350.5-concentration) / (350.5-500.4) * 500)
    else:
        return 501


def fail(end_message: str) -> None:
    """Print failure message

    Args:
        end_message: end message of web API

    Returns:
        None

    """
    print('FAILED')
    print(end_message)
    sys.exit()


def _format_coordinates(coordinates: [float, float]) -> str:
    """Take provided coordinates and formats them

    Args:
        coordinates: two float values representing longitude and latitude

    Returns:
        str: A string of the coordinates

    """
    if coordinates[0] > 0:
        lat_str = str(coordinates[0]) + '/N'
    elif coordinates[0] < 0:
        lat_str = str(-coordinates[0]) + '/S'
    else:
        lat_str = str(-coordinates[0])
    if coordinates[1] > 0:
        lon_str = str(coordinates[1]) + '/E'
    elif coordinates[1] < 0:
        lon_str = str(-coordinates[1]) + '/W'
    else:
        lon_str = str(-coordinates[1])
    return lat_str + ' ' + lon_str


def _open_file(file: str) -> 'data':
    """Open file provided

    Args:
        file: file path provided

    Returns:
        'data': data provided by given file

    """
    f = None
    try:
        f = open(file, encoding = 'UTF-8')
        file_data = f.read()
    except FileNotFoundError:
        _fail(file, 'MISSING')
    finally:
        if f != None:
            f.close()
    try:
        return json.loads(file_data)
    except:
        print(file)
        _fail(file, 'FORMAT')


def _fail(file: str, end_message: str) -> None:
    """Print file failure message

    Args:
        file: file provided
        end_message: error message

    Returns:
        None

    """
    print('FAILED')
    print(str(Path().resolve()) + '\\' + file)
    print(end_message)
    sys.exit()

