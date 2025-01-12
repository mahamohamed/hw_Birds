from django.db import models
from django.urls import reverse

MEALS = (
    ('B', 'Breakfast'),
    ('L', 'Lunch'),
    ('D', 'Dinner')
)

class Bird(models.Model):
    name=models.CharField(max_length=100)
    breed=models.CharField(max_length=100)
    describtion = models.TextField(max_length=250)
    age = models.IntegerField()
    image=models.ImageField(upload_to='main_app/static/upload/',default="")
    def __str__(self):
     return self.name
    def get_absolute_url(self):
     return reverse('detail',kwargs={'bird_id':self.id})
    


class Feeding(models.Model):
  date = models.DateField()
  meal = models.CharField(max_length=1, choices=MEALS, default=MEALS[0][0])
  bird = models.ForeignKey(Bird, on_delete=models.CASCADE)
  def __str__(self):
   return f"{self.bird.name}{self.get_meal_display()} on {self.date}"