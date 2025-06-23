document.addEventListener('DOMContentLoaded', () => {
    // ✏️ 프로필 수정 모달 관련
    const editBtn = document.querySelector('.edit-button');
    const modal = document.getElementById('edit-profile-modal');
    const closeBtn = document.getElementById('close-modal');
    const fileInput = document.getElementById('profile_image');

    if (editBtn && modal) {
        editBtn.addEventListener('click', () => {
            modal.classList.remove('hidden');
        });
    }

    if (closeBtn && modal) {
        closeBtn.addEventListener('click', () => {
            modal.classList.add('hidden');
        });
    }

    if (fileInput) {
        fileInput.addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (file) {
                console.log("선택된 파일:", file.name);
                // 미리보기 추가 가능
            }
        });
    }

    // 🍯 기프티콘 모달 관련
    const openBtn = document.getElementById('openGifticonModal');
    const modal2 = document.getElementById('gifticonModal');
    const checkbox = document.getElementById('confirmCheck');
    const redeemBtn = document.getElementById('redeemGiftBtn');

    if (openBtn && modal2) {
        openBtn.addEventListener('click', () => {
            console.log("모달 열기 버튼 클릭됨");
            modal2.classList.add('active');
            document.body.style.overflow = 'hidden';
        });
    }

    if (checkbox && redeemBtn) {
        checkbox.addEventListener('change', () => {
            redeemBtn.disabled = !checkbox.checked;
        });
    }

    if (redeemBtn && modal2) {
        redeemBtn.addEventListener('click', () => {
            const gifticonForm = document.getElementById('gifticonForm');
            const phone = document.getElementById('phoneInput')?.value;

            if (!phone) {
                alert('전화번호를 입력해주세요.');
                return;
            }

            const phoneInputHidden = document.createElement('input');
            phoneInputHidden.type = 'hidden';
            phoneInputHidden.name = 'phone';
            phoneInputHidden.value = phone;
            gifticonForm.appendChild(phoneInputHidden);

            modal2.classList.remove('active');
            document.body.style.overflow = '';
            gifticonForm.submit();
        });
    }
});