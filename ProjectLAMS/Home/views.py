from django.shortcuts import render

# Render the front page
def front(request):
    # Render a template named 'attendance/front.html'
    return render(request, 'home.html')

# Render the index page
def attendancerecords(request):
    # Render a template called 'attendance/index.html'
    return render(request, 'table.html')
