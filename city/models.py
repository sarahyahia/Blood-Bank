from django.db import models




class City(models.Model):
    name = models.CharField(max_length=255)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    
    
    class Meta:
        verbose_name_plural = "Cities"
        ordering = ("name",)
        
    def __str__(self):
        return self.name