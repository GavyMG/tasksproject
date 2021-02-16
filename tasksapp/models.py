from django.db import models


class Task(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    owner_id = models.ForeignKey('auth.User', related_name='task_ids', on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['create_date']

    def __str__(self):
        return self.name
