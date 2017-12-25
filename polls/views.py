from boto.dynamodb import condition
from django.shortcuts import render
from django.http import HttpResponse, request


from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, TemplateView, CreateView, FormView
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from django import forms
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, logout
from django.contrib import auth
from listofcourse import courses
import json
# Create your views here.

def polls(request):
    return render(request, 'Start.html',locals())

def thanks(request):
    return render(request, 'thanks.html',locals())

def course(request):
    return render(request, 'CourseList.html', {'list':courses})

def teacher(request):
    return render(request, 'Teacher.html',locals())

# def reg(request):
#     return render(request, 'Reg.html')
def authen(request):
    # courses = CoursesView.get_queryset(CoursesView)
    return render(request, 'auth.html',{'list':courses})


class Authen(ListView):

    def get(self, request):
        return render(
            request,
            'auth.html',
            {
                'wall_courses': CoursesView.get_queryset(self)
            }
        )



def authorization(request):
    redirect_url = reverse('course')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(username=form.cleaned_data['login'],
                                     password=form.cleaned_data['password'])
            if user is not None:
                auth.login(request, user)
                return HttpResponseRedirect(redirect_url)
            else:
                form.add_error(None, 'Wrong login or password')
    else:
        form = LoginForm()
    return render(
       request,
       'login.html',
       {'form': form, 'continue': redirect_url}
    )

class UsersView(ListView):
    context_object_name = 'Teacher'
    template_name = 'Teacher.html'
    def get_queryset(self):
        qs = auth.get_user_model().objects.all().order_by('-name')
        return qs



class UserView(View):

    def get(self, request, id):
        redirect_url = reverse('repet-detail',args=[id])
        name = auth.get_user_model().objects.get(id__exact=id)

        # reps = list()
        # for course in CoursesView.get_queryset(self) :
        #     if course == name.id:
        #     reps.append(course)
        #   for rep in cooperated.repetitor.all():
        #
       # return HttpResponseRedirect(redirect_url)
        return render(
           request,
           'repetinfo.html',
           {
              'selected_rep': name,
              'wall_courses': CoursesView.get_queryset(self)
                  #  key=lambda b: b.name,
               #   reverse=True
               # )
            }
           )


def reg(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return authorization(request)
        return render(request, 'register_done.html', {'form': form})
    else:
        form = UserRegistrationForm()
    return render(request, 'Reg.html', {'form': form})

@login_required
def user_cooperate(request, id, fid):
  #if 'button_cpr' in request.POST:
    if id == fid:
        return HttpResponse('Вы пытаетесь сотрудничать с самим собой, обратитесь к врачу')
    user = Repetitor.objects.filter(id__exact=id)[0]
    copuser = Repetitor.objects.filter(id__exact=fid)[0]
    if copuser in user.cooperate.all():
        return HttpResponse('Вы уже сотрудничаете')
    user.cooperate.add(copuser)
    return HttpResponse('Теперь вы сотрудничаете с {}'.format(
       copuser.get_username()
    ))


@login_required
def user_uncooperate(request, id, fid):
    if id == fid:
        return HttpResponse(
           'Вы пытаетесь перестать сотрудничать с самим собой, к врачу уже можно не идти вам пезда'
        )
    user = Repetitor.objects.filter(id__exact=id)[0]
    copuser = Repetitor.objects.filter(id__exact=fid)[0]
    if copuser in user.cooperate.all():
        user.cooperate.remove(copuser)
        return HttpResponse('Вы перестали сотрудничать с {}'.format(
           copuser.get_username()
        ))
    return HttpResponse('Вы не сотрудничали с {}'.format(
       copuser.get_username()
    ))

@login_required
def exit(request):
    logout(request)
    return render(request, 'logout.html')

class CoursesView(ListView):
    context_object_name = 'Course'
    template_name = 'CourseList.html'
    model = Course
    def get_queryset(self):
        #qs = Course.objects.all()
        return Course.objects.all()
    def get_List(Course):
        listc = list(Course.objects())
        return listc

class CourseView(View):
    def get(self, request, id):
        redirect_url = reverse('course_detail', args=[id])
        course = Course.objects.get(id__exact=id)
        return render(request, 'Course.html', {'course':course})



    # template_name = 'NewCourse.html'
    # form_class = CourseForm
    # success_url = '/thanks/'
    #
    # def newcourse(request):
    #     if request.method == 'POST':
    #         form = CourseCreate(request.POST, request.FILES)
    #         form.save()
    #         return render(request, 'auth.html', {'form': form})
    #     else:
    #         form = NewCourse()
    #     return render(request, 'NewCourse.html', {'form': form})

    # def form_valid(self, form):
    #     # This method is called when valid form data has been POSTed.
    #     # It should return an HttpResponse.
    #     form.send_email()
    #     return super().form_valid(form)


    # def get(self, request, id):
    #     name = Course.name
    #     description = Course.description
    #     cost = Course.cost
    #     repetitor_id = Course.repetitor
    #     return render(
    #        request,
    #        'repetinfo.html',
    #        {
    #           'selected_user': repetitor_id,
    #           'wall_courses': sorted(
    #              Course,
    #              key=lambda b: b.name,
    #              reverse=True
    #           )
    #        }
    #     )

@login_required
def newcourse(request):
    # instance = Course(user_posted = request.name)
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            # course.user_posted = request.name
            # print(course.user_posted.id)
            course.save()
            return redirect(reverse('course'))
        return render(request, 'thanks.html', {'form': form})
    else:
        form = CourseForm()
    return render(request, 'NewCourse.html', {'form': form})




class CourseCreate(CreateView):
    model = Course
    views_class = CourseView
    fields = [ 'name',  'description' ,  'cost' ,  'repetitor', 'avatar' ]


class LoadView(View):
    def get(self, request):
        start = (int)(request.GET.get('start'))
        #start = 2
        # condition = {}
        # if start is not None and start.isnumeric():
        #     condition['start'] = int(start)
        #start = int(start)
        users = []
        cour = Course.objects.all().order_by('-name')

        res = cour[start:start+4]
        print(res)
        for r in res:
            users.append(
                {"name": r.name, "description": r.description, "id": r.id, "avatar": r.avatar.url})
        return HttpResponse(json.dumps(users), content_type='application/json')