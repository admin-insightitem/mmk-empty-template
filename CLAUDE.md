# 한국 증시 유튜브 요약 자동화 시스템

## 프로젝트 개요
한국 증시 관련 YouTube 채널을 모니터링하여 신규 영상의 자막을 추출하고 요약한 뒤, Slack 알림 및 Notion 데이터베이스 저장을 자동화하는 시스템입니다.

## 아키텍처
```
YouTube RSS Feed → youtube_fetcher.py (필터링)
    → subtitle_extractor.py (자막 추출)
    → Claude 요약 (스킬 내 직접 생성)
    → Slack MCP (알림) + Notion MCP (저장)
```

## 파일 구조
- `scripts/config.json` - 채널 설정, 키워드 필터, 실행 주기
- `scripts/processed_videos.json` - 처리된 영상 이력 (중복 방지)
- `scripts/youtube_fetcher.py` - YouTube RSS에서 신규 영상 조회 및 필터링
- `scripts/subtitle_extractor.py` - yt-dlp로 한국어 자막 추출

## 사용 가능한 스킬 (Custom Commands)
- `/fetch-youtube` - 신규 증시 영상 조회
- `/extract-summarize` - 자막 추출 및 요약 생성
- `/notify-slack` - Slack 채널에 요약 전송
- `/save-notion` - Notion DB에 요약 저장
- `/stock-summary` - 전체 파이프라인 실행 (위 4개를 순차 실행)

## 스케줄링
```
/loop 60m /stock-summary
```
위 명령으로 1시간마다 자동 실행됩니다.

## 의존성
```bash
pip install -r scripts/requirements.txt
```
- `feedparser` - YouTube RSS 피드 파싱
- `yt-dlp` - YouTube 자막 다운로드

## MCP 연동
- **Slack MCP**: `slack_search_channels`, `slack_send_message` 도구 사용
- **Notion MCP**: `notion-search`, `notion-create-database`, `notion-create-pages` 도구 사용

## 채널 추가/변경
`scripts/config.json`의 `channels` 배열에 새 채널을 추가하세요:
```json
{
  "name": "채널명",
  "channel_id": "YouTube 채널 ID",
  "keywords": ["키워드1", "키워드2"]
}
```
채널 ID는 YouTube 채널 페이지 URL에서 확인할 수 있습니다.
