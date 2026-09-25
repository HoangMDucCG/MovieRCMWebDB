from django.db import models
from django.utils import timezone


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Movie(models.Model):
    TYPE_CHOICES = [
        ("Phim Lẻ", "Phim Lẻ"),
        ("Phim Bộ", "Phim Bộ"),
    ]

    title = models.CharField(max_length=255)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)

    # Bắt buộc là DateField để so sánh ngày tháng cho mục "Phim sắp chiếu"
    release_date = models.DateField(null=True, blank=True)

    description = models.TextField(blank=True, null=True)
    poster_url = models.URLField(max_length=1000, blank=True, null=True)
    trailer = models.URLField(max_length=1000, blank=True, null=True)
    rating = models.FloatField(default=0.0)

    runtime_minutes = models.IntegerField(null=True, blank=True)
    total_episodes = models.IntegerField(null=True, blank=True)

    genres = models.ManyToManyField(Genre, related_name="movies")

    def __str__(self):
        return self.title


class TheaterLink(models.Model):
    # Liên kết bảng này với bảng Movie để 1 phim có nhiều nút đặt vé rạp khác nhau
    movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE, related_name="theater_links"
    )
    theater_name = models.CharField(max_length=100)  # VD: CGV, Lotte, Beta, Netflix
    link = models.URLField(max_length=1000)

    def __str__(self):
        return f"{self.theater_name} - {self.movie.title}"
