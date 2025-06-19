/* login page - JS */
document.addEventListener("DOMContentLoaded", function () {
    const idInput = document.getElementById("username");  // 닉네임 입력창
    const pwInput = document.getElementById("password");  // 비밀번호 입력창
    const loginBtn = document.getElementById("login-btn");  // 로그인 버튼

    function validateLoginForm() {
        const idFilled = idInput.value.trim() !== "";
        const pwFilled = pwInput.value !== "";

        // 둘 다 입력되었을 때만 버튼 활성화
        const isValid = idFilled && pwFilled;
        loginBtn.disabled = !isValid;
    }

    // 입력될 때마다 검사
    idInput.addEventListener("input", validateLoginForm);
    pwInput.addEventListener("input", validateLoginForm);
});

console.log("Login page JS loaded");
