import calendar
import datetime


def range_of_current_month():
    today = datetime.datetime.today()
    month = today.month
    year = today.year
    month_range = calendar.monthrange(year, month)
    end_of_month = str(today.year)+'-'+str(today.month)+'-'+str(month_range[1])
    beginning_of_month = str(today.year)+'-'+str(today.month)+'-01'
    return calendar.month_name[month], year, beginning_of_month, end_of_month


def month_name_to_number(month_name):
    months_dict = {
        'January': 1,
        'February': 2,
        'March': 3,
        'April': 4,
        'May': 5,
        'June': 6,
        'July': 7,
        'August': 8,
        'September': 9,
        'October': 10,
        'November': 11,
        'December': 12
    }
    return months_dict[month_name]
