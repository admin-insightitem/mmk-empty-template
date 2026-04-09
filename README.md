# 한국 증시 유튜브 요약 자동화

한국 증시 관련 YouTube 채널을 모니터링하여 신규 영상의 자막을 자동으로 추출, 요약하고 Slack/Notion에 전달하는 Claude Code 기반 자동화 시스템입니다.

## 주요 기능

- **YouTube 모니터링**: RSS 피드 기반으로 신규 영상 감지 및 키워드 필터링
- **자막 추출**: yt-dlp를 활용한 한국어 자동생성 자막 추출
- **AI 요약**: Claude가 자막을 분석하여 핵심 요약, 언급 종목, 시장 전망 정리
- **Slack 알림**: MCP를 통해 Slack 채널에 요약 자동 전송
- **Notion 저장**: MCP를 통해 Notion 데이터베이스에 체계적 저장
- **스케줄 자동화**: 1시간 간격 자동 실행

## 모니터링 채널

| 채널 | 키워드 |
|------|--------|
| 삼프로TV | 증시, 주식, 코스피, 코스닥, 시황, 전망, 투자 |
| 슈카월드 | 주식, 증시, 경제, 투자, 코스피 |

## 설치

```bash
pip install -r scripts/requirements.txt
```

## 사용법

### 개별 스킬 실행
```
/fetch-youtube          # 신규 영상 조회
/extract-summarize      # 자막 추출 + 요약
/notify-slack           # Slack 전송
/save-notion            # Notion 저장
/stock-summary          # 전체 파이프라인
```

### 자동 스케줄링 (1시간 간격)
```
/loop 60m /stock-summary
```

## 사전 요구사항

- Python 3.11+
- Slack MCP 서버 설정
- Notion MCP 서버 설정
- Claude Code CLI

## 채널 추가

`scripts/config.json`에서 채널을 추가/수정할 수 있습니다.
