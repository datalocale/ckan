import datetime

from pylons.i18n import _, ungettext
from babel import numbers

import ckan.lib.i18n as i18n


##################################################
#                                                #
#              Month translations                #
#                                                #
##################################################

def month_jan():
    return _('January')


def month_feb():
    return _('February')


def month_mar():
    return _('March')


def month_apr():
    return _('April')


def month_may():
    return _('May')


def month_june():
    return _('June')


def month_july():
    return _('July')


def month_aug():
    return _('August')


def month_sept():
    return _('September')


def month_oct():
    return _('October')


def month_nov():
    return _('November')


def month_dec():
    return _('December')


# MONTH_FUNCTIONS provides an easy way to get a localised month via
# MONTH_FUNCTIONS[month]() where months are zero based ie jan = 0, dec = 11
MONTH_FUNCTIONS = [month_jan, month_feb, month_mar, month_apr,
                   month_may, month_june, month_july, month_aug,
                   month_sept, month_oct, month_nov, month_dec]


def localised_nice_date(datetime_):
    ''' Returns a friendly localised unicode representation of a datetime. '''
    now = datetime.datetime.now()
    date_diff = now - datetime_
    days = date_diff.days
    if days < 1 and now > datetime_:
        # less than one day
        seconds = date_diff.seconds
        if seconds < 3600:
            # less than one hour
            if seconds < 60:
                return _('Just now')
            else:
                return ungettext('{mins} minute ago}', '{mins} minutes ago',
                                 seconds / 60).format(mins=seconds / 60)
        else:
            return ungettext('{hours} hour ago}', '{hours} hours ago',
                             seconds / 3600).format(hours=seconds / 3600)
    # more than one day
    if days < 31:
        return ungettext('{days} day ago}', '{days} days ago',
                         days).format(days=days)
    # actual date
    month = datetime_.month
    day = datetime_.day
    year = datetime_.year
    month_name = MONTH_FUNCTIONS[month - 1]()
    return _('{month} {day}, {year}').format(month=month_name, day=day,
                                             year=year)


def localised_number(number):
    ''' Returns a localised unicode representation of number '''
    return numbers.format_number(number, locale=i18n.get_lang())


def localised_filesize(number):
    ''' Returns a localised unicode representation of a number in bytes, MiB
    etc '''
    def rnd(number, divisor):
        # round to 1 decimal place
        return localised_number(float(number * 10 / divisor) / 10)

    if number < 1024:
        return _('{bytes} bytes').format(bytes=number)
    elif number < 1024 ** 2:
        return _('{kibibytes} KiB').format(kibibytes=rnd(number, 1024))
    elif number < 1024 ** 3:
        return _('{mebibytes} KiB').format(mebibytes=rnd(number, 1024 ** 2))
    elif number < 1024 ** 4:
        return _('{gibibytes} KiB').format(gibibytes=rnd(number, 1024 ** 3))
    else:
        return _('{tebibytes} KiB').format(tebibytes=rnd(number, 1024 ** 4))