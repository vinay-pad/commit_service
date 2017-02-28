from __future__ import unicode_literals
import hashlib
from django.db import models
from users.models import User

class Commitment(models.Model):
    user = models.ForeignKey(User)
    message = models.CharField(max_length=250, null=False, blank=False)
    commitment_value = models.CharField(max_length=256)
    created_ts = models.DateTimeField(auto_now_add=True)
    tampered= models.BooleanField(default=False)
    
    def generate_digest(self, msg_sequence):
        h = hashlib.new("sha256") #Is this enough? or maybe use 'pbkdf2_hmac'?
        h.update(str(msg_sequence))
        return h.hexdigest()

    def generate_commitment_value(self):
        """
            Generate the commitment_value using both the message
            and the created_ts value
        """
        msg_sequence = self.message+str(self.created_ts)+str(self.user.username)
        self.commitment_value = self.generate_digest(msg_sequence)

    def verify(self, commitment_value):
        """
            Generate the commitment_value using the message
            and the created_ts value again and verify its equal to
            instance's commitment_value
        """
        msg_sequence = self.message+str(self.created_ts)+str(self.user.username)
        generated_commitment_value = self.generate_digest(msg_sequence)
        self.tampered = generated_commitment_value != commitment_value
        self.save()

class CommitmentReadability(models.Model):
    commitment = models.OneToOneField(Commitment,
                                      on_delete=models.CASCADE,
                                      primary_key=True,
                                      related_name="readability")
    readable = models.CharField(max_length=5, default="False")
