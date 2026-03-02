# v2.0.0 — PyQt6 Migration Release

## What's New

### 🎉 Major: PyQt6 전면 마이그레이션
기존 `customtkinter` 기반에서 **PyQt6** 기반으로 완전히 재작성되었습니다.

### ✨ 변경 사항

#### UI / 창 렌더링
- **진짜 투명 모서리** — `FramelessWindowHint` + `WA_TranslucentBackground` 적용으로 macOS에서 완벽한 라운드 처리
- `customtkinter`의 한계(모서리에 직각 테두리 잔재)를 근본적으로 해결
- 드롭존 hover 시 파란 대시 테두리 애니메이션 추가

#### 드래그 앤 드롭
- `tkinterdnd2` 의존성 제거 → Qt 네이티브 drag & drop 이벤트로 교체
- 공백 포함 경로, 다중 파일 드롭 등 엣지케이스 처리 개선

#### 창 드래그
- 기존 `event.x/y` 상대좌표 → `globalPosition()` 절대좌표로 수정
- 위젯마다 좌표 기준이 달라 창이 튀던 버그 수정

#### 기타
- 변환 성공 팝업 제거 — 하단 상태바(`Done: filename.csv`)로 대체
- 의존성 간소화: `customtkinter`, `tkinterdnd2` 제거

---

## Dependencies

```
PyQt6>=6.10
pandas>=1.2
pyreadstat>=1.2
```

---

## Breaking Changes

- `customtkinter` / `tkinterdnd2` 미사용 → 제거해도 무방
- Python 3.9+ 필요 (PyQt6 요구사항)
