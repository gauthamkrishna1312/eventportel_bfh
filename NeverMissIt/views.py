from django.contrib import auth
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from datetime import date

from .models import EventDetails, EventParticipants
from .forms import SignUpForm, EventCreationForm

# Create your views here.

def homepage(request):
    if request.user.is_authenticated:
        return redirect('NeverMissIt:profilepage')

    else:
        # EventDetails.objects.filter(lastdatetoreg__gt=date.today()).order_by('lastdatetoreg')
        coming_events_in_order = EventDetails.objects.filter(lastdatetoreg__gte=date.today()).order_by('lastdatetoreg')
        context = {'events':coming_events_in_order}
        return render(request, 'NeverMissIt/homepage.html', context)

def signuppage(request):
    if request.user.is_authenticated:
        return redirect('NeverMissIt:profilepage')
    
    else:
        form = SignUpForm()

        if request.method == "POST":
            form = SignUpForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Account created succesfully for ' + form.cleaned_data.get('username'))
                return redirect('NeverMissIt:loginpage')

        context = {'form':form}
        return render(request, 'NeverMissIt/signuppage.html', context)

def loginpage(request):
    if request.user.is_authenticated:
        return redirect('NeverMissIt:profilepage')

    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('NeverMissIt:profilepage')
            else :
                messages.info(request, 'username and password does not match')

        context = {}
        return render(request, 'NeverMissIt/loginpage.html', context)

@login_required(login_url='NeverMissIt:loginpage') # only allowed if " LOGGED IN "
def logoutpage(request):
    logout(request)
    return redirect('NeverMissIt:loginpage')

@login_required(login_url='NeverMissIt:loginpage') # only allowed if " LOGGED IN "
def profilepage(request):
    registered_not_over = EventDetails.objects.filter( id__in=[x.eventid_id for x in EventParticipants.objects.filter(teamleader_id = request.user.pk) ] ).filter(eventdate__gte=date.today()).order_by('eventdate')
    registered_over = EventDetails.objects.filter( id__in=[x.eventid_id for x in EventParticipants.objects.filter(teamleader_id = request.user.pk) ] ).filter(eventdate__lt=date.today()).order_by('-eventdate')
    created_not_over = EventDetails.objects.filter(createduserid_id = request.user.pk).filter(eventdate__gte=date.today()).order_by('eventdate')
    created_over = EventDetails.objects.filter(createduserid_id = request.user.pk).filter(eventdate__lt=date.today()).order_by('-eventdate')
    available_events = EventDetails.objects.filter(lastdatetoreg__gte=date.today()).exclude( id__in=[x.eventid_id for x in EventParticipants.objects.filter(teamleader_id = request.user.pk) ] ).exclude( createduserid_id = request.user.pk ).order_by('lastdatetoreg')
    context = {'registered_not_over':registered_not_over, 'registered_over':registered_over, 'created_not_over':created_not_over, 'created_over':created_over, 'available_events':available_events}
    return render(request, 'NeverMissIt/profilepage.html', context)

@login_required(login_url='NeverMissIt:loginpage') # only allowed if " LOGGED IN "
def createeventpage(request):
    form = EventCreationForm()

    if request.method == "POST":
        form = EventCreationForm(request.POST)
        if form.is_valid():
            eventform = form.save(commit=False)
            eventform.createduserid_id = request.user.pk
            eventform.save()
            return redirect('NeverMissIt:profilepage')

    context = {'form':form}
    return render(request, 'NeverMissIt/createeventpage.html', context)

@login_required(login_url='NeverMissIt:loginpage') # only allowed if " LOGGED IN "
def detaileventpage(request):
    eventid = request.GET['eventid']
    event = EventDetails.objects.get(pk=eventid)
    teammates = []
    #condition for the user for being the creator (EventDetails.objects.get(pk=eventid).createduserid_id==request.user.pk)
    #condition for the user if he is a registered participant ( it is the else condition for the previous one )
    if not EventDetails.objects.get(pk=eventid).createduserid_id == request.user.pk:
        team = EventParticipants.objects.get(teamleader_id=request.user.pk, eventid_id=eventid).participants
        teammates = team.split('&')
    context = {'event':event, 'teammates':teammates}
    return render(request, 'NeverMissIt/detaileventpage.html', context)

@login_required(login_url='NeverMissIt:loginpage') # only allowed if " LOGGED IN "
def editeventpage(request):
    eventid = request.GET['eventid']
    event = EventDetails.objects.get(pk=eventid)

    if request.method == "POST":
        if bool(request.POST.get('delyesorno')):
            EventDetails.objects.filter(pk=eventid).delete()
            EventParticipants.objects.filter(eventid_id=eventid).delete()
            return redirect('NeverMissIt:profilepage')

    context = {'event':event}
    return render(request, 'NeverMissIt/editeventpage.html', context)

@login_required(login_url='NeverMissIt:loginpage') # only allowed if " LOGGED IN "
def registereventpage(request):
    eventid = request.GET['eventid']
    no_of_teammates = EventDetails.objects.get(pk=eventid).maxparticipants - 1
    teammates = ["teammate "+str(x) for x in range(1, no_of_teammates+1)]
    event = EventDetails.objects.get(pk=eventid)

    if request.method == 'POST':
        t = []
        for i in teammates:
            t.append(request.POST.get(i).strip())
        while '' in t:
            t.remove('')
        team = "&".join(t)
        print(team)
        eventregister = EventParticipants(teamleader_id=request.user.pk, eventid_id=eventid, participants=team)
        eventregister.save()
        return redirect('NeverMissIt:profilepage')
    
    # passing teammates, eventdetail object of the current event
    context = {'teammates':teammates, 'event':event}
    return render(request, 'NeverMissIt/registereventpage.html', context)