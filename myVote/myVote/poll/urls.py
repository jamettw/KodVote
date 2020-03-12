from django.urls import path

from . import views

urlpatterns = [
    path('add-poll/', views.page_addPoll, name='addPoll'),
    path('add-poll/<int:poll_id>/', views.page_addPoll, name='addPolls'),
    path('add-choice/<int:poll_id>/', views.page_addChoice, name='addChoice'),
    path('mypoll/', views.page_myPoll, name='myPoll'),
    path('vote-page/<int:poll_id>/', views.page_votePage, name='votePage'),
    path('delete-poll/<int:poll_id>/', views.delete_poll, name='deletePoll'),
    path('need-password/<int:poll_id>/', views.need_Password, name='needPassword'),
    path('edit-poll/<int:poll_id>/', views.edit_poll, name='editPoll'),
    path('report/<int:poll_id>/', views.report_vote, name='reportVote'),
    path('vote-complete/<int:choice_id>', views.send_vote, name='voteComplete'),
    path('choice-list/<int:poll_id>/', views.choice_list, name='choiceList'),
    path('delete-choice/<int:choice_id>', views.delete_choice, name='deleteChoice')
]