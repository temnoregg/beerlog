from math import ceil
from django.template import Library
from django.template.defaultfilters import date

register = Library()

@register.simple_tag
def chart(logs, size=(400,200), max_values=100):
    temps, labels = [], []
    logs = logs.reduce(step)
    total = len(logs)

    if total > max_values:
        step = int(ceil(total/max_values))
    else:
        step = 1 

    mod = 10 * step

    for log in logs:
        temp = '%s' % log[2]
	label = date(log[1], "H:i")
        temps.append(temp)
        
        if not log[0] % mod:
            labels.append(label)
        else:
            labels.append('|')
    
    labels = labels[1:]
    
    
    return """http://chart.apis.google.com/chart?chs=400x200&cht=lc&chd=t:%s&chxt=x,y&chxl=0:|%s&chds=15,25&chxr=1,15,25,1&chg=0,10""" % (u','.join(temps), u'|'.join(labels))
