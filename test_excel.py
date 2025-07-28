import pandas as pd

# 엑셀 파일 읽기
filename = '2025주문양식_클라레오키즈_2025_07월28일.xlsx'
df = pd.read_excel(filename)

print(f"컬럼 수: {len(df.columns)}")
print(f"행 수: {len(df)}")
print("\n컬럼명들:")
for i, col in enumerate(df.columns):
    print(f"  {i}: {col}")

print("\n상위 5개 행:")
print(df.head())

print("\nE열(4번째 인덱스) 샘플 데이터:")
if len(df.columns) > 4:
    print("E열 데이터 타입:", type(df.iloc[0, 4]))
    print("E열 상위 10개 샘플:")
    for i, value in enumerate(df.iloc[:10, 4]):
        if pd.notna(value):
            print(f"  행 {i}: '{value}' (길이: {len(str(value))}, 띄어쓰기 있음: {' ' in str(value)})")
            if ' ' in str(value):
                parts = str(value).split(' ', 1)
                print(f"    -> 분할: 브랜드='{parts[0]}', 상품명='{parts[1] if len(parts) > 1 else ''}'")
        else:
            print(f"  행 {i}: NaN 또는 빈 값")
else:
    print("5번째 컬럼이 없습니다!")

print("\n브랜드/상품명 분리 가능성 분석:")
if len(df.columns) > 4:
    e_col_data = df.iloc[:, 4].dropna()
    total_rows = len(e_col_data)
    has_space = sum(1 for x in e_col_data if ' ' in str(x))
    print(f"  총 데이터 행: {total_rows}")
    print(f"  띄어쓰기 포함 행: {has_space}")
    print(f"  띄어쓰기 포함 비율: {has_space/total_rows*100:.1f}%" if total_rows > 0 else "  데이터 없음") 