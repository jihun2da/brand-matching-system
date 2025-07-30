#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
키워드 제거 기능 테스트
"""

import pandas as pd
from brand_matching_system import BrandMatchingSystem

def test_keyword_removal():
    """키워드 제거 기능 테스트"""
    print("=== 키워드 제거 기능 테스트 ===")
    
    # 시스템 초기화
    matching_system = BrandMatchingSystem()
    
    # 현재 키워드 목록 확인
    print(f"현재 키워드 목록: {matching_system.keyword_list}")
    print(f"키워드 개수: {len(matching_system.keyword_list)}")
    
    # 사용자가 추가한 키워드들이 있는지 확인
    test_keywords = ['s~xl', '13-15', 'js-jxl']
    for keyword in test_keywords:
        if keyword in matching_system.keyword_list:
            print(f"✅ '{keyword}' 키워드가 목록에 있습니다.")
        else:
            print(f"❌ '{keyword}' 키워드가 목록에 없습니다.")
    
    # 테스트 상품명들
    test_products = [
        "베베쭈나 프릴티셔츠(s~xl)",
        "베베쭈나 반바지(13-15)",
        "베베쭈나 원피스(js-jxl)",
        "베베쭈나 티셔츠(s~xl),반바지(13-15)",
        "일반 상품명 (다른키워드)",
    ]
    
    print(f"\n키워드 제거 테스트:")
    print("-" * 80)
    
    for product in test_products:
        normalized = matching_system.normalize_product_name(product)
        print(f"원본: '{product}'")
        print(f"결과: '{normalized}'")
        print()

def test_with_real_file():
    """실제 베베쭈나 파일로 테스트"""
    print(f"\n{'='*50}")
    print("실제 0730 베베쭈나.xlsx 파일 테스트")
    print(f"{'='*50}")
    
    matching_system = BrandMatchingSystem()
    
    try:
        # 엑셀 파일 로드
        df = pd.read_excel('0730 베베쭈나.xlsx')
        print(f"파일 로드 완료: {len(df)}개 행")
        
        print("\n컬럼명:")
        for i, col in enumerate(df.columns):
            print(f"  {i}: {col}")
        
        # 브랜드/상품명 컬럼 (E열, 인덱스 4) 확인
        if len(df.columns) >= 5:
            print(f"\nE열 ({df.columns[4]}) 샘플 데이터:")
            brand_product_data = df.iloc[:, 4].dropna()
            
            for i, value in enumerate(brand_product_data.head(10)):
                print(f"  행 {i+1}: '{value}'")
                
                # 키워드 제거 테스트
                normalized = matching_system.normalize_product_name(str(value))
                if str(value) != normalized:
                    print(f"    -> 키워드 제거 후: '{normalized}'")
                else:
                    print(f"    -> 변화 없음")
        
        # Sheet2 형식으로 변환 테스트
        print(f"\n전체 프로세스 테스트:")
        result_df = matching_system.convert_sheet1_to_sheet2(df)
        
        print(f"변환 완료: {len(result_df)}개 행")
        
        # I열(상품명) 확인
        if 'I열(상품명)' in result_df.columns:
            print(f"\nI열(상품명) 샘플 결과:")
            for i, product_name in enumerate(result_df['I열(상품명)'].head(5)):
                print(f"  {i+1}: '{product_name}'")
        
    except Exception as e:
        print(f"❌ 오류: {e}")

if __name__ == "__main__":
    test_keyword_removal()
    test_with_real_file() 