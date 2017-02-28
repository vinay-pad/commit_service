from __future__ import unicode_literals
import hashlib
from django.db import models
from users.models import User

class Commitment(models.Model):
    user = models.ForeignKey(User)
    message = models.CharField(max_length=250, null=False, blank=False)
    commitment_value = models.CharField(max_length=256)
    created_ts = models.DateTimeField(auto_now_add=True)

    def generate_commitment_value(self):
        """
            Generate the commitment_value using both the message 
            and the created_ts value
        """
        h = hashlib.new("sha256") #Is this enough? or maybe use 'pbkdf2_hmac'?
        h.update(self.message+str(self.created_ts))
        self.commitment_value = h.hexdigest()

class CommitmentReadability(models.Model):
    commitment = models.OneToOneField(Commitment,
                                      on_delete=models.CASCADE,
                                      primary_key=True,
                                      related_name="readability")
    readable = models.CharField(max_length=5, default="False")
