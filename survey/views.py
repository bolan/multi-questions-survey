from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from survey.models import SurveyPaper, Question, Choice
from django.contrib.auth import authenticate, login

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            #return HttpResponseRedirect("/survey/register_success/")
    else:
        form = UserCreationForm()
    return render(request, "survey/register.html",{'form': form,})

def login_page(request):
    return render(request, 'survey/login_page.html', {})

def logging_in(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect(reverse("survey.views.login_success"))
        #else:
            # Return a 'disabled account' error message.
    #else:
        # Return an 'invalid login' error message. 

def login_success(request):
    return render(request, 'survey/login_success.html', {})

def logout_view(request):
    logout()
    return HttpResponseRedirect(reverse("survey.views.logout_success"))

def logout_success(request):
    return render(request, "survey/logout_success.html", {})

def index(request):
    surveypaper_list = SurveyPaper.objects.all().order_by('-pub_date')
    paginator = Paginator(surveypaper_list, 20)

    page = request.GET.get('page')
    try:
        surveypapers = paginator.page(page)
    except PageNotAnInteger:
        surveypapers = paginator.page(1)
    except EmptyPage:
        surveypapers = paginator.page(paginator.num_pages)

    return render(request, 'survey/index.html', {'surveypapers': surveypapers})

def detail(request, surveypaper_id):
    surveypaper = get_object_or_404(SurveyPaper, pk=surveypaper_id)
    return render(request, 'survey/detail.html', {'surveypaper': surveypaper})

def vote(request, surveypaper_id):
    surveypaper = get_object_or_404(SurveyPaper, pk=surveypaper_id)
    questions = Question.objects.filter(surveypaper=surveypaper_id)
    for i in range (0,len(questions)):
        question_name = str(i+1)
        selected_choice = questions[i].choice_set.get(pk=request.POST[question_name])
        selected_choice.votes += 1
        selected_choice.save()
    return HttpResponseRedirect(reverse('survey.views.results', args=(surveypaper.id,)))

def results(request, surveypaper_id):
    surveypaper = get_object_or_404(SurveyPaper, pk=surveypaper_id)
    return render(request, 'survey/results.html', {'surveypaper': surveypaper})
