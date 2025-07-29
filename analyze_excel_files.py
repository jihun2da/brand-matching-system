#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
엑셀 파일 구조 분석 - 색상/사이즈 파싱 문제 분석
"""

import pandas as pd
import re

def analyze_excel_files():
    """두 엑셀 파일의 색상/사이즈 파싱 문제 분석"""
    print("=== 엑셀 파일 구조 분석 ===")
    
    files = [
        '7-29AA084(사월에).xlsx',
        '7-29A084다른 브랜드사입청건.xlsx'
    ]
    
    for filename in files:
        print(f"\n{'='*50}")
        print(f"파일: {filename}")
        print(f"{'='*50}")
        
        try:
            df = pd.read_excel(filename)
            print(f"행 수: {len(df)}")
            print(f"컬럼 수: {len(df.columns)}")
            
            print("\n컬럼명들:")
            for i, col in enumerate(df.columns):
                print(f"  {i}: {col}")
            
            # F열 (옵션) 데이터 분석 (일반적으로 6번째 컬럼)
            if len(df.columns) >= 6:
                print(f"\nF열 ({df.columns[5]}) 샘플 데이터:")
                option_col_data = df.iloc[:, 5].dropna()
                
                for i, value in enumerate(option_col_data.head(10)):
                    print(f"  행 {i+1}: '{value}'")
                    
                    # 현재 파싱 로직 테스트
                    color, size = parse_options_current(str(value))
                    print(f"    -> 현재 파싱: 색상='{color}', 사이즈='{size}'")
            else:
                print("6번째 컬럼(F열)이 없습니다!")
            
            print(f"\n상위 3개 행 전체 데이터:")
            print(df.head(3).to_string())
            
        except Exception as e:
            print(f"❌ 파일 읽기 오류: {e}")

def parse_options_current(option_text):
    """현재 시스템의 옵션 파싱 로직"""
    if not option_text or pd.isna(option_text) or str(option_text).strip().lower() == 'nan':
        return "", ""
    
    option_text = str(option_text).strip()
    color = ""
    size = ""
    
    # 색상 추출 - '색상:' 다음부터 콤마, '사이즈:', 또는 문자열 끝까지
    color_match = re.search(r'색상\s*:\s*([^,]+?)(?:\s*,|\s*사이즈:|$)', option_text, re.IGNORECASE)
    if color_match:
        color = color_match.group(1).strip()
        # 색상에서 불필요한 기호와 공백 제거
        color = re.sub(r'\s*[/\\|]+\s*$', '', color)  # 끝의 /, \, | 기호와 공백 제거
        color = color.strip()
    
    # 사이즈 추출 - '사이즈:' 다음부터 콤마 또는 문자열 끝까지
    size_match = re.search(r'사이즈\s*:\s*(.+?)(?:\s*,|$)', option_text, re.IGNORECASE)
    if size_match:
        size = size_match.group(1).strip()
        # 사이즈에서 불필요한 기호와 공백 제거
        size = re.sub(r'\s*[/\\|]+\s*$', '', size)  # 끝의 /, \, | 기호와 공백 제거
        size = size.strip()
    
    return color, size

def test_various_patterns():
    """다양한 옵션 패턴 테스트"""
    print(f"\n{'='*50}")
    print("다양한 옵션 패턴 테스트")
    print(f"{'='*50}")
    
    test_patterns = [
        "색상: 빨강, 사이즈: 100",
        "색상: 파랑 / 사이즈: 90",
        "색상:노랑,사이즈:95",
        "빨강/100",
        "파랑-90",
        "색상:핑크",
        "사이즈:110",
        "핑크/M",
        "L-검정",
        "색상 빨강 사이즈 100",
        "빨강색 100사이즈",
        "",
        "nan"
    ]
    
    for pattern in test_patterns:
        color, size = parse_options_current(pattern)
        print(f"'{pattern}' -> 색상='{color}', 사이즈='{size}'")

if __name__ == "__main__":
    analyze_excel_files()
    test_various_patterns() 