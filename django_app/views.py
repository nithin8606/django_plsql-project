from django.http import HttpResponseBadRequest, HttpResponseNotFound
from django.shortcuts import redirect, render
from django.db import connection



def view_users(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM users;")
        users = cursor.fetchall()
    context={
        'users':users
    }
    return render(request,'view_users.html',context)


def add_users(request):
    if request.method=='POST':
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM users WHERE username = %s OR email = %s", [username, email])
            count = cursor.fetchone()[0]
        if count > 0:
            return render(request, 'add_users.html', {'error': 'Username or email already exists.'})
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", [username, email, password])

        return redirect('view_users')
    return render(request,'add_users.html')



def update_users(request, id):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if not username or not email or not password:
            return HttpResponseBadRequest("All fields are required")

        with connection.cursor() as cursor:
            cursor.execute("UPDATE users SET username = %s, email = %s, password = %s, updated_at = CURRENT_TIMESTAMP WHERE id = %s;", [username, email, password, id])

        return redirect('view_users')  
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE id = %s;", [id])
        user = cursor.fetchone()

    if user is None:
        return HttpResponseNotFound("User not found")

    context = {
        'users': user
    }
    return render(request, 'update_users.html', context)



def delete_users(request,id):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM users WHERE id=%s",[id])
        return render(request,'view_users.html')
