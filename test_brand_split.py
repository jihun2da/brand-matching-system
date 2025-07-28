import pandas as pd
import re

def test_brand_split(e_value):
    """브랜드/상품명 분리 테스트"""
    print(f"\n원본 데이터: '{e_value}'")
    
    # 현재 시스템과 동일한 로직
    e_value = e_value.strip()  # 앞뒤 공백 제거
    print(f"공백 제거 후: '{e_value}'")
    
    if e_value:
        # 괄호를 이용한 브랜드 추출 시도 (예: 클라레오(기린) 상품명)
        bracket_match = re.match(r'^([^)]+\)[^)]*?)\s+(.+)$', e_value)
        if bracket_match:
            # 괄호가 포함된 브랜드명과 상품명 분리
            brand_part = bracket_match.group(1).strip()
            product_part = bracket_match.group(2).strip()
            print(f"괄호 패턴 매칭 성공:")
            print(f"  브랜드: '{brand_part}'")
            print(f"  상품명: '{product_part}'")
            return brand_part, product_part
            
        elif ' ' in e_value:
            # 일반적인 띄어쓰기 분할 (공백 제거 후)
            parts = e_value.split(' ', 1)
            if parts[0].strip():  # 첫 번째 부분이 비어있지 않으면
                brand_part = parts[0].strip()
                product_part = parts[1].strip() if len(parts) > 1 else ""
                print(f"일반 띄어쓰기 분할:")
                print(f"  브랜드: '{brand_part}'")
                print(f"  상품명: '{product_part}'")
                return brand_part, product_part
            else:
                # 첫 번째 부분이 비어있으면 전체를 상품명으로 처리
                print(f"첫 부분이 비어있어 전체를 상품명으로 처리:")
                print(f"  브랜드: ''")
                print(f"  상품명: '{e_value}'")
                return "", e_value
        else:
            # 띄어쓰기가 없으면 전체를 브랜드로 처리
            print(f"띄어쓰기 없어 전체를 브랜드로 처리:")
            print(f"  브랜드: '{e_value}'")
            print(f"  상품명: ''")
            return e_value, ""
    else:
        print("빈 데이터")
        return "", ""

# 실제 엑셀 파일에서 테스트
filename = '2025주문양식_클라레오키즈_2025_07월28일.xlsx'
df = pd.read_excel(filename)

print("=== 브랜드/상품명 분리 테스트 ===")
print(f"E열 컬럼명: {df.columns[4]}")

# 실제 데이터로 테스트
for i, value in enumerate(df.iloc[:5, 4]):
    if pd.notna(value):
        print(f"\n[테스트 {i+1}]")
        brand, product = test_brand_split(str(value))
        print(f"최종 결과 -> 브랜드: '{brand}', 상품명: '{product}'")
    else:
        print(f"\n[테스트 {i+1}] NaN 값")

print("\n=== 추가 테스트 케이스 ===")
test_cases = [
    " 클라레오(기린) 퐁퐁반팔세트 ",
    "새로빈 모달골지반팔실내복",
    " 브랜드명 상품명 ",
    "단일브랜드",
    " 앞공백만있음",
    "뒤공백만있음 ",
    ""
]

for i, test_case in enumerate(test_cases):
    print(f"\n[추가 테스트 {i+1}]")
    brand, product = test_brand_split(test_case)
    print(f"최종 결과 -> 브랜드: '{brand}', 상품명: '{product}'") 