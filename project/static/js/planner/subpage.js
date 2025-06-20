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

document.addEventListener("DOMContentLoaded", () => {
    const display = document.getElementById("timer-display");
    const button = document.getElementById("timer-button");
    let timer = null;
    let seconds = 0;

    function formatTime(s) {
        const hrs = String(Math.floor(s / 3600)).padStart(2, "0");
        const mins = String(Math.floor((s % 3600) / 60)).padStart(2, "0");
        const secs = String(s % 60).padStart(2, "0");
        return `${hrs} : ${mins} : ${secs}`;
    }

    button.addEventListener("click", () => {
        const todoId = button.dataset.todoId;

        if (button.textContent === "START") {
            // 서버에 시작 요청
            fetch(`/start-timer/${todoId}/`)
                .then(() => {
                    button.textContent = "STOP";
                    timer = setInterval(() => {
                        seconds++;
                        display.textContent = formatTime(seconds);
                    }, 1000);
                });
        } else {
            // 서버에 종료 요청
            fetch(`/stop-timer/${todoId}/`)
                .then(() => {
                    clearInterval(timer);
                    button.textContent = "START";
                    seconds = 0;
                    display.textContent = "00 : 00 : 00";
                });
        }
    });
});
