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


// 타이머 기능

document.addEventListener("DOMContentLoaded", function () {
    const timers = {};  // 각 todoId별 setInterval ID 저장
    const secondsElapsed = {};  // 각 todoId별 경과 시간 저장

    // 시간 형식 변환 함수
    function formatTime(s) {
        const hrs = String(Math.floor(s / 3600)).padStart(2, "0");
        const mins = String(Math.floor((s % 3600) / 60)).padStart(2, "0");
        const secs = String(s % 60).padStart(2, "0");
        return `${hrs} : ${mins} : ${secs}`;
    }

    // 모든 타이머 버튼에 대해 이벤트 바인딩
    document.querySelectorAll(".start-btn").forEach(function (button) {
        const todoId = button.dataset.todoId;
        const display = document.getElementById(`timer-display-${todoId}`);
        let seconds = 0;

        // 서버에서 started 상태라면 초기부터 타이머 동작
        if (button.dataset.started === "true") {
            button.textContent = "STOP";
            timers[todoId] = setInterval(() => {
                seconds++;
                display.textContent = formatTime(seconds);
            }, 1000);
        }

        // 버튼 클릭 시 START/STOP 동작
        button.addEventListener("click", function () {
            if (button.textContent === "START") {
                fetch(`/start-timer/${todoId}/`)
                    .then(() => {
                        button.textContent = "STOP";
                        seconds = 0;
                        timers[todoId] = setInterval(() => {
                            seconds++;
                            display.textContent = formatTime(seconds);
                        }, 1000);
                    })
                    .catch(error => console.error("Start Timer Error:", error));
            } else {
                fetch(`/stop-timer/${todoId}/`)
                    .then(() => {
                        clearInterval(timers[todoId]);
                        button.textContent = "START";
                        display.textContent = "00 : 00 : 00";
                        seconds = 0;
                    })
                    .catch(error => console.error("Stop Timer Error:", error));
            }
        });
    });
});
