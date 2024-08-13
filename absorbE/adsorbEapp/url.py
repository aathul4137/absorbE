from django.urls import path
from . import views

urlpatterns = [
    path('base/', views.base, name='base'),
    path('books/',views.books,name='books'),
    path('game/', views.game, name='game'),
    path('dictionary/',views.dictionary,name='dictionary'),
    path('', views.home, name='home'),
    path('homework/',views.homework,name='homework'),
    path('upload_file/<int:homework_id>/', views.upload_file, name='upload_file'),
    path('delete_homework/<int:homework_id>/', views.delete_homework, name='delete_homework'),
    path('logout/',views.logout,name='logout'),
    path('profile/',views.profile,name='profile'),
    path('notes/',views.notes,name='notes'),
    path('delete_notes/<int:notes_id>',views.delete_notes,name='delete_notes'),
    path('notes_detail/<int:pk>',views.notes_detail,name='notes_detail'),
    path('todo/', views.todo, name='todo'),
    path('update_todo/<int:pk>/', views.update_todo, name='update_todo'),
    path('delete_todo/<int:todo_id>/', views.delete_todo, name='delete_todo'),
    path('wiki/',views.wiki,name='wiki'),
    path('youtube/', views.youtube, name='youtube'),
]