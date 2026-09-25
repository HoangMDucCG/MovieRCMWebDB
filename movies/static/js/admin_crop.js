document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('id_poster_image');
    if (!fileInput) return;

    // 1. Tạo giao diện khung crop chèn ngay dưới nút chọn file
    const container = document.createElement('div');
    container.innerHTML = `
        <div id="crop-modal" style="display:none; margin-top: 15px; border: 1px dashed #ccc; padding: 10px;">
            <p style="margin-top:0; font-weight:bold;">Căn chỉnh khung ảnh:</p>
            <div style="max-width: 500px; margin-bottom: 10px;">
                <img id="image-to-crop" style="max-width: 100%; display: block;">
            </div>
            <button type="button" id="btn-crop" style="background: #f39c12; padding: 8px 15px; color: white; border: none; font-weight:bold; cursor: pointer; border-radius: 4px;">✂️CẮT</button>
            <span id="crop-status" style="color: #28a745; margin-left: 10px; font-weight:bold; display: none;">✔ Đã cắt xong 600x900! Hãy bấm Save.</span>
        </div>
    `;
    fileInput.parentNode.insertBefore(container, fileInput.nextSibling);

    let cropper = null;
    const image = document.getElementById('image-to-crop');
    const modal = document.getElementById('crop-modal');
    const btnCrop = document.getElementById('btn-crop');
    const status = document.getElementById('crop-status');

    // 2. Bắt sự kiện khi bạn vừa chọn file từ máy tính
    fileInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(event) {
                image.src = event.target.result;
                modal.style.display = 'block';
                status.style.display = 'none';

                if (cropper) cropper.destroy();
                cropper = new Cropper(image, { aspectRatio: 600 / 900, viewMode: 1 });
            };
            reader.readAsDataURL(file);
        }
    });

    // 3. Xử lý thuật toán cắt và đánh tráo file
    btnCrop.addEventListener('click', function() {
        if (!cropper) return;
        
        cropper.getCroppedCanvas({ width: 600, height: 900 }).toBlob(function(blob) {
            // Đóng gói lại thành file mới chuẩn mực
            const croppedFile = new File([blob], fileInput.files[0].name, { type: "image/jpeg", lastModified: Date.now() });
            
            // Tráo đổi file gốc vừa chọn bằng file đã cắt
            const dataTransfer = new DataTransfer();
            dataTransfer.items.add(croppedFile);
            fileInput.files = dataTransfer.files;

            status.style.display = 'inline';
            modal.style.display = 'none';
            cropper.destroy();
        }, 'image/jpeg', 0.9);
    });
});