import random
from datetime import date
from django.shortcuts import render, get_object_or_404, redirect
from .models import Movie, Genre


def home_page(request):
    today = date.today()

    # 1. PHIM SẮP CHIẾU: Rating 0.0 và ngày phát hành lớn hơn hôm nay
    upcoming_movies = Movie.objects.filter(rating=0.0, release_date__gt=today).order_by(
        "release_date"
    )

    # 2. PHIM ĐANG HOT: Rating > 7.0 và đã/đang chiếu
    hot_movies = Movie.objects.filter(rating__gt=7.0, release_date__lte=today).order_by(
        "-rating"
    )

    # 3. PHIM MỚI RA: Đã chiếu, sắp xếp từ mới nhất đến cũ nhất
    new_movies = Movie.objects.filter(release_date__lte=today).order_by("-release_date")

    danh_sach_the_loai = Genre.objects.all()

    context = {
        # Truyền tạm new_movies vào biến 'movies' để vòng lặp ở home.html cũ không bị sập
        "movies": new_movies,
        "upcoming_movies": upcoming_movies,
        "hot_movies": hot_movies,
        "new_movies": new_movies,
        "categories": danh_sach_the_loai,
    }
    return render(request, "movies/home.html", context)


def the_loai(request):
    ten_the_loai_duoc_chon = request.GET.get("ten")
    danh_sach_the_loai = Genre.objects.all()

    if ten_the_loai_duoc_chon:
        # Lọc Movie thông qua quan hệ ManyToMany với Genre
        ket_qua_phim = Movie.objects.filter(
            genres__name=ten_the_loai_duoc_chon
        ).order_by("-release_date")
    else:
        ket_qua_phim = Movie.objects.none()

    context = {
        "movies": ket_qua_phim,
        "categories": danh_sach_the_loai,
        "tieu_de_muc": ten_the_loai_duoc_chon,
    }
    return render(request, "movies/home.html", context)


def search_movie(request):
    query = request.GET.get("q")
    danh_sach_the_loai = Genre.objects.all()

    if query:
        ket_qua = Movie.objects.filter(title__icontains=query).order_by("-release_date")
    else:
        ket_qua = Movie.objects.none()

    context = {"movies": ket_qua, "query": query, "categories": danh_sach_the_loai}
    return render(request, "movies/home.html", context)


def phim_le(request):
    danh_sach_phim = Movie.objects.filter(type="Phim Lẻ").order_by("-release_date")
    danh_sach_the_loai = Genre.objects.all()

    context = {
        "movies": danh_sach_phim,
        "categories": danh_sach_the_loai,
    }
    return render(request, "movies/phim_le.html", context)


def phim_bo(request):
    danh_sach_phim = Movie.objects.filter(type="Phim Bộ").order_by("-release_date")
    danh_sach_the_loai = Genre.objects.all()

    context = {
        "movies": danh_sach_phim,
        "categories": danh_sach_the_loai,
    }
    return render(request, "movies/phim_bo.html", context)


def ngau_nhien(request):
    movies = list(Movie.objects.all())

    if movies:
        movie = random.choice(movies)
        return redirect("xem_series", id=movie.id)

    return redirect("home")


def xem_series(request, id):
    # Hàm này dùng cho trang Chi tiết phim (series_detail.html)
    phim_hien_tai = get_object_or_404(Movie, id=id)
    danh_sach_the_loai = Genre.objects.all()

    context = {
        # Đặt tên biến là 'series' để tương thích với {{ series.title }} trong HTML cũ
        "series": phim_hien_tai,
        "categories": danh_sach_the_loai,
    }
    return render(request, "movies/series_detail.html", context)


# XÓA BỎ HOÀN TOÀN HÀM xem_phim(request, id)
