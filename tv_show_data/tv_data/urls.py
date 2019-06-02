from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('view-show-data/<show_title>', views.view_show, name='view_show'),
    path('all-shows/', views.all_shows, name='all_shows'),
    path('show-comparer/', views.show_comparer, name='show_comparer'),
    path('show-comparer/<show1>-vs-<show2>', views.show_comparer_shows, name='show_comparer_shows'),
    path('best-of-the-best', views.best_of_the_best, name='best_of_the_best'),
    path('about-us', views.about_us, name='about_us')
]