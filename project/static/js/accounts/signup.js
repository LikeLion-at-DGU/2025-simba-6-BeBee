document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('form');
    const nicknameInput = document.getElementById('nickname');
    const pwInput = document.getElementById('password');
    const pwConfirmInput = document.getElementById('password-confirm');
    const nicknameCheckBtn = document.querySelector('.icon-button');

    // 🔍 닉네임 중복 확인 버튼 클릭 시
    nicknameCheckBtn.addEventListener('click', async () => {
        const nickname = nicknameInput.value.trim();
        if (!nickname) {
            alert('닉네임을 입력하세요.');
            return;
        }

        try {
            const response = await fetch(`/accounts/check_nickname/?nickname=${nickname}`);
            const data = await response.json();
            if (data.exists) {
                alert('이미 사용 중인 닉네임입니다.');
            } else {
                alert('사용 가능한 닉네임입니다!');
            }
        } catch (err) {
            console.error(err);
            alert('닉네임 확인 중 오류가 발생했습니다.');
        }
    });

    // ✅ 폼 제출 시 검사
    form.addEventListener('submit', function (e) {
        const pw = pwInput.value;
        const pwConfirm = pwConfirmInput.value;

        if (pw.length < 8) {
            alert('비밀번호는 최소 8자 이상이어야 합니다.');
            e.preventDefault();
        }

        if (pw !== pwConfirm) {
            alert('비밀번호가 일치하지 않습니다.');
            e.preventDefault();
        }
    });

});
