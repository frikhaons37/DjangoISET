from django.db import models
from django.contrib.auth.models import User
from groups.models import Group

import datetime





class Post(models.Model):
    TYPEPOSTCHOICES = [
        ('offre', 'offre'),
        ('demande', 'demande')]
    MODELECHOICES = [
        ('stage', 'stage'),
        ('transport', 'transport'),
        ('evenement', 'evenement'),
        ('logement', 'logement'),]  
    poste_type = models.TextField(choices=TYPEPOSTCHOICES, default='demande')
    poste_modele=models.TextField(choices=MODELECHOICES, blank=True)
# Les champs de transport---------------------------------------------------------------------------
    depart = models.CharField(max_length=255, null=True, blank=True)
    destination = models.CharField(max_length=255, null=True, blank=True)
    heure_depart = models.CharField(max_length=255, null=True, blank=True)
    nombre_sieges = models.IntegerField(null=True, blank=True)
    contact_info_transport = models.CharField(max_length=255, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    # Les champs de logement-----------------------------------------------------------------------
    localisation = models.CharField(max_length=255, null=True, blank=True)
    description_logement = models.TextField(null=True, blank=True)
    contact_info_logement = models.CharField(max_length=255, null=True, blank=True)
    # Les champs de stage---------------------------------------------------------------------------
    TYPESTAGECHOICES=[
        (1,'ouvrier'),
        (2,'technicien'),
        (3,'PFE')]
    type_stage = models.IntegerField(choices=TYPESTAGECHOICES, null=True, blank=True)
    societe = models.CharField(max_length=255, null=True, blank=True)
    duree = models.IntegerField(null=True, blank=True)
    sujet = models.TextField(null=True, blank=True)
    contact_info_stage = models.CharField(max_length=255, null=True, blank=True)
    specialiste = models.CharField(max_length=255, null=True, blank=True)
    # Les champs d'événement--------------------------------------------------------------------------
    intitule = models.CharField(max_length=255, null=True, blank=True)
    description_evenement = models.TextField(null=True, blank=True)
    lieu = models.CharField(max_length=255, null=True, blank=True)
    contact_info_evenement = models.CharField(max_length=255, null=True, blank=True)


    nombre_pers=models.IntegerField( default=1,blank=True)

    content=models.TextField(max_length=2000 )
    created_at=models.DateTimeField(auto_now_add=True)
    image=models.ImageField(null=True, blank=True)
    owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name="post")
    group=models.ForeignKey(Group,on_delete=models.CASCADE, null=True,blank=True,related_name="post")
    liked=models.ManyToManyField(User,default=None,blank=True,related_name="liked")
    def __str__(self):
        return str(self.content[0:15]+"...")

    @property
    def num_likes(self):
        self.liked.all().count()

class Comment(models.Model):

    content=models.TextField(max_length=1000 )
    created_at=datetime.datetime.now()

    owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name="comments")
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name="comments")
    def __str__(self):
        return str(self.content[0:15]+"...")

LIKE_CHOICES = (
    ('Like','Like'),
    ('Unlike','Unlike')
)



class Like(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    value=models.CharField(choices=LIKE_CHOICES ,default='Like',max_length=10)
   
    def __str__(self):
        return str(self.post)






      
        
class BadWord(models.Model):

    word   = models.CharField(max_length=100)
    
    def __str__(self):
        return self.word



class Reservation(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    name= models.CharField(max_length=100, null=True, blank=True)
    nombre_pers=models.IntegerField( blank=True)


    def __str__(self):
        return f"Reservation {self.pk} for Post {self.post.pk} by User {self.user.username}"