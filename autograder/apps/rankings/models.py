from django.db import models


class RatingChange(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey("index.GraderUser", on_delete=models.CASCADE, default=1)
    rating = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"RatingChange #{self.id} for User {self.user_id} -> {self.rating}"
