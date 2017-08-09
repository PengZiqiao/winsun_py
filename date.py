import datetime
import calendar

class Week():
    """
    monday, sunday 为上周一、日
    N 为上周周数
    """
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

    def history(self, i):
        """
        从上周起往前的第i周
        :return: (monday, sunday, N)
        """
        monday = self.monday - datetime.timedelta(weeks=i)
        sunday = self.sunday - datetime.timedelta(weeks=i)
        N = self.N - i
        return (monday,sunday,N)   

class Month():
    N = datetime.date.today().month
