from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_page, name="home"),
    path("the-loai/", views.the_loai, name="the_loai"),
    path("tim-kiem/", views.search_movie, name="search"),
    path("phim-le/", views.phim_le, name="phim_le"),
    path("phim-bo/", views.phim_bo, name="phim_bo"),
    path("ngau-nhien/", views.ngau_nhien, name="ngau_nhien"),
    path("chi-tiet/<int:id>/", views.xem_series, name="xem_series"),
    path("dang-chieu/", views.phim_dang_chieu, name="phim_dang_chieu"),
    path("live-search/", views.live_search, name="live_search"),
]
