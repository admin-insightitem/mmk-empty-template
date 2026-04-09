#!/usr/bin/env python3
"""
YouTube RSS 피드에서 한국 증시 관련 신규 영상을 가져오고 필터링하는 스크립트.
config.json 설정에 따라 키워드 매칭, 중복 제거를 수행합니다.
외부 의존성 없이 표준 라이브러리만 사용합니다.
"""

import json
import sys
import os
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from urllib.request import urlopen, Request
from urllib.error import URLError

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(SCRIPT_DIR, "config.json")
PROCESSED_PATH = os.path.join(SCRIPT_DIR, "processed_videos.json")

RSS_URL_TEMPLATE = "https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"

# YouTube Atom 피드 네임스페이스
NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "yt": "http://www.youtube.com/xml/schemas/2015",
    "media": "http://search.yahoo.com/mrss/",
}


def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def load_processed():
    try:
        with open(PROCESSED_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def parse_published_time(published_str):
    """ISO 8601 문자열을 UTC datetime으로 변환"""
    if not published_str:
        return None
    try:
        # YouTube RSS는 ISO 8601 형식 사용: 2026-04-09T10:30:00+00:00
        published_str = published_str.strip()
        if published_str.endswith("Z"):
            published_str = published_str[:-1] + "+00:00"
        return datetime.fromisoformat(published_str)
    except (ValueError, TypeError):
        return None


def matches_keywords(title, keywords):
    """제목에 키워드 중 하나라도 포함되면 True"""
    title_lower = title.lower()
    return any(kw.lower() in title_lower for kw in keywords)


def has_exclude_keywords(title, exclude_keywords):
    """제목에 제외 키워드가 포함되면 True"""
    title_lower = title.lower()
    return any(kw.lower() in title_lower for kw in exclude_keywords)


def fetch_rss(url):
    """URL에서 RSS XML을 가져와 파싱"""
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(req, timeout=15) as resp:
        return ET.parse(resp)


def fetch_channel_videos(channel, filter_config, processed_ids, cutoff_time):
    """단일 채널의 RSS 피드에서 새 영상을 가져와 필터링"""
    url = RSS_URL_TEMPLATE.format(channel_id=channel["channel_id"])
    results = []

    try:
        tree = fetch_rss(url)
        root = tree.getroot()
    except Exception as e:
        print(f"[ERROR] {channel['name']} RSS 피드 조회 실패: {e}", file=sys.stderr)
        return results

    # 채널 키워드 + 글로벌 필터 키워드 합치기
    all_keywords = list(set(channel.get("keywords", []) + filter_config.get("keywords", [])))
    exclude_keywords = filter_config.get("exclude_keywords", [])

    for entry in root.findall("atom:entry", NS):
        # video_id 추출
        video_id_elem = entry.find("yt:videoId", NS)
        if video_id_elem is None or not video_id_elem.text:
            continue
        video_id = video_id_elem.text.strip()

        # 이미 처리된 영상 스킵
        if video_id in processed_ids:
            continue

        # 게시 시간 확인
        published_elem = entry.find("atom:published", NS)
        published_str = published_elem.text if published_elem is not None else None
        published = parse_published_time(published_str)
        if published and published < cutoff_time:
            continue

        # 제목 추출
        title_elem = entry.find("atom:title", NS)
        title = title_elem.text.strip() if title_elem is not None and title_elem.text else ""

        # 제외 키워드 체크
        if has_exclude_keywords(title, exclude_keywords):
            continue

        # 키워드 매칭
        if not matches_keywords(title, all_keywords):
            continue

        # 링크 추출
        link_elem = entry.find("atom:link", NS)
        link = link_elem.get("href", f"https://www.youtube.com/watch?v={video_id}") if link_elem is not None else f"https://www.youtube.com/watch?v={video_id}"

        results.append({
            "video_id": video_id,
            "title": title,
            "url": link,
            "channel_name": channel["name"],
            "published": published.isoformat() if published else "",
        })

    return results


def main():
    config = load_config()
    processed = load_processed()
    processed_ids = set(processed.keys())

    filter_config = config.get("filter", {})
    max_age_hours = filter_config.get("max_video_age_hours", 24)
    cutoff_time = datetime.now(timezone.utc) - timedelta(hours=max_age_hours)

    all_videos = []
    for channel in config.get("channels", []):
        videos = fetch_channel_videos(channel, filter_config, processed_ids, cutoff_time)
        all_videos.extend(videos)

    # JSON 출력
    print(json.dumps(all_videos, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
