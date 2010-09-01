from django.db import models


class TemperatureLogManager(models.Manager):
   def reduce(self, step):
      from django.db import connections
      cursor = connections['temperature'].cursor()
      cursor.execute("""
      	SELECT * FROM ( 
	   SELECT @row := @row +1 AS rownum, timestamp, temp 
	   FROM ( SELECT @row :=0) r, beer_log 
	) ranked WHERE rownum %%%s = 1""", (int(step),))
      return cursor.fetchall()
