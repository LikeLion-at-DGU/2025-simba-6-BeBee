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
    const form = document.getElementById("todo-form");  // ✅ 이 줄 꼭 필요
    const taskInput = document.getElementById("todo-input");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        const task = taskInput.value.trim();
        if (!task) return;

        addTaskToDOM(task, 0);  // DB 없이 테스트용
        taskInput.value = "";
    });
});

