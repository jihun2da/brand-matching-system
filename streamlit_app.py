import streamlit as st
import pandas as pd
import os
from datetime import datetime
import sys
import os
sys.path.append(os.path.dirname(__file__))

from brand_matching_system import BrandMatchingSystem
from file_processor import BrandFileProcessor
import io

# 페이지 설정
st.set_page_config(
    page_title="브랜드 매칭 시스템",
    page_icon="🔗",
    layout="wide"
)

# 커스텀 CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# 메인 헤더
st.markdown("""
<div class="main-header">
    <h1>🔗 브랜드 매칭 시스템</h1>
    <p>Excel 파일을 업로드하여 브랜드 상품을 자동으로 매칭하세요</p>
</div>
""", unsafe_allow_html=True)

# 초기화
@st.cache_resource
def init_system():
    """시스템 초기화 (캐시됨)"""
    try:
        matching_system = BrandMatchingSystem()
        file_processor = BrandFileProcessor()
        return matching_system, file_processor
    except Exception as e:
        st.error(f"시스템 초기화 중 오류 발생: {str(e)}")
        st.info("기본 모드로 실행합니다.")
        return None, None

def main():
    matching_system, file_processor = init_system()
    
    if matching_system is None or file_processor is None:
        st.error("🚨 시스템을 초기화할 수 없습니다.")
        st.markdown("""
        ### 💡 **해결 방법**
        1. 페이지를 새로고침해 보세요
        2. 몇 분 후 다시 시도해 보세요
        3. 문제가 지속되면 관리자에게 문의하세요
        """)
        return
    
    # 사이드바
    st.sidebar.title("📋 메뉴")
    menu = st.sidebar.selectbox(
        "작업 선택",
        ["매칭 처리", "시스템 정보", "사용법"]
    )
    
    if menu == "매칭 처리":
        show_matching_page(matching_system, file_processor)
    elif menu == "시스템 정보":
        show_info_page(matching_system)
    else:
        show_usage_page()

def show_matching_page(matching_system, file_processor):
    """매칭 처리 페이지"""
    
    # 두 개의 컬럼으로 나누기
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📁 파일 업로드")
        
        # 파일 업로드
        uploaded_files = st.file_uploader(
            "Excel 파일을 선택하세요 (여러 파일 가능)",
            type=['xlsx', 'xls'],
            accept_multiple_files=True,
            help="브랜드 정보가 포함된 Excel 파일을 업로드하세요"
        )
        
        if uploaded_files:
            st.markdown("""
            <div class="success-box">
                <strong>✅ 파일 업로드 완료!</strong><br>
                총 <strong>{}</strong>개 파일이 선택되었습니다.
            </div>
            """.format(len(uploaded_files)), unsafe_allow_html=True)
            
            # 업로드된 파일 목록 표시
            st.markdown("#### 📋 선택된 파일 목록")
            for i, file in enumerate(uploaded_files, 1):
                file_size = f"{file.size:,} bytes" if file.size < 1024*1024 else f"{file.size/(1024*1024):.1f} MB"
                st.markdown(f"**{i}.** `{file.name}` ({file_size})")
            
            # 매칭 실행 버튼
            st.markdown("---")
            if st.button("🚀 매칭 시작", type="primary", use_container_width=True):
                process_matching(uploaded_files, matching_system, file_processor)
        else:
            st.markdown("""
            <div class="info-box">
                <strong>📤 파일을 업로드해주세요</strong><br>
                위의 업로드 영역을 클릭하거나 파일을 드래그해주세요.
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 📊 시스템 현황")
        
        # 브랜드 데이터 정보
        if hasattr(matching_system, 'brand_data') and matching_system.brand_data:
            st.metric("🏷️ 브랜드 상품", f"{len(matching_system.brand_data):,}개")
        
        # 키워드 정보
        if hasattr(matching_system, 'keyword_list') and matching_system.keyword_list:
            st.metric("🔍 제외 키워드", f"{len(matching_system.keyword_list)}개")
        
        # 지원 형식 안내
        st.markdown("---")
        st.markdown("#### 📋 지원 형식")
        st.markdown("""
        - **파일 형식**: `.xlsx`, `.xls`
        - **최대 크기**: 50MB
        - **다중 선택**: 가능
        - **필수 컬럼**: 브랜드, 상품명
        """)
        
        # 매칭 규칙 안내
        st.markdown("#### 🎯 매칭 규칙")
        st.markdown("""
        1. 브랜드명 일치 확인
        2. 상품명 유사도 검사
        3. 사이즈/컬러 매칭
        4. 최적 점수 기반 선택
        """)

def process_matching(uploaded_files, matching_system, file_processor):
    """매칭 처리 실행"""
    temp_files = []  # 스코프 문제 해결
    try:
        # 진행 상황 표시
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # 1단계: 파일 읽기
        status_text.text("📖 파일을 읽는 중...")
        progress_bar.progress(20)
        
        # 업로드된 파일들을 임시로 저장하고 처리
        for uploaded_file in uploaded_files:
            temp_path = f"temp_{uploaded_file.name.replace(' ', '_')}"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            temp_files.append(temp_path)
        
        st.info(f"📁 {len(temp_files)}개 파일을 처리합니다.")
        
        # 2단계: 파일 결합
        status_text.text("🔗 파일을 결합하는 중...")
        progress_bar.progress(40)
        
        combined_df = file_processor.combine_excel_files(temp_files)
        st.info(f"📊 총 {len(combined_df)}개 행을 읽었습니다.")
        
        # 3단계: Sheet2 형식 변환
        status_text.text("📋 데이터를 변환하는 중...")
        progress_bar.progress(60)
        
        sheet2_df = matching_system.convert_sheet1_to_sheet2(combined_df)
        st.info(f"🔄 {len(sheet2_df)}개 행으로 변환했습니다.")
        
        # 4단계: 매칭 처리
        status_text.text("🎯 매칭을 수행하는 중...")
        progress_bar.progress(80)
        
        result_df = matching_system.process_matching(sheet2_df)
        
        # 5단계: 완료
        status_text.text("✅ 매칭 완료!")
        progress_bar.progress(100)
        
        # 결과 표시
        show_results(result_df)
        
        # 임시 파일 정리
        for temp_file in temp_files:
            if os.path.exists(temp_file):
                os.remove(temp_file)
                
    except Exception as e:
        st.error(f"❌ 오류 발생: {str(e)}")
        st.error(f"🔍 상세 오류: {type(e).__name__}")
        
        # 디버깅 정보 표시
        if temp_files:
            st.warning(f"📂 임시 파일들: {temp_files}")
        
        # 임시 파일 정리
        for temp_file in temp_files:
            if os.path.exists(temp_file):
                os.remove(temp_file)

def show_results(result_df):
    """결과 표시"""
    
    # 완료 메시지
    st.markdown("""
    <div class="success-box">
        <h3>🎉 매칭이 완료되었습니다!</h3>
        <p>결과를 확인하고 Excel 파일을 다운로드하세요.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 통계 정보
    st.markdown("### 📊 매칭 결과 통계")
    col1, col2, col3, col4 = st.columns(4)
    
    matched_count = len(result_df[result_df['매칭여부'] == 'Y'])
    unmatched_count = len(result_df[result_df['매칭여부'] == 'N'])
    
    with col1:
        st.metric("📦 총 상품 수", f"{len(result_df):,}개")
    
    with col2:
        st.metric("✅ 매칭 성공", f"{matched_count:,}개", 
                 delta=f"{matched_count}개 매칭")
    
    with col3:
        st.metric("❌ 매칭 실패", f"{unmatched_count:,}개")
    
    with col4:
        if len(result_df) > 0:
            success_rate = (matched_count / len(result_df)) * 100
            st.metric("📈 성공률", f"{success_rate:.1f}%",
                     delta=f"{success_rate:.1f}%" if success_rate >= 80 else None)
    
    # 결과 미리보기
    st.markdown("---")
    st.markdown("### 📋 결과 미리보기 (상위 10개)")
    
    # 매칭 성공/실패별 필터
    tab1, tab2, tab3 = st.tabs(["🔍 전체", "✅ 매칭 성공", "❌ 매칭 실패"])
    
    with tab1:
        st.dataframe(result_df.head(10), use_container_width=True)
    
    with tab2:
        success_df = result_df[result_df['매칭여부'] == 'Y']
        if len(success_df) > 0:
            st.dataframe(success_df.head(10), use_container_width=True)
        else:
            st.info("매칭 성공한 항목이 없습니다.")
    
    with tab3:
        fail_df = result_df[result_df['매칭여부'] == 'N']
        if len(fail_df) > 0:
            st.dataframe(fail_df.head(10), use_container_width=True)
        else:
            st.info("매칭 실패한 항목이 없습니다.")
    
    # 다운로드 섹션
    st.markdown("---")
    st.markdown("### 💾 결과 다운로드")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("""
        <div class="info-box">
            <strong>📁 Excel 파일로 저장</strong><br>
            매칭 결과를 Excel 파일로 다운로드할 수 있습니다.<br>
            파일명에는 현재 날짜와 시간이 포함됩니다.
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Excel 파일 생성
        excel_buffer = io.BytesIO()
        result_df.to_excel(excel_buffer, index=False, engine='openpyxl')
        excel_buffer.seek(0)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"브랜드매칭결과_{timestamp}.xlsx"
        
        st.download_button(
            label="📥 Excel 다운로드",
            data=excel_buffer.getvalue(),
            file_name=filename,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            type="primary",
            use_container_width=True
        )

def show_info_page(matching_system):
    """시스템 정보 페이지"""
    st.header("ℹ️ 시스템 정보")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 브랜드 데이터")
        if hasattr(matching_system, 'brand_data') and matching_system.brand_data:
            st.metric("브랜드 상품 수", len(matching_system.brand_data))
            
            # 브랜드별 통계
            if matching_system.brand_data:
                brands = {}
                for item in matching_system.brand_data:
                    brand = item.get('브랜드', 'Unknown')
                    brands[brand] = brands.get(brand, 0) + 1
                
                st.subheader("🏷️ 브랜드별 상품 수")
                brand_df = pd.DataFrame(list(brands.items()), columns=['브랜드', '상품수'])
                brand_df = brand_df.sort_values('상품수', ascending=False).head(10)
                st.dataframe(brand_df, use_container_width=True)
        else:
            st.warning("브랜드 데이터를 로드할 수 없습니다.")
    
    with col2:
        st.subheader("🔧 키워드 정보")
        if hasattr(matching_system, 'keyword_list') and matching_system.keyword_list:
            st.metric("제외 키워드 수", len(matching_system.keyword_list))
            
            # 키워드 목록 표시
            keywords_text = ", ".join(matching_system.keyword_list[:20])
            if len(matching_system.keyword_list) > 20:
                keywords_text += f" ... (총 {len(matching_system.keyword_list)}개)"
            st.text_area("키워드 목록 (상위 20개)", keywords_text, height=100)

def show_usage_page():
    """사용법 페이지"""
    st.header("📖 사용법")
    
    st.markdown("""
    ### 🚀 **매칭 프로세스**
    
    1. **파일 업로드**: Excel 파일(들)을 선택합니다
    2. **매칭 시작**: '매칭 시작' 버튼을 클릭합니다
    3. **결과 확인**: 매칭 결과와 통계를 확인합니다
    4. **다운로드**: 결과 파일을 다운로드합니다
    
    ### 📋 **파일 형식**
    
    - **지원 형식**: `.xlsx`, `.xls`
    - **필요 컬럼**: 브랜드, 상품명, 옵션 정보 등
    - **여러 파일**: 동시에 여러 파일 업로드 가능
    
    ### 🎯 **매칭 규칙**
    
    - **브랜드명** 일치 확인
    - **상품명** 유사도 검사 (키워드 제외 후)
    - **사이즈/컬러** 옵션 매칭
    - **우선순위** 기반 최적 매칭
    
    ### ⚠️ **주의사항**
    
    - 파일 크기는 50MB 이하로 제한됩니다
    - 처리 시간은 데이터 양에 따라 다릅니다
    - 결과 파일은 자동으로 다운로드됩니다
    """)

if __name__ == "__main__":
    main() 