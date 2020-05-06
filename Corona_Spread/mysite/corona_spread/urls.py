from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('US_Corona.html/', views.US_Corona, name='US_Corona'),
    path('Global_Corona.html/', views.Global_Corona, name='Global_Corona'),
    path('hospital.html/', views.Hospitals, name='Hospitals'),
    path('temperature.html/', views.Temperature, name='Temperature'),
    path('update.html/', views.Update, name='Update'),
    path('reference.html/', views.Reference, name='Reference'),

    path('update.html/us_update.html/', views.US_Update, name='US_Update'),
    path('update.html/us_update.html/insert_us.html/', views.US_Insert, name='US_Insert'),
    path('update.html/us_update.html/insert_us.html/us_update_results.html/', views.Insert_to_US_Data, name='Insert_to_US_Data'),
    path('update.html/us_update.html/add_sub_us.html/', views.US_Add_Sub, name='US_Add_Sub'),
    path('update.html/us_update.html/add_sub_us.html/us_update_results.html/', views.Add_Sub_US_Data, name='Add_Sub_US_Data'),
    path('update.html/us_update.html/set_us.html/', views.US_Set, name='US_Set'),
    path('update.html/us_update.html/set_us.html/us_update_results.html/', views.Set_US_Data, name='Set_US_Data'),
    path('update.html/us_update.html/delete_us.html/', views.US_Delete, name='US_Delete'),
    path('update.html/us_update.html/delete_us.html/delete_us_results.html/', views.Delete_US_Data, name='Delete_US_Data'),

    path('update.html/global_update.html/', views.Global_Update, name='Global_Update'),
    path('update.html/global_update.html/insert_global.html/', views.Global_Insert, name='Global_Insert'),
    path('update.html/global_update.html/insert_global.html/global_update_results.html/', views.Insert_to_Global_Data, name='Insert_to_Global_Data'),
    path('update.html/global_update.html/set_global.html/', views.Global_Set, name='Global_Set'),
    path('update.html/global_update.html/set_global.html/global_update_results.html/', views.Set_Global_Data, name='Set_Global_Data'),
    path('update.html/global_update.html/add_sub_global.html/', views.Global_Add_Sub, name='Global_Add_Sub'),
    path('update.html/global_update.html/add_sub_global.html/global_update_results.html/', views.Add_Sub_Global_Data, name='Add_Sub_Global_Data'),
    path('update.html/global_update.html/delete_global.html/', views.Global_Delete, name='Global_Delete'),
    path('update.html/global_update.html/delete_global.html/delete_global_results.html/', views.Delete_Global_Data, name='Delete_Global_Data'),

    path('hosp_results.html/', views.Hosp_Num, name='Hosp_Num'),
    path('temp_results.html/', views.Avg_Temp, name='Avg_Temp'),
    path('us_results.html/', views.US_Corona_Cases, name='US_Corona_Cases'),
    path('global_results.html/', views.Global_Corona_Cases, name='Global_Corona_Cases'),
]
