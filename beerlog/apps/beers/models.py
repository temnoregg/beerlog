from django.db import models
from django.utils.translation import ugettext_lazy as _

from managers import *


BREWING_METHODS = (
    (1, _('All Grains')),
    (2, _('Malt Extract'))
)

class Beer(models.Model):
    """Beer Model"""
    name = models.CharField(_('title'), max_length=80)
    slug = models.SlugField(_('slug'))
    category = models.ForeignKey('Category', verbose_name=_('Category'))
    method = models.PositiveIntegerField(_('brewing method'), choices=BREWING_METHODS)
    
    batch = models.DecimalField(_('batch volume in litres'), max_digits=6, decimal_places=2)
    
    procedure = models.TextField(_('procedure'), blank=True)
    
    date_started = models.DateTimeField(_('date started'), blank=True, null=True)
    date_finished = models.DateTimeField(_('date finished'), blank=True, null=True)
    
    original_gravity = models.IntegerField(_('original gravity'), blank=True, null=True)
    final_gravity = models.IntegerField(_('final gravity'), blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = []
        verbose_name, verbose_name_plural = _('beer'), _('beers')

    def __unicode__(self):
        return u"Beer"

    @models.permalink
    def _get_absolute_url(self):
        return ('Beer_detail', (), {})

    def get_temp_log(self):
        ds, df = self.date_started, self.date_finished
        
        if ds and df:
            temp_list = TemperatureLog.objects.filter(timestamp__gte=ds, timestamp__lte=df)
            return temp_list
        elif ds:
            temp_list = TemperatureLog.objects.filter(timestamp__gte=ds)
            return temp_list
        
        return None

class Category(models.Model):
    name = models.CharField(_('name'), max_length=80)
    slug = models.SlugField(_('slug'), max_length=80)

    def __unicode__(self):
        return u'%s' % (self.name,)


UNITS = (
    ('pc', _('piece')),
    ('g', _('gram')),
    ('kg', _('kilogram')),
    ('l', _('litre')),
    ('ml', _('mililitre')),
)

class Ingredient(models.Model):
    """(Ingredient description)"""
    beer = models.ForeignKey(Beer)
    name = models.CharField(_('name'), max_length=80)
    price = models.DecimalField(_('price per unit'), max_digits=6, decimal_places=2)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(_('unit'), choices=UNITS, max_length=2)

    class Meta:
        ordering = []
        verbose_name, verbose_name_plural = "", "s"

    def __unicode__(self):
        return u"Ingredient"

    @models.permalink
    def _get_absolute_url(self):
        return ('Ingredient_detail', (), {})


LOG_CATEGORIES = (
    ('brewstart', _('Brewing Started')),
    ('brewend', _('Brewing Ended')),
    ('bottling', _('Bottling')),
    ('gravity', _('Gravity')),
)

class Log(models.Model):
    """(Log description)"""
    beer = models.ForeignKey(Beer)
    category = models.CharField(_('category'), choices=LOG_CATEGORIES, max_length=15)
    note = models.TextField(_('note'), blank=True, null=True)
    timestamp = models.DateTimeField()

    class Meta:
        ordering = ['timestamp',]

    def __unicode__(self):
        return u"Log"


class TemperatureLog(models.Model):
    timestamp = models.DateTimeField(primary_key=True)
    temp = models.DecimalField(_('temperature'), max_digits=5, decimal_places=2)

    objects = TemperatureLogManager()

    class Meta:
        ordering = ['timestamp',]
        db_table = 'beer_log'
        
    def __unicode__(self):
        return u'%s %s: %s' % (_('Temperature'), self.timestamp, self.temp)
