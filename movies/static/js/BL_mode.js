document.addEventListener('DOMContentLoaded', function() {
    const themeToggleBtn = document.querySelector('.theme-toggle');
    const body = document.body;

    // 1. Kiểm tra trạng thái đã lưu từ lần truy cập trước
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'light') {
        body.classList.add('light-mode');
        if (themeToggleBtn) themeToggleBtn.textContent = 'Mode: Tối';
    }

    // 2. Bắt sự kiện khi người dùng bấm nút
    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', function() {
            body.classList.toggle('light-mode');
            
            // 3. Đổi chữ trên nút và lưu trạng thái vào localStorage
            if (body.classList.contains('light-mode')) {
                localStorage.setItem('theme', 'light');
                themeToggleBtn.textContent = 'Mode: Tối';
            } else {
                localStorage.setItem('theme', 'dark');
                themeToggleBtn.textContent = 'Mode: Sáng';
            }
        });
    }
});