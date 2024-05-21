from django import forms
from .models import Post, Reservation
from .models import Comment
from .models import BadWord
from django.core.exceptions import ValidationError
class PostForm(forms.ModelForm):

    class Meta:
        model = Post    
        fields = ("content","image","poste_type","poste_modele",
            # Fields for transport
            "depart",
            "destination",
            "heure_depart",
            "nombre_sieges",
            "contact_info_transport",
            # Fields for logement
            "localisation",
            "description_logement",
            "contact_info_logement",
            # Fields for stage
            "type_stage",
            "societe",
            "duree",
            "sujet",
            "contact_info_stage",
            "specialiste",
            # Fields for evenement
            "intitule",
            "description_evenement",
            "lieu",
            "contact_info_evenement",'nombre_pers')
    def __init__(self, *args, **kwargs):
            super(PostForm, self).__init__(*args, **kwargs)
            self.fields['content'].error_messages = {'required': ''}

           
    def clean_content(self):
            content = self.cleaned_data.get('content')
            bad_words = BadWord.objects.all()
            results = list(map(lambda x: x.word, bad_words))
            
            body_list = content.split()
            bad_words_list = []
            for word in results:
                if word in body_list:
                    bad_words_list.append(word)
            bad_words_string = ', '.join(bad_words_list)
            
            if len(bad_words_list) > 0:
                raise ValidationError("The content of a post contain bad words (" + bad_words_string + ") , please remove it")
            return content


class PostEditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image', 'poste_type', 'poste_modele', 'depart', 
                  'destination', 'heure_depart', 'nombre_sieges', 'contact_info_transport', 
                  'localisation', 'description_logement', 'contact_info_logement', 'type_stage', 
                  
                  'societe', 'duree', 'sujet', 'contact_info_stage', 'specialiste', 'intitule',
                    'description_evenement', 'lieu', 'contact_info_evenement','nombre_pers']



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment 
        fields = ("content",)

    def clean_content(self):
            content = self.cleaned_data.get('content')
            bad_words = BadWord.objects.all()
            results = list(map(lambda x: x.word, bad_words))
            
            body_list = content.split()
            bad_words_list = []
            for word in results:
                if word in body_list:
                    bad_words_list.append(word)
            bad_words_string = ', '.join(bad_words_list)
            
            if len(bad_words_list) > 0:
                raise ValidationError("The content of a comment contain bad words (" + bad_words_string + "), please remove it")
            return content   
    

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['name', 'nombre_pers']

