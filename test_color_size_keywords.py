#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
다양한 색상/사이즈 키워드 파싱 테스트
"""

from brand_matching_system import BrandMatchingSystem

def test_color_size_keywords():
    """다양한 색상/사이즈 키워드 파싱 테스트"""
    print("=== 다양한 색상/사이즈 키워드 파싱 테스트 ===")
    
    # 시스템 초기화
    matching_system = BrandMatchingSystem()
    
    # 테스트 패턴들
    test_patterns = [
        # 기존 한국어 형태
        '색상: 네이비 / 사이즈: free',
        '색상=올리브, 사이즈=XL',
        '색상: 빨강, 사이즈: 100',
        
        # 컬러 키워드 사용
        '컬러: 화이트 / 사이즈: 13',
        '컬러=파랑, 사이즈=M',
        '컬러: 검정 / Size: L',
        
        # 영어 Color 키워드 사용
        'Color: 블루 / Size: XL',
        'Color=그린, Size=90',
        'Color: 노랑 / 사이즈: free',
        
        # 혼합 패턴
        '컬러: 핑크 / Size: 110',
        'Color: 아이보리 / 사이즈: M',
        '색상=레드, Size=L',
        
        # 다양한 구분자
        '컬러=브라운/Size=XL',
        'Color:오렌지,사이즈:95',
        '컬러 : 퍼플 / Size : S',
        
        # 기타 패턴
        '화이트/XL',  # 키워드 없는 형태
        '블루-L',     # 대시 구분
    ]
    
    print("다양한 키워드 패턴 테스트:")
    print("-" * 80)
    
    success_count = 0
    total_count = len(test_patterns)
    
    for pattern in test_patterns:
        color, size = matching_system.parse_options(pattern)
        has_result = bool(color or size)
        status = "✅" if has_result else "❌"
        
        if has_result:
            success_count += 1
        
        print(f"{status} '{pattern}' -> 색상='{color}', 사이즈='{size}'")
    
    print(f"\n성공률: {success_count}/{total_count} ({success_count/total_count*100:.1f}%)")
    
    return success_count == total_count

def test_real_world_patterns():
    """실제 사용될 수 있는 패턴들 테스트"""
    print(f"\n{'='*50}")
    print("실제 사용 패턴 테스트")
    print(f"{'='*50}")
    
    matching_system = BrandMatchingSystem()
    
    real_patterns = [
        # 쇼핑몰에서 자주 사용되는 형태
        'Color: White / Size: M',
        'Color: Black / Size: L', 
        'Color: Navy / Size: XL',
        '컬러: 화이트 / 사이즈: 100',
        '컬러: 블랙 / 사이즈: 110',
        'Color: Red / Size: Free',
        '컬러=핑크, Size=13',
        'Color=Blue, 사이즈=90',
        
        # 대소문자 혼합
        'color: 그레이 / size: L',
        'COLOR: 베이지 / SIZE: M',
        '컬러: NAVY / Size: xl',
    ]
    
    print("실제 사용 패턴:")
    print("-" * 80)
    
    for pattern in real_patterns:
        color, size = matching_system.parse_options(pattern)
        print(f"'{pattern}' -> 색상='{color}', 사이즈='{size}'")

if __name__ == "__main__":
    # 키워드 테스트
    test_result = test_color_size_keywords()
    
    # 실제 패턴 테스트
    test_real_world_patterns()
    
    if test_result:
        print(f"\n🎉 모든 키워드 테스트 통과! 다양한 색상/사이즈 키워드를 지원합니다.")
    else:
        print(f"\n⚠️ 일부 패턴이 실패했습니다. 추가 개선이 필요할 수 있습니다.") 