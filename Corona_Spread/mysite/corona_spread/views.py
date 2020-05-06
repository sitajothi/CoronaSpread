from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.template import Context, loader
from .models import GlobalCases
from .models import HospitalData
from .models import TemperatureData
from .models import UsCasesDay
from .models import predict_death
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from django.shortcuts import render
import math

#Graphing includes
from plotly.offline import plot
import plotly.graph_objs as go
from datetime import date

#test graphing
def test_graph(request):
    #using data from US_Cases_Day db (graphing date vs cases or death)
    state = 'Illinois'
    with connection.cursor() as cursor:
        cursor.execute("SELECT date, cases, deaths FROM US_Cases_Day where state=%s", [state])
        rows = cursor.fetchall()
    x_data = []
    cases_data = []
    deaths_data = []
    for tup in rows:
        x_data.append(tup[0])
        cases_data.append(tup[1])
        deaths_data.append(tup[2])

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_data, y=cases_data, mode='lines', name='cases'))
    fig.add_trace(go.Scatter(x=x_data, y=deaths_data, mode='lines', name='deaths'))
    fig.add_trace(go.Scatter(x=['4/21/20'], y = [50000], name='predicted death'))
    fig.update_layout(title="Cases/Deaths per Day", xaxis_title='Date', yaxis_title='Number')
    plot_div = plot(fig)
    return render(request, "corona_spread/test_graph.html", context={'plot_div': plot_div})

#find number of hospitals
def Hosp_Num(request):
    ans = request.GET.get('id')
    selected = HospitalData.objects.raw('SELECT * FROM hospital_data WHERE id = %s', [ans])
    for state in selected:
        return render(request, 'corona_spread/hosp_results.html/', {'state':state})

#find average temperature per state
def Avg_Temp(request):
    ans = request.GET.get('id')
    selected = TemperatureData.objects.raw('SELECT * FROM temperature_data WHERE id = %s', [ans])
    for state in selected:
        return render(request, 'corona_spread/temp_results.html/', {'state':state})

#find number of corona cases per state
def US_Corona_Cases(request):
    state = request.GET.get('state')
    date = request.GET.get('date')
    selected = UsCasesDay.objects.raw('SELECT * FROM us_cases_day WHERE state = %s AND date <= %s', [state, date])
    if len(selected) > 0:
        x_data = []
        cases_data = []
        deaths_data = []
        cases = 0
        deaths = 0
        for tup in selected:
            x_data.append(tup.date)
            if (tup.date == date):
                cases = tup.cases
                deaths = tup.deaths
            cases_data.append(tup.cases)
            deaths_data.append(tup.deaths)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x_data, y=cases_data, mode='lines', name='cases'))
        fig.add_trace(go.Scatter(x=x_data, y=deaths_data, mode='lines', name='deaths'))
        fig.update_layout(title="Cases/Deaths per Day", xaxis_title='Date', yaxis_title='Count')


        cursor = connection.cursor()
        cursor.callproc('advanced_func')
        results = cursor.fetchall()
        print("len: ", len(results))
        d_num = 0
        for row in results:
            if row[0]==state:
                d_num = math.floor(row[1])
                break
        fig.add_trace(go.Scatter(x=['4/21/20'], y = [d_num], name='predicted death'))
        plot_div = plot(fig)
        return render(request, 'corona_spread/us_results.html/', {'state':state, 'date':date, 'cases':cases, 'deaths':deaths, 'death_num' : d_num})
    else:
        return render(request, 'corona_spread/us_res_dne.html/', {'state': state, 'date':date})

#General US Update Page
def US_Update(request):
    page = loader.get_template("corona_spread/us_update.html")
    return HttpResponse(page.render())

#Delete state from database
def US_Delete(request):
    dates_all = UsCasesDay.objects.all().order_by('date')
    dates = dates_all.values('date').distinct()
    states_all = UsCasesDay.objects.all().order_by('state')
    states = states_all.values('state').distinct()
    return render(request, 'corona_spread/delete_us.html', {'states':states, 'dates':dates})

@csrf_exempt
def Delete_US_Data(request):
    state = request.POST.get('state')
    date = request.POST.get('date')
    selected = UsCasesDay.objects.raw('SELECT * FROM us_cases_day WHERE state = %s AND date = %s', [state, date])
    if len(selected) > 0:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM us_cases_day WHERE state = %s and date = %s", [state, date])
    return render(request, 'corona_spread/delete_us_results.html/', {'state': state, 'date':date})

#Insert state into database
def US_Insert(request):
    page = loader.get_template("corona_spread/insert_us.html")
    return HttpResponse(page.render())

@csrf_exempt
def Insert_to_US_Data(request):
    state = request.POST.get('state')
    date = request.POST.get('date')
    cases = request.POST.get('cases')
    deaths = request.POST.get('deaths')
    if (int(cases) < 0 or int(deaths) < 0):
        return render(request, 'corona_spread/usage.html/')
    selected = UsCasesDay.objects.raw('SELECT * FROM us_cases_day WHERE state = %s AND date = %s', [state, date])
    if (len(selected) > 0):
        with connection.cursor() as cursor:
            cursor.execute("UPDATE us_cases_day set deaths = %s where state = %s and date = %s", [deaths, state, date])
            cursor.execute("UPDATE us_cases_day set cases = %s where state = %s and date = %s", [cases, state, date])
            cursor.execute("SELECT * FROM us_cases_day WHERE state = %s and date = %s", [state, date])
            row = cursor.fetchone()
            return render(request, 'corona_spread/us_update_results.html/', {'state':row[2], 'date': row[1], 'cases':row[3], 'deaths':row[4]})
    else:
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO us_cases_day (state, date, cases, deaths) VALUES(%s, %s, %s, %s)", [state, date, cases, deaths])
            cursor.execute("SELECT * FROM us_cases_day WHERE state = %s and date = %s", [state, date])
            row = cursor.fetchone()
            return render(request, 'corona_spread/us_update_results.html/', {'state':row[2], 'date': row[1], 'cases':row[3], 'deaths':row[4]})

#increase/decrease numbers for a state
def US_Add_Sub(request):
    dates_all = UsCasesDay.objects.all().order_by('date')
    dates = dates_all.values('date').distinct()
    states_all = UsCasesDay.objects.all().order_by('state')
    states = states_all.values('state').distinct()
    return render(request, 'corona_spread/add_sub_us.html', {'states':states, 'dates':dates})

@csrf_exempt
def Add_Sub_US_Data(request):
    state = request.POST.get('state')
    date = request.POST.get('date')
    cases = request.POST.get('cases')
    deaths = request.POST.get('deaths')
    selected = UsCasesDay.objects.raw('SELECT * FROM us_cases_day WHERE state = %s AND date = %s', [state, date])
    if len(selected) > 0:
        with connection.cursor() as cursor:
            cursor.execute("UPDATE us_cases_day set deaths = GREATEST(deaths + %s, 0) where state = %s and date = %s", [deaths, state, date])
            cursor.execute("UPDATE us_cases_day set cases = GREATEST(cases + %s, 0) where state = %s and date = %s", [cases, state, date])
            cursor.execute("SELECT * FROM us_cases_day WHERE state = %s and date = %s", [state, date])
            row = cursor.fetchone()
            return render(request, 'corona_spread/us_update_results.html/', {'state':row[2], 'date': row[1], 'cases':row[3], 'deaths':row[4]})
    else:
        return render(request, 'corona_spread/usage.html/')

#set numbers for a state
def US_Set(request):
    dates_all = UsCasesDay.objects.all().order_by('date')
    dates = dates_all.values('date').distinct()
    states_all = UsCasesDay.objects.all().order_by('state')
    states = states_all.values('state').distinct()
    return render(request, 'corona_spread/set_us.html', {'states':states, 'dates':dates})

@csrf_exempt
def Set_US_Data(request):
    state = request.POST.get('state')
    date = request.POST.get('date')
    cases = request.POST.get('cases')
    deaths = request.POST.get('deaths')
    if (int(cases) < 0 or int(deaths) < 0):
        return render(request, 'corona_spread/usage.html/')
    selected = UsCasesDay.objects.raw('SELECT * FROM us_cases_day WHERE state = %s AND date = %s', [state, date])
    if (len(selected) > 0):
        with connection.cursor() as cursor:
            cursor.execute("UPDATE us_cases_day set deaths = %s where state = %s and date = %s", [deaths, state, date])
            cursor.execute("UPDATE us_cases_day set cases = %s where state = %s and date = %s", [cases, state, date])
            cursor.execute("SELECT * FROM us_cases_day WHERE state = %s and date = %s", [state, date])
            row = cursor.fetchone()
            return render(request, 'corona_spread/us_update_results.html/', {'state':row[2], 'date': row[1], 'cases':row[3], 'deaths':row[4]})
    else:
        return render(request, 'corona_spread/usage.html/')

#General Global Update Page
def Global_Update(request):
    page = loader.get_template("corona_spread/global_update.html")
    return HttpResponse(page.render())

#find number of cases per country
def Global_Corona_Cases(request):
    ans = request.GET.get('id')
    selected = GlobalCases.objects.raw('SELECT * FROM global_cases WHERE id = %s', [ans])
    for country in selected:
        return render(request, 'corona_spread/global_results.html/', {'country':country})

#Delete country from database
def Global_Delete(request):
    countries = GlobalCases.objects.all().order_by('country')
    return render(request, 'corona_spread/delete_global.html', {'countries':countries})

@csrf_exempt
def Delete_Global_Data(request):
    id = request.POST.get('id')
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM global_cases WHERE id = %s", [id])
        row = cursor.fetchone()
        cursor.execute("DELETE FROM global_cases WHERE id = %s", [id])
        return render(request, 'corona_spread/delete_global_results.html/', {'country':row[1]})

#Insert country into database
def Global_Insert(request):
    page = loader.get_template("corona_spread/insert_global.html")
    return HttpResponse(page.render())

@csrf_exempt
def Insert_to_Global_Data(request):
    country = request.POST.get('country')
    cases = request.POST.get('cases')
    if (int(cases) < 0):
        return render(request, 'corona_spread/usage.html/')
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO global_cases (country, cases) VALUES(%s, %s)", [country, cases])
        cursor.execute("SELECT * FROM global_cases WHERE country = %s", [country])
        row = cursor.fetchone()
    return render(request, 'corona_spread/global_update_results.html/', {'country':row[1], 'cases':row[2]})

#increase number of cases for a country
def Global_Add_Sub(request):
    countries = GlobalCases.objects.all().order_by('country')
    return render(request, 'corona_spread/add_sub_global.html', {'countries':countries})

@csrf_exempt
def Add_Sub_Global_Data(request):
    id = request.POST.get('id')
    cases = request.POST.get('cases')
    with connection.cursor() as cursor:
        cursor.execute("UPDATE global_cases set cases = GREATEST(cases + %s, 0) where id = %s", [cases, id])
        cursor.execute("SELECT * FROM global_cases WHERE id = %s", [id])
        row = cursor.fetchone()
    return render(request, 'corona_spread/global_update_results.html/', {'country':row[1], 'cases':row[2]})

#Set numbers for a country
def Global_Set(request):
    countries = GlobalCases.objects.all().order_by('country')
    return render(request, 'corona_spread/set_global.html', {'countries':countries})

@csrf_exempt
def Set_Global_Data(request):
    id = request.POST.get('id')
    cases = request.POST.get('cases')
    if (int(cases) < 0):
        return render(request, 'corona_spread/usage.html/')
    with connection.cursor() as cursor:
        cursor.execute("UPDATE global_cases set cases = GREATEST(%s, 0) where id = %s", [cases, id])
        cursor.execute("SELECT * FROM global_cases WHERE id = %s", [id])
        row = cursor.fetchone()
    return render(request, 'corona_spread/global_update_results.html/', {'country':row[1], 'cases':row[2]})

def index(request):
    page = loader.get_template("corona_spread/index.html")
    return HttpResponse(page.render())

def Reference(request):
    page = loader.get_template("corona_spread/reference.html")
    return HttpResponse(page.render())

def US_Corona(request):
    dates_all = UsCasesDay.objects.all().order_by('date')
    dates = dates_all.values('date').distinct()
    states_all = UsCasesDay.objects.all().order_by('state')
    states = states_all.values('state').distinct()
    page = loader.get_template("corona_spread/US_Corona.html")
    return render(request, 'corona_spread/US_Corona.html', {'states':states, 'dates':dates})

def Global_Corona(request):
    countries = GlobalCases.objects.all().order_by('country')
    return render(request, 'corona_spread/Global_Corona.html', {'countries':countries})

def Hospitals(request):
    states = HospitalData.objects.all().order_by('state')
    return render(request, 'corona_spread/hospital.html', {'states':states})

def Temperature(request):
    states = TemperatureData.objects.all().order_by('state')
    return render(request, 'corona_spread/temperature.html', {'states':states})

def Update(request):
    page = loader.get_template("corona_spread/update.html")
    return HttpResponse(page.render())
