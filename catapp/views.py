# views.py
import os

from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection
from django.db import connections

from django.contrib.auth import logout, authenticate

from django.core.files.storage import FileSystemStorage
import pandas as pd
from .forms import AddUserForm
from catapp.utils import create_user
from django.contrib.auth.models import User
from django.conf import settings

# view function for the query_builder page
def query_builder(request):
    if request.method == 'POST':
        keyword = request.POST.get('keyword')
        country = request.POST.get('Country')
        city = request.POST.get('city')
        state = request.POST.get('state')
        indus = request.POST.get('indus')
        year = request.POST.get('year')
        year = float(year) if year!='' else year
        from_emp = request.POST.get('fromemp')
        to_emp = request.POST.get('empto')

        print('in- country----', keyword, country,city,state,indus,year,from_emp,to_emp)

        query='select * from Company where 1=1 '
        if keyword:
            query=query+f'''and ( name like '%{keyword}%' or domain like '%{keyword}%' or linkedin_url like '%{keyword}%' ) '''

        if country:
            query = query + f''' and country='{country}' '''


        if city:
            query = query + f'''and city='{city}' '''

        if state:
            query = query + f'''and state='{state}' '''


        if indus:
            query = query + f'''and industry='{indus}' '''


        if year:
            query = query + f'''and year_founded = '{year}' '''

        if to_emp:
            query = query + f''' LIMIT {to_emp} '''

        if from_emp:
            query = query + f''' OFFSET {from_emp} '''


        print('query-->',query)


        with connection.cursor() as cursor:
            cursor.execute(query)
            test_table_data = cursor.fetchall()


        print('len of the test_table_data list is :',len(list(test_table_data)))
        messages.success(request, f' {len(list(test_table_data))} records found for the query.')




    context={'variable':'this is sent'}
    return render(request, 'query_builder.html',context)


# view function for the user_list page
def user_list(request):
    users = User.objects.all()
    return render(request, 'users.html', {'users': users})


# view function for the add_user page
def add_user(request):
    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']

            if create_user(username, password,email):
                form.save()
                messages.success(request, 'User added successfully.')

            else:
                print('User already exists')
                messages.error(request, 'User already exists.')
            return redirect('add_user')
        else:
            print(form.errors)
            messages.error(request, 'Form submission error. Please check your data.')
    else:
        form = AddUserForm()


    return render(request, 'add_user.html', {'form': form})


# view function for the index page
def indx(request):
    context={'variable':'this is sent'}
    return render(request, 'indx.html',context)


# view function for the upload_file page
def upload_file(request):
    print('uploadingg.......')
    if request.method == 'POST' and request.FILES['file']:
        print('in postt.......')
        uploaded_file = request.FILES['file']
        print('1 -->',uploaded_file)

        # Save the file to a temporary location
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        print('2 uploaded_file.name -->', uploaded_file.name)

        # Get the path to the saved file
        file_path = fs.url(filename)

        print('3  file_path -->', file_path)

        # Read the Excel or CSV file into a Pandas DataFrame
        if filename.endswith(('.xls', '.xlsx')):
            print('making df of xlsx -->')
            df = pd.read_excel(fs.path(filename))
            print('df shape -->',df.shape)
        elif filename.endswith('.csv'):
            df = pd.read_csv(fs.path(filename))
        else:
            return render(request, 'up.html', {'error': 'Unsupported file format'})

        df['year founded'] = df['year founded'].fillna('')
        df['inx'] = df.index
        df['city'] =''
        df['state'] =''
        def helper(row):
            i = row['inx']
            if row['locality'] or row['locality'] != 'nan':
                lst = str(row['locality']).split(',')
                df.loc[i, 'city'] = str(lst[0]).strip()
                try:
                    df.loc[i, 'state'] = str(lst[1]).strip()
                except:
                    df.loc[i, 'state'] = None

            return str(int(row['inx'] + 1))
        df['Row'] = df.apply(helper, axis=1)
        df.drop(['inx'], axis=1, inplace=True)


        if df.shape[0]>0:
            with connections['default'].cursor() as cursor:
                # Delete all previous data from the company table
                delete_query = "DELETE FROM company"
                cursor.execute(delete_query)

                # Convert the DataFrame to a list of tuples
                data = [tuple(row) for row in df.itertuples(index=False, name=None)]
                # print('data-->',data[:5])
                # data =data[:5]
                # Defining the SQL query for bulk insert

                insert_query = """
                            INSERT INTO company (id,name,domain,year_founded,industry,size_range,locality,country,linkedin_url,current_employee_estimate,total_employee_estimate,city,state,row) VALUES (%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s, %s, %s)
                        """

                cursor.executemany(insert_query, data)
                print('data imserted...')
                row_count=df.shape[0]

                try:
                    file_name=file_path.replace('/','')
                    print('file_name new-->',file_name)
                    file_path = os.path.join(settings.BASE_DIR, '.', file_name)
                    os.remove(file_path)
                    print(f'file removed named {file_path}')
                except Exception as e:
                    print('Exception in removing file..',e)


        # Display the uploaded data details
        return render(request, 'up.html', {'row_count': row_count, 'df': df})

    return render(request, 'up.html')

# view function for the loginUser page
def loginUser(request):
    print('hii helloo...123')
    print('request.method..',request.method)
    if request.method == 'POST':
        username=request.POST.get('uname')
        password=request.POST.get('pass')
        print('in-----',username,password)
        user = authenticate(username=username,password=password)
        if user is not None:

            return redirect('/')
        else:
            messages.error(request, 'Invalid username or password. Please try again.')

    return render(request,'login.html')



def logoutuser(request):
    logout(request)
    return redirect('/login')


