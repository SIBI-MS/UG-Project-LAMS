from django.shortcuts import render

# Render the front page
def front(request):
    # Render a template named 'home.html'
    return render(request, 'home.html')

# Render the index page
def attendancerecords(request):
    # Render a template called 'attendancerecords.html'
    return render(request, 'attendancerecords.html')
