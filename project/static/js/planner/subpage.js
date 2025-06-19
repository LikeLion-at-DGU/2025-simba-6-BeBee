// subpage.js

let timerInterval;
let seconds = 0;

const timerEl = document.getElementById("timer");
const startBtn = document.getElementById("start-timer");

startBtn.addEventListener("click", () => {
    if (timerInterval) clearInterval(timerInterval);
    timerInterval = setInterval(() => {
        seconds++;
        const hrs = String(Math.floor(seconds / 3600)).padStart(2, '0');
        const mins = String(Math.floor((seconds % 3600) / 60)).padStart(2, '0');
        const secs = String(seconds % 60).padStart(2, '0');
        timerEl.textContent = `${hrs}:${mins}:${secs}`;
    }, 1000);
});

const taskInput = document.getElementById("task-input");
const taskList = document.getElementById("task-list");
const addTaskBtn = document.getElementById("add-task");

addTaskBtn.addEventListener("click", () => {
    const text = taskInput.value.trim();
    if (!text) return;

    const taskEl = document.createElement("div");
    taskEl.className = "task-item";
    taskEl.innerHTML = `<span>${text}</span> <button class="complete-btn">⬢</button>`;

    taskEl.querySelector(".complete-btn").addEventListener("click", () => {
        taskEl.classList.toggle("done");
    });

    taskList.appendChild(taskEl);
    taskInput.value = "";
});

// 요일 강조
const days = document.querySelectorAll(".day");
const today = new Date().getDay();
const dayMap = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"];
days.forEach(day => {
    if (day.dataset.day === dayMap[today]) {
        day.classList.add("active");
    }
});
