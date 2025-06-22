// ⏱ 시간 포맷 함수
function formatTime(seconds) {
    const h = String(Math.floor(seconds / 3600)).padStart(2, '0');
    const m = String(Math.floor((seconds % 3600) / 60)).padStart(2, '0');
    const s = String(seconds % 60).padStart(2, '0');
    return `${h} : ${m} : ${s}`;
}

// ✅ CSRF 토큰 함수
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.addEventListener("DOMContentLoaded", () => {
    const userId = document.querySelector(".login-user-info").dataset.userId;

    const selectedDate = window.location.pathname.split("/")[4];

    // ✅ 할일 등록 (AJAX)
    const form = document.getElementById("todo-form");
    if (form) {
        form.addEventListener("submit", function (e) {
            e.preventDefault();
            const category = document.getElementById("todo-category").value;
            const deadline = document.getElementById("todo-deadline").value;
            const content = document.getElementById("todo-input").value;

            fetch(`/planner/create/ajax/${userId}/${selectedDate}/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                body: `category=${category}&deadline=${deadline}&content=${content}`
            })
                .then(res => res.json())
                .then(data => {
                    if (data.id) {
                        addTaskToDOM(data.content, data.id);
                        form.reset();
                    } else {
                        alert("할일 등록 실패: " + (data.error || "Unknown error"));
                    }
                })
                .catch(err => console.error("에러 발생:", err));
        });
    }

    // ✅ 타이머/버디 토글 버튼
    const timerBtn = document.getElementById("show-timer-btn");
    const buddyBtn = document.getElementById("show-buddy-btn");

    if (timerBtn && buddyBtn) {
        timerBtn.addEventListener("click", () => {
            document.querySelectorAll(".right-box2").forEach(box => box.style.display = "block");
            document.getElementById("buddy-box").style.display = "none";
        });
        buddyBtn.addEventListener("click", () => {
            document.querySelectorAll(".right-box2").forEach(box => box.style.display = "none");
            document.getElementById("buddy-box").style.display = "flex";
        });
    }

    // ✅ 개별 타이머 박스 토글 버튼
    document.querySelectorAll(".show-timer-btn").forEach((btn) => {
        btn.addEventListener("click", () => {
            const todoId = btn.dataset.todoId;
            document.querySelectorAll(".right-box2").forEach(box => box.style.display = "none");
            const targetBox = document.getElementById(`timer-box-${todoId}`);
            if (targetBox) {
                targetBox.style.display = "block";
                document.getElementById("buddy-box").style.display = "none";
            }
        });
    });

    // ✅ 타이머 기능 연결
    document.querySelectorAll(".start-btn").forEach(function (button) {
        const todoId = button.dataset.todoId;
        const display = document.getElementById(`timer-display-${todoId}`);
        let totalSeconds = parseInt(display.dataset.elapsedSeconds || '0', 10);
        let intervalId = null;

        display.textContent = formatTime(totalSeconds);

        const startTimer = () => {
            intervalId = setInterval(() => {
                totalSeconds += 1;
                display.textContent = formatTime(totalSeconds);
            }, 1000);
        };

        const stopTimer = () => {
            clearInterval(intervalId);
        };

        // ✅ 초기 로딩 시 started인 경우 자동 실행
        if (button.dataset.started === "true") {
            button.textContent = "STOP";
            startTimer();
        }

        button.addEventListener("click", () => {
            const isStart = button.textContent.trim() === "START";
            if (isStart) {
                fetch(`/planner/start/${userId}/${todoId}/${selectedDate}/`)
                    .then(res => res.json())
                    .then(() => {
                        button.textContent = "STOP";
                        startTimer();
                    })
                    .catch(err => console.error("START 오류:", err));
            } else {
                fetch(`/planner/stop/${userId}/${todoId}/${selectedDate}/`)
                    .then(res => res.json())
                    .then(() => {
                        button.textContent = "START";
                        stopTimer();
                    })
                    .catch(err => console.error("STOP 오류:", err));
            }
        });
    });

    // ✅ 할일 상태 토글
    document.querySelectorAll(".todo-status-toggle").forEach(checkbox => {
        checkbox.addEventListener("change", () => {
            const todoId = checkbox.dataset.todoId;

            fetch(`/planner/toggle/${userId}/${todoId}/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCookie("csrftoken")
                },
            })
                .then(res => {
                    if (!res.ok) throw new Error("상태 변경 실패");
                })
                .catch(err => console.error("Toggle error:", err));
        });
    });
});
