import datetime as dt


def calc_total_exp(*args, end2=None):
    total = dt.timedelta()
    dl, ml, yl = map(int, end2.split('.'))
    end2 = dt.date(yl, ml, dl)
    for i in args:
        d1, m1, y1 = map(int, i[0].split('.'))
        start_date = dt.date(y1, m1, d1)
        if start_date > end2:
            continue
        if i[1] != 'null':
            d2, m2, y2 = map(int, i[1].split('.'))
            end_date = dt.date(y2, m2, d2)
        else:
            end_date = end2
        end_date = min(end2, end_date)
        interval_len = end_date - start_date
        total = total + interval_len
    return total.days if total.days > 0 else 0


def calc_before_entering_exp(entered_date, *args, end2=None):
    if entered_date == 'null':
        return calc_total_exp(*args, end2=end2)
    total = dt.timedelta()
    entered_d, entered_m, entered_y = map(int, entered_date.split('.'))
    entered_date = dt.date(entered_y, entered_m, entered_d)
    dl, ml, yl = map(int, end2.split('.'))
    end2 = dt.date(yl, ml, dl)
    for i in args:
        d1, m1, y1 = map(int, i[0].split('.'))
        start_date = dt.date(y1, m1, d1)
        if i[1] != 'null':
            d2, m2, y2 = map(int, i[1].split('.'))
            end_date = dt.date(y2, m2, d2)
        else:
            end_date = end2
        if start_date >= entered_date or start_date >= end2:
            continue
        end_date = min(entered_date, end2, end_date)
        interval_len = end_date - start_date
        total = total + interval_len
    return total.days


def today():
    t = dt.date.today()
    return t.year, t.month, t.day
