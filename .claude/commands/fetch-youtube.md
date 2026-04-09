# 한국 증시 YouTube 신규 영상 조회

한국 증시 관련 YouTube 채널에서 새로운 영상을 가져옵니다.

## 실행 단계

1. 먼저 Python 의존성이 설치되어 있는지 확인합니다:
   ```
   pip install -r scripts/requirements.txt --quiet
   ```

2. YouTube fetcher 스크립트를 실행합니다:
   ```
   python3 scripts/youtube_fetcher.py
   ```

3. 스크립트 출력은 JSON 배열입니다. 각 항목에는 `video_id`, `title`, `url`, `channel_name`, `published` 필드가 있습니다.

4. 결과를 파싱하여 아래 형식으로 사용자에게 보여주세요:

   **새로운 증시 관련 영상 N개 발견:**
   
   각 영상별로:
   - **채널**: 채널명
   - **제목**: 영상 제목
   - **게시일**: 게시 시간
   - **링크**: YouTube URL

5. 만약 빈 배열 `[]`이 반환되면 "새로운 증시 관련 영상이 없습니다."라고 보고하세요.

6. 오류가 발생하면 stderr 출력을 확인하고 사용자에게 알려주세요.
