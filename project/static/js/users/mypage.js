const editBtn = document.querySelector('.edit-button'); // ✏️ 수정 버튼
const modal = document.getElementById('edit-profile-modal');
const closeBtn = document.getElementById('close-modal');
const fileInput = document.getElementById('profile-image-input');

// 모달 열기
editBtn.addEventListener('click', () => {
    modal.classList.remove('hidden');
});

// 모달 닫기 (X 버튼)
closeBtn.addEventListener('click', () => {
    modal.classList.add('hidden');
});

// 이미지 클릭 → 파일 선택
fileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        console.log("선택된 파일:", file.name);
        // 원한다면 여기서 즉시 미리보기 표시도 가능
    }
});