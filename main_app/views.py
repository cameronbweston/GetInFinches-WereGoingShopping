from django.shortcuts import redirect, render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Finch
from .forms import FeedingForm

def finches_index(request):
  finches = Finch.objects.all()
  return render(request, 'finches/index.html', { 'finches': finches })
# Create your views here.
def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

def finches_detail(request, finch_id):
  finch = Finch.objects.get(id=finch_id)
  #instantiate the feeding form to be rendered in the template
  feeding_form = FeedingForm()
  #pass the cat and feeding_form in the context
  return render(request, 'finches/detail.html', {'finch' : finch, 'feeding_form' : feeding_form})

class FinchCreate(CreateView):
  model = Finch
  fields = '__all__'
  success_url = '/finches/'

class FinchUpdate(UpdateView):
  model = Finch
  fields = '__all__'

class FinchDelete(DeleteView):
  model = Finch
  success_url = '/finches/'

def add_feeding(request, finch_id):
  #Need an instance of the feeding form to use...
  form = FeedingForm(request.POST)
  if form.is_valid():
    #dont save form to db until it has the cat_id assigned
    new_feeding = form.save(commit=False)
    new_feeding.finch_id = finch_id
    new_feeding.save()
  return redirect('finches_detail', finch_id = finch_id)