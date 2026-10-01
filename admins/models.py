from django.db import models

class svmmodel(models.Model):
    accuracy = models.FloatField()
    precision = models.FloatField()
    recall = models.FloatField()
    f1_score = models.FloatField()
    

    def __str__(self):
        return f"svm model (Accuracy: {self.accuracy}) - {self.created_at}"
    
