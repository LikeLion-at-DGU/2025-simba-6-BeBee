// 할일을 DOM에 추가하는 함수
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

// 타이머 숫자를 hh:mm:ss 형식으로 변환하는 함수
function formatTime(seconds) {
    const h = String(Math.floor(seconds / 3600)).padStart(2, '0');
    const m = String(Math.floor((seconds % 3600) / 60)).padStart(2, '0');
    const s = String(seconds % 60).padStart(2, '0');
    return `${h} : ${m} : ${s}`;
}


// // 아이콘 클릭 시 타이머 박스 또는 버디 박스를 표시하는 기능
// document.addEventListener("DOMContentLoaded", () => {
//     const form = document.getElementById("todo-form");
//     const timerBox = document.getElementById("timer-box");
//     const buddyBox = document.getElementById("buddy-box");
//     const timerBtn = document.getElementById("show-timer-btn");
//     const buddyBtn = document.getElementById("show-buddy-btn");

//     if (timerBtn && buddyBtn && timerBox && buddyBox) {
//         timerBtn.addEventListener("click", () => {
//             timerBox.style.display = "block";
//             buddyBox.style.display = "none";
//         });

//         buddyBtn.addEventListener("click", () => {
//             timerBox.style.display = "none";
//             buddyBox.style.display = "block";
//         });
//     } else {
//         console.warn("아이콘 또는 박스 요소를 찾을 수 없습니다.");
//     }
// });

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


document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("buddy-form");
    const input = document.querySelector(".goal-input");
    const messageList = document.querySelector(".buddy-messages");

    form.addEventListener("submit", (event) => {
        event.preventDefault();  // ✅ form의 기본 제출 동작 막기

        const text = input.value.trim();
        if (text) {
            const li = document.createElement("li");
            li.classList.add("buddy-message-item");

            const span = document.createElement("span");
            span.textContent = text;

            const deleteBtn = document.createElement("button");
            deleteBtn.innerHTML = '<i class="fas fa-trash"></i>';
            deleteBtn.classList.add("buddy-delete-btn");
            deleteBtn.addEventListener("click", () => li.remove());

            li.appendChild(span);
            li.appendChild(deleteBtn);
            messageList.appendChild(li);

            input.value = "";
        }
    });
});
