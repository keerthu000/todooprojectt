from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from .models import Project,Todo
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db import transaction
from django.views.decorators.http import require_POST
from django.utils import timezone

# Create your views here.
def loginpage(request):
    return render(request,'login.html')

def loginn(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  # Authenticating the user
            if user.is_staff:
                return redirect('/')
            else:
                messages.info(request, 'Please add username and password')
                return redirect('loginportal')
        else:
            messages.error(request, 'Invalid Username or Password. Try again')
            return redirect('loginpage')  # Redirect to the login page
    else:
        return redirect('loginpage')
    



def loginportal(request):
    return render(request, 'loginadmin.html')
def register(request):
      return render(request, 'register.html')
def createuser(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        repassword = request.POST['repassword']

        # Check if the username already exists
        if User.objects.filter(username=name).exists():
            # Handle the case where the username already exists
            return render(request, 'register.html', {'error_message': 'Username already exists'})

        # Create the new user
        user = User.objects.create_user(first_name=name, username=name, password=password, email=email)
        user.save()
        return redirect('loginpage')
    return render(request, 'register.html')

def createproject(request):
    return render(request, 'projtcreate.html')
def addproject(request):
    if request.method == 'POST':
        user = request.user
        projt_name=request.POST['p_name']
        date=request.POST['c_date']
        project=Project(title=projt_name,created_date=date,user=user)
        project.save()
        return redirect('views_project')
    else:
        return render(request,'projtcreate.html')
    

def todocreate(request):
    projt=Project.objects.filter(user=request.user)
    return render(request, 'todocreate.html',{'projt':projt})

def  addtodo(request):
    if request.method == 'POST':
        user = request.user
        projt_id=request.POST['prjtname']
        # todo=request.POST['todo']
        des=request.POST['description']
        cre_date=request.POST['created_date']
        up_date=request.POST['updated_date']
        status=request.POST['status']
        project = get_object_or_404(Project, id=projt_id)
        todo=Todo(user=user,project=project,description=des,created_date=cre_date,updated_date=up_date,status=status)
        todo.save()
        return redirect('todolist',projt_id)

    else:
        return render(request,'todocreate.html')


def views_project(request):
    prjt = Project.objects.filter(user = request.user)
    
    return render(request, 'prjttable.html', {'prjt': prjt})



def projectdetails(request, id):
    user = request.user
    project = get_object_or_404(Project, user=user, id=id)

    todos = Todo.objects.filter(user=user, project=project)
    todos_pending = todos.filter(status="Pending")
    todos_completed = todos.filter(status="Completed")

    to_completed = todos_completed.count()
    todos_total = todos.count()

    print('todos_total', todos_total)  # Correct debugging statement

    context = {
        'prjt': project,
        'todo': todos_pending,
        'todos_completed': todos_completed,
        'to_completed': to_completed,
        'todos_total': todos_total  ,# Removed whitespace from the key here
        'todos':todos
    }

    return render(request, 'prjtdetails.html', context)


def status_change(request, todo_id):
   
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)

    # Toggle the status
    if todo.status == "Pending":
        todo.status = "Completed"
        
    else:
        todo.status = "Pending"
    
    todo.save()
    return redirect('projectdetails', id=todo.project.id)  
 
@login_required
@require_POST
def delete_project(request, id):
    project = get_object_or_404(Project, pk=id, user=request.user)
    Todo.objects.filter(project=project, user=request.user).delete()
    project.delete()
    # messages.success(request, "Project deleted successfully.")
    return redirect('views_project')  # Redirect to the list of projects, adjust the URL name as necessary


@login_required
def edit_todo(request, todo_id):
    selected_todo = get_object_or_404(Todo, id=todo_id, user=request.user)
    projects = Project.objects.filter(user=request.user)

    if request.method == 'POST':
        projt_id = request.POST.get('prjtname')
        project = get_object_or_404(Project, id=projt_id)
        
        selected_todo.project = project
        selected_todo.description = request.POST.get('description')
        selected_todo.status = request.POST.get('status')
        selected_todo.todo = request.POST.get('todo')
        selected_todo.updated_date = request.POST.get('updated_date')
        selected_todo.save()
        
        # Redirect to the project details view of the project associated with the todo
        return redirect('projectdetails', id=project.id)

    return render(request, 'edittodo.html', {
        'selected_todo': selected_todo,
        'todos': Todo.objects.filter(user=request.user),
        'projects': projects
    })

def delete_todo(request, project_id, id):
    
    project = get_object_or_404(Project, id=project_id, user=request.user)
    todo = get_object_or_404(Todo, id=id, user=request.user, project=project)
    todo.delete()
    messages.success(request, "Todo deleted successfully.")

    
    return redirect('projectdetails', id=project_id)

def edit_project(request,id):
    projects = Project.objects.get(user=request.user,id=id)
    if request.method == 'POST':
        projects.title=request.POST['p_name']
        projects.created_date=request.POST['c_date']
        projects.save()
        return redirect('views_project')
    return render(request, 'editproject.html',{'project':projects})


def todolist(request,id):
    user = request.user
    project = get_object_or_404(Project, user=user, id=id)
    

    todos = Todo.objects.filter(user=user, project=project)
    return render(request, 'todolist.html',{'prjt':project,'todos':todos})





import requests
from django.http import HttpResponse
import os

def generate_markdown_summary(project_id):
    project = Project.objects.get(id=project_id)
    todos = Todo.objects.filter(project=project)
    completed_todos = todos.filter(status="Completed")
    pending_todos = todos.filter(status="Pending")

    num_completed = completed_todos.count()
    num_total = todos.count()

    content = f"# {project.title}\n\n"
    content += f"## Summary: {num_completed} / {num_total} completed.\n\n"

    # Section for pending todos
    if pending_todos.exists():
        content += "## Section 1: Task list of pending todos\n"
        for todo in pending_todos:
            content += f"- [ ] {todo.description}\n"
    else:
        content += "## Section 1: No pending todos\n"

    # Section for completed todos
    if completed_todos.exists():
        content += "\n## Section 2: Task list of completed todos\n"
        for todo in completed_todos:
            content += f"- [x] {todo.description}\n"
    else:
        content += "\n## Section 2: No completed todos\n"

    return content


def export_to_gist(content, project_title):
    token = os.getenv('GITHUB_TOKEN')  # Access token from environment variables
    if not token:
        raise Exception("GitHub token not found. Set the GITHUB_TOKEN environment variable.")
    
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    data = {
        "description": "Project Summary",
        "public": False,
        "files": {
            f"{project_title}.md": {
                "content": content
            }
        }
    }

    response = requests.post("https://api.github.com/gists", headers=headers, json=data)
    if response.status_code == 201:
        return response.json()['html_url']
    else:
        raise Exception("Failed to create gist")

def export_project_summary(request, project_id):
    if not request.user.is_authenticated:
        return HttpResponse("Unauthorized", status=401)

    try:
        content = generate_markdown_summary(project_id)
        project_title = Project.objects.get(id=project_id).title
        gist_url = export_to_gist(content, project_title)
        messages.success(request, f'Gist exported successfully: <a href="{gist_url}" target="_blank">View Gist</a>')
    except Exception as e:
        messages.error(request, f'Failed to export gist: {str(e)}')

    return redirect('projectdetails', id=project_id) 
