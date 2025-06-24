const calendarDates = document.getElementById("calendarDates");
const currentMonthElement = document.getElementById("currentMonth");
const currentYearElement = document.getElementById("currentYear");
const prevBtn = document.getElementById("prevBtn");
const nextBtn = document.getElementById("nextBtn");
const successRates = JSON.parse(document.getElementById("success-rates-data").textContent);

const today = new Date();
let currentMonth = today.getMonth();
let currentYear = today.getFullYear();

const userId = document.body.dataset.userid;

function renderCalendar() {
  const firstDayOfMonth = new Date(currentYear, currentMonth, 1);
  const daysInMonth = new Date(currentYear, currentMonth + 1, 0).getDate();
  const startDayOfWeek = firstDayOfMonth.getDay();

  // 월 표시 (영문 → 한글 월명 원한다면 변환 가능)
  const monthName = new Intl.DateTimeFormat('en-US', { month: 'short' }).format(
    new Date(currentYear, currentMonth)
  );
  currentMonthElement.textContent = monthName.toUpperCase();
  currentYearElement.textContent = `${currentYear}`;

  calendarDates.innerHTML = "";

  // 빈 칸 생성
  for (let i = 0; i < startDayOfWeek; i++) {
    const emptyDate = document.createElement("div");
    emptyDate.classList.add("date", "empty");
    calendarDates.appendChild(emptyDate);
  }

  // 날짜 생성 및 배경색 적용
  for (let i = 1; i <= daysInMonth; i++) {
    const dateElement = document.createElement("div");
    dateElement.classList.add("date");
    dateElement.textContent = i;

    // 날짜 문자열 (YYYY-MM-DD)
    const monthStr = String(currentMonth + 1).padStart(2, '0');
    const dayStr = String(i).padStart(2, '0');
    const dateStr = `${currentYear}-${monthStr}-${dayStr}`;

    // 성공률 조회
    const match = successRates.find(item => item.date === dateStr);
    if (match) {
      const rate = match.success_rate;

      // 성공률 기반 배경색 지정
      if (rate > 66 && rate <= 100) {
        dateElement.style.backgroundColor = "#FFCE8E"; // 높은 성공률
      } else if (rate > 33 && rate <= 66) {
        dateElement.style.backgroundColor = "#FFE0C2";
      } else if (rate > 0 && rate <= 33) {
        dateElement.style.backgroundColor = "#FFEF96";
      }
      // 성공률 0% 또는 데이터 없음: 기본색 유지 (#FFFDC2)
    }

    // 클릭 시 해당 날짜의 subpage로 이동
    dateElement.addEventListener("click", () => {
      window.location.href = `/planner/subpage/${userId}/${dateStr}/`;
    });

    calendarDates.appendChild(dateElement);
  }
}


renderCalendar();

prevBtn.addEventListener("click", () => {
  currentMonth--;
  if (currentMonth < 0) {
    currentMonth = 11;
    currentYear--;
  }
  renderCalendar();
});

nextBtn.addEventListener("click", () => {
  currentMonth++;
  if (currentMonth > 11) {
    currentMonth = 0;
    currentYear++;
  }
  renderCalendar();
});

console.log("✅ successRates", successRates);