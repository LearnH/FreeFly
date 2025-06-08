from django.shortcuts import render

# Create your views here.
def index(request):
    if request.method == 'GET':
        return render(request, 'index.html')

    username = request.POST['username']
    password = request.POST['password']
    if username == 'admin' and password == '11111':
        return render(request, 'main.html')

    return render(request, 'index.html', {'error_msg': 'Invalid username or password'})

def main(request):
    return render(request, 'main.html')