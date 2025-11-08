from django.db import models


class Document(models.Model):
    file = models.FileField(upload_to="documents/")
    text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Question(models.Model):
    document = models.ForeignKey(
        Document, on_delete=models.CASCADE, related_name="questions"
    )
    question = models.TextField()
    answer = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
