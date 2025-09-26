#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VOCALOID 생일송 데이터 수집기
니코니코 동화 API를 사용해서 매월 매일의 VOCALOID 곡 데이터를 수집합니다.
"""

import requests
import json
import os
from datetime import datetime, timedelta
from urllib.parse import urlencode
import time


def make_filters_all_years(month, day):
    """특정 월/일에 업로드된 곡들을 찾기 위한 필터 생성"""
    filters = []
    
    # 2007년부터 현재년도+1년까지 모든 년도 확인
    current_year = datetime.now().year
    for year in range(2007, current_year + 2):
        try:
            # 해당 날짜 생성
            dt_from = datetime(year, month, day)
            dt_to = datetime(year, month, day) + timedelta(days=1)
            
            # 유효한 날짜인지 확인 (2월 29일 등)
            if dt_from.month != month or dt_from.day != day:
                continue
            
            # JST 시간대로 변환
            from_iso = format_to_jst(dt_from)
            to_iso = format_to_jst(dt_to)
            
            filters.append({
                "type": "range",
                "field": "startTime",
                "from": from_iso,
                "to": to_iso,
                "include_lower": True
            })
            
        except ValueError:
            # 잘못된 날짜 (예: 2월 30일)는 건너뛰기
            continue
    
    return {
        "type": "and",
        "filters": [
            {"type": "or", "filters": filters},
            {
                "type": "not",
                "filter": {
                    "type": "equal",
                    "field": "tags",
                    "value": "歌ってみた"
                }
            }
        ]
    }


def format_to_jst(dt):
    """datetime 객체를 JST 시간대 ISO 형식으로 변환"""
    return dt.strftime("%Y-%m-%dT%H:%M:%S+09:00")


def search_vocaloid_songs(month, day, max_count=50):
    """특정 월/일의 VOCALOID 곡 검색"""
    try:
        filters_dict = make_filters_all_years(month, day)
        
        if not filters_dict or not filters_dict.get("filters"):
            print(f"  ⚠️  {month:02d}/{day:02d}: 유효한 날짜 필터가 없음")
            return []

        api_url = "https://snapshot.search.nicovideo.jp/api/v2/snapshot/video/contents/search"
        
        params = {
            "q": "VOCALOID",
            "targets": "tagsExact",
            "fields": "contentId,title,startTime,thumbnailUrl,viewCounter,lengthSeconds",
            "jsonFilter": json.dumps(filters_dict, separators=(',', ':')),
            "_sort": "-viewCounter",
            "_limit": max_count,
            "_context": "vocaloid_birthday_search"
        }

        headers = {
            "User-Agent": "vocaloid_birthday_search/1.0 (GitHub Actions)"
        }

        response = requests.get(api_url, params=params, headers=headers, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            songs = data.get("data", [])
            print(f"  ✅ {month:02d}/{day:02d}: {len(songs)}개 곡 수집 완료")
            return songs
        else:
            print(f"  ❌ {month:02d}/{day:02d}: API 오류 (상태코드: {response.status_code})")
            return []
            
    except Exception as e:
        print(f"  ❌ {month:02d}/{day:02d}: 오류 발생 - {str(e)}")
        return []


def collect_all_birthday_data():
    """모든 날짜의 VOCALOID 생일송 데이터 수집"""
    print("🎵 VOCALOID 생일송 데이터 수집 시작...")
    print(f"📅 수집 시작 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    all_data = {}
    total_songs = 0
    
    # 12개월 * 31일 = 372일 (존재하지 않는 날짜는 자동으로 건너뛰기)
    for month in range(1, 13):
        print(f"\n📅 {month}월 데이터 수집 중...")
        
        month_data = {}
        for day in range(1, 32):
            try:
                # 유효한 날짜인지 확인
                datetime(2024, month, day)  # 윤년을 고려해서 2024년으로 체크
                
                songs = search_vocaloid_songs(month, day, max_count=50)
                
                if songs:  # 곡이 있는 경우만 저장
                    key = f"{month:02d}-{day:02d}"
                    month_data[key] = songs
                    total_songs += len(songs)
                
                # API 호출 간격 조절 (너무 빠른 요청 방지)
                time.sleep(0.5)
                
            except ValueError:
                # 존재하지 않는 날짜 (예: 2월 30일, 4월 31일 등)
                continue
            except Exception as e:
                print(f"  ⚠️  {month:02d}/{day:02d}: 예상치 못한 오류 - {str(e)}")
                continue
        
        # 월별 데이터를 전체 데이터에 병합
        all_data.update(month_data)
        print(f"  📊 {month}월 완료: {len(month_data)}일, {sum(len(songs) for songs in month_data.values())}개 곡")
    
    print(f"\n🎉 데이터 수집 완료!")
    print(f"📊 총 {len(all_data)}일, {total_songs}개 곡 수집됨")
    
    return all_data


def save_data_to_file(data, filename="vocaloid_birthday_songs.json"):
    """데이터를 JSON 파일로 저장"""
    # data 폴더가 없으면 생성
    os.makedirs("data", exist_ok=True)
    
    filepath = os.path.join("data", filename)
    
    # 메타데이터 추가
    output_data = {
        "metadata": {
            "collected_at": datetime.now().isoformat(),
            "total_days": len(data),
            "total_songs": sum(len(songs) for songs in data.values()),
            "description": "VOCALOID 곡들의 생일별 데이터베이스"
        },
        "data": data
    }
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2, separators=(',', ': '))
    
    print(f"💾 데이터 저장 완료: {filepath}")
    return filepath


def main():
    """메인 실행 함수"""
    try:
        # 1. 데이터 수집
        all_data = collect_all_birthday_data()
        
        # 2. 파일로 저장
        save_data_to_file(all_data)
        
        print("\n✅ 모든 작업이 성공적으로 완료되었습니다!")
        
    except KeyboardInterrupt:
        print("\n⚠️  사용자에 의해 중단되었습니다.")
    except Exception as e:
        print(f"\n❌ 예상치 못한 오류가 발생했습니다: {str(e)}")
        raise


if __name__ == "__main__":
    main()