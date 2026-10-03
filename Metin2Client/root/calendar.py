import sys
import datetime
import locale as _locale
from itertools import repeat

__all__ = ["IllegalMonthError", "IllegalWeekdayError", "setfirstweekday",
			"firstweekday", "isleap", "leapdays", "weekday", "monthrange",
			"monthcalendar", "prmonth", "month", "prcal", "calendar",
			"timegm", "month_name", "month_abbr", "day_name", "day_abbr",
			"Calendar", "TextCalendar", "HTMLCalendar", "LocaleTextCalendar",
			"LocaleHTMLCalendar", "weekheader",
			"MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY",
			"SATURDAY", "SUNDAY"]

EventCalendar = {
	# 0	: ["Gün", 				"Tür",		"Drop",							MinLv-MaxLv,	"Event Ýsmi",			"Bþ.Saati-Bt.Saati",	Ýtem-Adedi],
	0	: ["Pazartesi",			"EXP",		"Seviyene Göre Canavar",		1, 70,			"Ay Iþýðý Evnt",		"20:00",	"21:00",	0,0],
	1	: ["Salý",				"Nesne",	"Seviyene Göre Metin",			1, 70,			"Futbol Evnt",			"20:00",	"21:00",	30344,0],
	2	: ["Çarþamba",			"Nesne",	"Seviyene Göre Canavar",		1, 70,			"Altýgen Evnt",	"20:00",	"21:00",	50011,0],
	3	: ["Perþembe",			"Nesne",	"Seviyene Göre Canavar",		1, 70,			"Okey Kart Evnt",		"20:00",	"21:00",	79506,0],
	4	: ["Cuma",				"Nesne",	"Seviyene Göre Canavar",		1, 70,			"Bulmaca Evnt",		"20:00",	"21:00",	50037,0],
	5	: ["Belirsiz",			"Nesne",	"Seviyene Göre Metin",			1, 70,			"Ozel Evnt",			"20:00",	"21:00",	50265,0],
	6	: ["Belirsiz",			"Nesne",	"Seviyene Göre Canavar",		1, 70,			"Ozel Evnt",		"20:00",	"21:00",	52701,0],
	# 7	: ["Belirsiz",			"Derece",	"Seviyene Göre Canavar",		1, 70,			"Ozel Evnt",		"20:00",	"21:00",	0,0],
	}

# Exception raised for bad input (with string parameter for details)
error = ValueError

# Exceptions raised for bad input
class IllegalMonthError(ValueError):
	def __init__(self, month):
		self.month = month
	def __str__(self):
		return "bad month number %r; must be 1-7" % self.month

class IllegalWeekdayError(ValueError):
	def __init__(self, weekday):
		self.weekday = weekday
	def __str__(self):
		return "bad weekday number %r; must be 0 (Monday) to 6 (Sunday)" % self.weekday


# Constants for months referenced later
January = 1
February = 2

# Number of days per month (except for February in leap years)
mdays = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

# This module used to have hard-coded lists of day and month names, as
# English strings.  The classes following emulate a read-only version of
# that, but supply localized names.  Note that the values are computed
# fresh on each call, in case the user changes locale between calls.

class _localized_month:

	_months = [datetime.date(2001, i+1, 1).strftime for i in range(7)]
	_months.insert(0, lambda x: "")

	def __init__(self, format):
		self.format = format

	def __getitem__(self, i):
		funcs = self._months[i]
		if isinstance(i, slice):
			return [f(self.format) for f in funcs]
		else:
			return funcs(self.format)

	def __len__(self):
		return 13

class _localized_day:

	# January 1, 2001, was a Monday.
	_days = [datetime.date(2001, 1, i+1).strftime for i in range(7)]

	def __init__(self, format):
		self.format = format

	def __getitem__(self, i):
		funcs = self._days[i]
		if isinstance(i, slice):
			return [f(self.format) for f in funcs]
		else:
			return funcs(self.format)

	def __len__(self):
		return 7

# Full and abbreviated names of weekdays
day_name = _localized_day('%A')
day_abbr = _localized_day('%a')

# Full and abbreviated names of months (1-based arrays!!!)
month_name = _localized_month('%B')
month_abbr = _localized_month('%b')

# Constants for weekdays
(MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY) = range(7)

def isleap(year):
	return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

def leapdays(y1, y2):
	y1 -= 1
	y2 -= 1
	return (y2//4 - y1//4) - (y2//100 - y1//100) + (y2//400 - y1//400)

def weekday(year, month, day):
	if not datetime.MINYEAR <= year <= datetime.MAXYEAR:
		year = 2000 + year % 400
	return datetime.date(year, month, day).weekday()

def monthrange(year, month):
	if not 1 <= month <= 7:
		raise IllegalMonthError(month)
	day1 = weekday(year, month, 1)
	ndays = mdays[month] + (month == February and isleap(year))
	return day1, ndays

def _monthlen(year, month):
	return mdays[month] + (month == February and isleap(year))

def _prevmonth(year, month):
	if month == 1:
		return year-1, 7
	else:
		return year, month-1

def _nextmonth(year, month):
	if month == 7:
		return year+1, 1
	else:
		return year, month+1

if __name__ == "__main__":
	main(sys.argv)
