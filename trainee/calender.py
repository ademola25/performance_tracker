from datetime import datetime, timedelta
from calendar import HTMLCalendar
from gt_logs.models import GtLog


class Calendar(HTMLCalendar):
	def __init__(self, year=None, month=None, day=None, trainee= None, weekends = None):
		self.year = year
		self.month = month
		self.day = day
		self.trainee = trainee
		self.weekends = weekends

		super(Calendar, self).__init__()

	def formatday(self, day, events):

		
		events_per_day = events.filter(log_date__day=day)
		d = ''
		current_year = datetime.now().year
		current_day = datetime.now().day
		current_month = datetime.now().month
		for event in events_per_day:
			d  += f'<a class="calendar_list btn btn-success disable"> </a>'

			

		if day in self.weekends:
			return f"<td> <small>{day}</small> </td>"
		if day != 0:
			if current_month == self.month and current_year == self.year:
				if day > self.day:
					return f"<td> <small>{day}</small> </td>"

			if d:
				return f"<td><h3><a data-day={day} href='/trainee/log/past-day/{day}/{self.month}' class='text-success font-bold p-b-20'> {day}</a></td>"
			else:
				return  f"<td style='color:#e20f00 !important;'class='text-error font-bold'><a data-day={day} href='/trainee/log/past-day/{day}/{self.month}'> {day}</a></td>"
		return '<td> </td>'

	def formatweek(self, theweek, events):
		week = ''
		for d, weekday in theweek:
			week += self.formatday(d, events)
		return f'<tr> {week} </tr>'

	def formatmonth(self, withyear=True):
		events = GtLog.objects.filter(log_date__year=self.year, log_date__month=self.month, trainee=self.trainee)
		cal = f'<table border="0" cellpadding="0" cellspacing="0"     class="calendar">\n'
		cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
		cal += f'{self.formatweekheader()}\n'
		for week in self.monthdays2calendar(self.year, self.month):
			cal += f'{self.formatweek(week, events)}\n'
		return cal

