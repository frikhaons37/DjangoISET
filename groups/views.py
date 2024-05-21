from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponse
from .models import Group
from itertools import chain
from .forms import GroupForm
from posts.models import Post
from groups.models import Group, GroupInvite, GroupRequestJoin
from msgnotifications.models import Message,Notification
from posts.forms import PostForm
from accounts.models import UserProfile
from django.contrib.auth.models import User


def index(request):
    notifyCounter=len(  Notification.objects.filter(reciever=request.user).filter(read=False) )

    query = request.GET.get('q', '')
    if(query):
        groups = Group.objects.filter(name__icontains=str(query)).union(
            Group.objects.filter(name__in=[query]))
    else:
        groups = Group.objects.all()

    return render(request, "groups/index.html", {

        "groups": groups,
        "notifyCounter":notifyCounter


    })


def create(request):
    form = GroupForm(request.POST, request.FILES or None)
    if form.is_valid():
        print(form)

        name = form.cleaned_data['name']
        privacy = form.cleaned_data['privacy']
        description = form.cleaned_data['description']
        cover = form.cleaned_data['cover']
        group = Group.objects.create(
            name=name, privacy=privacy, description=description, cover=cover, owner=request.user)
        request.user.userprofile.groups.add(group)
        return redirect("/groups/show/"+str(group.id))
    return render(request, "groups/create.html", {
        "form": form
    })


def show(request, id):
    group = Group.objects.get(id=id)
    query = request.GET.get('q', '')
    post = PostForm(request.POST or None)
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

        post_obj = Post.objects.create(
            content=form_content, 
            owner=request.user,
              group=group,
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
            
            
            
            
        post_obj.save()
        return redirect("/groups/show/"+str(group.id))

    if(query):
        first_name_query1 = User.objects.filter(userprofile__first_name__icontains=str(query)).filter(userprofile__groups__in=[group])
        first_name_query2 = User.objects.filter(userprofile__first_name__in=[query]).filter(userprofile__groups__in=[group])
        last_name_query1 = User.objects.filter(userprofile__last_name__icontains=str(query)).filter(userprofile__groups__in=[group])
        last_name_query2 = User.objects.filter(userprofile__last_name__in=[query]).filter(userprofile__groups__in=[group])
        username_query1 = User.objects.filter(username__in=[query]).filter(userprofile__groups__in=[group])
        username_query2 = User.objects.filter(username__icontains=str(query)).filter(userprofile__groups__in=[group])

        users = first_name_query1.union(first_name_query1,first_name_query2, last_name_query1, last_name_query2,username_query1,username_query2)
        return render(request, "groups/searchResult.html", {
            "usersResult": users,
            "query": query,
            "group":group,
            "form":post
        })
    posts = Post.objects.filter(group=group).order_by('-created_at')

    groups = Group.objects.all()
    users_in_group = UserProfile.objects.filter(Q(groups=id))
    request_sent=True
    try:
        GroupRequestJoin.objects.get(requestFrom=request.user, requestTo=group.owner, group=group)
    except:
        request_sent=False
    invited = GroupInvite.objects.filter(
        inviteTo=request.user).filter(group=group)

    members = []
    for user in users_in_group:
        members.append(user.user)
    
    notifyCounter=len(  Notification.objects.filter(reciever=request.user).filter(read=False) )
        
    return render(request, "groups/show.html", {
        "posts": posts,
        "form": post,
        "groups": groups,
        "group": group,
        "users_in_group": members,
        "invited": invited,
        "request_sent":request_sent,
        "notifyCounter":notifyCounter
    })


def delete(request, id):
    post = Post.objects.get(pk=id)
    if request.user != post.owner:
        return render(request,'unauthorized.html')
    post.delete()
    return redirect("/groups/show/"+str(post.group.id))


def edit(request, id):
    postData = Post.objects.get(pk=id)
    if request.user != postData.owner:
        return render(request,'unauthorized.html')
    post = PostForm(request.POST or None, instance=postData)

    if post.is_valid():
        post.save()
        return redirect("/groups/show/"+str(postData.group.id))
    return render(request, "group-posts/edit.html", {'form': post, "data": postData})


def view(request, id):
    post = Post.objects.get(pk=id)
    return render(request, "group-posts/view.html", {
        "post": post
    })


def invite(request, id):

    users = UserProfile.objects.filter(~Q(groups=id))
    group = Group.objects.get(id=id)
    alreadyInvitedUsers = GroupInvite.objects.filter(group=group)
    print(alreadyInvitedUsers)
    notMember = []
    notInvited = False
    for user in users:
        for alreadyInvitedUser in alreadyInvitedUsers:
            if user.user == alreadyInvitedUser.inviteTo:
                notInvited = True
        if notInvited == False:
            notMember.append(user.user.id)
        notInvited = False
    invites = User.objects.filter(id__in=notMember).exclude(id=request.user.id)
    return render(request, "groups/invite.html", {
        "invites": invites,
        "id": id,
        "alreadyInvitedUsers": alreadyInvitedUsers
    })


def groupRequest(request, id):
    group = Group.objects.get(id=id)
    if request.POST:
        for user_id in dict(request.POST)["groupRequest"]:
            user = User.objects.get(id=user_id)
            invite = GroupInvite.objects.create(
                inviteFrom=request.user, inviteTo=user, group=group)
            invite.save()

    return redirect("/groups/invite/"+str(group.id))


def acceptInvitation(request, id):
    profile = UserProfile.objects.get(user=request.user)
    group = Group.objects.get(id=id)
    profile.groups.add(group)
    invitedGroup = GroupInvite.objects.get(inviteTo=request.user, group=group)
    invitedGroup.delete()
    return redirect("/groups/show/"+str(group.id))


def cancelInvitation(request, id):
    group = Group.objects.get(id=id)
    invitedGroup = GroupInvite.objects.get(inviteTo=request.user, group=group)
    invitedGroup.delete()
    return redirect("/groups/show/"+str(group.id))


def sendRequestJoin(request, id):
    group = Group.objects.get(id=id)

    try:
        GroupRequestJoin.objects.get(
            requestFrom=request.user, requestTo=group.owner, group=group)
        return render(request,'groups/inv_already_sent.html')
    except:
        invite = GroupRequestJoin.objects.create(
            requestFrom=request.user, requestTo=group.owner, group=group)
        invite.save()
    return redirect("group")



def request(request, id):
    group = Group.objects.get(id=id)
    requests = GroupRequestJoin.objects.filter(
        requestTo=request.user).filter(group=group)
    return render(request, "groups/groupRequests.html", {
        "requests": requests,
        "id": id
    })

def acceptrequest(request, id):
    group = Group.objects.get(id=id)
    text = " you are now a member in " + \
        str(group.name+" group")
    for user_id in dict(request.POST)["groupRequest"]:
        user = User.objects.get(id=user_id)
        user.userprofile.groups.add(group)
        notify_instance = Notification.objects.create(
            sender=group.owner, reciever=user, text=text, notifyType="groupView", instance_id=group.id)
        notify_instance.save()
    return redirect("group")


def acceptRefuseRequest(request, id):
    group = Group.objects.get(id=id)
    user_id = request.POST['user']
    user = User.objects.get(id=int(user_id))
    if dict(request.POST)['submit'] == ['Accept']:
        user.userprofile.groups.add(group)
        text = " you are now a member in " + str(group.name+" group")
        notify_instance = Notification.objects.create(
            sender=group.owner, reciever=user, text=text, notifyType="groupView", instance_id=group.id)
        notify_instance.save()
    elif dict(request.POST)['submit'] == ['Refuse']:
        text = " Admin of " + str(group.name+" group refused your request")
        notify_instance = Notification.objects.create(
            sender=group.owner, reciever=user, text=text, notifyType="groupView", instance_id=group.id)
        notify_instance.save()
    request = GroupRequestJoin.objects.get(
        requestTo=request.user, group=group)
    request.delete()
    return redirect("group")

def cancelRequestJoin(request,id):
    group = Group.objects.get(id=id)
    join_request = GroupRequestJoin.objects.get(
        requestFrom=request.user, group=group)
    join_request.delete()
    notification=Notification.objects.filter(sender=request.user,reciever=group.owner,instance_id=group.id,notifyType="groupRequest").order_by('created_at').last()
    notification.delete()
    return redirect("/groups/show/"+str(group.id))

def leave(request, id):
    group = Group.objects.get(id=id)
    request.user.userprofile.groups.remove(group)
    if request.user == group.owner:
        group.delete()

    return redirect("group")


def listMembers(request, id):
    group = Group.objects.get(id=id)
    users = User.objects.filter(Q(userprofile__groups=group))
    print(users)

    return render(request, "groups/members.html", {
        "users": users,
        "group": group
    })
