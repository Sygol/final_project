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
