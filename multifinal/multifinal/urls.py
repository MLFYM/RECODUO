"""multifinal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from mlfu import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'mlfu'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('test/', views.test, name='test'),
    # path('camera/', views.camera, name='camera'),
    path('camera2/', views.camera2, name='camera2'),
    path('camera2/neutral/', views.giveQuestion_neutral, name='giveQuestion1'),
    path('camera2/positive/', views.giveQuestion_positive, name='giveQuestion2'),
    path('camera2/negative/', views.giveQuestion_negative, name='giveQuestion3'),
    path('image_upload/', views.image_upload, name='image_upload'),
    path('camera2/check_playlist/', views.song_list, name='songlist'),
    path('camera2/check_playlist/recommend_song/', views.recommend_function, name='recommend_function'),
    path('recommend_repeat/', views.recommend_repeat, name='repeat_function')
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
