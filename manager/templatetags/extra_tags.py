from django import template
from manager.models import CryptoEngine
import datetime


register = template.Library()


@register.filter(is_safe=True)
def decrypt(text, master_key):
    engine = CryptoEngine(master_key=master_key)
    return engine.decrypt(text)


@register.filter(is_safe=True)
def progressbar_days_left(date):

    if date is None:
        return 'Never'
    else:
        now = datetime.date.today()
        delta = date - now
        return delta.days


@register.filter(is_safe=True)
def progressbar_width(date):

    _max = 100
    _min = 0

    if date is None:
        return '100'
    else:
        now = datetime.date.today()
        delta = date - now
        diff = delta.days
        if diff > _max:
            diff = _max
        return (_max - diff) * 100 / (_max - _min)


@register.filter(is_safe=True)
def progressbar_class(date):

    _max = 100
    _min = 0

    if date is None:
        return 'progress-success'
    else:
        now = datetime.date.today()
        delta = date - now
        diff = delta.days
        if diff > _max:
            diff = _max
        percent = (_max - diff) * 100 / (_max - _min)
        if percent < 20:
            return 'progress-success'
        elif percent < 80:
            return 'progress-warning'
        else:
            return 'progress-danger'
