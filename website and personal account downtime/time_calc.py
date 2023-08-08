import datetime
import math
import re

def corector(param1:str, param2:str):
    result_date_1 = f'{param1[2]}-{param1[1]}-{param1[0]} {param1[3]}:{param1[4]}:{param1[5]}'
    result_date_2 = f'{param2[2]}-{param2[1]}-{param2[0]} {param2[3]}:{param2[4]}:{param2[5]}'
    return [result_date_1, result_date_2]

def slicing_time(date_one, date_two):
    
    if date_one == date_two:
        return False
    try:
        date_one = [item for item in re.split("|".join(" -:"), date_one) if item]
        date_one = [int(date) for date in date_one]

        date_two = [item for item in re.split("|".join(" -:"), date_two) if item]
        date_two = [int(date) for date in date_two]

        date_mod_1 = datetime.datetime(year=date_one[0],month=date_one[1],day=date_one[2],
                                    hour=date_one[3],minute=date_one[4],second=date_one[5])

        date_mod_2 = datetime.datetime(year=date_two[0],month=date_two[1],day=date_two[2],
                                    hour=date_two[3],minute=date_two[4],second=date_two[5])

        delta = date_mod_2 - date_mod_1
        delta_sec = delta.total_seconds()
        diff = delta_sec / 3600
        segments = math.ceil(diff / 12)
        list_segm = [date_mod_1]

        for i in range(segments):
            diff_time = datetime.timedelta(hours=12)
            new_time = diff_time+list_segm[-1]
            if new_time > date_mod_2 or new_time == date_mod_2:
                list_segm.append(date_mod_2)
                break
            list_segm.append(new_time)
        return list_segm
    except:
        return False