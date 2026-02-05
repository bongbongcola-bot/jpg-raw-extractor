# JPG & RAW Extractor 🎬

카메라에서 촬영한 JPG + RAW 파일을 효율적으로 관리하는 도구입니다.

## 기능

- 📁 JPG와 RAW 파일을 동일한 이름으로 자동 매칭
- 📋 선택한 JPG에 해당하는 RAW 파일만 복사
- ⚡ 대량 파일 처리 가능
- 📊 실시간 진행률 표시
- 🔄 초기화 버튼으로 선택 리셋

## 지원하는 RAW 형식

- `.raw`, `.arw` (Sony)
- `.CR2`, `.CR3` (Canon)
- `.nef`, `.nrw` (Nikon)
- `.raf` (Fujifilm)
- `.rw2` (Panasonic)
- `.orf` (Olympus)
- `.dng` (DNG)

## 설치 및 사용

### macOS
1. [최신 Release](https://github.com/bongbongcola-bot/jpg-raw-extractor/releases)에서 `jpg-raw-extractor-macos.zip` 다운로드
2. 압축 해제 후 `jpg-raw-extractor.app` 실행

### Windows
1. [최신 Release](https://github.com/bongbongcola-bot/jpg-raw-extractor/releases)에서 `jpg-raw-extractor-windows.zip` 다운로드
2. 압축 해제 후 `jpg-raw-extractor.exe` 실행

## 사용 방법

1. **JPG 폴더 선택** - JPG 파일이 있는 폴더 선택
2. **RAW 폴더 선택** - RAW 파일이 있는 폴더 선택
3. **복사 대상 폴더 선택** - RAW 파일을 복사할 폴더 선택
4. **복사 시작** 버튼 클릭
5. 진행률을 확인하며 대기

## 개발

### 필요한 환경
- Python 3.11+
- pip

### 설치

```bash
git clone https://github.com/bongbongcola-bot/jpg-raw-extractor.git
cd jpg-raw-extractor
pip install -r requirements.txt
```

### 실행

```bash
python src/main.py
```

### 빌드

```bash
# Windows
pyinstaller pyinstaller.spec

# macOS
pyinstaller pyinstaller.spec
```

## 자동 빌드 및 배포

Git 태그를 추가하면 GitHub Actions가 자동으로 빌드하고 Release를 생성합니다.

```bash
git tag v1.0.0
git push origin v1.0.0
```

## 라이선스

MIT License

## 작성자

- bongbongcola-bot

---

문제가 있으면 [Issues](https://github.com/bongbongcola-bot/jpg-raw-extractor/issues)에서 보고해주세요.
