from ..client.client_factory import ClientFactory
from datetime import datetime, timedelta
import holidays


def calculate_fine(value: float, 
                   due: datetime, 
                   payment: datetime) -> float:

    selic_table = ClientFactory.create_ipea_client("SELIC").get_table()

    selic_ref_rate = (float(selic_table["VALVALOR"].iloc[-1])**1/12)/100

    next_working = next_working_day(due)

    late_days = (payment - next_working).days + 1


    if payment.month > due.month:

        diff = payment.month - due.month

        fine = 0.01 * value + value * (selic_ref_rate * diff)
    
    else:

        fine = 0.01 * value

    if (0.0033 * late_days) < 0.2:

        interest = value * (0.0033 * late_days)

    else:

        interest = value * 0.2


    return interest + fine


def count_working_days(start_date: datetime, end_date: datetime) -> int:

    current_date = start_date
    working_days = 0

    brazilian_holidays = holidays.BR()

    while current_date <= end_date:
        if current_date.weekday() < 5 and current_date not in brazilian_holidays:
            working_days += 1

        current_date += timedelta(days=1)
    
    return working_days

def next_working_day(current_date: datetime) -> datetime:
    next_day = current_date + timedelta(days=1)

    brazilian_holidays = holidays.BR()
    
    while next_day.weekday() >= 5 or next_day in brazilian_holidays:
        next_day += timedelta(days=1)

    return next_day