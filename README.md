# 🎵 VOCALOID 생일송 검색기

생일 날짜를 입력하면 해당 날짜에 업로드된 VOCALOID 곡들을 찾아주는 웹사이트입니다!

## ✨ 특징

- 📅 **생일별 검색**: 원하는 날짜를 선택하면 해당 날짜에 업로드된 VOCALOID 곡들을 보여줍니다
- 🔄 **자동 데이터 업데이트**: GitHub Actions가 매일 자동으로 최신 데이터를 수집합니다
- 🚀 **빠른 로딩**: CORS 문제 없이 미리 수집된 데이터를 사용해 빠르게 로딩됩니다
- 📱 **반응형 디자인**: 모바일과 데스크톱에서 모두 사용 가능합니다

## 🛠️ 기술 스택

- **Frontend**: HTML, CSS, JavaScript (바닐라)
- **Backend**: GitHub Actions + Python
- **API**: 니코니코 동화 스냅샷 API
- **배포**: GitHub Pages

## 📁 프로젝트 구조

```
VOCALOID-Birthday-Song/
├── .github/
│   └── workflows/
│       └── collect-data.yml          # 자동 데이터 수집 워크플로우
├── data/
│   └── vocaloid_birthday_songs.json  # 수집된 VOCALOID 데이터
├── collect_vocaloid_data.py          # 데이터 수집 Python 스크립트
├── index.html                        # 메인 웹페이지
└── README.md                         # 프로젝트 설명서
```

## 🚀 사용 방법

### 온라인에서 사용
1. [GitHub Pages 링크](https://monoletP.github.io/VOCALOID-Birthday-Song/)에 접속
2. 생일 날짜를 선택
3. "🔍 검색하기" 버튼 클릭
4. 해당 날짜의 VOCALOID 곡들 확인!

### 로컬에서 실행
```bash
# 저장소 클론
git clone https://github.com/monoletP/VOCALOID-Birthday-Song.git
cd VOCALOID-Birthday-Song

# 로컬 서버 실행
python -m http.server 8000

# 브라우저에서 http://localhost:8000 접속
```

## 🔄 데이터 수집 방식

1. **GitHub Actions 스케줄**: 매일 한국시간 오전 6시에 자동 실행
2. **Python 스크립트**: 니코니코 동화 API에서 VOCALOID 태그가 달린 곡들 수집
3. **JSON 저장**: 수집된 데이터를 `data/vocaloid_birthday_songs.json`에 저장
4. **Git 커밋**: 새로운 데이터를 자동으로 저장소에 커밋

## 🎯 수집 기준

- **태그**: "VOCALOID" 태그가 정확히 포함된 곡
- **제외**: "歌ってみた" (커버곡) 태그가 있는 곡 제외
- **정렬**: 조회수 순으로 정렬
- **기간**: 2007년부터 현재까지 모든 연도

## 📊 데이터 형식

```json
{
  "metadata": {
    "collected_at": "수집 시간",
    "total_days": "총 날짜 수",
    "total_songs": "총 곡 수"
  },
  "data": {
    "MM-DD": [
      {
        "contentId": "동영상 ID",
        "title": "곡 제목",
        "startTime": "업로드 시간",
        "thumbnailUrl": "썸네일 URL",
        "viewCounter": "조회수",
        "lengthSeconds": "재생시간(초)"
      }
    ]
  }
}
```

## 🤝 기여하기

1. 이 저장소를 Fork합니다
2. 새 기능 브랜치를 생성합니다 (`git checkout -b feature/새기능`)
3. 변경사항을 커밋합니다 (`git commit -am '새 기능 추가'`)
4. 브랜치에 Push합니다 (`git push origin feature/새기능`)
5. Pull Request를 생성합니다

## 📜 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 🙏 감사의 말

- [니코니코 동화](https://nicovideo.jp)의 스냅샷 API 제공
- VOCALOID 문화에 기여하는 모든 크리에이터들

---

💝 **생일축하 메시지와 함께 특별한 VOCALOID 곡을 찾아보세요!**