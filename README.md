# 2025-simba-6-BeBee

★2025 심바톤 6조 깃허브 레포지토리입니다★

---

## 📌 Repository 구조

- **Upstream Repository**: 팀 공식 저장소 (PR을 보내는 대상)
  - 🔗 https://github.com/LikeLion-at-DGU/2025-simba-6-BeBee
- **Origin Repository**: 개인 GitHub 계정에서 fork한 복사본 (작업용)

---

## 🔧 협업 시작 절차

1. Upstream Repository를 자신의 GitHub 계정으로 `Fork`
2. Fork한 Origin Repository를 로컬에 `Clone`
3. 기능 개발 후 변경사항을 Origin Repository로 `Push`
4. 작업 완료 시 Upstream Repository로 `Pull Request` 전송
5. PR이 머지되면, 내 로컬에서 Upstream Repository의 최신 변경사항을 `Pull`

---

## 🔨 기능 개발 절차 (기능 브랜치 기준)

### 1️⃣ Issue 생성

- Upstream Repository에서 기능 단위 Issue 생성

---

### 2️⃣ 기능 브랜치 생성 (develop 기준)

| 명령어                                     | 설명                                     |
| ------------------------------------------ | ---------------------------------------- |
| `git fetch upstream`                       | upstream의 최신 상태 가져오기 (적용 X)   |
| `git checkout develop`                     | 로컬 develop 브랜치로 이동 (없으면 생성) |
| `git rebase upstream/develop`              | upstream 기준으로 develop 최신화         |
| `git checkout -b feature/#이슈번호-작업명` | 최신 develop 기준으로 기능 브랜치 생성   |

---

### 3️⃣ 기능 개발 & 커밋

| 명령어                                        | 설명                 |
| --------------------------------------------- | -------------------- |
| `git add .`                                   | 수정된 파일 스테이징 |
| `git commit -m "feat: 기능 설명 (#이슈번호)"` | 커밋 메시지 작성     |

---

### 4️⃣ Push 전 최신 develop 기준으로 rebase

| 명령어                        | 설명                               |
| ----------------------------- | ---------------------------------- |
| `git fetch upstream`          | 최신 upstream 상태 다시 가져오기   |
| `git rebase upstream/develop` | 내 브랜치를 최신 develop 위로 정렬 |

---

### 5️⃣ origin에 Push

| 명령어                                             | 설명                                |
| -------------------------------------------------- | ----------------------------------- |
| `git push origin feature/#이슈번호-작업명 --force` | rebase 했기 때문에 `--force`로 푸시 |

---

## 🔁 PR 생성 및 머지 후 로컬 최신화

### 1️⃣ GitHub에서 Pull Request(PR) 생성

| 항목    | 의미                           | 설정 값                               |
| ------- | ------------------------------ | ------------------------------------- |
| base    | PR이 병합될 브랜치 (목적지)    | `upstream` → `develop`                |
| compare | PR을 보내는 내 브랜치 (출발지) | `origin` → `feature/#이슈번호-작업명` |

> ✅ PR 생성 후, 승인자가 코드 확인 및 머지 진행  
> ✅ Merge 완료 시, `upstream/develop`에 코드 반영

---

### ⚠️ Squash and Merge 권장

- 여러 커밋을 하나로 압축해 merge
- develop 브랜치 커밋 히스토리를 깔끔하게 유지 가능
- 기능 단위로 커밋을 정리할 수 있어 유지보수에 유리

---

### 2️⃣ 로컬 최신화

| 명령어                      | 설명                                |
| --------------------------- | ----------------------------------- |
| `git checkout develop`      | 로컬 develop 브랜치로 이동          |
| `git pull upstream develop` | 최신 upstream develop 코드 가져오기 |

---

### 3️⃣ Origin Repository 최신화

| 명령어                    | 설명                                         |
| ------------------------- | -------------------------------------------- |
| `git push origin develop` | origin develop 브랜치도 최신 상태로 업데이트 |

---

