#!/usr/bin/env python3
"""
YouTube 영상에서 한국어 자막(자동 생성 포함)을 추출하는 스크립트.
yt-dlp를 사용하여 자막을 다운로드하고, VTT 파일을 정제하여 텍스트를 출력합니다.
"""

import sys
import os
import re
import glob
import tempfile

import yt_dlp


def extract_video_id(url):
    """URL에서 video_id 추출"""
    if "v=" in url:
        return url.split("v=")[-1].split("&")[0]
    if "youtu.be/" in url:
        return url.split("youtu.be/")[-1].split("?")[0]
    return "unknown"


def download_subtitles(url, output_dir):
    """yt-dlp로 한국어 자막 다운로드"""
    video_id = extract_video_id(url)
    output_template = os.path.join(output_dir, f"subs_{video_id}")

    ydl_opts = {
        "writesubtitles": True,
        "writeautomaticsub": True,
        "subtitleslangs": ["ko"],
        "subtitlesformat": "vtt",
        "skip_download": True,
        "quiet": True,
        "no_warnings": True,
        "noprogress": True,
        "outtmpl": output_template,
        "nocheckcertificate": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    # 생성된 자막 파일 찾기
    pattern = os.path.join(output_dir, f"subs_{video_id}*.vtt")
    files = glob.glob(pattern)

    if not files:
        return None

    return files[0]


def clean_vtt(vtt_path):
    """VTT 파일에서 타임스탬프, 태그를 제거하고 정제된 텍스트 반환"""
    with open(vtt_path, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.split("\n")
    cleaned = []
    prev_line = ""

    for line in lines:
        line = line.strip()

        # VTT 헤더, 메타 라인 스킵
        if not line:
            continue
        if line.startswith("WEBVTT"):
            continue
        if line.startswith("Kind:") or line.startswith("Language:"):
            continue
        if line.startswith("NOTE"):
            continue

        # 타임스탬프 라인 스킵 (00:00:00.000 --> 00:00:05.000)
        if re.match(r"^\d{2}:\d{2}:\d{2}\.\d{3}\s*-->", line):
            continue

        # 숫자만 있는 큐 인덱스 스킵
        if re.match(r"^\d+$", line):
            continue

        # HTML 태그 제거
        line = re.sub(r"<[^>]+>", "", line)

        # 포지셔닝 메타데이터 제거
        line = re.sub(r"align:start position:\d+%", "", line).strip()

        if not line:
            continue

        # 연속 중복 라인 제거 (자동 자막의 특성)
        if line != prev_line:
            cleaned.append(line)
            prev_line = line

    return "\n".join(cleaned)


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 subtitle_extractor.py <youtube_url>", file=sys.stderr)
        sys.exit(1)

    url = sys.argv[1]

    with tempfile.TemporaryDirectory() as tmp_dir:
        try:
            vtt_path = download_subtitles(url, tmp_dir)
        except Exception as e:
            print(f"[ERROR] 자막 다운로드 실패: {e}", file=sys.stderr)
            sys.exit(1)

        if not vtt_path:
            print("[ERROR] 한국어 자막을 찾을 수 없습니다.", file=sys.stderr)
            sys.exit(1)

        text = clean_vtt(vtt_path)

        if not text.strip():
            print("[ERROR] 자막 내용이 비어있습니다.", file=sys.stderr)
            sys.exit(1)

        print(text)


if __name__ == "__main__":
    main()
