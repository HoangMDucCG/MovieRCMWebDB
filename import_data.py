import json
import os
import django
from datetime import datetime

# Thiết lập môi trường Django (Thay 'core' bằng tên thư mục chứa file settings.py của bạn nếu khác)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

# Import các models (Thay 'movies' bằng tên app của bạn)
from movies.models import Movie, Genre, TheaterLink


def run_import():
    # Đọc dữ liệu từ file JSON
    file_path = "data_phim_python.json"

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"Lỗi: Không tìm thấy file {file_path}")
        return

    print(f"Bắt đầu import {len(data)} bộ phim...")

    for item in data:
        # 1. Xử lý ngày tháng từ DD-MM-YYYY sang Date object
        release_date_obj = None
        date_str = item.get("release_date")
        if date_str:
            try:
                release_date_obj = datetime.strptime(date_str, "%d-%m-%Y").date()
            except ValueError:
                print(
                    f"Bỏ qua ngày không hợp lệ của phim {item.get('title')}: {date_str}"
                )

        # 2. Tạo hoặc cập nhật bản ghi Movie
        movie, created = Movie.objects.update_or_create(
            title=item.get("title"),
            defaults={
                "type": item.get("type", "Phim Lẻ"),
                "release_date": release_date_obj,
                "description": item.get("description", ""),
                "poster_url": item.get("poster_url", ""),
                "trailer": item.get("trailer", ""),
                "rating": item.get("rating", 0.0),
                "runtime_minutes": item.get("runtime_minutes"),
                "total_episodes": item.get("total_episodes"),
            },
        )

        # 3. Xử lý Thể loại (Genres)
        genres_data = item.get("genres", [])
        if genres_data:
            movie.genres.clear()  # Xóa thể loại cũ nếu cập nhật lại
            for genre_name in genres_data:
                genre, _ = Genre.objects.get_or_create(name=genre_name.strip())
                movie.genres.add(genre)

        # 4. Xử lý Link đặt vé/xem phim (TheaterLink)
        detail_links = item.get("detail_link", {})
        if detail_links:
            # Xóa các link cũ để tránh trùng lặp nếu chạy script nhiều lần
            TheaterLink.objects.filter(movie=movie).delete()

            for theater_name, link_url in detail_links.items():
                TheaterLink.objects.create(
                    movie=movie,
                    theater_name=theater_name.strip(),
                    link=link_url.strip(),
                )

        print(f"Đã xử lý: {movie.title}")

    print("Hoàn tất import dữ liệu!")


if __name__ == "__main__":
    run_import()
