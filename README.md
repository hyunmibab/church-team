# church-team

> 이 저장소는 2026-11-19 기준 보관본입니다. 현재 코드와 유지보수는 비공개 [church-suite의 team 앱](https://github.com/hyunmibab/church-suite/tree/master/apps/team)에서 관리합니다. 기존 코드와 Git 이력은 보존합니다.

CSV 참가자 명단을 업로드해 팀을 배정하고 결과를 수정하는 교회 행사 운영용 웹 도구입니다.

## 주요 기능

- 참가 여부를 기준으로 배정 대상 선택
- 같은 분리그룹에 속한 참가자를 여러 팀에 나누어 배정
- 일반 참가자를 현재 인원이 적은 팀부터 배정
- 팀별 인원과 남녀 인원 집계
- 참가자 정보 수정과 재배정

나이와 성별은 명단 정보와 집계에 사용합니다. 현재 배정 알고리즘은 나이 또는 성비의 균형을 보장하지 않습니다. 같은 분리그룹의 인원이 팀 수보다 많으면 같은 팀에 배정될 수 있습니다.

## 실행

Python 3.10 이상이 필요합니다. 저장소 루트에서 실행합니다.

```bash
python -m venv .venv
```

가상환경을 활성화합니다.

```bash
# macOS / Linux
source .venv/bin/activate

# Windows PowerShell
.\.venv\Scripts\Activate.ps1
```

```bash
python -m pip install -r requirements.txt
python -m uvicorn main:app --host 127.0.0.1 --port 8000
```

브라우저에서 `http://127.0.0.1:8000`에 접속합니다.

## CSV 형식

UTF-8 또는 UTF-8 BOM CSV를 사용합니다. 열 이름은 아래와 같아야 합니다.

```csv
이름,나이,성별,참가여부,분리그룹
예시참가자01,20,남,true,A
예시참가자02,21,여,true,A
예시참가자03,22,남,true,
예시참가자04,23,여,false,
```

- `참가여부`: `true`인 행만 배정합니다.
- `분리그룹`: 분산 배정할 참가자에게 같은 값을 지정합니다.
- `player.csv`: 가상 예시 명단입니다.
- 실제 명단은 `player.local.csv`처럼 로컬 전용 파일로 관리합니다.

## 구성

- `main.py`: CSV 처리, 팀 배정, 결과 캐시, HTTP 라우트
- `templates/`: 업로드, 결과, 명단 수정 화면
- `static/`: 화면 스타일
- `tests/`: 예시 명단 배정과 HTTP 흐름 검증

## 테스트

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

## 데이터와 현재 범위

배정 결과는 서버 메모리에 저장되며 재시작하면 사라집니다. 현재 구조는 단일 프로세스 실행을 기준으로 합니다. CSV 열 누락과 잘못된 팀 수에 대한 입력 처리는 추가 보완이 필요합니다.
