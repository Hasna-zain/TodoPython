from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy

from todoapp.forms import task_form
from todoapp.models import Task
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView,DeleteView


class tasklistview(ListView):
    model = Task
    template_name = 'home.html'
    context_object_name = 't'

class taskdetailview(DetailView):
    model = Task
    template_name = 'detail.html'
    context_object_name = 'task'

class taskupdateview(UpdateView):
    model = Task
    template_name = 'edit.html'
    context_object_name = 'task'
    fields = ('name','priority','date')
    def get_success_url(self):
        return reverse_lazy('todoapp:cbvdetail',kwargs={'pk':self.object.id})

class taskdeleteview(DeleteView):
    model = Task
    template_name = 'delete.html'
    success_url = reverse_lazy('todoapp:cbvhome')


def home(request):
    t = Task.objects.all()
    if request.method == 'POST':
        name=request.POST.get('name','')
        priority=request.POST.get('priority','')
        date=request.POST.get('date','')
        task=Task(name=name,priority=priority,date=date)
        task.save()
    return render(request,'home.html',{'t':t})



def delete(request,tid):
    task=Task.objects.get(id=tid)
    if request.method=='POST':
        task.delete()
        return redirect('/')
    return render(request,'delete.html')


def update(request,id):
    task= Task.objects.get(id=id)
    form = task_form(request.POST or None, instance=task)
    if form.is_valid():
        form.save()
        return redirect('/')

    return render(request,'update.html',{'task':task,'form':form})
# def detail(request):
#     t=Task.objects.all()
#     return render(request,'delete.html',{'t':t})