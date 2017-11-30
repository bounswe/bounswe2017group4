from django.conf.urls import url
from chatBot import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    # url(r'^users/$', views.user_list), Çalışan url
    # url(r'^users/(?P<pk>[0-9]+)/$', views.user_detail),
    url(r'^users/$', views.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
    url(r'^userinterests/$', views.UserInterestList.as_view()),
    url(r'^userinterests/(?P<pk>[0-9]+)/$', views.UserInterestDetail.as_view()),
    url(r'^userratings/$', views.UserRatingList.as_view()),
    url(r'^userratings/(?P<pk>[0-9]+)/$', views.UserRatingDetail.as_view()),
    url(r'^usercomments/$', views.UserCommentList.as_view()),
    url(r'^usercomments/(?P<pk>[0-9]+)/$', views.UserCommentDetail.as_view()),
    url(r'^states/$', views.StateList.as_view()),
    url(r'^states/(?P<pk>[0-9]+)/$', views.StateDetail.as_view()),
    url(r'^edges/$', views.EdgeList.as_view()),
    url(r'^edges/(?P<pk>[0-9]+)/$', views.EdgeDetail.as_view()),
    url(r'^responses/$', views.ResponseList.as_view()),
    url(r'^responses/(?P<pk>[0-9]+)/$', views.ResponseDetail.as_view()),
    url(r'^histories/$', views.HistoryList.as_view()),
    url(r'^histories/(?P<pk>[0-9]+)/$', views.HistoryDetail.as_view()),

    # GET 
    url('isAdmin', views.isAdmin),
    url('getRatings', views.getRatings),

    # POST
    url('addState', views.addState),

]


urlpatterns = format_suffix_patterns(urlpatterns)
