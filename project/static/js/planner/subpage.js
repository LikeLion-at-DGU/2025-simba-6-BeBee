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
    // ✅ 안정적인 방식으로 userId 가져오기
    const userId = document.querySelector(".login-user-info").dataset.userId;
    const pathParts = window.location.pathname.split("/");
    const selectedDate = pathParts[4];

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
                        location.reload();
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

    // ✅ 타이머 기능
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
            const url = isStart ? "start" : "stop";

            fetch(`/planner/${url}/${userId}/${todoId}/${selectedDate}/`)
                .then(res => res.json())
                .then(() => {
                    button.textContent = isStart ? "STOP" : "START";
                    isStart ? startTimer() : stopTimer();
                })
                .catch(err => console.error(`${url.toUpperCase()} 오류:`, err));
        });
    });


    // ✅ 할일 상태 토글 + 꿀 업데이트 + 시각 효과
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
            return res.json();  // ✅ JSON 응답 파싱
        })
        .then(data => {
            // ✅ 꿀 수치 업데이트
            const honeyElement = document.getElementById("honey-count");
            if (honeyElement && data.honey_count !== undefined) {
                honeyElement.textContent = `${data.honey_count}g`;
            }

            // ✅ 리스트 항목 시각 업데이트 및 재정렬
            const listItem = checkbox.closest("li.todo-item");
            const ul = document.getElementById("todo-list");

            if (data.status === "completed") {
                listItem.classList.add("completed");   // 흐림 효과
                ul.appendChild(listItem);              // 맨 아래로 이동
            } else {
                listItem.classList.remove("completed"); // 흐림 제거
                ul.prepend(listItem);                  // 맨 위로 복귀 (선택)
            }
        })
        .catch(err => console.error("Toggle error:", err));
    });
});


    // ✅ 요일 버튼 클릭 시 이동
    document.querySelectorAll(".hexagon-inner").forEach((button) => {
        button.addEventListener("click", function () {
            const dayMap = {
                'SUN': 0, 'MON': 1, 'TUE': 2,
                'WED': 3, 'THU': 4, 'FRI': 5, 'SAT': 6,
            };

            const targetDay = dayMap[this.dataset.day];
            const [year, month, day] = selectedDate.split("-").map(Number);
            const baseDate = new Date(year, month - 1, day);
            const baseDay = baseDate.getDay();
            const diff = targetDay - baseDay;
            baseDate.setDate(baseDate.getDate() + diff);

            const formatted = baseDate.toISOString().split("T")[0];
            window.location.href = `/planner/subpage/${userId}/${formatted}/`;
        });
    });
});

