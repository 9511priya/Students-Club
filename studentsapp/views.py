from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from studentsapp.models import User, Events, EventsRegistered, Sports, SportsRegistered, Accommodation
from django.contrib import messages

# Create your views here.
from studentsapp.utils import convert_date_time_to_format


def index_page(request):
    return render(request, "index.html", {})


def home_page(request):
    return render(request, "home.html", {})


def register(request):
    if request.method == "POST":
        try:
            User.objects.get(shu_id=request.POST['shu_id'])
            messages.error(request, "Student Already Exist")
        except Exception as E:
            User.objects.create(first_name=request.POST['first_name'], email=request.POST["shu_email"],
                                last_name=request.POST['last_name'], dob=request.POST['dob'],
                                shu_id=request.POST['shu_id'], username=request.POST['shu_id'],
                                password=make_password(request.POST["password"]))
            messages.success(request, "Student Registered Successfully")
        return redirect('index_login')


def login(request):
    if request.method == "POST":
        username, password = request.POST['username'], request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            auth_login(request, user)
            # user_name = request.user
            # messages.success(request, 'Login Successful')
            return redirect('home')
        else:
            messages.error(request, 'Invalid Login Credentials')
            return redirect('index_login')
    else:
        return redirect('index_login')


def events_update(request, event_id):
    if request.method == "POST":
        request_data = request.POST
        events_obj = Events.objects.get(event_id=event_id)
        events_obj.event_name = request_data["event_name"]
        events_obj.event_date_time = request_data["event_date_time"]
        events_obj.event_place = request_data["event_place"]
        events_obj.save()
    return redirect("add_events")


def events_delete(request, event_id):
    events_obj = Events.objects.get(event_id=event_id)
    events_obj.delete()
    return redirect("add_events")


def add_events(request):
    data = []
    if request.method == "POST":
        request_data = request.POST
        Events.objects.create(event_id=request_data["event_id"], event_name=request_data["event_name"],
                              event_date_time=request_data["event_date_time"],
                              event_place=request_data["event_place"])
        return redirect("add_events")
    events_obj = Events.objects.all()
    all_events_registered = EventsRegistered.objects.all()
    # to get registered / not registered status for event
    events_registered = all_events_registered.filter(student_id=request.user)
    registered_events_li = []
    for registered_event in events_registered:
        registered_events_li.append(registered_event.event_id)
    # ends
    for event in events_obj:
        event_details = {
            "event_id": event.event_id,
            "event_name": event.event_name,
            "event_date": event.event_date_time.date,
            "event_time": event.event_date_time.time,
            "event_date_time": convert_date_time_to_format(event.event_date_time, "%Y-%m-%dT%H:%M"),
            "event_place": event.event_place,
            "registered_students": all_events_registered.filter(event_id=event).count()
        }
        if request.user.is_superuser:
            data.append(event_details)
        else:
            if event in registered_events_li:
                event_details["is_registered"] = True
            else:
                event_details["is_registered"] = False
            data.append(event_details)
    return render(request, "events.html", {"context_data": data})


def event_registered_students_list(request, event_id):
    event_data = []
    students_data = []
    events_registered_obj = EventsRegistered.objects.filter(event_id=Events.objects.get(event_id=event_id))
    for registered_event in events_registered_obj:
        event_data.append({
            "event_id": registered_event.event_id.event_id,
            "event_name": registered_event.event_id.event_name,
        })
        students_data.append({
            "student_id": registered_event.student_id.shu_id,
            "first_name": registered_event.student_id.first_name,
            "last_name": registered_event.student_id.last_name,
        })
    return render(request, "registered_events_students.html",
                  {"event_data": event_data, "students_data": students_data})


def register_for_event(request, event_id):
    user_obj = User.objects.get(username=request.user)
    event_obj = Events.objects.get(event_id=event_id)
    EventsRegistered.objects.create(event_id=event_obj, student_id=user_obj)
    return redirect("add_events")


def deregister_for_event(request, event_id):
    user_obj = User.objects.get(username=request.user)
    event_obj = Events.objects.get(event_id=event_id)
    EventsRegistered.objects.get(event_id=event_obj, student_id=user_obj).delete()
    return redirect("add_events")


def add_sports(request):
    data = []
    if request.method == "POST":
        request_data = request.POST
        Sports.objects.create(sport_id=request_data["sport_id"], sport_name=request_data["sport_name"],
                              sport_date_time=request_data["sport_date_time"],
                              sport_place=request_data["sport_place"])
        return redirect("add_sports")
    sports_obj = Sports.objects.all()
    all_sports_registered = SportsRegistered.objects.all()
    # to get registered / not registered status for event
    sports_registered = all_sports_registered.filter(student_id=request.user)
    registered_sports_li = []
    for registered_sport in sports_registered:
        registered_sports_li.append(registered_sport.sport_id)
    # ends
    for sport in sports_obj:
        sport_details = {
            "sport_id": sport.sport_id,
            "sport_name": sport.sport_name,
            "sport_date": sport.sport_date_time.date,
            "sport_time": sport.sport_date_time.time,
            "sport_date_time": convert_date_time_to_format(sport.sport_date_time, "%Y-%m-%dT%H:%M"),
            "sport_place": sport.sport_place,
            "registered_students": all_sports_registered.filter(sport_id_id=sport).count()
        }
        if request.user.is_superuser:
            data.append(sport_details)
        else:
            if sport in registered_sports_li:
                sport_details["is_registered"] = True
            else:
                sport_details["is_registered"] = False
            data.append(sport_details)
    return render(request, "sports.html", {"context_data": data})


def sports_update(request, sport_id):
    if request.method == "POST":
        request_data = request.POST
        sports_obj = Sports.objects.get(sport_id=sport_id)
        sports_obj.sport_name = request_data["sport_name"]
        sports_obj.sport_date_time = request_data["sport_date_time"]
        sports_obj.sport_place = request_data["sport_place"]
        sports_obj.save()
    return redirect("add_sports")


def sports_delete(request, sport_id):
    sports_obj = Sports.objects.get(sport_id=sport_id)
    sports_obj.delete()
    return redirect("add_sports")


def register_for_sport(request, sport_id):
    user_obj = User.objects.get(username=request.user)
    sport_obj = Sports.objects.get(sport_id=sport_id)
    SportsRegistered.objects.create(sport_id=sport_obj, student_id=user_obj)
    return redirect("add_sports")


def deregister_for_sport(request, sport_id):
    user_obj = User.objects.get(username=request.user)
    sport_obj = Sports.objects.get(sport_id=sport_id)
    SportsRegistered.objects.get(sport_id=sport_obj, student_id=user_obj).delete()
    return redirect("add_sports")


def sport_registered_students_list(request, sport_id):
    sport_data = []
    students_data = []
    sports_registered_obj = SportsRegistered.objects.filter(sport_id=Sports.objects.get(sport_id=sport_id))
    for registered_sport in sports_registered_obj:
        sport_data.append({
            "event_id": registered_sport.sport_id.sport_id,
            "event_name": registered_sport.sport_id.sport_name,
        })
        students_data.append({
            "student_id": registered_sport.student_id.shu_id,
            "first_name": registered_sport.student_id.first_name,
            "last_name": registered_sport.student_id.last_name,
        })
    return render(request, "registered_sports_students.html",
                  {"event_data": sport_data, "students_data": students_data})


def accommodation_get_post(request):
    if request.method == "POST":
        request_data = request.POST
        print("REQUEST DATA", request_data)
        Accommodation.objects.create(gender_type=request_data["gender_type"],
                                     availability_count=request_data["availability_count"],
                                     contact=request_data["contact"], city=request_data["city"],
                                     state=request_data["state"], address1=request_data["address1"],
                                     address2=request_data["address2"], user=request.user)
        return redirect("add_accommodation")
    accommodation_obj = Accommodation.objects.all()
    data = []
    for accommodation in accommodation_obj:
        data.append({
            "acc_id": accommodation.id,
            "user_name": accommodation.user.username,
            "availability_count": accommodation.availability_count,
            "gender_type": accommodation.gender_type,
            "contact": accommodation.contact,
            "city": accommodation.city,
            "state": accommodation.state,
            "address1": accommodation.address1,
            "address2": accommodation.address2,
            "available": accommodation.available
        })
    return render(request, "accommodation.html", {"context_data": data})


def accommodation_update(request, acc_id):
    if request.method == "POST":
        request_data = request.POST
        acc_obj = Accommodation.objects.get(id=acc_id)
        acc_obj.city = request_data["city"]
        acc_obj.state = request_data["state"]
        acc_obj.contact = request_data["contact"]
        acc_obj.gender_type = request_data["gender_type"]
        acc_obj.available = True if str(request_data.get("available")) == "on" else False
        acc_obj.availability_count = request_data["availability_count"]
        acc_obj.address1 = request_data["address1"]
        acc_obj.address2 = request_data["address2"]
        acc_obj.save()
    return redirect("add_accommodation")


def accommodation_delete(request, acc_id):
    acc_obj = Accommodation.objects.get(id=acc_id)
    acc_obj.delete()
    return redirect("add_accommodation")


def logout(request):
    auth_logout(request)
    return redirect('login')
