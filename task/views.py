from django.shortcuts import render,get_object_or_404,redirect,HttpResponse

from .forms import TaskForm,CommentForm,UpdateForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from .models import Task,Comment
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView,TemplateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.utils import timezone



class AboutView(TemplateView):
    template_name = 'about.html'

class TaskListView(ListView):
    model = Task
    ordering = ['-date_posted']
    print("task list in view")
    def get_queryset(self):
        return Task.objects.all()

class TaskDetailView(DetailView):
    model = Task

def task_detail(request,pk):
    task=Task.objects.get(pk=pk)
    author=request.user.username
    context={
        'task':task,
        'author':author
        }

    return render(request,'task/task_detail.html',context)


class TaskCreateView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    redirect_field_name = 'task/task_detail.html'

    form_class = TaskForm

    model = Task


class TaskUpdateView(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    redirect_field_name = 'task/task_detail.html'

    form_class = UpdateForm

    model = Task


class DraftListView(LoginRequiredMixin,ListView):
    login_url = '/login/'
    redirect_field_name = 'task/task_list.html'

    model = Task

    def get_queryset(self):
        return Task.objects.filter(date_posted__isnull=True).order_by('date_posted')


class TaskDeleteView(LoginRequiredMixin,DeleteView):
    model = Task
    success_url = reverse_lazy('task-home')

#######################################
## Functions that require a pk match ##
#######################################

@login_required
def task_publish(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.publish()
    return redirect('task_detail', pk=pk)

@login_required
def add_comment_to_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            author_name=form.cleaned_data.get('author')
            if author_name==request.user:
                comment = form.save(commit=False)
                comment.task = task
                comment.save()
                return redirect('task_detail', pk=task.pk)
            else:
                return HttpResponse("Please select the correct username ")
    else:
        form = CommentForm()
    return render(request, 'task/comment_form.html', {'form': form})


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('task_detail', pk=comment.task.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    task_pk = comment.task.pk
    comment.delete()
    return redirect('task_detail', pk=task_pk)

# def home(request):
#     context = {
#         'tasks': Task.objects.all()
#     }
#     return render(request, 'task/task_list.html', context)
#
#
# class TaskListView(ListView):
#     model = Task
#     template_name = 'task/task_list.html'  # <app>/<model>_<viewtype>.html
#     context_object_name = 'tasks'
#     ordering = ['-date_posted']
#     paginate_by = 5
#
# class UserTaskListView(ListView):
#     model = Task
#     template_name = 'task/user_task.html'  # <app>/<model>_<viewtype>.html
#     context_object_name = 'tasks'
#     paginate_by = 5
#
#     def get_queryset(self):
#
#         user = get_object_or_404(User, username=self.kwargs.get('username'))
#
#         return Task.objects.filter(author=user).order_by('-date_posted')
#
#
# class TaskDetailView(DetailView):
#     model = Task
#
#
# class TaskCreateView(LoginRequiredMixin, CreateView):
#     model = Task
#     fields = ['title', 'status']
#
#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         return super().form_valid(form)
#
#
# class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
#     model = Task
#     fields = ['title', 'status','date_posted']
#
#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         return super().form_valid(form)
#
#     def test_func(self):
#         task = self.get_object()
#         if self.request.user == task.author:
#             return True
#         return False
#
#
# class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
#     model = Task
#     success_url = '/'
#
#     def test_func(self):
#         task = self.get_object()
#         if self.request.user == task.author:
#             return True
#         return False
#
#
#
# @login_required
# def task_publish(request, pk):
#     task = get_object_or_404(Task, pk=pk)
#     task.publish()
#     return redirect('task_detail', pk=pk)
#
# @login_required
# def add_comment_to_task(request, pk):
#     post = get_object_or_404(Task, pk=pk)
#     if request.method == "POST":
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.post = post
#             comment.save()
#             return redirect('task_detail', pk=pk)
#     else:
#         form = CommentForm()
#     return render(request, 'task/comment_form.html', {'form': form})
#
#
# @login_required
# def comment_approve(request, pk):
#     comment = get_object_or_404(Comment, pk=pk)
#     comment.approve()
#     return redirect('task_detail', pk=pk)
#
#
# @login_required
# def comment_remove(request, pk):
#     comment = get_object_or_404(Comment, pk=pk)
#     task_pk = comment.post.pk
#     comment.delete()
#     return redirect('task_detail', pk=task_pk)
#
# def about(request):
#     return render(request, 'task/about.html', {'title': 'About'})

