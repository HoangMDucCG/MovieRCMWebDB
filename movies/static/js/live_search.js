document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search-input');
    const searchDropdown = document.getElementById('search-dropdown');
    const resultsList = document.getElementById('search-results-list');
    let debounceTimer;

    searchInput.addEventListener('input', function() {
        clearTimeout(debounceTimer);
        const query = this.value.trim();

        // Ẩn dropdown nếu xóa hết chữ
        if (query.length === 0) {
            searchDropdown.style.display = 'none';
            return;
        }

        // Đợi 300ms sau khi ngừng gõ mới gọi API để tránh lag web
        debounceTimer = setTimeout(() => {
            fetch(`/live-search/?q=${encodeURIComponent(query)}`)
                .then(response => response.json())
                .then(data => {
                    resultsList.innerHTML = ''; // Xóa kết quả cũ
                    
                    if (data.results.length > 0) {
                        data.results.forEach(movie => {
                            const item = document.createElement('a');
                            item.href = movie.url; // Link lấy từ views.py
                            item.className = 'search-result-item';
                            item.innerHTML = `
                                <img src="${movie.poster_url}" class="search-result-img" alt="poster">
                                <div class="search-result-info">
                                    <div class="search-result-title">${movie.title}</div>
                                    <div class="search-result-meta">Phim • ${movie.year}</div>
                                </div>
                            `;
                            resultsList.appendChild(item);
                        });
                    } else {
                        resultsList.innerHTML = '<div style="padding: 15px; color: #888; font-size: 14px;">Không tìm thấy phim phù hợp.</div>';
                    }
                    searchDropdown.style.display = 'block'; // Hiển thị khung
                });
        }, 300); 
    });

    // Tự động ẩn khung kết quả khi click chuột ra ngoài
    document.addEventListener('click', function(e) {
        if (!searchInput.contains(e.target) && !searchDropdown.contains(e.target)) {
            searchDropdown.style.display = 'none';
        }
    });
});