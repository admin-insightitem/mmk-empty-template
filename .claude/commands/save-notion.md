# Notion 데이터베이스에 증시 요약 저장

한국 증시 YouTube 영상 요약을 Notion 데이터베이스에 저장합니다.

## 입력

$ARGUMENTS

- 인자로 저장할 영상 메타데이터와 요약 텍스트를 받습니다.
- 인자가 없으면 사용자에게 저장할 내용을 요청하세요.

## 실행 단계

### 1. Notion 데이터베이스 찾기
`notion-search` MCP 도구로 "주식 유튜브 요약" 또는 "Stock Summary"를 검색합니다.

### 2. 데이터베이스가 없으면 생성
검색 결과에 해당 데이터베이스가 없으면 `notion-create-database` MCP 도구로 새로 생성합니다.

데이터베이스 스키마:
- **제목** (Title): 영상 제목 - TITLE 타입
- **채널** (Channel): 채널명 - SELECT 타입 (옵션: 삼프로TV, 슈카월드)
- **게시일** (Published): 영상 게시일 - DATE 타입
- **핵심요약** (Summary): 핵심 요약 텍스트 - RICH_TEXT 타입
- **언급종목** (Stocks): 언급된 종목들 - MULTI_SELECT 타입
- **시장전망** (Outlook): 시장 전망 - RICH_TEXT 타입
- **영상링크** (Video URL): YouTube 링크 - URL 타입
- **처리일시** (Processed At): 처리 시각 - DATE 타입

### 3. 페이지 생성
`notion-create-pages` MCP 도구로 데이터베이스에 새 페이지를 생성합니다.

각 필드에 맞는 데이터를 매핑합니다:
- 제목: 영상 제목
- 채널: 채널명 (SELECT 값)
- 게시일: 영상 게시일
- 핵심요약: 핵심 요약 텍스트 (최대 2000자로 잘라서 저장)
- 언급종목: 요약에서 추출한 종목명들 (MULTI_SELECT)
- 시장전망: 시장 전망 텍스트
- 영상링크: YouTube URL
- 처리일시: 현재 날짜/시간

페이지 본문(content)에는 전체 요약을 마크다운 형식으로 넣습니다.

### 4. 결과 보고
- 성공 시: "Notion에 저장 완료: [페이지 제목]" + 페이지 URL
- 실패 시: 에러 내용과 함께 보고
