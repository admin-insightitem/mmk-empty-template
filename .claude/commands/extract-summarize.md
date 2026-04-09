# 유튜브 영상 자막 추출 및 한국어 요약

YouTube 영상의 한국어 자막을 추출하고 증시 관련 내용을 요약합니다.

## 입력

$ARGUMENTS

- 인자가 YouTube URL이면 해당 영상만 처리합니다.
- 인자가 JSON 배열(fetch-youtube 결과)이면 각 영상을 순차 처리합니다.
- 인자가 없으면 `python3 scripts/youtube_fetcher.py`를 먼저 실행하여 새 영상 목록을 가져옵니다.

## 실행 단계

### 1. 의존성 확인
```
pip install -r scripts/requirements.txt --quiet
```

### 2. 영상 목록 준비
- 인자가 없으면 `python3 scripts/youtube_fetcher.py`를 실행하여 영상 목록을 가져옵니다.
- 영상이 없으면 "새로운 영상이 없습니다."라고 보고하고 종료합니다.

### 3. 각 영상에 대해 자막 추출
```
python3 scripts/subtitle_extractor.py "<video_url>"
```
- 자막 추출에 실패하면 해당 영상을 건너뛰고 다음 영상으로 진행합니다.

### 4. 자막 요약 생성
추출된 자막 텍스트를 읽고, 아래 형식으로 **한국어** 요약을 직접 생성하세요:

```
## [채널명] 영상 제목
📅 게시일: YYYY-MM-DD
🔗 링크: YouTube URL

### 핵심 요약
1-3문장으로 영상의 핵심 메시지를 요약

### 주요 내용
- 주요 포인트 1
- 주요 포인트 2
- 주요 포인트 3
(최대 5개)

### 언급된 종목/지표
- 종목명1, 종목명2, ... (없으면 "특정 종목 언급 없음")

### 시장 전망
영상에서 언급된 시장 전망이나 투자 의견 요약 (없으면 "별도 전망 언급 없음")
```

### 5. 처리 완료 기록
요약 생성에 성공한 영상은 `scripts/processed_videos.json`에 기록합니다:
- 파일을 읽고, `video_id`를 키로, 현재 타임스탬프를 값으로 추가한 뒤 저장합니다.

```python
# processed_videos.json 업데이트 예시
import json
from datetime import datetime
with open("scripts/processed_videos.json", "r") as f:
    data = json.load(f)
data["VIDEO_ID"] = datetime.now().isoformat()
with open("scripts/processed_videos.json", "w") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
```

### 6. 결과 출력
모든 영상의 요약을 순서대로 출력하세요. 실패한 영상이 있으면 마지막에 실패 목록도 보고합니다.
