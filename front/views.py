from django.shortcuts import render, redirect


# Create your views here.
def login_page(request):
    if request.user.is_authenticated:
        return redirect('board/')
    else:
        return render(request, 'front/login.html')


def board_page(request):
    if request.user.is_authenticated:
        return render(request, 'front/board.html')
    else:
        return redirect('front:login_page')


def signup_page(request):
    if request.user.is_authenticated:
        return redirect('front:board_page')
    else:
        return render(request, 'front/signup.html')


def edit_page(request):
    if request.user.is_authenticated:
        return render(request, 'front/board_edit.html')
    else:
        return redirect('front:login_page')


def view_page(request):
    if request.user.is_authenticated:
        return render(request, 'front/board_view.html')
    else:
        return redirect('front:login_page')