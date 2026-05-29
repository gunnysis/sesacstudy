## 0. 메모
- git
```
git config --global user.name "gunny"
git config --global user.email "qkr133456@gmail.com"
```
`git config credential.helper store`
- 데이터셋 사이트
[https://aihub.or.kr/](https://)
[https://www.kaggle.com/datasets](https://)


## 1. 정적 페이지 크롤링
- requests
- BeautifulSoup
## 2. 동적 페이지 크롤링
- playwright
- selenium
## 3. 크롤링에 필요한 라이브러리 설치
```
pip install requests
pip install beautifulsoup4
pip install selenium
pip install openpyxl
pip install lxml
pip install pillow
pip install konlpy
pip install wordcloud
```
## 4. Windows 패키지 관리자(winget)를 사용하여 C++ 개발에 필요한 Visual Studio 빌드 도구(Build Tools)를 사용자 개입 없이 자동으로 설치
`winget install Microsoft.VisualStudio.BuildTools --override " --passive --wait --add Microsoft.VisualStudio.Workload.VCTools --includeRecommended" `
