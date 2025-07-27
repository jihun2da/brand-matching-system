# 🚀 Streamlit Cloud 배포 가이드

브랜드 매칭 시스템을 Streamlit Cloud에서 무료로 배포하는 방법을 안내합니다.

## ✨ **장점**
- 🆓 **완전 무료**
- ⚡ **매우 쉬운 배포** (클릭 몇 번)
- 🔗 **GitHub 자동 연동**
- 📱 **모바일 친화적**

## 📋 **배포 단계**

### **1단계: GitHub 커밋**

현재 폴더에서 다음 명령어 실행:

```bash
# 모든 변경사항 추가
git add .

# Streamlit 버전 커밋
git commit -m "Streamlit 버전 추가 및 배포 설정"

# GitHub에 푸시
git push
```

### **2단계: Streamlit Cloud 회원가입**

1. **[share.streamlit.io](https://share.streamlit.io)** 접속
2. **"Sign up with GitHub"** 클릭
3. GitHub 계정으로 로그인

### **3단계: 앱 배포**

1. **"New app"** 버튼 클릭
2. **설정 입력**:
   - **Repository**: `jihun2da/brand-matching-system`
   - **Branch**: `main`
   - **Main file path**: `매칭2/streamlit_app.py`
   - **App URL**: 원하는 주소 (예: `brand-matching`)

3. **"Deploy!"** 클릭

### **4단계: 완료 (2-3분 후)**

```
🎉 Your app is live!
🌐 https://brand-matching.streamlit.app
```

## 🔧 **고급 설정 (선택사항)**

### **환경 변수 설정**

Streamlit Cloud 대시보드에서:

1. 배포된 앱 클릭
2. **"Settings"** → **"Secrets"** 탭
3. 필요한 설정 추가:

```toml
# 예시
[general]
debug = false
max_file_size = 50

[matching]
similarity_threshold = 0.8
```

### **도메인 커스터마이징**

무료 플랜에서는 `*.streamlit.app` 형식만 가능하지만:
- 유료 플랜에서 커스텀 도메인 가능
- GitHub Pages와 연동 가능

## 📊 **Flask vs Streamlit 비교**

| 기능 | Flask 버전 | Streamlit 버전 |
|------|------------|----------------|
| **UI** | HTML/CSS/JS | 자동 생성 |
| **배포** | 복잡함 | 매우 쉬움 |
| **커스터마이징** | 높음 | 제한적 |
| **개발 속도** | 느림 | 빠름 |
| **파일 업로드** | 직접 구현 | 내장 기능 |
| **데이터 시각화** | 직접 구현 | 내장 기능 |

## 🚀 **로컬에서 Streamlit 실행**

```bash
# 매칭2 폴더로 이동
cd 매칭2

# Streamlit 앱 실행
streamlit run streamlit_app.py
```

브라우저에서 `http://localhost:8501` 접속

## 📱 **모바일 지원**

Streamlit은 자동으로 모바일 친화적 UI를 제공합니다:
- 반응형 레이아웃
- 터치 친화적 버튼
- 자동 스크롤

## 🔍 **문제 해결**

### **배포 실패 시**

1. **로그 확인**: Streamlit Cloud에서 빌드 로그 확인
2. **파일 경로**: `매칭2/streamlit_app.py` 경로 확인
3. **패키지 오류**: `requirements.txt` 확인

### **메모리 부족**

```python
# streamlit_app.py에 추가
import streamlit as st

# 메모리 사용량 제한
st.set_option('deprecation.showfileUploaderEncoding', False)
```

### **파일 업로드 제한**

```python
# 최대 파일 크기 설정 (200MB)
st.set_option('server.maxUploadSize', 200)
```

## 🎯 **성능 최적화**

### **캐싱 활용**

```python
@st.cache_data
def load_brand_data():
    # 브랜드 데이터 로딩
    pass

@st.cache_resource
def init_matching_system():
    # 매칭 시스템 초기화
    pass
```

### **세션 상태 관리**

```python
# 파일 업로드 상태 유지
if 'uploaded_files' not in st.session_state:
    st.session_state.uploaded_files = []
```

## 📈 **모니터링**

Streamlit Cloud에서 제공하는 기본 모니터링:
- 🔍 **앱 사용량** 통계
- 📊 **리소스 사용량**
- 🐛 **에러 로그**
- 👥 **사용자 접속** 정보

## 🔐 **보안**

### **기본 보안**
- HTTPS 자동 제공
- GitHub 계정 기반 인증
- 환경 변수 암호화

### **접근 제한 (선택)**

```python
# 비밀번호 보호
def check_password():
    def password_entered():
        if st.session_state["password"] == "your_password":
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        st.error("😞 Password incorrect")
        return False
    else:
        return True

if check_password():
    # 메인 앱 코드
    main()
```

## 🎉 **완료!**

이제 다음 두 가지 방법으로 앱을 사용할 수 있습니다:

1. **Streamlit 버전**: https://your-app.streamlit.app
2. **Flask 버전**: 기존 배포 방법들 (Render, Railway 등)

둘 다 동일한 매칭 로직을 사용하므로 결과는 동일합니다! 🚀 