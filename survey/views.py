from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from survey.models import SurveyPaper, Question, Choice
from django.contrib.auth import authenticate, login, logout
from django.forms.models import inlineformset_factory
from django.forms.models import ModelForm

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/survey/register_success/")
    else:
        form = UserCreationForm()
    return render(request, "survey/register.html",{'form': form,})

def register_success(request):
    return render(request, 'survey/register_success.html', {})

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
        else:
            return render(request, 'survey/login_page.html', {
                'error_message': 'Sorry, your account has been disabled for some reasons.',
            })
    else:
        return render(request, 'survey/login_page.html', {
            'error_message': 'Sorry, your username or password is incorrect, or does not exist.',
        })

def login_success(request):
    return render(request, 'survey/login_success.html', {})

def logout_view(request):
    logout(request)
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
        try:
            selected_choice = questions[i].choice_set.get(pk=request.POST[question_name])
        except (KeyError, Choice.DoesNotExist):
            return render(request, 'survey/detail.html', {
                'surveypaper': surveypaper,
                'error_message': "Please select every question, thank you.",
            })
        else:
            selected_choice.votes += 1
            selected_choice.save()
    return HttpResponseRedirect(reverse('survey.views.results', args=(surveypaper.id,)))

def results(request, surveypaper_id):
    surveypaper = get_object_or_404(SurveyPaper, pk=surveypaper_id)
    return render(request, 'survey/results.html', {'surveypaper': surveypaper})

# Make a survey paper creating form
class SurveyPaperForm(ModelForm):
    class Meta:
        model = SurveyPaper

def paper_creator(request):
    # This page is limiting access to logged-in users
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/survey/login_page/')

    if request.method == 'POST':
        form = SurveyPaperForm(request.POST)
        if form.is_valid():
            new_paper = form.save(commit=False)
            new_paper.author = request.user
            new_paper = form.save()
        new_paper_str_id = str(new_paper.id)
        return HttpResponseRedirect('/survey/'+new_paper_str_id+'/created_success/')
    else:
        form = SurveyPaperForm()

    return render(request, 'survey/paper_creator.html', {
            'form': form,
    })

def created_success(request, surveypaper_id):
    surveypaper = get_object_or_404(SurveyPaper, pk=surveypaper_id)
    if not request.user == surveypaper.author:
        return HttpResponseRedirect('/survey/login_page/')

    return render(request, 'survey/created_success.html', {
            'surveypaper': surveypaper,
    })
