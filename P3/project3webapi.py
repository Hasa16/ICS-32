import urllib.request
import urllib.parse
import sys
import time
import json


BASE_URL = 'https://nominatim.openstreetmap.org'
PURPLEAIR_URL = 'https://www.purpleair.com/data.json'
REFERER_URL = 'https://www.ics.uci.edu/~thornton/ics32/ProjectGuide/Project3/jchan20'


class APIforAQI:
    def __init__(self) -> None:
        """Connect to PurpleAir webAPI

        Returns:
            None

        """
        file, status = _get_result(PURPLEAIR_URL)
        self._AQIInfo = []
        try:
            for data in file['data']:
                self._AQIInfo.append([data[1],data[4],data[25],data[27],data[28]])
        except:
            _fail(status, PURPLEAIR_URL, 'FORMAT')

    def AQIInfo(self) -> [['data']]:
        """Get PurpleAir Data

        Returns:
            'data': information given from PurpleAir"""
        return self._AQIInfo


class CenAPI:
    def __init__(self, location_name: str) -> None:
        """Search on Nominatim street map of location

        Args:
            location_name: Name of the location given

        Returns:
            None

        """
        url = BASE_URL + '/search?' + \
              urllib.parse.urlencode([('q', location_name),('format', 'json'),('Referer', 'https://www.ics.uci.edu/~thornton/ics32/ProjectGuide/Project3/dpnhan')])
        file, status = _get_result(url)
        try:
            self._latitude = float(file[0]['lat'])
            self._longitude = float(file[0]['lon'])
        except:
            _fail(status, url, 'FORMAT')

    def coordinates(self) -> (float, float):
        """Receive coordinates and returns them

        Return:
            float: Longitude and Latitude values"""
        return self._latitude, self._longitude


class APIReverse:
    def display(self, coordinates: [float,float]) -> str:
        """Find display name of webAPI

        Returns:
            str: Name of display name"""
        url = BASE_URL + '/reverse?' + \
              urllib.parse.urlencode([('lat', coordinates[0]),('lon', coordinates[1]),('format','json'),('Referer', 'https://www.ics.uci.edu/~thornton/ics32/ProjectGuide/Project3/dpnhan')])
        file, status = _get_result(url)
        time.sleep(1)
        try:
            return file['display_name']
        except:
            _fail(status, PURPLEAIR_URL, 'FORMAT')


def _get_result(url: str) -> (dict, int):
    """Get result from webAPI

    Args:
        url: string of URL used

    Returns:
        dict: status
        int: error code

    """
    response = None
    try:
        request_url = urllib.request.Request(url)
        response = urllib.request.urlopen(request_url)
        status = response.getcode()
        if status == 200:
            try:
                json_text = response.read().decode(encoding = 'utf-8')
                return json.loads(json_text), status
            except:
                _fail(status, url, 'FORMAT')
        else:
            _fail(status, url, 'NOT 200')
    except urllib.error.HTTPError as error:
        status = int(str(error)[10:14])
        _fail(status, url, 'NOT 200')
    except urllib.error.URLError:
        _fail(None, url, 'NETWORK')
    finally:
        if response != None:
            response.close()


def _fail(status: int or None, url: str, end_message: str) -> None:
    """Print failure message

    Args:
        status: status of webAPI
        url: URL of web API
        end_message: end_message of web API

    Returns:
        None

    """
    print('FAILED')
    if status == None:
        print(url)
    else:
        print(status, url)
    print(end_message)
    sys.exit()

