from django.shortcuts import render, redirect, reverse, get_object_or_404 
from tasks.models import TodoItem
from tasks.forms import AddTaskForm, TodoItemForm, TodoItemExportForm
from django.views import View
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q
from django.core.mail import send_mail
from todoapp import settings
from taggit.models import Tag
from django.db.models import Count

def tasks_by_tag(request, tag_slug=None):
	u = request.user
	tasks = TodoItem.objects.filter(owner=u).all()
	tag = None
	if tag_slug:
		tag = get_object_or_404(Tag, slug=tag_slug)
		tasks = tasks.filter(tags__in=[tag])
	
	all_tags = []
	for t in tasks:
		all_tags.append(list(t.tags.all()))
	all_tags = filter_tags(all_tags)

	return render(request, "tasks/list_by_tag.html", 
	{"tag": tag, "tasks":tasks, "all_tags": all_tags })

class TaskExportView(LoginRequiredMixin, View):
	
	def generate_body(self, user, priorities):
		
		q = Q()
		if priorities["prio_high"]:
			q = q | Q(priority=TodoItem.PRIORITY_HIGH)
		if priorities["prio_med"]:
			q = q | Q(priority=TodoItem.PRIORITY_MEDIUM)
		if priorities["prio_low"]:
			q = q | Q(priority=TodoItem.PRIORITY_LOW)
		
		tasks = TodoItem.objects.filter(owner=user).filter(q).all()
		body = "Ваши задачи и приоритеты:\n"
		
		for t in list(tasks):
			if t.is_completed:
				body += f"[x] {t.description} ({t.get_priority_display()})\n"
			else:
				body += f"[ ] {t.description} ({t.get_priority_display()})\n"
		
		return body

	def post(self, request, *args, **kwargs):
		
		form = TodoItemExportForm(request.POST)
		
		if form.is_valid():
			email = request.user.email
			body = self.generate_body(request.user, form.cleaned_data)
			send_mail("Задачи", body, settings.EMAIL_HOST_USER, [email])
			messages.success(request, "Задачи были отправлены на почту %s" % email)
		else:
			messages.error(request, "Что-то пошло не так, попробуйте ещё раз")
		
		return redirect(reverse("tasks:list"))

	def get(self, request, *args, **kwargs):
		form = TodoItemExportForm()
		return render(request, "tasks/export.html", {"form": form})

class TaskEditView(LoginRequiredMixin, View):
	def post(self, request, pk, *args, **kwargs):
		t = TodoItem.objects.get(id=pk)
		form = TodoItemForm(request.POST, instance=t)
		if form.is_valid():
			new_task = form.save(commit=False)
			new_task.owner = request.user
			new_task.save()
			form.save_m2m()
			return redirect(reverse("tasks:list"))
		return render(request, "tasks/edit.html", {"form": form, "task": t})


	def get(self, request, pk, *args, **kwargs):
		t = TodoItem.objects.get(id=pk)
		form = TodoItemForm(instance=t)
		return render(request, "tasks/edit.html", {"form": form, "task": t})


class TaskDetailsView(DetailView):
	model = TodoItem
	template_name = 'tasks/details.html'

class TaskListView(LoginRequiredMixin,ListView):
	
	model = TodoItem
	context_object_name = "tasks"
	template_name = "tasks/list.html" 
	
	
	
	def get_queryset(self):
		u = self.request.user
		return u.tasks.all()
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		user_tasks = self.get_queryset()
		tags = []
		for t in user_tasks:
			tags.append(list(t.tags.all()))
			context['tags'] = filter_tags(tags)
		return context

class TaskCreateView(View):
	
	def my_render(self, request, form):
		return render(request, "tasks/create.html", {"form": form})
	
	def post(self, request, *args, **kwargs):
		form = TodoItemForm(request.POST)
		if form.is_valid():
			new_task = form.save(commit=False)
			new_task.owner = request.user
			new_task.save()
			form.save_m2m()
			messages.info(request, "Новая задача создана")
			return redirect(reverse("tasks:list"))
		return self.my_render(request, form)

	def get(self, request, *args, **kwargs):
		form = TodoItemForm()
		return self.my_render(request, form)


def complete_task(request, uid):
	t = TodoItem.objects.get(id=uid)
	t.complete_trigger()
	t.save()
	messages.success(request, "Задача выполнена")
	return redirect("tasks:list")

def delete_task(request, uid):
	t = TodoItem.objects.get(id=uid)
	t.delete()
	messages.warning(request, "Задача удалена")
	return redirect("tasks:list")

@login_required
def index(request):
	counts = Tag.objects.annotate(total_tasks=Count('todoitem')).order_by("-total_tasks")
	counts = {c.name: c.total_tasks for c in counts}
	return render(request, "tasks/index.html", {"counts": counts})

def filter_tags(tags_by_task):
		set_of_tags = set([])
		for task_tags in tags_by_task:
			set_of_tags = set_of_tags.union(set(task_tags))
		return list(set_of_tags)