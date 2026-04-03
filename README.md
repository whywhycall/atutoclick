# Galaxy A15 ADB Auto Clicker

갤럭시 A15를 ADB(Android Debug Bridge)로 제어하는 간단한 자동 클릭 GUI 앱입니다.

## 기능
- ADB 기기 연결 확인
- 특정 좌표 1회 터치
- 반복 자동 터치
- 테스트 스와이프
- 앱 패키지명으로 앱 실행
- 프리셋 저장 / 불러오기

## 준비물
- Windows PC
- Python 3.x
- Android ADB 설치
- Galaxy A15
- USB 디버깅 활성화

## 사용 전 설정

### 1. 개발자 옵션 활성화
갤럭시 A15에서:
- 설정 → 휴대전화 정보 → 소프트웨어 정보
- 빌드 번호 7번 터치

### 2. USB 디버깅 활성화
- 설정 → 개발자 옵션 → USB 디버깅 ON

### 3. ADB 연결 확인
PC에서:

```bash
adb devices
```

정상 연결되면:
```bash
List of devices attached
R58XXXXXXXX    device
```

## 실행 방법

```bash
python main.py
```

## 좌표 확인 방법
갤럭시 A15에서:
- 설정 → 개발자 옵션 → 포인터 위치 ON

화면 상단에 터치 좌표(X/Y)가 표시됩니다.

## 예시
- X = 532
- Y = 1478

이 값을 앱에 입력하면 해당 위치를 자동 터치합니다.

## 확장 가능
- 여러 좌표 순차 클릭
- 매크로 시퀀스 저장
- 랜덤 간격
- 이미지 기반 버튼 탐색
- EXE 빌드
