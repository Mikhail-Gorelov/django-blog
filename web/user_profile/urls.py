from django.urls import include, path
from main.views import TemplateAPIView
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'user_profile'

router = DefaultRouter()

router.register('profile', views.ProfileViewSet)
router.register('user', views.UserViewSet)

urlpatterns = [
    path('', views.ProfileViewSet.as_view({'get': 'profile'}), name='user_profile'),
]

urlpatterns += [
    path('news-feed-article/', views.NewsFeedArticleListView.as_view(),
         name='news_feed_article'),
    path('news-feed-comment/', views.NewsFeedCommentListView.as_view(),
         name='news_feed_comment'),
    path('news-feed-followers/', views.NewsFeedFollowerListView.as_view(),
         name='news_feed_follower'),
    path('news-feed-likes/', views.NewsFeedLikeListView.as_view(),
         name='news_feed_like'),
    path('settings-update/<user_id>', views.ProfileSettingsView.as_view(), name='change_user_credentials'),
    path('settings-retrieve/<user_id>/', views.ProfileSettingsRetrieveViewSet.as_view({'get': 'retrieve'}),
         name='user_settings'),
    path('true-users/', views.TrueUserViewSet.as_view({'get': 'user_list'}), name='api_list_true_users'),
    path('password-change/', views.UserViewSet.as_view({"post": 'password_change'}), name='password_change'),
    path('update-image/', views.UserViewSet.as_view({"post": 'update_image'}), name='update_image'),
    path('<id>/', views.ProfileViewSet.as_view({'get': 'retrieve'}), name='user_profile_id'),
]

urlpatterns += router.urls
