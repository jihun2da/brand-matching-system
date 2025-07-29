#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
개선된 옵션 파싱 로직 테스트
"""

import pandas as pd
from brand_matching_system import BrandMatchingSystem

def test_improved_parsing():
    """개선된 파싱 로직 테스트"""
    print("=== 개선된 옵션 파싱 테스트 ===")
    
    # 시스템 초기화
    matching_system = BrandMatchingSystem()
    
    # 실제 엑셀 파일의 옵션 데이터
    real_data_patterns = [
        # 첫 번째 파일 형식
        '색상=올리브, 사이즈=XL',
        '색상=흑청, 사이즈=XL',
        '색상=핑크, 사이즈=XL',
        '색상=SET, 사이즈=M',
        '색상=소라, 사이즈=M',
        '색상=아이보리, 사이즈=free',
        
        # 두 번째 파일 형식
        '색상=노랑 / 사이즈: 12M',
        '색상=오렌지 / 사이즈: 12M',
        '색상=크림 / 사이즈: 12M',
        '색상=검정 / 사이즈: 6M',
        '색상=블루, 사이즈=18M',
        
        # 기존 지원 형식
        '색상: 빨강, 사이즈: 100',
        '색상: 파랑 / 사이즈: 90',
        '색상:노랑,사이즈:95',
        
        # 추가 패턴
        '빨강/100',
        '파랑-90',
        '핑크/M',
        'L-검정',
    ]
    
    print("실제 데이터 패턴 테스트:")
    print("-" * 80)
    
    success_count = 0
    total_count = len(real_data_patterns)
    
    for pattern in real_data_patterns:
        color, size = matching_system.parse_options(pattern)
        has_result = bool(color or size)
        status = "✅" if has_result else "❌"
        
        if has_result:
            success_count += 1
        
        print(f"{status} '{pattern}' -> 색상='{color}', 사이즈='{size}'")
    
    print(f"\n성공률: {success_count}/{total_count} ({success_count/total_count*100:.1f}%)")
    
    return success_count == total_count

def test_with_real_files():
    """실제 엑셀 파일로 전체 프로세스 테스트"""
    print(f"\n{'='*50}")
    print("실제 엑셀 파일 전체 프로세스 테스트")
    print(f"{'='*50}")
    
    matching_system = BrandMatchingSystem()
    
    files = [
        '7-29AA084(사월에).xlsx',
        '7-29A084다른 브랜드사입청건.xlsx'
    ]
    
    for filename in files:
        print(f"\n파일: {filename}")
        print("-" * 40)
        
        try:
            # 엑셀 파일 로드
            df = pd.read_excel(filename)
            
            # Sheet2 형식으로 변환
            result_df = matching_system.convert_sheet1_to_sheet2(df)
            
            # 색상/사이즈 파싱 결과 확인
            color_success = 0
            size_success = 0
            total_rows = len(result_df)
            
            print("색상/사이즈 파싱 결과:")
            for i, row in result_df.iterrows():
                color = row.get('J열(색상)', '')
                size = row.get('K열(사이즈)', '')
                
                if color.strip():
                    color_success += 1
                if size.strip():
                    size_success += 1
                
                if i < 5:  # 상위 5개만 표시
                    print(f"  행 {i+1}: 색상='{color}', 사이즈='{size}'")
            
            print(f"\n결과:")
            print(f"  색상 파싱 성공: {color_success}/{total_rows} ({color_success/total_rows*100:.1f}%)")
            print(f"  사이즈 파싱 성공: {size_success}/{total_rows} ({size_success/total_rows*100:.1f}%)")
            
        except Exception as e:
            print(f"❌ 오류: {e}")

if __name__ == "__main__":
    # 패턴 테스트
    test_result = test_improved_parsing()
    
    # 실제 파일 테스트
    test_with_real_files()
    
    if test_result:
        print(f"\n🎉 모든 테스트 통과! 개선된 파싱 로직이 정상 작동합니다.")
    else:
        print(f"\n⚠️ 일부 패턴이 실패했습니다. 추가 개선이 필요합니다.") 