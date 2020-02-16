
from . import views
from django.urls import path

# urlpatterns = [
#     path('', views.index, name='home'),   
#     path('test/<question>', views.test, name='test'),
# ]

urlpatterns = [
    path('', views.index, name='home'),
    path('form/', views.FormQAView, name='form'),
    path('upload/', views.simple_upload, name='simple_upload'),
    path('getfilenames/', views.getFileNames, name='getFileNames'),
    path('getanswer/', views.getAnswer, name='getAnswer'),
    path('deletefile/', views.deleteFile, name='deleteFile'),
    path('incident_upload/', views.FileUploadView.as_view())
]
