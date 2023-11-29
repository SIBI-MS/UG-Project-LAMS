from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Student, Log
from datetime import datetime, time, date
from django.db.models import Sum, Count
from decimal import Decimal

# Global variables
global stat
stat = ''
global selected
selected = None

#This function used to find the no.of student presently in the library
def livemembers(request):
    # Get the current date
    current_date = date.today()
    
    # Query the Log model to retrieve users who have not logged out (time_out is None) and have a matching date
    users_in_library = Log.objects.filter(time_out=None, date=current_date)
    
    # Perform an additional query to group the retrieved records by card_id and select specific fields
    users = users_in_library.values('admission_no', 'name', 'level', 'department')
    
    # Render a template called 'attendance/livemembers.html' and pass the 'users' data to it
    return render(request, 'livemember/livemembers.html', {'users': users})


# Import necessary modules or classes
def topuser(request):
    # Calculate the total hours sum for each user by grouping logs by card_id
    users = Student.objects.values('card_id','admission_no', 'name', 'level', 'department','time_spend')

    # Sort users by time_spend in descending order (finding the top user)     
    users = users.order_by('-time_spend')
    
    # Prepare context data for rendering search.html
    context = {
        'users': users,
    }

    # Render a template called 'attendance/topuser.html' and pass the 'users' data to it
    return render(request, 'topuser/topuser.html',context)



# Render the attendance page
def index1(request):
    # Create an empty list to store filtered logs
    logf = []
    
    # Retrieve all logs from the Log model
    logs = Log.objects.all()
    
    # Iterate through each log
    for log in logs:
        # Filter logs for the current date by comparing log.date with the current date
        if str(log.date) == str(datetime.now())[:10]:
            logf.append(log)
    
    # Reverse the order of filtered logs (possibly to show the most recent logs first)
    logf.reverse()
    
    # Create a dataset containing the filtered logs
    dataset = {'log': logf}
    
    # Render a template called 'attendance/attendance.html' and pass the 'dataset' to it
    return render(request, 'attendance/attendance.html', dataset)


# Render the index page
def index(request):
    # Render a template called 'attendance/index.html'
    return render(request, 'attendance/index.html')



# Render the edit data page
def editdata(request):
    # Render a template called 'attendance/edit.html'
    return render(request, 'studentmanage/edit.html')



# Process the card and log attendance
def process(request):
    # Get the 'card_id' parameter from the request's GET data or set it to 'Invalid Credential' by default
    card = request.GET.get('card_id', 'Invalid Credential')
    
    # Retrieve all users from the 'Student' model
    users = Student.objects.all()
    
    # Iterate through each user
    for user in users:
        # Check if the user's 'card_id' matches the provided 'card'
        if user.card_id == int(card):
            name=user.name
            # If a matching user is found, log attendance using the 'attend' function and return the response
            ans = attend(user)
            context = {'name': name, 'ans': ans}
            return render(request, 'switchuser/switchuser.html', {'ans': context})
    
    # If the card is not found among registered users, return a message to register it as a new user
    ans='Card is not found, register it as a new user'
    return render(request, 'switchuser/switchuser.html', {'ans': ans})




    # Log attendance for a user
def attend(user):
    if user.name is None:
        # Handle case where user profile is incomplete
        statu = 'Profile is incomplete. Please complete your profile.'
        return statu
    
    # Get the current date and time
    current_datetime = datetime.now()
    current_date = current_datetime.date()
    current_time = current_datetime.strftime('%H:%M:%S.%f')  # Include milliseconds in time format
    # Check if there is an open attendance record for today
    open_log = Log.objects.filter(card_id=user.card_id, date=current_date, time_out__isnull=True).first()
    if open_log:
        # User is already checked in, so this is a check-out
        
        # Update the 'time_out' field with the current time
        open_log.time_out = current_time

        # Parse the 'time_in' and 'time_out' strings as datetime objects
        time_in = datetime.strptime(f'{current_date} {open_log.time_in}', '%Y-%m-%d %H:%M:%S.%f')
        time_out = datetime.strptime(f'{current_date} {current_time}', '%Y-%m-%d %H:%M:%S.%f')

        # Calculate total hours
        time_difference = time_out - time_in

        total_seconds = time_difference.total_seconds()
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        seconds = int(total_seconds % 60)
        # Format total hours as HH:MM:SS
        total_hours = f'{hours:02d}:{minutes:02d}:{seconds:02d}'
        
        open_log.total_hours = total_hours
        open_log.save()


        student = Student.objects.get(card_id=user.card_id)
        # Split the string into hours, minutes, and seconds
        time_parts=student.time_spend
        time_parts=time_parts+total_seconds
        
        # Update the time_spend field in the Student table with all_total
        student.time_spend = time_parts
        student.save()

        
        # here write a code to update the time_spend field in Student table by all_total based on a checking card_id=user.card_id
        
        statu = 'Until Next Time, Keep Reading!'
    else:
        # User is not checked in, so this is a check-in
        
        # Create a new attendance log entry for the user
        new_log = Log(
            card_id=user.card_id,
            admission_no=user.admission_no,
            name=user.name,
            department=user.department,
            level=user.level,
            date=current_date,
            time_in=current_time,
            status='Welcome To CK NAIR Library'
        )
        new_log.save()
        
        statu = 'Welcome To CK NAIR Library'
    
    return statu



def check(request):
        # Calculate the total hours sum for each user by grouping logs by card_id
    users = Student.objects.values('card_id','admission_no', 'name', 'department','level','phone','dob','sex','email','address')
    
    # Render a template called 'attendance/topuser.html' and pass the 'users' data to it
    return render(request, 'studentmanage/manage.html', {'users': users})


def manage1(request):
    users = Student.objects.all()
    us = []
    for user in users:
        us.append(user)
    us.reverse()
    global stat
    userset = {'users': us}
    stat = ''
    return render(request, 'studentmanage/allusers.html', userset)
    
# Render the manage page
def manage(request):
    # Access the global variable 'stat', which appears to store some status information
    global stat
    
    # Create a dictionary 'status' containing the value of 'stat' under the key 'cardstatus'
    status = {'cardstatus': stat}
    
    # Render a template named 'attendance/edit.html' and pass the 'status' data to it
    return render(request, 'studentmanage/edit.html', status)



# Render the front page
def front(request):
    # Render a template named 'attendance/front.html'
    return render(request, 'attendance/front.html')


# Handle card selection and deletion
def card(request):
    global stat
    global selected
    global Use
    # Retrieve all user records from the 'Student' model
    users = Student.objects.all()

    # Access global variables 'stat' and 'selected', which may store status information and a selected user

    # Check if the request method is POST
    if request.method == 'POST':
        # Check if the 'sel' button was clicked (indicating card selection)
        if request.POST.get("sel"):
            # Get the card ID from the POST data or set a default message if no card is selected
            ids = request.POST.get('card_id')

            # Iterate through users to find a matching card ID
            for user in users:
                if user.card_id == int(ids):
                    stat = 'Card Found'  # Set the status to indicate card found
                    selected = user
                    break
            else:
                Use = int(ids)
                stat = 'Card not found'  # Set the status to indicate card not found

        # Check if the 'del' button was clicked (indicating card deletion)
        elif request.POST.get("del"):
            # Get the card ID from the POST data
            ids = request.POST.get('card_id')
            
            try:
                # Attempt to retrieve the user with the specified card ID and delete it
                user_to_delete = Student.objects.get(card_id=int(ids))
                user_to_delete.delete()
                stat = 'Removed Successfully'  # Set the status to indicate successful removal
            except Student.DoesNotExist:
                stat = "Can't remove: Card not found"  # Set the status to indicate card not found

    
    # Create a dictionary 'status' containing the value of 'stat' under the key 'cardstatus'
    status = {'cardstatus': stat}
    # Render a template named 'attendance/edit.html' and pass the 'status' data to it
    return render(request, 'studentmanage/edit.html', status)

# Edit user profile
def edit(request):
    i = 0  # Initialize a variable for iteration
    users = Student.objects.all()  # Retrieve all user records
    global selected  # Access the global 'selected' variable, which stores the selected user
    global stat
    global Use# Access the global 'stat' variable, which stores status information

    # Check if no user is selected
    if selected is None:
        card_id=request.POST.get('card_id')
        admission_no=request.POST.get('admission_no')
        name = request.POST.get('name')
        dob = request.POST.get('date')
        phone = request.POST.get('phone')
        department=request.POST.get('department')
        level=request.POST.get('level')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        address = request.POST.get('address')
        new = [card_id,admission_no,name, phone, dob,department,level, email, gender, address]

        # Check if the selected card_id matches any student's card_id
        Student.objects.create(
                card_id=card_id,
                admission_no=admission_no or None,
                name=name or None,
                dob=dob or None,
                phone=phone or None,
                level=level or None,
                email=email or None,
                department=department or None,
                sex=gender or None,
                address=address or None,
            )
        stat = 'New Student Added'
        return redirect('/manage') 


    else:
        admission_no=request.POST.get('admission_no')
        name = request.POST.get('name')
        dob = request.POST.get('date')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        address = request.POST.get('address')
        department=request.POST.get('department')
        level=request.POST.get('level')
        new = [admission_no,name, phone, dob,department,level, email, gender, address]

        for user in users:
                if user.card_id == selected.card_id:
                    old = [user.admission_no,user.name, user.phone, user.dob,user.department,user.level, user.email, user.sex, user.address]
                    
                    # Iterate through the new profile data and update it if not empty or None
                    for item in new:
                        if item == '' or item is None:
                            new[i] = old[i]
                        i = i + 1

                    # Update the user's profile fields and save the changes
                    user.admission_no = new[0]
                    user.name = new[1]
                    user.phone = new[2]
                    user.dob = new[3]
                    user.department=new[4]
                    user.level=new[5]
                    user.email = new[6]
                    user.sex = new[7]
                    user.address = new[8]
                    user.save()
                    stat = 'Profile Updated'

        # Reset the 'selected' variable and redirect to the check page
    selected = None
    return redirect('/check')


# Handle user search and display results
def search(request):
    # Get user input values from the POST request
    admission_no = request.POST.get('admission_no')
    department = request.POST.get('department')
    level = request.POST.get('level')

    # If card_id is provided, show search results in search.html
    if admission_no:
        try:
            # Try to retrieve a user with the provided card_id
            sel_user = Student.objects.get(admission_no=admission_no)
        except Student.DoesNotExist:
            sel_user = None
        
        if sel_user:
            # Calculate the exact sum of total_hours for the selected user
            # Filter log entries for the current month
            logf = Log.objects.filter(admission_no=admission_no, date__month=datetime.now().month).order_by('-date')
            # Assuming total_seconds is a string representing seconds
            total_seconds_str = sel_user.time_spend

            # Convert total_seconds_str to an integer
            try:
                total_seconds = int(total_seconds_str)
            except ValueError:
                # Handle the case where total_seconds_str is not a valid integer
                total_seconds = 0  # or any default value you prefer

            # Perform the calculations
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60
            # Format total hours as HH:MM:SS
            
            all_total=f'{hours:02d}:{minutes:02d}:{seconds:02d}'
            

            # Prepare context data for rendering search.html
            context = {
                'use': sel_user,
                'log': logf,
                'all_total':all_total,
            }
            return render(request, 'search/search.html', context)
        else:
            # Handle the case where card_id is not found
            return render(request, 'search/search.html', {'card_not_found': True})

    # If department and level are provided, show results in data.html
    elif department:
        students = Student.objects.filter(department=department)

        # Filter students by level (ug, pg, all)
        if level != 'all':
            students = students.filter(level=level)

        # Prepare context data for rendering data.html
        context = {
            'students': students,
        }
        return render(request, 'search/data.html', context)

    # If only level is provided, show results in data.html
    elif level:
        if level != 'all':
            students = Student.objects.filter(level=level)
        else:
            students = Student.objects.all()
        
        # Prepare context data for rendering data.html
        context = {
            'students': students,
        }
        return render(request, 'search/data.html', context)
    
    # If none of the search criteria are provided, redirect back to the previous page
    else:
        return redirect(request.META['HTTP_REFERER'])

# Handle log search and log display results
from django.utils.dateparse import parse_date

def logsrch(request):
    # Get user input values from the POST request
    admission_no = request.POST.get('admission_no')
    department = request.POST.get('department')
    level = request.POST.get('level')
    datepicker = request.POST.get('datepicker')  # Get the selected date in DD/MM/YYYY format

    # Parse the datepicker value into a Python datetime object
    selected_date = None
    if datepicker:
        try:
            selected_date = parse_date(datepicker)
        except ValueError:
            selected_date = None  # Handle invalid date format gracefully

    # If card_id is provided, show search results in search.html
    if admission_no:
        try:
            # Try to retrieve a user with the provided card_id
            sel_user = Student.objects.get(admission_no=admission_no)
        except Student.DoesNotExist:
            sel_user = None
        
        if sel_user:
            # Calculate the exact sum of total_hours for the selected user
            # Filter log entries for the current month
            logf = Log.objects.filter(admission_no=admission_no, date__month=datetime.now().month).order_by('-date')
            # Assuming total_seconds is a string representing seconds
            total_seconds_str = sel_user.time_spend

            # Convert total_seconds_str to an integer
            try:
                total_seconds = int(total_seconds_str)
            except ValueError:
                # Handle the case where total_seconds_str is not a valid integer
                total_seconds = 0  # or any default value you prefer

            # Perform the calculations
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60
            # Format total hours as HH:MM:SS
            
            all_total=f'{hours:02d}:{minutes:02d}:{seconds:02d}'
            

            # Prepare context data for rendering search.html
            context = {
                'use': sel_user,
                'log': logf,
                'all_total':all_total,
            }
            return render(request, 'search/search.html', context)
        else:
            # Handle the case where card_id is not found
            return render(request, 'search/search.html', {'card_not_found': True})
    # If department and level are provided, show results in data.html
    elif department:
        logs = Log.objects.filter(department=department)

        # Filter students by level (ug, pg, all)
        if level != 'all':
            logs = logs.filter(level=level)
            if selected_date:
                logs = logs.filter(date=selected_date.strftime('%Y-%m-%d'))
                context = {
                    'logs': logs,
                    'selected_date':selected_date,

                }
                return render(request, 'search/logsearch.html', context)
        else:
            if selected_date:
                logs = logs.filter(date=selected_date.strftime('%Y-%m-%d'))
                context = {
                    'logs': logs,
                    'selected_date':selected_date,

                }
                return render(request, 'search/logsearch.html', context)
    
        context = {
            'logs': logs,
        }
        return render(request, 'searchlogallsearch.html', context)

    # If only level is provided, show results in data.html
    elif level:
        if level != 'all':
            logs = Log.objects.filter(level=level)
            if selected_date:
                logs = logs.filter(date=selected_date.strftime('%Y-%m-%d'))
                # Prepare context data for rendering data.html
                context = {
                    'logs': logs,
                    'selected_date':selected_date,

                }
                return render(request, 'search/logsearch.html', context)
            context = {
                    'logs': logs,
            }
            return render(request, 'search/logallsearch.html', context)
        else:
            logs = Log.objects.all()
            if selected_date:
                logs = logs.filter(date=selected_date.strftime('%Y-%m-%d'))
                # Prepare context data for rendering data.html
                context = {
                    'logs': logs,
                    'selected_date':selected_date,
                }
                return render(request, 'search/logsearch.html', context)
            context = {
                    'logs': logs,
            }
            return render(request, 'search/logallsearch.html', context)
    elif selected_date:
            logs = Log.objects.all()
            logs = logs.filter(date=selected_date.strftime('%Y-%m-%d'))
            # Prepare context data for rendering data.html
            context = {
                'logs': logs,
                'selected_date':selected_date,

            }
            return render(request, 'search/logsearch.html', context)
    
    # If none of the search criteria are provided, redirect back to the previous page
    else:
        return redirect(request.META['HTTP_REFERER'])

def analysis(request):
    # Query the database to get the number of students in each department
    department_counts = Student.objects.values('department').annotate(total_students=Count('card_id'))

    # Query the database to get the total time spent by students in each department
    department_times = Log.objects.values('department').annotate(total_time=Sum('total_hours'))

    # Extract the department names and student counts
    departments = [entry['department'] for entry in department_counts]
    student_counts = [entry['total_students'] for entry in department_counts]

    # Extract the department names and total times
    total_times = [entry['total_time'] for entry in department_times]

    # Debugging: Print the extracted data to the console
    print("Departments:", departments)
    print("Student Counts:", student_counts)
    print("Total Times:", total_times)

    # Prepare the context with data to pass to the template
    context = {
        'departments': departments,
        'student_counts': student_counts,
        'total_times': total_times,
    }

    # Render the 'attendance/analysis.html' template with the context data
    return render(request, 'analysis/analysis.html', context)


import csv
from django.shortcuts import render
from .forms import CSVUploadForm
from .models import Student
from datetime import datetime

def datafs(request):
    # Render a template named 'student/upload.html'
    return render(request, 'studentmanage/upload.html')

def upload_csv(request):
    file_name = None
    error_message = None  # Initialize error_message variable

    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['file_name']
            if csv_file.name.endswith('.csv'):
                file_name = csv_file.name
                csv_data = csv.DictReader(csv_file.read().decode('utf-8').splitlines())
                
                for row in csv_data:
                    # Convert the date from the CSV file to YYYY-MM-DD format
                    dob_str = row['dob']
                    try:
                        dob = datetime.strptime(dob_str, '%d/%m/%Y').strftime('%Y-%m-%d')
                    except ValueError:
                        # Handle invalid date format
                        dob = None

                    # Check if a student with the same card_id already exists
                    existing_student = Student.objects.filter(card_id=row['card_id']).first()
                    if existing_student:
                        error_message = f'Student with card_id {row["card_id"]} already exists.'
                        break  # Stop processing the CSV file if an error occurs
                    
                    student = Student(
                        card_id=row['card_id'],
                        admission_no=row['admission_no'],
                        name=row['name'],
                        dob=dob,  # Use the converted date
                        department=row['department'],
                        level=row['level'],
                        phone=row['phone'],
                        sex=row['sex'],
                        email=row['email'],
                        address=row['address']
                    )
                    student.save()

                if not error_message:
                    students = Student.objects.all()
                    return render(request, 'studentmanage/manage.html', {'students': students})  
            else:
                error_message = 'Invalid file format. Please upload a CSV file.'
    
    form = CSVUploadForm()
    return render(request, 'studentmanage/upload.html', {'form': form, 'file_name': file_name, 'error_message': error_message})


def switchuser(request):
        return render(request, 'switchuser/switchuser.html')

import csv
from django.http import HttpResponse
from django.shortcuts import render

# ...

def download_csv(request):
    csv_data = request.POST.get('csvData')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="log_data.csv"'

    writer = csv.writer(response)
    lines = csv_data.split('\n')
    for line in lines:
        writer.writerow(line.split(','))

    return response
