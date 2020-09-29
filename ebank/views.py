from random import randint

from atlabs.airtime import Airtime
from atlabs.sms import Sms
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, JsonResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.csrf import csrf_exempt
from requests.exceptions import ConnectionError

from ebank.models import User, Transfer, TempTransfer


HEADER = {
    "base_url": "https://sandboxapi.fsi.ng",
    "Sandbox-Key": settings.FSI_SANDBOX_KEY,
    "Content-Type": "application/json"
}


def extract_user(request):
    """Extracts user credentials from request object."""

    data = {
        'username': request.POST.get('username', ''),
        'password': request.POST.get('password', '')
    }
    user = authenticate(
        request, username=data['username'], password=data['password']
    )
    if user is not None:
        return user
    return None


def is_authenticated(request):
    """Performs custom authentication check."""

    if request.user.is_authenticated:
        return True
    else:
        user = extract_user(request)
        if user:
            return True
    return False


def index(request):
    """This view is the home page."""
    if request.is_ajax():
        return JsonResponse({"content": "E-Bank website"})
    return HttpResponse('<h1>Welcome to E-bank</h1>')


@csrf_exempt
def login_user(request):
    """Log in user if the credentials are correct."""

    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return JsonResponse({"loggedIn": True})
    else:
        return JsonResponse({"loggedIn": False})


@csrf_exempt
def register(request):
    """Registers new account if the data is correct."""

    data = {
        'username': request.POST.get('username', ''),
        'phone': request.POST.get('phone', ''),
        'email': request.POST.get('email', ''),
        'password': request.POST.get('password', '')
    }

    if (data['username'] and data['email'] and data['password'] and
            data['phone']):
        name_taken = User.objects.filter(
            username__iexact=data['username']).exists()
        phone_taken = User.objects.filter(
            phone=data['phone']).exists()
        email_taken = User.objects.filter(
            email__iexact=data['email']).exists()

        if name_taken or phone_taken or email_taken:
            data["username_taken"] = name_taken,
            data["phone_taken"] = phone_taken,
            data["email_taken"] = email_taken,
            data["password"] = ""
            return JsonResponse(data)

        User.objects.create_user(
            username=data['username'], phone=data['phone'],
            email=data['email'], password=data['password']
        )
        data["created"] = True
        data["password"] = ""
        return JsonResponse(data)

    data["created"] = False
    data["password"] = ""
    return JsonResponse(data)


@csrf_exempt
def init_transfer(request):
    """Initializes transfer to the given account."""

    if not is_authenticated(request):
        return JsonResponse({"user": "Not authenticated", "status": "failed"})

    if request.user.is_authenticated:
        user = request.user
    else:
        user = extract_user(request)
    try:
        token = 100000  # randint(100000, 999999)
        body = {
            "to": f"+{request.POST['phone'] or user.profile.phone}",
            "from": "Ebank Transfer",
            "message": f"Use {token} as token to complete the transaction."
        }
        print(Sms(HEADER).SendSms(body))
        TempTransfer.objects.create(
            user=user, amount=request.POST['amount'],
            account=request.POST['account'], token=token
        )
        return JsonResponse({"initialized": True})
    except (MultiValueDictKeyError, AttributeError, ConnectionError):
        return JsonResponse({"invalid_details": True, "status": "failed"})
    return JsonResponse({"message": "Unkonwn error", "status": "failed"})


@csrf_exempt
def transfer(request):
    """Transfers amount if token is correct."""

    if not is_authenticated(request):
        return JsonResponse({"user": "Not authenticated", "status": "failed"})

    token = request.POST.get('token', 0)
    temp_transfer = TempTransfer.objects.get(token=token)
    if temp_transfer:
        Transfer.objects.create(
            user=temp_transfer.user, account=temp_transfer.account,
            amount=temp_transfer.amount, note=temp_transfer.note,
        )
        temp_transfer.delete()
        return JsonResponse({"transfer": "success"})
    return JsonResponse({"transfer": "failed"})


@csrf_exempt
def buy_airtime(request):
    """Buys airtime for given phone number."""

    if not is_authenticated(request):
        return JsonResponse({"user": "Not authenticated", "status": "failed"})

    phone = request.POST.get('phone', '0')
    amount = int(request.POST.get('amount', 0))
    if len(phone) < 13 or amount > 10000:
        return JsonResponse({
            "phone": phone,
            "amount": amount,
            "phone_valid": len(phone) == 13,
            "amount_valid": amount < 10000,
            "status": "failed"
        })
    body = {
        "recipients": [{
            "phoneNumber": f"+{phone}", "amount": amount, "currencyCode": "NGN"
        }]
    }
    result = Airtime(HEADER).SendAirtime(body)
    if result:
        print(result)
        return JsonResponse({"status": "airtime sent"})
    return JsonResponse({"status": "unknown"})
