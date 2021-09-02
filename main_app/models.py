from django.db import models
from django.urls import reverse

MEALS = (
  ('B', 'Breakfast'),
  ('L', 'Lunch'),
  ('D', 'Dinner')
)

# Create your models here.
class Finch(models.Model):
  name = models.CharField(max_length=100)
  color = models.CharField(max_length=100)
  description = models.TextField(max_length=250)
  canFly = models.BooleanField(default=True)

  def __str__(self):
    return self.name

  def get_absolute_url(self):
    return reverse('finches_detail', kwargs={'finch_id' : self.id})

class Feeding(models.Model):
  date = models.DateField('Feeding date')
  meal = models.CharField(max_length=1, choices=MEALS, default=MEALS[0][0])

  finch = models.ForeignKey(Finch, on_delete = models.CASCADE)

  def __str__(self):
    return f"{self.get_meal_display()} on {self.date}"

  class Meta:
    ordering = ['-date']