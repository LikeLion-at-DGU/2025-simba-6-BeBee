/* 전역 상태 저장용 */
const timerIntervals = {};   // todoId → setInterval ID
const timerSeconds   = {};   // todoId → 누적 초

/* 공통 유틸 ───────────────────────────── */
function formatTime(sec) {
  const h = String(Math.floor(sec / 3600)).padStart(2, "0");
  const m = String(Math.floor((sec % 3600) / 60)).padStart(2, "0");
  const s = String(sec % 60).padStart(2, "0");
  return `${h}시간 ${m}분 ${s}초`;
}

function getCookie(name) {
  let v = null;
  if (document.cookie && document.cookie !== "") {
    for (let c of document.cookie.split(";")) {
      c = c.trim();
      if (c.startsWith(name + "=")) {
        v = decodeURIComponent(c.slice(name.length + 1));
        break;
      }
    }
  }
  return v;
}

/* DOMContentLoaded ──────────────────── */
document.addEventListener("DOMContentLoaded", () => {
  /* URL 파츠 추출 */
  const userId       = document.body.dataset.userid;
  const pathParts    = window.location.pathname.split("/");
  const selectedDate = pathParts[4];               // "YYYY-MM-DD"

  /* 오늘 여부 판정 */
  const isToday = () => {
    const t = new Date();
    return (
      `${t.getFullYear()}-${String(t.getMonth() + 1).padStart(2, "0")}-${String(
        t.getDate()
      ).padStart(2, "0")}` === selectedDate
    );
  };

  /* ========== 1. 할일 생성 (AJAX) ========== */
  const todoForm = document.querySelector(".todo-form-inline");
  if (todoForm) {
    todoForm.addEventListener("submit", (e) => {
      e.preventDefault();

      const category = document.getElementById("todo-category").value;
      const deadline = document.getElementById("todo-deadline").value;
      const content  = document.getElementById("todo-input").value;

      fetch(`/planner/create/${userId}/${selectedDate}/`, {
        method : "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
          "X-CSRFToken" : getCookie("csrftoken"),
        },
        body:
          `category=${encodeURIComponent(category)}` +
          `&deadline=${encodeURIComponent(deadline)}` +
          `&content=${encodeURIComponent(content)}`,
      })
        .then((res) => {
          /* Django에서 redirect(302) 가 오더라도 OK → 그냥 새로고침 */
          if (res.ok) {
            location.reload();
          } else {
            return res.text().then((txt) => {
              console.error("할일 등록 실패:", txt);
              alert("할일 등록 실패!");
            });
          }
        })
        .catch((err) => console.error("할일 등록 중 오류:", err));
    });
  }

  /* ========== 2. 오른쪽 패널 토글 ========== */
  const timerBtn = document.getElementById("show-timer-btn");
  const buddyBtn = document.getElementById("show-buddy-btn");
  if (timerBtn && buddyBtn) {
    timerBtn.addEventListener("click", () => {
      document
        .querySelectorAll(".right-box2")
        .forEach((b) => (b.style.display = "block"));
      document.getElementById("buddy-box").style.display = "none";
    });
    buddyBtn.addEventListener("click", () => {
      document
        .querySelectorAll(".right-box2")
        .forEach((b) => (b.style.display = "none"));
      document.getElementById("buddy-box").style.display = "flex";
    });
  }

  /* ========== 3. 개별 타이머 박스 토글 ========== */
  document.querySelectorAll(".show-timer-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      const todoId = btn.dataset.todoId;
      document
        .querySelectorAll(".right-box2")
        .forEach((b) => (b.style.display = "none"));
      const box = document.getElementById(`timer-box-${todoId}`);
      if (box) {
        box.style.display = "block";
        document.getElementById("buddy-box").style.display = "none";
      }
    });
  });

  /* ========== 4. 타이머 START/STOP ========== */
  const startTimer = (id, disp) => {
    timerIntervals[id] = setInterval(() => {
      timerSeconds[id] += 1;
      disp.textContent = formatTime(timerSeconds[id]);
    }, 1000);
  };
  const stopTimer = (id) => clearInterval(timerIntervals[id]);

  document.querySelectorAll(".start-btn").forEach((btn) => {
    const todoId  = btn.dataset.todoId;
    const display = document.getElementById(`timer-display-${todoId}`);

    timerSeconds[todoId] = parseInt(
      display.dataset.elapsedSeconds || "0",
      10
    );
    display.textContent = formatTime(timerSeconds[todoId]);

    if (btn.dataset.started === "true") {
      btn.textContent = "STOP";
      startTimer(todoId, display);
    }

    btn.addEventListener("click", () => {
      const isStart = btn.textContent.trim() === "START";
      const url     = isStart ? "start" : "stop";

      fetch(`/planner/${url}/${userId}/${todoId}/${selectedDate}/`)
        .then((r) => r.json())
        .then((d) => {
          btn.textContent = isStart ? "STOP" : "START";
          if (isStart) {
            startTimer(todoId, display);
          } else {
            stopTimer(todoId);
            if (d.total_seconds !== undefined) {
              timerSeconds[todoId] = parseInt(d.total_seconds, 10);
              display.textContent   = formatTime(timerSeconds[todoId]);
            }

            /* 공부시간 div 갱신/생성 */
            const studyDiv = document.getElementById(`study-time-${todoId}`);
            if (studyDiv) {
              studyDiv.textContent = `공부 시간: ${d.total_elapsed}`;
            } else {
              const todoItem = document
                .querySelector(
                  `li.todo-item button[data-todo-id="${todoId}"]`
                )
                ?.closest("li.todo-item");
              const bottomRow = todoItem?.querySelector(".todo-bottom-row");
              if (bottomRow) {
                const newDiv = document.createElement("div");
                newDiv.id = `study-time-${todoId}`;
                newDiv.className = "todo-studytime";
                newDiv.textContent = `공부 시간: ${d.total_elapsed}`;
                bottomRow.insertBefore(
                  newDiv,
                  bottomRow.querySelector(".todo-deadline").nextSibling
                );
              }
            }
          }
        })
        .catch((err) => console.error(`${url.toUpperCase()} 오류:`, err));
    });
  });

  /* ========== 5. 상태 토글 + 꿀 / UI 갱신 ========== */
  document.querySelectorAll(".todo-status-toggle").forEach((cb) => {
    cb.addEventListener("change", () => {
      if (!isToday()) {
        alert("오늘의 할 일만 체크할 수 있습니다!");
        cb.checked = !cb.checked; // 이전 상태로 복구
        return;
      }

      const todoId = cb.dataset.todoId;
      fetch(`/planner/toggle/${userId}/${todoId}/`, {
        method : "POST",
        headers: { "X-CSRFToken": getCookie("csrftoken") },
      })
        .then((r) => {
          if (!r.ok) throw new Error("상태 변경 실패");
          return r.json();
        })
        .then((d) => {
          /* 꿀 수치 */
          const hEl = document.getElementById("honey-count");
          if (hEl && d.honey_count !== undefined)
            hEl.textContent = `${d.honey_count}g`;

          /* 프로그레스 바 */
          const prog  = document.querySelector("progress");
          const label = document.querySelector(".honey-label");
          if (prog && label && d.daily_earned !== undefined) {
            prog.value = d.daily_earned;
            label.textContent = `${d.daily_earned} / 50g`;
          }

          /* 리스트 항목 효과 / 정렬 */
          const li = cb.closest("li.todo-item");
          const ul = document.getElementById("todo-list");
          if (d.status === "completed") {
            li.classList.add("completed");
            ul.appendChild(li);
          } else {
            li.classList.remove("completed");
            ul.prepend(li);
          }
        })
        .catch((err) => console.error("Toggle error:", err));
    });
  });

  /* ========== 6. 요일 버튼 이동 ========== */
  document.querySelectorAll(".hexagon-inner").forEach((b) => {
    b.addEventListener("click", () => {
      const dayMap = { MON: 1, TUE: 2, WED: 3, THU: 4, FRI: 5, SAT: 6, SUN: 7 };
      const target = dayMap[b.dataset.day];

      const [y, m, d] = selectedDate.split("-").map(Number);
      const fixedDate = new Date(y, m - 1, d);
      const baseDay   = fixedDate.getDay();          // 0(일) ~ 6(토)
      const diffToMon = (baseDay + 6) % 7 * -1;
      const monday    = new Date(fixedDate);
      monday.setDate(fixedDate.getDate() + diffToMon);

      const tgt = new Date(monday);
      tgt.setDate(monday.getDate() + target);

      const nextDate = tgt.toISOString().split("T")[0];
      window.location.href = `/planner/subpage/${userId}/${nextDate}/`;
    });
  });
});

/* ========== 7. 좋아요 AJAX ========== */
const likeForm = document.querySelector(".box1-right form");
if (likeForm) {
  const btn   = likeForm.querySelector(".heart-icon");
  const span  = likeForm.querySelector(".heart-label span");
  const csrf  = getCookie("csrftoken");

  likeForm.addEventListener("submit", (e) => {
    e.preventDefault();
    fetch(likeForm.action, {
      method : "POST",
      headers: { "X-CSRFToken": csrf, Accept: "application/json" },
    })
      .then((r) => r.json())
      .then((d) => {
        btn.innerText  = d.liked ? "❤️" : "🤍";
        span.innerText = d.like_count;
      })
      .catch((err) => console.error("좋아요 오류:", err));
  });
}
