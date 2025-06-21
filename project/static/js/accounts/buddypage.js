document.addEventListener("DOMContentLoaded", function () {
    const searchBox = document.querySelector(".search-box");
    const input = searchBox.querySelector("input");
    const button = searchBox.querySelector("button");
    const profileBox = document.getElementById("friend-profile");

    button.addEventListener("click", handleSearch);
    input.addEventListener("keydown", function (e) {
        if (e.key === "Enter") {
            handleSearch();
        }
    });

    function handleSearch() {
        const query = input.value.trim();
        if (!query) {
            resetProfile("친구의 프로필에 방문하여 방명록을 작성해 보세요~");
            return;
        }

        fetch(`/accounts/api/friend_profile/?q=${encodeURIComponent(query)}`)
            .then((response) => response.json())
            .then((data) => {
                if (data.exists) {
                    renderFriendProfile(data);
                } else {
                    resetProfile("일치하는 친구가 없습니다. 다시 검색해 주세요.");
                }
            })
            .catch(() => {
                resetProfile("검색 중 오류가 발생했습니다.");
            });
    }

    function resetProfile(message) {
        profileBox.innerHTML = `
        <div style="
            border: 2px dotted #ccc;
            border-radius: 30px;
            width: 100%;
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: locus_sangsang;
            font-size: 20px;
            color: #6e5a5a;">
            ${message}
        </div>`;
    }

    function renderFriendProfile(data) {
        profileBox.innerHTML = `
        <div class="friend-top">
            <div class="profile-border">
                ${data.profile_image_url ? `<img src="${data.profile_image_url}" class="profile-img">` : '<div class="bee-text">🐝</div>'}
            </div>
            <div class="friend-info">
                <div class="friend-nickname">${data.username}</div>
                <div class="cheer-msg">오늘 하루도 화이팅!</div>
            </div>
            <button class="follow-button" data-user-id="${data.id}">
                ${data.is_following ? '언팔로우' : '팔로우'}
            </button>
        </div>
        <div class="friend-honey">
            <img src="/static/assets/images/mainpage_honeypot_img.png" class="honeypot-icon">
            <div class="honey-amount">
                <div style="font-size: 25px;">현재 버디의 꿀</div>
                <div class="honey-value">${data.honey}g</div>
            </div>
        </div>
        <button class="calendar-button">Buddy's Calendar</button>`;

        const followBtn = profileBox.querySelector(".follow-button");
        followBtn.addEventListener("click", () => {
            const userId = followBtn.dataset.userId;
            fetch(`/accounts/follow/${userId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCSRFToken(),
                },
            })
            .then(res => {
                if (res.ok) {
                    handleSearch(); // 프로필 갱신
                }
            });
        });
    }

    function getCSRFToken() {
        const name = 'csrftoken';
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                return decodeURIComponent(cookie.substring(name.length + 1));
            }
        }
        return '';
    }
});

