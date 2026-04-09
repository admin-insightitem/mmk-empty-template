# 한국 증시 유튜브 요약 자동화 (전체 파이프라인)

한국 증시 관련 YouTube 신규 영상을 조회하고, 자막을 추출하여 요약한 뒤, Slack 알림과 Notion 저장을 자동으로 수행합니다.

## 전체 파이프라인

### Step 1: 신규 영상 조회

Python 의존성을 확인하고 YouTube fetcher를 실행합니다:
```
pip install -r scripts/requirements.txt --quiet
python3 scripts/youtube_fetcher.py
```

출력된 JSON 배열을 파싱합니다. 빈 배열이면 "새로운 증시 관련 영상이 없습니다."라고 보고하고 여기서 종료합니다.

### Step 2: 각 영상에 대해 자막 추출 및 요약

발견된 각 영상에 대해 순차적으로:

1. **자막 추출**:
   ```
   python3 scripts/subtitle_extractor.py "<video_url>"
   ```
   실패하면 해당 영상을 건너뛰고 다음으로 진행합니다.

2. **요약 생성**: 추출된 자막을 바탕으로 아래 형식의 한국어 요약을 생성합니다:
   ```
   ## [채널명] 영상 제목
   📅 게시일: YYYY-MM-DD
   🔗 링크: YouTube URL

   ### 핵심 요약
   1-3문장 핵심 메시지

   ### 주요 내용
   - 포인트 1
   - 포인트 2
   - 포인트 3 (최대 5개)

   ### 언급된 종목/지표
   - 종목 목록 (없으면 "특정 종목 언급 없음")

   ### 시장 전망
   시장 전망 요약 (없으면 "별도 전망 언급 없음")
   ```

3. **처리 기록 업데이트**: 성공한 영상의 video_id를 `scripts/processed_videos.json`에 추가합니다:
   ```python
   import json
   from datetime import datetime
   with open("scripts/processed_videos.json", "r") as f:
       data = json.load(f)
   data["VIDEO_ID"] = datetime.now().isoformat()
   with open("scripts/processed_videos.json", "w") as f:
       json.dump(data, f, ensure_ascii=False, indent=2)
   ```

### Step 3: Slack 알림 전송

각 요약에 대해 Slack MCP 도구로 알림을 보냅니다:

1. `slack_search_channels` 도구로 "stock" 또는 "주식" 키워드로 채널을 검색합니다. 처음 한 번만 검색하고 이후 같은 채널을 재사용합니다.

2. `slack_send_message` 도구로 아래 형식의 메시지를 전송합니다:
   ```
   📊 *한국 증시 유튜브 요약*

   *[채널명] 영상 제목*
   🔗 <영상링크|YouTube에서 보기>
   📅 게시일

   *핵심 요약*
   요약 내용

   *주요 내용*
   • 포인트들

   *언급된 종목/지표*
   종목 목록

   *시장 전망*
   전망 내용

   ---
   🕐 자동 요약 | {현재 날짜 및 시간}
   ```

### Step 4: Notion 데이터베이스 저장

각 요약에 대해 Notion MCP 도구로 저장합니다:

1. `notion-search` 도구로 "주식 유튜브 요약" 데이터베이스를 검색합니다. 처음 한 번만 검색합니다.

2. 데이터베이스가 없으면 `notion-create-database` 도구로 생성합니다:
   - 제목 (TITLE), 채널 (SELECT), 게시일 (DATE), 핵심요약 (RICH_TEXT)
   - 언급종목 (MULTI_SELECT), 시장전망 (RICH_TEXT), 영상링크 (URL), 처리일시 (DATE)

3. `notion-create-pages` 도구로 페이지를 생성합니다. 각 필드에 요약 데이터를 매핑합니다.

### Step 5: 최종 보고

모든 영상 처리가 끝나면 결과를 요약합니다:
```
## 처리 결과
- 발견된 영상: N개
- 성공적으로 처리: M개
- 실패: K개 (실패 사유 포함)
- Slack 전송: 성공/실패
- Notion 저장: 성공/실패
```

## 에러 처리

- 개별 영상 처리 실패 시 해당 영상만 건너뛰고 나머지 계속 진행
- Slack 전송 실패 시 로그만 남기고 Notion 저장은 계속 진행
- Notion 저장 실패 시 로그만 남기고 다음 영상으로 진행
- 전체 파이프라인이 중단되지 않도록 각 단계별 에러를 독립적으로 처리
