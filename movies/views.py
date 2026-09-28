import random
from datetime import date
from django.shortcuts import render, get_object_or_404, redirect
from .models import Movie, Genre
from urllib.parse import urlparse, parse_qs
from django.http import JsonResponse
from django.urls import reverse


def home_page(request):
    today = date.today()
    # 1. PHIM ĐANG HOT: Rating > 7.0 và đã/đang chiếu
    hot_movies = Movie.objects.filter(rating__gt=8.0, release_date__lte=today).order_by(
        "-rating"
    )[:10]
    # 2. PHIM SẮP CHIẾU: Rating 0.0 và ngày phát hành lớn hơn hôm nay
    upcoming_movies = Movie.objects.filter(rating=0.0, release_date__gt=today).order_by(
        "release_date"
    )[:10]
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
        ket_qua_phim = (
            Movie.objects.filter(genres__name=ten_the_loai_duoc_chon)
            .distinct()
            .order_by("-release_date")
        )
    else:
        ket_qua_phim = Movie.objects.none()

    context = {
        "movies": ket_qua_phim,
        "categories": danh_sach_the_loai,
        "tieu_de_muc": ten_the_loai_duoc_chon,
    }

    return render(request, "movies/the_loai.html", context)


def search_movie(request):
    # Lấy dữ liệu từ URL, mặc định là chuỗi rỗng nếu không có
    query = request.GET.get("q", "").strip()
    genre_filter = request.GET.get("genre", "").strip()

    # 1. Khởi tạo danh sách chứa TOÀN BỘ phim
    movies = Movie.objects.all().order_by("-id")

    # 2. Nếu người dùng có gõ tìm tên phim -> Lọc theo tên
    if query:
        movies = movies.filter(title__icontains=query)

    # 3. Nếu người dùng có chọn thể loại -> Lọc tiếp theo thể loại
    if genre_filter:
        movies = movies.filter(genres__name=genre_filter)

    # 4. Gửi kết quả ra giao diện
    context = {
        "movies": movies,
        "categories": Genre.objects.all(),
        "query": query,
        "selected_genre": genre_filter,
    }

    return render(request, "movies/search.html", context)


def live_search(request):
    query = request.GET.get("q", "").strip()
    if query:
        # Lấy tối đa 5 kết quả khớp nhất
        movies = Movie.objects.filter(title__icontains=query)[:5]
        results = []
        for m in movies:
            results.append(
                {
                    "title": m.title,
                    "poster_url": m.poster_url,
                    # Lấy năm khởi chiếu (nếu có)
                    "year": m.release_date.year if m.release_date else "N/A",
                    # Tự động tạo link chuyển đến trang chi tiết phim
                    "url": reverse("xem_series", args=[m.id]),
                }
            )
        return JsonResponse({"results": results})
    return JsonResponse({"results": []})


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


def get_youtube_id(url):
    if not url:
        return None

    parsed_url = urlparse(url)

    # youtube.com/watch?v=...
    if parsed_url.hostname in ["www.youtube.com", "youtube.com"]:
        if parsed_url.path == "/watch":
            return parse_qs(parsed_url.query).get("v", [None])[0]

        # youtube.com/embed/...
        if parsed_url.path.startswith("/embed/"):
            return parsed_url.path.split("/embed/")[1]

    # youtu.be/...
    if parsed_url.hostname == "youtu.be":
        return parsed_url.path.lstrip("/")

    return None


def xem_series(request, id):
    phim_hien_tai = get_object_or_404(Movie, id=id)
    danh_sach_the_loai = Genre.objects.all()
    trailer_id = get_youtube_id(phim_hien_tai.trailer)

    online_links = phim_hien_tai.theater_links.filter(theater_name="Netflix")

    theater_links = phim_hien_tai.theater_links.exclude(theater_name="Netflix")

    context = {
        "series": phim_hien_tai,
        "categories": danh_sach_the_loai,
        "trailer_id": trailer_id,
        "online_links": online_links,
        "theater_links": theater_links,
    }

    return render(request, "movies/series_detail.html", context)


def phim_dang_chieu(request):
    # Lọc ra những phim có trường is_chieu_rap = True (Giống như đợt trước bạn lọc phim lẻ/bộ bằng số tập)
    movies = Movie.objects.filter(is_chieu_rap=True)

    # Trả về một template (ví dụ: phim_dang_chieu.html) kèm theo danh sách phim đã lọc
    return render(request, "movies/phim_dang_chieu.html", {"movies": movies})


def view_phim_sap_chieu(request):
    today = date.today()
    movies = Movie.objects.filter(release_date__gt=today)
    return render(request, "movies/phim_sap_chieu.html", {"movies": movies})


def view_phim_hot(request):
    movies = Movie.objects.order_by("-rating")

    # Mẹo: Nếu chỉ muốn lấy Top 10 phim hot nhất trang chủ, bạn dùng slice như sau:
    # movies = Movie.objects.order_by('-rating')[:10]

    return render(request, "movies/phim_hot.html", {"movies": movies})


# XÓA BỎ HOÀN TOÀN HÀM xem_phim(request, id)
