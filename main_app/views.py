from django.shortcuts import redirect, render
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Finch, Toy
from .forms import FeedingForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class Home(LoginView):
  template_name = 'home.html'

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('finches_index')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'signup.html', context)

def finches_index(request):
  finches = Finch.objects.filter(user = request.user)
  return render(request, 'finches/index.html', { 'finches': finches })

def about(request):
  return render(request, 'about.html')

@login_required
def finches_detail(request, finch_id):
  finch = Finch.objects.get(id=finch_id)
  toys_finch_doesnt_have = Toy.objects.exclude(id__in = finch.toys.all().values_list('id'))
  #instantiate the feeding form to be rendered in the template
  feeding_form = FeedingForm()
  #pass the cat and feeding_form in the context
  return render(request, 'finches/detail.html', {'finch' : finch, 'feeding_form' : feeding_form, 'toys' : toys_finch_doesnt_have})

class FinchCreate(LoginRequiredMixin, CreateView):
  model = Finch
  fields = ['name', 'color', 'description']
  
  def form_valid(self, form):
    #form.instance is the cat being assigned to the user
    form.instance.user = self.request.user
    return super().form_valid(form)

class FinchUpdate(UpdateView):
  model = Finch
  fields = '__all__'

class FinchDelete(DeleteView):
  model = Finch
  success_url = '/finches/'

@login_required
def add_feeding(request, finch_id):
  #Need an instance of the feeding form to use...
  form = FeedingForm(request.POST)
  if form.is_valid():
    #dont save form to db until it has the cat_id assigned
    new_feeding = form.save(commit=False)
    new_feeding.finch_id = finch_id
    new_feeding.save()
  return redirect('finches_detail', finch_id = finch_id)

class ToyCreate(CreateView):
  model = Toy
  fields = '__all__'

class ToyList(ListView):
  model = Toy

class ToyDetail(DetailView):
  model = Toy

class ToyUpdate(UpdateView):
  model = Toy
  fields = ['name', 'color']

class ToyDelete(DeleteView):
  model = Toy
  success_url = '/toys/'

@login_required
def assoc_toy(request, finch_id, toy_id):
  # Note that you can pass a toy's id instead of the whole object
  Finch.objects.get(id=finch_id).toys.add(toy_id)
  return redirect('finches_detail', finch_id=finch_id)