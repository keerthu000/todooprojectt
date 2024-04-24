from django.urls import path,include
from . import views
from .views import export_project_summary 

urlpatterns = [
    path('',views.register,name='register'),
    path('loginpage',views.loginpage,name='loginpage'),
    path('loginn',views.loginn,name='loginn'),
    path('loginportal',views.loginportal,name='loginportal'),
    
    path('createuser',views.createuser,name='createuser'),
    path('createproject',views.createproject,name='createproject'),
    path('addproject',views.addproject,name='addproject'),
    path('todocreate',views.todocreate,name='todocreate'),
    path('addtodo',views.addtodo,name='addtodo'),
    path('views_project',views.views_project,name='views_project'),
    path('projectdetails/<int:id>',views.projectdetails,name='projectdetails'),
    path('delete_project/<int:id>',views.delete_project,name='delete_project'),
    path('edit_todo/<int:todo_id>/', views.edit_todo, name='edit_todo'),
    path('status_change/<int:todo_id>/',views.status_change,name='status_change'),
    path('delete_todo/<int:project_id>/<int:id>/',views.delete_todo,name='delete_todo'),
    path('edit_project/<int:id>/',views.edit_project,name='edit_project'),
    path('todolist/<int:id>/',views.todolist,name='todolist'),

    path('export_summary/<int:project_id>/', views.export_project_summary, name='export_project_summary'),


   
]