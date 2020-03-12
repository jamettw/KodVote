from asyncio.windows_events import NULL
from builtins import object
from datetime import datetime
from fnmatch import filter
from itertools import count
from lib2to3.fixes.fix_input import context
from os.path import isdir
from venv import create

from astroid import objects
from astroid.scoped_nodes import objects
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.db.models.deletion import SET_NULL
from django.shortcuts import redirect, render
from django.template.context_processors import request
from django.templatetags.static import static

from .models import Poll, Poll_Choice, Poll_Vote


# Create your views here.
@login_required
def index(request):
    all_poll = Poll.objects.all()
    time = datetime.now()
    return render(request, template_name='index.html', context={'all_poll' : all_poll, 'time' : time})

@login_required
def page_addPoll(request):
    msg = ''
    current_user = request.user
    if request.method == 'POST':
        try:
            poll = Poll.objects.create(
                subject=request.POST.get('title'),
                detail=request.POST.get('description'),
                start_date=request.POST.get('start_date'),
                end_date=request.POST.get('end_date'),
                create_by=User.objects.get(pk=current_user.id),
                password = request.POST.get('password'),
                picture = request.FILES['picture']
            )
        except:
            poll = Poll.objects.create(
                subject=request.POST.get('title'),
                detail=request.POST.get('description'),
                start_date=request.POST.get('start_date'),
                end_date=request.POST.get('end_date'),
                create_by=User.objects.get(pk=current_user.id),
                password = request.POST.get('password'),
                picture = None
            )
        return redirect('addChoice', poll_id=poll.id)
    else:
        poll = Poll.objects.none()

    context = {
        'msg': msg
    }

    return render(request, template_name='poll/addPoll.html', context=context)

@login_required
def page_addChoice(request, poll_id):
    if request.method == 'POST':
        if 'more_choice' in request.POST:
            try:
                choice = Poll_Choice.objects.create(
                subject=request.POST.get('title'),
                poll_id=Poll.objects.get(pk=poll_id),
                image = request.FILES['picture']
                )
            except:
                choice = Poll_Choice.objects.create(
                subject=request.POST.get('title'),
                poll_id=Poll.objects.get(pk=poll_id),
                image = None
                )
            context = {'poll_id' : poll_id}
            return render(request, template_name='poll/addChoice.html', context=context)

        if 'success' in request.POST:
            try:
                choice = Poll_Choice.objects.create(
                subject=request.POST.get('title'),
                poll_id=Poll.objects.get(pk=poll_id),
                image = request.FILES['picture']
                )
            except:
                choice = Poll_Choice.objects.create(
                subject=request.POST.get('title'),
                poll_id=Poll.objects.get(pk=poll_id),
                image = None
                )
            return redirect('index')
    else:
        choice = Poll.objects.none()

    context = {
        'poll_id' : poll_id
    }
    return render(request, template_name='poll/addChoice.html', context=context)

@login_required
def page_myPoll(request):
    current_user = request.user
    all_poll = Poll.objects.filter(create_by=current_user.id)
    return render(request, template_name='poll/myPoll.html', context={'all_poll' : all_poll})

@login_required
def page_votePage(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)
    all_choice = Poll_Choice.objects.filter(poll_id_id=poll_id)
    context={
        'poll' : poll,
        'all_choice' : all_choice
    }
    return render(request, template_name='poll/votePage.html', context=context)

@login_required
def delete_poll(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)
    poll.delete()
    return redirect(to='myPoll')

@login_required
def need_Password(request, poll_id):
    msg = ''
    poll = Poll.objects.get(pk=poll_id)
    if request.method == 'POST':
        pass1 = request.POST.get('password')
        if pass1==poll.password:
            return redirect('votePage', poll_id=poll.id)
        else:
            msg = 'รหัสไม่ถูกต้อง!!!'
    context={
        'poll' : poll,
        'msg' : msg
    }
    return render(request, template_name='poll/needPassword.html', context=context)

@login_required
def edit_poll(request, poll_id):
    msg = ''
    poll = Poll.objects.get(pk=poll_id)
    current_user = request.user
    if request.method == 'POST':
        try:
            poll.subject=request.POST.get('title')
            poll.detail=request.POST.get('description')
            poll.start_date=request.POST.get('start_date')
            poll.end_date=request.POST.get('end_date')
            poll.create_by=User.objects.get(pk=current_user.id)
            poll.password = request.POST.get('password')
            poll.picture = request.FILES['picture']
        except:
            poll.subject=request.POST.get('title')
            poll.detail=request.POST.get('description')
            poll.start_date=request.POST.get('start_date')
            poll.end_date=request.POST.get('end_date')
            poll.create_by=User.objects.get(pk=current_user.id)
            poll.password = request.POST.get('password')
            poll.picture = None

        poll.save()
        msg = 'Successfully update - id: %i' % (poll.id)

    context = {
        'poll' : poll,
        'msg' : msg
    }

    return render(request, 'poll/editPoll.html', context=context)

@login_required
def send_vote(request, choice_id):
    choice = Poll_Choice.objects.get(pk=choice_id)
    poll = Poll.objects.get(pk=choice.poll_id_id)
    current_user = request.user
    count = Poll_Vote.objects.filter(poll_id=poll.id, vote_by=current_user.id).count()
    print(count)
    if count > 0:
        return redirect(to='index')
    else:
        vote = Poll_Vote.objects.create(
            choice_id = Poll_Choice.objects.get(pk=choice.id),
            poll_id = Poll.objects.get(pk=poll.id),
            vote_by =User.objects.get(pk=current_user.id)
        )
    context = {
        'choice' : choice,
        'poll' : poll,
        'current_user' : current_user
    }
    return render(request, 'poll/voteComplete.html', context=context)

@login_required
def report_vote(request, poll_id):
    amount = []
    poll = Poll.objects.get(pk=poll_id)
    all_choice = Poll_Choice.objects.filter(poll_id_id=poll_id)
    all_vote = Poll_Vote.objects.filter(poll_id_id=poll_id)
    for i in all_choice:
        amount.append(all_vote.filter(choice_id=i.id).count())
    context={
        'poll' : poll,
        'all_choice' : all_choice,
        'all_vote' : all_vote,
        'amount' : amount,
    }
    return render(request, 'poll/report.html', context=context)

@login_required
def choice_list(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)
    all_choice = Poll_Choice.objects.filter(poll_id=poll.id)
    context={
        'poll' : poll,
        'all_choice' : all_choice
    }
    return render(request, 'poll/choiceList.html', context=context)

@login_required
def delete_choice(request, choice_id):
    choice = Poll_Choice.objects.get(pk=choice_id)
    poll = Poll.objects.get(pk=choice.poll_id_id)
    choice.delete()
    return redirect(to='choiceList', poll_id=poll.id)
