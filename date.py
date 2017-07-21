import datetime
import calendar

class Week():
    sunday = datetime.date.today()
    while sunday.weekday() != calendar.SUNDAY:
        sunday -= datetime.timedelta(days=1)
    monday = sunday - datetime.timedelta(days=6)
    N = int(monday.strftime('%U'))
    

    def day_str(self, day, str_format = '%Y%m%d'):
        if day == 'start':
            day = self.monday
        elif day == 'end':
            day = self.sunday
        return f'{day.strftime(str_format)}'