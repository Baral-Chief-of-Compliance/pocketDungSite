from django.urls import path  
from . import views  
  
app_name = "wiki" #пространство имен для приложения wiki
urlpatterns = [  
    path("", views.index, name="index"),
    path("login/", views.login_wiki, name="login"),
    path("logout/", views.logout_wiki, name="logout"),
    path("media/materials/<str:filename>", views.secure_file, name="secure_file"),
    path("searh_results/", views.searh, name="search"),
    path("searh_results/<int:i_id>", views.result_search, name="result_search"),
    path("<str:ic_url>/", views.InfoChapterDetails, name="InfoChapterDetails"),
    path("<str:ic_url>/<str:iss_url>/", views.InfoSubSectionDetails, name="InfoSubSectionDetails"),
    path("<str:ic_url>/<str:iss_url>/<int:i_id>/", views.InfoDetails, name="InfoDetails"),
    path("<str:ic_url>/<str:iss_url>/<int:i_id>/materials/<str:m_id>/delete/", views.deleteMaterial, name="deleteMaterial"),
]
