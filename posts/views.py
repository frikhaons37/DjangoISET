from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Post , Comment , Like ,BadWord 
from groups.models import Group
from .forms import PostForm,PostEditForm, ReservationForm
from .forms import CommentForm
from django.contrib.auth.models import User
from accounts.models import UserProfile
from django import forms
from friend.models import FriendList
from django.contrib.auth.decorators import login_required
from msgnotifications.models import Message, Notification 
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView


def index(request):
    notifyCounter = len(Notification.objects.filter(reciever=request.user).filter(read=False))
    msgCounter = len(Message.objects.filter(reciever=request.user, read=False))

    query = request.GET.get('q', '')
    if(query):
        first_name_query1 = User.objects.filter(userprofile__first_name__icontains=str(query))
        first_name_query2 = User.objects.filter(userprofile__first_name__in=[query])
        last_name_query1 = User.objects.filter(userprofile__last_name__icontains=str(query))
        last_name_query2 = User.objects.filter(userprofile__last_name__in=[query])
        username_query1 = User.objects.filter(username__in=[query])
        username_query2 = User.objects.filter(username__icontains=str(query))

        users = first_name_query1.union(
            first_name_query1, last_name_query1, last_name_query2,username_query1,username_query2)
        
        return render(request, "users/index.html", {
            "usersResult": users,
            "query": query,
        })
    try:
        posts=Post.objects.filter(owner=request.user)
    except:
        pass
    try:
        friend_list = FriendList.objects.get(user=request.user)
        for friend in friend_list.friends.all():
            posts=posts.union(Post.objects.filter(owner=friend))
    except FriendList.DoesNotExist:
        pass
    try:
        user_groups = request.user.userprofile.groups.all()
        for group in user_groups:
            posts=posts.union(Post.objects.filter(group=group))
    except:
        pass

    if request.method == 'POST':
        post = PostForm(request.POST, request.FILES)

        if post.is_valid():
            form_content = post.cleaned_data['content']
            form_image = None
            form_poste_type = post.cleaned_data['poste_type']
            form_poste_modele = post.cleaned_data['poste_modele']
            form_nombre_pers=post.cleaned_data['nombre_pers']
            #champs de transport
            form_depart = post.cleaned_data['depart']
            form_destination = post.cleaned_data['destination']
            form_heure_depart = post.cleaned_data['heure_depart']
            form_nombre_sieges = post.cleaned_data['nombre_sieges']
            form_contact_info_transport = post.cleaned_data['contact_info_transport']

            # Champs de logement
            form_localisation = post.cleaned_data['localisation']
            form_description_logement = post.cleaned_data['description_logement']
            form_contact_info_logement = post.cleaned_data['contact_info_logement']

            # Champs de stage
            form_type_stage = post.cleaned_data['type_stage']
            form_societe = post.cleaned_data['societe']
            form_duree = post.cleaned_data['duree']
            form_sujet = post.cleaned_data['sujet']
            form_contact_info_stage = post.cleaned_data['contact_info_stage']
            form_specialiste = post.cleaned_data['specialiste']

            # Champs d'événement
            form_intitule = post.cleaned_data['intitule']
            form_description_evenement = post.cleaned_data['description_evenement']
            form_lieu = post.cleaned_data['lieu']
            form_contact_info_evenement = post.cleaned_data['contact_info_evenement']


            if 'image' in request.FILES:
                form_image = request.FILES['image']
 
            # Create a new Post object but don't save it yet
            post_obj = Post(
                content=form_content,
                owner=request.user,
                image=form_image,
                poste_type=form_poste_type,
                poste_modele=form_poste_modele,
                nombre_pers=form_nombre_pers,
                #transport
                depart=form_depart,
                destination=form_destination,
                heure_depart=form_heure_depart,
                nombre_sieges=form_nombre_sieges,
                contact_info_transport=form_contact_info_transport,
                # Champs de logement
                localisation=form_localisation,
                description_logement=form_description_logement,
                contact_info_logement=form_contact_info_logement,
                # Champs de stage
                type_stage=form_type_stage ,
                societe=form_societe,
                duree=form_duree,
                sujet=form_sujet,
                contact_info_stage=form_contact_info_stage,
                specialiste=form_specialiste,
                #Champs Evenement
                intitule=form_intitule,
                description_evenement=form_description_evenement,
                lieu=form_lieu,
                contact_info_evenement=form_contact_info_evenement)
            


            # Save the post object
            post_obj.save()

            return redirect("index")


    else:
        post = PostForm()
        
    try:
        posts = Post.objects.filter(owner=request.user)
    except:
        pass

    try:
        friend_list = FriendList.objects.get(user=request.user)
        for friend in friend_list.friends.all():
            posts = posts.union(Post.objects.filter(owner=friend))
    except FriendList.DoesNotExist:
        pass

    try:
        user_groups = request.user.userprofile.groups.all()
        for group in user_groups:
            posts = posts.union(Post.objects.filter(group=group))
    except:
        pass



    posts = posts.order_by('-created_at')
    groups = request.user.userprofile.groups.all()

    return render(request, "posts/index.html", {
        "form": post,
        "posts": posts,
        "groups": groups,
        "notifyCounter": notifyCounter,
        "msgCounter": msgCounter,
      
    })



class PostDeleteView(DeleteView):
    model = Post
    template_name = 'posts/index.html'  
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.owner != request.user:
            return render(request, 'unauthorized.html')
        self.object.delete() 
        return redirect("index")  


class PostUpdateView(UpdateView):
    model = Post
    form_class = PostEditForm
    template_name = 'posts/edit.html'
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = self.object
        return context



def view(request, id):
    post = Post.objects.get(pk=id)
    return render(request, "posts/view.html", {
        "post": post
    })


def AddCommentView(request, id):
    post = Post.objects.get(pk=id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        form_content = form.cleaned_data['content']
        comment_obj = Comment.objects.create(
            content=form_content, owner=request.user, post=post)
        comment_obj.save()
        return redirect("view", post.id)

    return render(request, "posts/add_comment.html", {
        "form": form,
        "post": post

    })

def delComment(request,id): 
    comment = Comment.objects.get(pk=id)
    if comment.owner != request.user:
        return render(request,'unauthorized.html')
    post=comment.post
    comment.delete()
    return redirect("/posts/view/"+str(post.id))

def like_post(request): 
    user = request.user
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post_obj = Post.objects.get(id=post_id)

        if user in post_obj.liked.all():
            post_obj.liked.remove(user)
        else:
            post_obj.liked.add(user)  

        like, created = Like.objects.get_or_create(user = user,post_id = post_id ) 

        if not created:
            if like.value == 'Like':
                like.value = 'Unlike' 
            else :
                 like.value = 'Like'    
        like.save()            
        return redirect("index")

def post_likes(request, id):
    post = Post.objects.get(pk=id)
    return render(request, "posts/post_likes.html", {
        "post": post
    })    


#La reservation
def ajout_reservation(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user  
            if reservation.nombre_pers <= post.nombre_pers:
                reservation.post = post
                reservation.save()
                post.nombre_pers -= reservation.nombre_pers
                post.save()
                return redirect("index")  
            else:
                form.add_error('nombre_pers', "Le nombre de personnes réservées dépasse le nombre de places disponibles.")
    else:
        form = ReservationForm()
    return render(request, 'posts/ajoutReservation.html', {'form': form, 'post': post})