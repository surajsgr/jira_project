from django.shortcuts import render,get_object_or_404,redirect

from django.forms import ModelForm

from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from .models import Task
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.models import User


def home(request):
    context = {
        'tasks': Task.objects.all()
    }
    return render(request, 'task/home.html', context)


class TaskListView(ListView):
    model = Task
    template_name = 'task/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'tasks'
    ordering = ['-date_posted']
    paginate_by = 5

class UserTaskListView(ListView):
    model = Task
    template_name = 'task/user_task.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'tasks'
    paginate_by = 5

    def get_queryset(self):

        user = get_object_or_404(User, username=self.kwargs.get('username'))

        return Task.objects.filter(author=user).order_by('-date_posted')


class TaskDetailView(DetailView):
    model = Task


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'status']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    fields = ['title', 'status','date_posted']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        task = self.get_object()
        if self.request.user == task.author:
            return True
        return False


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    success_url = '/'

    def test_func(self):
        task = self.get_object()
        if self.request.user == task.author:
            return True
        return False



# class TasksForm(ModelForm):
#     class Meta:
#         model = Task
#         fields = ['id', 'title', 'author']
#
# def task_list(request, template_name='task/home.html'):
#     tasks = Task.objects.all()
#     data = {}
#     data['object_list'] = tasks
#     return render(request, template_name, data)
#
# def task_create(request, template_name='task/task_form.html'):
#     form = TasksForm(request.POST or None)
#     if form.is_valid():
#         form.save()
#         return redirect('Task:post_list')
#     return render(request, template_name, {'form': form})
#
# def task_update(request, pk, template_name='task/task_form.html'):
#     task = get_object_or_404(Task, pk=pk)
#     form = TasksForm(request.POST or None, instance=task)
#     if form.is_valid():
#         form.save()
#         return redirect('Task:post_list')
#     return render(request, template_name, {'form': form})
#
# def task_delete(request, pk, template_name='blog_posts/post_delete.html'):
#     task = get_object_or_404(Task, pk=pk)
#     if request.method=='POST':
#         task.delete()
#         return redirect('Task:post_list')
#     return render(request, template_name, {'object': task})
#
#
def about(request):
    return render(request, 'task/about.html', {'title': 'About'})

