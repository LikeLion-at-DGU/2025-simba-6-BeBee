// ✅ 전역 함수
function addTaskToDOM(taskText, taskId) {
    console.log("할일 DOM에 추가:", taskText);
    const taskList = document.getElementById("todo-list");

    const placeholder = document.getElementById("placeholder");
    if (placeholder) {
        placeholder.style.display = "none";
    }

    const li = document.createElement("li");
    li.className = "todo-item";
    li.setAttribute("data-task-id", taskId);

    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";

    const span = document.createElement("span");
    span.textContent = taskText;

    const deleteBtn = document.createElement("button");
    deleteBtn.textContent = "삭제";
    deleteBtn.addEventListener("click", () => li.remove());

    li.appendChild(checkbox);
    li.appendChild(span);
    li.appendChild(deleteBtn);

    taskList.appendChild(li);
}





document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("todo-form");
    const timerBox = document.getElementById("timer-box");
    const buddyBox = document.getElementById("buddy-box");
    const timerBtn = document.getElementById("show-timer-btn");
    const buddyBtn = document.getElementById("show-buddy-btn");

    if (timerBtn && buddyBtn && timerBox && buddyBox) {
        timerBtn.addEventListener("click", () => {
            timerBox.style.display = "block";
            buddyBox.style.display = "none";
        });

        buddyBtn.addEventListener("click", () => {
            timerBox.style.display = "none";
            buddyBox.style.display = "block";
        });
    } else {
        console.warn("아이콘 또는 박스 요소를 찾을 수 없습니다.");
    }
});

const timers = {};           // ← 전역에서 사용할 수 있게 선언
const secondsElapsed = {};  // (추가로 쓰고 싶을 경우에 대비)

// 타이머 기능

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


document.querySelectorAll(".start-btn").forEach(function (button) {
    const todoId = button.dataset.todoId;
    const display = document.getElementById(`timer-display-${todoId}`);
    let seconds = 0;

    button.addEventListener("click", function () {
        const isStart = button.textContent.trim() === "START";

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
