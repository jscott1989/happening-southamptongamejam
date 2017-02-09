"""Game jam views."""

from django.shortcuts import render, redirect
from happening.utils import require_permission
from django.contrib import messages
from .forms import GuestLoginForm, RegisterMacForm
from happening.models import HappeningSite
from django.contrib.auth.decorators import login_required


@require_permission("manage_events")
def dashboard(request):
    hs = HappeningSite.objects.first()
    return render(request, "southampton_game_jam_2017/admin/index.html",
                           {"mac_addresses": hs._data.get("mac_addresses", []),
                            "guest_logins": hs._data.get("guest_logins", [])})


@require_permission("manage_events")
def add_guest_login(request):
    form = GuestLoginForm()
    if request.method == "POST":
        form = GuestLoginForm(request.POST)
        if form.is_valid():
            hs = HappeningSite.objects.first()
            guest_logins = hs._data.get("guest_logins", [])
            guest_logins.append({"username": form.cleaned_data['username'], "password": form.cleaned_data['password']})
            hs._data["guest_logins"] = guest_logins
            hs.save()
            messages.success(request, "Login added")
            form = GuestLoginForm()
    return render(request,
                  "southampton_game_jam_2017/admin/add_guest_login.html",
                  {"form": form})


@login_required
def register_mac_address(request):
    form = RegisterMacForm()
    hs = HappeningSite.objects.first()
    mac_addresses = hs._data.get("mac_addresses", [])
    this_macs = [x for x in mac_addresses if x.get("userid") == request.user.pk]
    if request.method == "POST":
        form = RegisterMacForm(request.POST)
        if form.is_valid():
            mac_addresses.append({"address": form.cleaned_data['mac_address'], 'userid': request.user.pk, "username": str(request.user)})
            hs._data["mac_addresses"] = mac_addresses
            hs.save()
            messages.success(request, "Registration request sent. If it's not complete within 10 minutes contact a volunteer.")
            return redirect("index")
    return render(request,
                  "southampton_game_jam_2017/register_mac_address.html", {"form": form, "this_macs": this_macs})


@login_required
def guest_login(request):
    hs = HappeningSite.objects.first()
    guest_logins = hs._data.get("guest_logins", [])
    this_login = [x for x in guest_logins if x.get("userid") == request.user.pk]
    if len(this_login) > 0:
        this_login = this_login[0]
    else:
        this_login = None

        if request.method == "POST":
            # Register one
            for i in guest_logins:
                if "userid" not in i:
                    i["userid"] = request.user.pk
                    i["claim_username"] = str(request.user)
                    hs.save()
                    return redirect("guest_login")

    return render(request, "southampton_game_jam_2017/guest_login.html", {"this_login": this_login})