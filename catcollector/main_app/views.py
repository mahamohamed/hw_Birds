from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Bird, Toy
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from .forms import FeedingForm
from django.views.generic import ListView,DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

class BirdCreate(LoginRequiredMixin,CreateView):
    model=Bird
    # fields = '__all__'
    fields=['name','breed','describtion','age','image']
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class BirdUpdate(LoginRequiredMixin,UpdateView):
    model=Bird
    # fields = '__all__'
    fields=['breed','describtion','age']

class BirdDelete(LoginRequiredMixin,DeleteView):
    model=Bird
    success_url ='/birds/'

class ToyList(LoginRequiredMixin,ListView):
    model=Toy
class ToyDetail(LoginRequiredMixin,DetailView):
    model=Toy
class ToyCreate(LoginRequiredMixin,CreateView):
    model=Toy
    fields='__all__'
class ToyUpdate(LoginRequiredMixin,UpdateView):
    model=Toy
    fields=['name','color']
class ToyDelete(LoginRequiredMixin,DeleteView):
    model=Toy
    success_url='/toys/'


# Create your views here.
def home(request):
    return render(request, 'home.html')
def about(request):
    return render(request, 'about.html')
def base(request):
    return render(request, 'base.html')

@login_required
def bird_index(request):
    # birds=Bird.objects.all()
    birds = Bird.objects.filter(user=request.user)
    return render(request, 'birds/index.html', {'birds':birds})
@login_required
def bird_detail(request, bird_id):
    bird = Bird.objects.get(id=bird_id)
    feeding_form = FeedingForm()
    toys_bird_doesnt_have=Toy.objects.exclude(id__in=bird.toys.all().values_list('id'))
    return render(request, 'birds/detail.html', {'bird': bird, 'feeding_form':feeding_form,'toys':toys_bird_doesnt_have})
@login_required
def add_feeding(request, bird_id):
  # create a ModelForm instance using the data in request.POST
  form = FeedingForm(request.POST)
  # validate the form
  if form.is_valid():
    # don't save the form to the db until it
    # has the cat_id assigned
    new_feeding = form.save(commit=False)
    new_feeding.bird_id = bird_id
    new_feeding.save()
  return redirect('detail', bird_id=bird_id)
@login_required
def assoc_toy(request, bird_id, toy_id):
  # Note that you can pass a toy's id instead of the whole object
  Bird.objects.get(id=bird_id).toys.add(toy_id)
  return redirect('detail', bird_id=bird_id)
@login_required
def unassoc_toy(request, bird_id, toy_id):
  # Note that you can pass a toy's id instead of the whole object
  Bird.objects.get(id=bird_id).toys.remove(toy_id)
  return redirect('detail', bird_id=bird_id)

def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)
