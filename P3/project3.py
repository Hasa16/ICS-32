import project3functions as p3f

    
def run() -> None:
    """Run the interface for the AQI finding program.
    Print INPUT FORMAT failure message if input is in incorrect format.

    Returns:
        None

    """
    center_str, range_miles, threshold, max_locations, aqi_str, reverse_str = p3f.take_input()
    try:
        center, mile_range, threshold, max_locations, aqi, reverse_data = \
            p3f.find_info(center_str, range_miles, threshold, max_locations, aqi_str, reverse_str)
    except ValueError:
        p3f.fail('INPUT FORMAT')
    p3f.print_center(center)
    store_data = p3f.find_data(aqi, center, mile_range)
    store_data.sort(key = highest_aqi)
    for data in store_data:
        data[0] = p3f.convert_pm_to_aqi(data[0])
    good_data = [i for i in store_data if i[0] >= threshold][0:max_locations]
    for data in good_data:
        p3f.print_data(data, reverse_data)


def highest_aqi(aqi_list: list['data']) -> 'aqi':
    """Sort based on highest AQI value.
    Args:
        aqi_list: list of AQIs

    Returns:
        'aqi': aqi values

    """
    return -aqi_list[0]


if __name__ == '__main__':
    run()
