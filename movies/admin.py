from django.contrib import admin
from .models import Genre, Movie, TheaterLink


# 1. Tạo giao diện dạng bảng (Inline) cho các link rạp
class TheaterLinkInline(admin.TabularInline):
    model = TheaterLink
    extra = 1  # Số dòng trống mặc định hiển thị để bạn thêm mới rạp


# 2. Tích hợp Inline vào giao diện quản lý Phim
class MovieAdmin(admin.ModelAdmin):
    inlines = [TheaterLinkInline]

    # (Tùy chọn) Cấu hình thêm để danh sách phim hiện đẹp hơn ở ngoài cùng
    list_display = ("title", "type", "release_date", "rating")
    list_filter = ("type", "genres")
    search_fields = ("title",)


# 3. Đăng ký các Model
admin.site.register(Genre)
admin.site.register(Movie, MovieAdmin)

# Không đăng ký admin.site.register(TheaterLink) ở đây nữa để nó không đứng độc lập bên ngoài
