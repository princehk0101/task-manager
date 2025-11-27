from django.shortcuts import render, redirect
from todolist.forms import TaskForm
from todolist.models import Task
from django.contrib import messages
from .forms import ContactForm
import datetime

from django.db.models import Q
from rest_framework import viewsets
from .serializers import TaskSerializer

from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required


# ---------------------------------------------------
#              TODO LIST (Search + Filter + Sort)
# ---------------------------------------------------
@login_required
def todolist(request):

    # Handle POST (new task)
    if request.method == 'POST':
        form_data = TaskForm(request.POST)
        if form_data.is_valid():
            instance = form_data.save(commit=False)
            instance.owner = request.user
            instance.save()
            messages.success(request, 'Task added successfully!')
            return redirect('todolist')
    else:
        form_data = TaskForm()

    # -------------------------
    #      FILTER + SEARCH
    # -------------------------
    qs = Task.objects.filter(owner=request.user)

    # SEARCH
    q = request.GET.get('q', '').strip()
    if q:
        qs = qs.filter(Q(task__icontains=q) | Q(description__icontains=q))

    # PRIORITY FILTER
    priority = request.GET.get('priority', '')
    if priority:
        qs = qs.filter(priority=priority)

    # CATEGORY FILTER
    category = request.GET.get('category', '')
    if category:
        qs = qs.filter(category=category)

    # STATUS FILTER
    status = request.GET.get('status', '')
    if status == 'completed':
        qs = qs.filter(completed=True)
    elif status == 'pending':
        qs = qs.filter(completed=False)

    # SORTING
    sort = request.GET.get('sort', '')

    if sort == 'newest':
        qs = qs.order_by('-created_at')

    elif sort == 'oldest':
        qs = qs.order_by('created_at')

    elif sort == 'due_soon':
        qs = qs.order_by('due_date')  # null values first

    elif sort == 'priority':
        qs = qs.extra(select={'priority_order':
                              "FIELD(priority, 'High','Medium','Low')"}).order_by('priority_order')

    else:
        qs = qs.order_by('-created_at')  # default

    # Pagination
    paginator = Paginator(qs, 5)
    page = request.GET.get('page')
    tasks = paginator.get_page(page)

    return render(request, 'todolist.html', {
        'tasks': tasks,
        'form': form_data,
        'q': q,
        'priority': priority,
        'category': category,
        'status': status,
        'sort': sort,
    })


# ---------------------------------------------------
#                 DELETE TASK
# ---------------------------------------------------
@login_required
def delete_task(request, task_id):
    task = Task.objects.get(id=task_id)

    if task.owner == request.user:
        task.delete()
        messages.success(request, f'Task "{task.task}" deleted successfully!')
    else:
        messages.error(request, "You are not authorized to delete this task.")
    return redirect('todolist')


# ---------------------------------------------------
#                 EDIT TASK
# ---------------------------------------------------
@login_required
def edit_task(request, task_id):
    task = Task.objects.get(id=task_id)

    if task.owner != request.user:
        messages.error(request, "You are not authorized to edit this task.")
        return redirect("todolist")

    if request.method == 'POST':
        form_data = TaskForm(request.POST, instance=task)
        if form_data.is_valid():
            form_data.save()
            messages.success(request, "Task updated!")
            return redirect("todolist")
    else:
        form_data = TaskForm(instance=task)

    return render(request, 'edit.html', {'form': form_data, 'task': task})


# ---------------------------------------------------
#              COMPLETE / PENDING
# ---------------------------------------------------
@login_required
def complete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    if task.owner == request.user:
        task.completed = True
        task.save()
        messages.success(request, "Status changed to Completed!")
    else:
        messages.error(request, "Unauthorized")
    return redirect('todolist')


@login_required
def pending_task(request, task_id):
    task = Task.objects.get(id=task_id)
    if task.owner == request.user:
        task.completed = False
        task.save()
        messages.success(request, "Status changed to Pending!")
    else:
        messages.error(request, "Unauthorized")
    return redirect('todolist')


# ---------------------------------------------------
#                    STATIC PAGES
# ---------------------------------------------------
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')


# ---------------------------------------------------
#                     CONTACT
# ---------------------------------------------------
def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been sent successfully!")
            return redirect('contact')
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})


# ---------------------------------------------------
#                     DASHBOARD
# ---------------------------------------------------
@login_required
def dashboard(request):
    tasks = Task.objects.filter(owner=request.user)

    total_tasks = tasks.count()
    completed_tasks = tasks.filter(completed=True).count()
    pending_tasks = tasks.filter(completed=False).count()
    overdue_tasks = tasks.filter(completed=False, due_date__lt=datetime.date.today()).count()

    today = datetime.date.today()
    todays_tasks = tasks.filter(due_date=today)
    upcoming_tasks = tasks.filter(due_date__gt=today).order_by('due_date')[:5]

    recent_activity = tasks.order_by('-updated_at')[:7]

    context = {
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'overdue_tasks': overdue_tasks,
        'todays_tasks': todays_tasks,
        'upcoming_tasks': upcoming_tasks,
        'recent_activity': recent_activity,
    }

    return render(request, 'dashboard.html', context)


# ---------------------------------------------------
#                   API VIEWSET
# ---------------------------------------------------
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
