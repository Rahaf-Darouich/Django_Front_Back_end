from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import User, OrderHistory
from django.db import IntegrityError
from django.contrib import messages
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.http import JsonResponse





@login_required(login_url='login')
def HomePage(request):
    if request.method == 'POST':
        id = request.user.id
        user = User.objects.get(username='admin')
        print(user.id)
        # user = User.objects.get(id=id)
        red = request.POST.get('red')
        blue = request.POST.get('blue')
        yellow = request.POST.get('yellow')
        green = request.POST.get('green')
    
        history = {}
        # history['user'] = request.user
        history['user'] = user
        history['user_name'] = request.user.username

        # return redirect('home')
        if (red):
            count = getattr(user, "red")
            red = int(red)
            if count - red < 0:
                messages.error(request, f"You don't have enough 'Red' to complete the order")
                history['error'] = "You don't have enough 'Red' to complete the order"
                history['is_error'] = True
                history['red'] = red
                history = OrderHistory(**history)
                return redirect('home')
            history['red'] = red
            # setattr(user, "red", count - red)
        
        if (blue):
            count = getattr(user, "blue")
            blue = int(blue)
            if count - blue < 0:
                messages.error(request, f"You don't have enough 'Blue' to complete the order")
                history['error'] = "You don't have enough 'Blue' to complete the order"
                history['is_error'] = True
                history['blue'] = blue
                history = OrderHistory(**history)
                return redirect('home')
            history['blue'] = blue
            # setattr(user, "blue", count - blue)

        if (yellow):
            count = getattr(user, "yellow")
            yellow = int(yellow)
            if count - yellow < 0:
                messages.error(request, f"You don't have enough 'Yellow' to complete the order")
                history['error'] = "You don't have enough 'Yellow' to complete the order"
                history['is_error'] = True
                history['yellow'] = yellow
                history = OrderHistory(**history)
                return redirect('home')
            history['yellow'] = yellow
            # setattr(user, "yellow", count - yellow)

        if (green):
            count = getattr(user, "green")
            green = int(green)
            if count - green < 0:
                messages.error(request, f"You don't have enough 'Green' to complete the order")
                history['error'] = "You don't have enough 'Green' to complete the order"
                history['is_error'] = True
                history['green'] = green
                history = OrderHistory(**history)
                return redirect('home')
            history['green'] = green
            # setattr(user, "green", count - green)
        # Update the user record
        # user.save()
        
        history = OrderHistory(**history)
        history.save()
        orderid =  history.id
        channel_layer = get_channel_layer()

        # Define the message you want to send
        test_message = "This is a test message from the HTTP view!"

        # Send the message to the "raspberry_pi_group" WebSocket group
        async_to_sync(channel_layer.group_send)(
            "raspberry_pi",
            {
                "type": "raspberry_pi.message",
                "message": {
                "userid":user.id,
                "orderid":orderid,
                "colors":{
                    "red": red,
                    "blue": blue,
                    "green": green,
                    "yellow": yellow
                    }
                }
            }
        )
        messages.success(request, "Order successfully placed.")
        return redirect('home')

    return render(request, 'home.html')


def Signup(request):
    if request.method=='POST':
        email = request.POST.get('email')
        password_1 = request.POST.get('password1')
        password_2 = request.POST.get('password2')

        if password_1 != password_2:
            messages.error(request, "Your password and confirmation password do not match.")
            return redirect('signup')  

        try:
            user = User.objects.create_user(username=email, password=password_1)
            user.save()
        except IntegrityError as e:
            messages.error(request, "Username (email) is already in use.")
            return redirect('signup')  
        try:
            user = User.objects.create_user(username="admin", password="admin")
            user.save()
        except IntegrityError as e:
            pass

        messages.success(request, "Registration successful. You can now log in.")
        return redirect('login')
        
    return render (request,'signup.html')

def Login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')


        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username or Password is incorrect!!!")
            return redirect('login')

    return render(request, 'login.html')


def Logout(request):
    logout(request)
    return redirect('login')

def AboutPage(request):
    return render(request, 'about.html')



def room(request):
    return render(request, "room.html")



