document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("todo-form");
    const categoryInput = document.getElementById("todo-category");
    const deadlineInput = document.getElementById("todo-deadline");
    const contentInput = document.getElementById("todo-input");

    form.addEventListener("submit", function (e) {
        e.preventDefault();

        const category = categoryInput.value;
        const deadline = deadlineInput.value;
        const content = contentInput.value;

        const urlParts = window.location.pathname.split("/");
        const userId = urlParts[3];
        const selectedDate = urlParts[4];

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
});

// 타이머 숫자를 hh:mm:ss 형식으로 변환하는 함수
function formatTime(seconds) {
    const h = String(Math.floor(seconds / 3600)).padStart(2, '0');
    const m = String(Math.floor((seconds % 3600) / 60)).padStart(2, '0');
    const s = String(seconds % 60).padStart(2, '0');
    return `${h} : ${m} : ${s}`;
}


document.addEventListener("DOMContentLoaded", () => {
    const timerBtn = document.getElementById("show-timer-btn");
    const buddyBtn = document.getElementById("show-buddy-btn");

    if (timerBtn && buddyBtn) {
        timerBtn.addEventListener("click", () => {
            // 모든 타이머 박스 보이기
            document.querySelectorAll(".right-box2").forEach(box => box.style.display = "block");
            document.getElementById("buddy-box").style.display = "none";
        });

        buddyBtn.addEventListener("click", () => {
            // 모든 타이머 박스 숨기기
            document.querySelectorAll(".right-box2").forEach(box => box.style.display = "none");
            document.getElementById("buddy-box").style.display = "flex";
        });
    }
});


const timers = {};           // ← 전역에서 사용할 수 있게 선언
const secondsElapsed = {};  // (추가로 쓰고 싶을 경우에 대비)



// 타이머 기능
// 각 할일의 타이머만 보이게 함
document.querySelectorAll(".show-timer-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
        const todoId = btn.dataset.todoId;

        // 모든 타이머 박스를 숨김
        document.querySelectorAll(".right-box2").forEach(box => box.style.display = "none");

        // 해당 타이머만 표시
        const targetBox = document.getElementById(`timer-box-${todoId}`);
        if (targetBox) {
            targetBox.style.display = "block";
            document.getElementById("buddy-box").style.display = "none";
        }
    });
});

// 타이머 시작/중지 로직 및 백엔드와 연동
document.querySelectorAll(".start-btn").forEach(function (button) {
    const todoId = button.dataset.todoId;
    let seconds = 0;

    button.addEventListener("click", function () {
        const display = document.getElementById(`timer-display-${todoId}`); // ✅ 여기서 매번 새로 참조
        const isStart = button.textContent.trim() === "START";

        if (!display) {
            console.warn(`❌ 타이머 표시 요소 없음: timer-display-${todoId}`);
            return;
        }

        if (isStart) {
            console.log("⏱ START fetch 시작");

            fetch(`/planner/start/${todoId}/`)
                .then(() => {
                    console.log("⏱ 타이머 시작!");
                    button.textContent = "STOP";
                    seconds = 0;
                    timers[todoId] = setInterval(() => {
                        seconds++;
                        display.textContent = formatTime(seconds);
                    }, 1000);
                })
                .catch(err => console.error("START 오류:", err));
        } else {
            console.log("🛑 STOP fetch 시작");

            fetch(`/planner/stop/${todoId}/`)
                .then(() => {
                    console.log("🛑 타이머 종료!");
                    clearInterval(timers[todoId]);
                    button.textContent = "START";
                    display.textContent = "00 : 00 : 00";
                    seconds = 0;
                })
                .catch(err => console.error("STOP 오류:", err));
        }
    });
});


// 할일 상태 토글 기능
document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".todo-status-toggle").forEach(checkbox => {
        checkbox.addEventListener("change", () => {
            const userId = checkbox.dataset.userId;
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

// CSRF 토큰 가져오는 함수 (필요한 경우에만 추가)
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
