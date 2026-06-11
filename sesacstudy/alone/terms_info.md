# 데이터 정제(전처리) 핵심 용어 정리

> 새싹 AI 교안 **2회차(데이터 구성 정제)** · **3회차(데이터 세부내용 정제)** 내용을 정리한 학습 노트.
> 각 항목은 **개념 → 왜 쓰는지 → 코드 예시 → 주의/공식 문서** 순서로 구성했다.
> 코드 예시의 `reserve_tb`(예약), `hotel_tb`(호텔), `customer_tb`(고객), `production_tb`(제조)는 교안 실습용 테이블이다.

---

## 📦 2회차 — 데이터 구성 정제

> "데이터의 **모양과 단위**를 바꾸는" 단계. 행/열을 고르고, 합치고, 요약하고, 나눈다.

## 1. 데이터 추출 — 필요한 행·열만 고르기

### 1-1. 열(column) 추출

```python
# 방법1: 대괄호에 열 이름 리스트 → 새 DataFrame 반환(원본 유지)
reserve_tb[['reserve_id', 'hotel_id', 'customer_id']]

# 방법2: loc[행, 열] — 2차원으로 행/열 동시 지정
reserve_tb.loc[:, ['reserve_id', 'hotel_id']]

# 방법3: drop — 불필요한 열을 제거 (axis=1=열, inplace=True면 원본 갱신)
reserve_tb.drop(['people_num', 'total_price'], axis=1, inplace=True)
```

> 💡 방법1·2는 **새 결과를 반환**(원본 그대로), 방법3의 `inplace=True`는 **원본을 직접 수정**한다.

### 1-2. 행(row) 추출 — 조건으로 거르기

```python
# 방법1: 불리언 마스크 (조건이 True인 행만)
reserve_tb[(reserve_tb['checkout_date'] >= '2016-10-13') &
           (reserve_tb['checkout_date'] <= '2016-10-14')]

# 방법2: loc 로 조건 지정
reserve_tb.loc[(reserve_tb['checkout_date'] >= '2016-10-13'), :]

# 방법3: query — 문자열 조건식 (가독성 좋음)
reserve_tb.query('"2016-10-13" <= checkout_date <= "2016-10-14"')
```

- 조건을 여러 개 묶을 때 각 조건을 `()`로 감싸고 `&`(AND) / `|`(OR)로 연결한다.

### 1-3. `isin()` — 목록에 포함되는 값만 추출 ⭐

특정 값 **목록(리스트) 중 하나와 일치**하는 행만 고른다. "이 열의 값이 리스트 안에 있는가?"를 행마다 `True/False`로 돌려준다.

```python
target = ['c_1', 'c_2']
reserve_tb[reserve_tb['customer_id'].isin(target)]   # c_1 또는 c_2 인 행
reserve_tb[~reserve_tb['customer_id'].isin(target)]  # ~ = NOT (포함되지 않는 행)
```

- `==`는 값 **하나**와, `isin()`은 값 **여러 개**와 비교한다.
- 📖 [pandas.DataFrame.isin](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.isin.html)

### 1-4. 샘플링 — 무작위로 일부만 뽑기

```python
reserve_tb.sample(frac=0.5)   # 전체의 50% 무작위 추출
```

> ⚠️ **분석 단위와 샘플링 단위를 맞춰야 한다.** 예) "고객 단위" 분석인데 "예약 1건 단위"로 샘플링하면
> 예약을 많이 한 고객이 과대표집되어 결과가 왜곡된다.
> → 해결: 고객 ID를 먼저 중복 제거(`unique`)해 샘플링한 뒤, 그 고객들의 레코드만 `isin`으로 추출.
>
> ```python
> target = pd.Series(reserve_tb['customer_id'].unique()).sample(frac=0.5)
> reserve_tb[reserve_tb['customer_id'].isin(target)]
> ```

---

## 2. 집계(Aggregation) — 분석 단위 바꾸기

여러 행을 **하나의 대표값으로 요약**하는 것. **정보 손실을 최소화하면서 분석 단위(행의 의미)를 바꾸는** 대표 기법이다.
예: "예약 1건 단위" → "호텔 1개 단위"(호텔별 예약 수). `groupby`로 묶을 단위를 정하고 집계 함수를 적용한다.

### 2-1. 개수 — `count` / `nunique`

```python
result = reserve_tb.groupby('hotel_id') \
    .agg({'reserve_id': 'count', 'customer_id': 'nunique'})
result.reset_index(inplace=True)                      # 그룹 키를 일반 열로
result.columns = ['hotel_id', 'rsv_cnt', 'cus_cnt']   # 열 이름 재설정
```

- `'count'` = **중복 포함** 개수, `'nunique'` = **중복 제외**(고유값) 개수.
- `agg({열: 함수})` 딕셔너리로 **여러 집계를 한 번에** 지정.

### 2-2. 합계·대표값 — `sum / mean / max / min / median / percentile`

```python
# 호텔×인원수 2단계 그룹의 매출 합계
result = reserve_tb.groupby(['hotel_id', 'people_num'])['total_price'] \
    .sum().reset_index()
result.rename(columns={'total_price': 'price_sum'}, inplace=True)

# 한 번에 여러 통계량 (백분위수는 lambda + np.percentile)
import numpy as np
reserve_tb.groupby('hotel_id').agg(
    {'total_price': ['max', 'min', 'mean', 'median',
                     lambda x: np.percentile(x, q=20)]})
```

> 🧮 **쉽게 이해하기 — 백분위수(percentile)와 중앙값(median)**
>
> 값들을 **작은 순서로 한 줄로 세웠을 때**, "앞에서 몇 %번째 자리"의 값을 말한다.
>
> - **중앙값(median)** = 50번째 백분위수 = 딱 가운데 사람의 값. (평균과 달리 극단값에 안 휘둘림)
> - **20번째 백분위수(`q=20`)** = 앞에서 20% 자리의 값. "하위 20%는 이 값 이하"라는 뜻.
>
> 예) 점수 `10, 30, 50, 70, 90` 이면 → 중앙값은 한가운데인 `50`, 20번째 백분위수는 하위 20% 근처인 `30`쯤.
> 평균은 큰 값 하나에 쉽게 끌려가지만, 중앙값/백분위수는 **순서(위치)** 기준이라 극단값에 강하다.

### 2-3. 분산·표준편차 — `var` / `std` (분포의 퍼짐 정도)

| 통계량 | 의미 | 비고 |
| --- | --- | --- |
| **분산 (var)** | 값이 평균에서 떨어진 정도를 제곱해 평균낸 값 | 단위가 원래의 제곱이라 직관적이지 않음 |
| **표준편차 (std)** | 분산에 √(제곱근)를 씌운 값 | **원래 데이터와 단위가 같아** 해석이 쉬움 |

> 🧮 **쉽게 이해하기 — "얼마나 흩어져 있나?"를 숫자로**
>
> 두 반의 시험 점수를 보자. 둘 다 **평균은 50점**이다.
> - A반: `50, 50, 50, 50` → 모두 평균과 똑같음. 전혀 안 흩어짐.
> - B반: `10, 50, 50, 90` → 평균은 같지만 위아래로 멀리 퍼져 있음.
>
> 평균만 보면 두 반이 똑같아 보이지만, 실제로는 다르다. 이 "**퍼진 정도**"를 숫자로 만든 게 분산·표준편차다.
>
> **분산 구하는 순서** (B반으로):
>
> 1. 각 값이 평균(50)에서 얼마나 떨어졌나 → `-40, 0, 0, +40`
> 2. 부호(+/−)를 없애려고 **제곱** → `1600, 0, 0, 1600`
>    *(왜 제곱? 그냥 더하면 +40과 −40이 상쇄돼 0이 되니까, 제곱해서 전부 양수로 만든다.)*
> 3. 평균 냄 → `(1600+0+0+1600) / 4 = 800` ← 이게 **분산**
> 4. 제곱했던 걸 되돌리려 **√(루트)** → `√800 ≈ 28.3` ← 이게 **표준편차**
>
> 표준편차 28.3점은 "보통 평균에서 ±28점쯤 떨어져 있다"는 뜻으로 바로 와닿는다. (A반은 분산·표준편차 모두 0)

```python
result = reserve_tb.groupby('hotel_id') \
    .agg({'total_price': ['var', 'std']}).reset_index()
result.columns = ['hotel_id', 'price_var', 'price_std']
result.fillna(0, inplace=True)   # 데이터 1개라 분산이 NaN이면 0으로 대체
```

> 💡 분산·std가 **클수록** 넓게 퍼져 있고, **작을수록** 평균 근처에 몰려 있다.
> 평균/중앙값이 "중심(어디에 모여 있나)"이라면, 분산/표준편차는 "흩어진 정도(얼마나 퍼졌나)"를 나타낸다.

### 2-4. 최빈값 — `mode` (가장 자주 나오는 값)

```python
reserve_tb['total_price'].round(-3).mode()   # round(-3): 천 단위 반올림 후 최빈값
```

- `round(-3)`으로 **비슷한 가격대를 묶은 뒤** 최빈값을 구하면 의미 있는 결과가 나온다.

### 2-5. 순위 — `rank` (그룹 내 순서 매기기)

```python
# 고객별, 예약시간이 빠른 순으로 순번 부여
reserve_tb['log_no'] = reserve_tb.groupby('customer_id')['reserve_datetime'] \
    .rank(ascending=True, method='first')
```

- `method='first'` : 동점이면 **먼저 등장한 행**이 앞 순위
- `method='min'` : 동점이면 **같은 순위**를 주고 다음 순위는 건너뜀 (1,2,2,4…)
- `ascending=False` : 내림차순(큰 값이 1등)

- 📖 [pandas groupby](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.groupby.html)

---

## 3. 여러 테이블 합치기 (Join / Merge)

### 3-1. 기본 결합 — `merge`

키(공통 열)를 기준으로 두 테이블을 옆으로 붙인다.

```python
# 숙박 1명(people_num==1) & 영업중(is_business)인 비즈니스 예약만
pd.merge(reserve_tb.query('people_num == 1'),
         hotel_tb.query('is_business'),
         on='hotel_id', how='inner')
```

- `how='inner'` : 양쪽에 **공통으로 있는 키**만 (교집합)
- `how='left'` : 왼쪽은 전부 유지, 오른쪽은 매칭되는 것만 (없으면 NaN)
- 키 이름이 다르면 `left_on='checkin_date', right_on='target_day'`

### 3-2. Cross Join — 양쪽 모든 조합 만들기

두 테이블의 **모든 행 조합**을 생성. 집계·학습용 데이터 틀을 만들 때 사용.

```python
# 최신 pandas: how='cross' 한 줄로
pd.merge(customer_tb[['customer_id']], month_mst, how='cross')

# 예전 방식(교안): 더미 키 join_key=0 을 양쪽에 만들고 그 키로 merge
customer_tb['join_key'] = 0
month_mst['join_key'] = 0
pd.merge(customer_tb[['customer_id', 'join_key']], month_mst, on='join_key')
```

### 3-3. Self Join — 같은 테이블을 자기 자신과 결합

"같은 고객의 과거 N일 예약"처럼 **한 행에 같은 그룹의 다른 행 정보**를 붙일 때.

```python
# 같은 고객(customer_id)끼리 결합 → 과거 90일 예약 합계
sum_table = pd.merge(
    reserve_tb[['reserve_id', 'customer_id', 'reserve_datetime']],
    reserve_tb[['customer_id', 'reserve_datetime', 'total_price']]
        .rename(columns={'reserve_datetime': 'reserve_datetime_before'}),
    on='customer_id')
```

### 3-4. 과거 데이터 활용 — `shift` / `rolling`

| 함수 | 역할 |
| --- | --- |
| `shift(periods=n)` | 열 전체를 **n칸 아래로 이동** (직전 값 가져오기) |
| `rolling(window=n).sum()/mean()` | **n행짜리 이동 창**에서 합/평균 (이동 집계) |

```python
# 직전 예약 2건의 금액을 같은 행에 붙이기
result['before_price'] = result.groupby('customer_id')['total_price'].shift(periods=2)

# 본 건 포함 과거 3건 합계 (최소 3건 모여야 계산)
result['price_sum'] = (result.groupby('customer_id')['total_price']
    .rolling(window=3, min_periods=3).sum().reset_index(drop=True))
```

- 📖 [pandas.merge](https://pandas.pydata.org/docs/reference/api/pandas.merge.html)

---

## 4. 학습용/검증용 데이터 나누기 (Data Split)

예측 모델을 **공정하게 평가**하려고 데이터를 역할별로 나눈다. 모델이 **본 적 없는 데이터**에서도 잘 맞히는지(일반화 성능)를 확인하는 게 목적.

- **학습(train)** : 모델 학습용
- **검증(validation)** : 하이퍼파라미터 튜닝·모델 선택용
- **테스트(test)** : 최종 성능 평가용 (학습 중엔 절대 보지 않음)

> 💡 정제는 학습/검증을 **같이** 처리하고, **모델에 넣기 직전에 분할**하는 것이 좋다.
> 정답을 모르는 "적용(운영) 데이터"는 분할할 필요가 없다.

### 4-1. 홀드아웃 + 교차검증 (K-Fold)

- **홀드아웃 검증** : 최종 평가용 테스트 데이터를 **미리 따로** 떼어 둔다.
- **교차검증(Cross Validation)** : 남은 데이터를 K조각으로 나눠, 번갈아 1조각=검증·나머지=학습으로 K번 평가 후 평균.

```python
from sklearn.model_selection import train_test_split, KFold

# 홀드아웃: 정답(fault_flg) 분리, 테스트 20%
train_data, test_data, train_target, test_target = train_test_split(
    production_tb.drop('fault_flg', axis=1),
    production_tb[['fault_flg']], test_size=0.2)

# 교차검증: 4조각 → 학습3 : 검증1
k_fold = KFold(n_splits=4, shuffle=True)
for train_idx, test_idx in k_fold.split(range(len(train_target))):
    train_cv = train_data.iloc[train_idx, :]
    test_cv  = train_data.iloc[test_idx, :]
```

### 4-2. 시계열 데이터 분할

시간 데이터는 **과거로 학습 → 미래로 검증**해야 한다(미래 정보가 학습에 새면 안 됨). 학습 창을 고정하거나 점점 늘려가며 윈도우를 이동시킨다.

```python
# sklearn 내장: 시계열 전용 분할기
from sklearn.model_selection import TimeSeriesSplit
for train_idx, test_idx in TimeSeriesSplit(n_splits=4).split(data):
    ...   # train_idx는 항상 test_idx보다 과거
```

> ⚠️ 테스트 데이터를 학습에 쓰면 점수가 부풀려진다(**데이터 누수, data leakage**).
> 📖 [sklearn train_test_split](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html) ·
> [KFold](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.KFold.html)

---

## 5. 불균형 데이터 보정 — 오버/언더 샘플링

분류 문제에서 한 클래스가 **지나치게 많거나 적으면**(클래스 불균형), 모델이 다수 클래스로만 치우쳐 예측한다. 개수를 인위적으로 맞춰 보정한다.

| 방법 | 설명 | 단점 |
| --- | --- | --- |
| **오버샘플링** | **소수** 클래스 데이터를 **늘림** | 과학습(overfitting) 위험 |
| **언더샘플링** | **다수** 클래스 데이터를 **줄임** | 정보 손실 위험 |

### SMOTE (Synthetic Minority Over-sampling Technique) ⭐

단순 복사는 똑같은 점만 늘려 과학습되기 쉽다. SMOTE는 복사 대신 **새 합성 데이터를 만든다.**

**동작 원리:** ① 소수 클래스 샘플 선택 → ② 그 샘플의 **k-최근접 이웃**(보통 k=5) 찾기 → ③ 이웃 하나를 골라 **두 점을 잇는 선분 위 임의 지점**에 새 점 생성(보간, interpolation).

> 🧮 **쉽게 이해하기 — "보간(interpolation)"이 뭐죠?**
>
> 보간 = **이미 있는 두 점 "사이"에 새 점을 끼워 넣기**.
> 예를 들어 키 데이터에 `160cm`와 `170cm` 두 사람이 있으면, 그 사이 어딘가(예: `164cm`)에 가상의 데이터를 하나 만드는 것.
>
> - **단순 복사**라면 `160`을 그대로 또 하나 만든다 → 똑같은 점만 쌓여 모델이 그 점만 외워버림(과학습).
> - **SMOTE(보간)**는 `160`과 이웃 `170` 사이의 `164` 같은 **새로운** 값을 만든다 → 자연스럽게 데이터가 늘어남.
>
> "k-최근접 이웃"은 그냥 **가장 가까이 있는 k명의 친구**라는 뜻이다(→ 8-4 KNN 참고).

```python
# pip install imbalanced-learn
from imblearn.over_sampling import SMOTE

sm = SMOTE(sampling_strategy='auto', k_neighbors=5, random_state=71)
balance_data, balance_target = sm.fit_resample(
    production_tb[['length', 'thickness']], production_tb['fault_flg'])
```

> ⚠️ 교안 코드와 최신 버전 차이: 옛 `ratio=` → **`sampling_strategy=`**, 옛 `fit_sample()` → **`fit_resample()`**.
> ⚠️ SMOTE는 **학습 데이터에만** 적용 (분할 전 적용 시 데이터 누수).
> "원본 특성은 유지하되 약간 다른" 데이터지만, 정확히는 단순 노이즈가 아니라 **이웃 사이 보간**이다.
> 📖 [imbalanced-learn SMOTE](https://imbalanced-learn.org/stable/references/generated/imblearn.over_sampling.SMOTE.html)

---

## 6. 전개(Spread / Pivot)와 희소 행렬

### 6-1. 전개 — 세로(long) → 가로(wide)

집계 결과를 **표 형태로 펼치는** 것. 추천 시스템 입력(행=사용자, 열=상품, 값=점수)을 만들 때 자주 쓴다. pandas에서는 `pivot_table`.

```python
# 행=고객, 열=투숙객수, 값=예약건수
pd.pivot_table(reserve_tb, index='customer_id', columns='people_num',
               values='reserve_id', aggfunc=lambda x: len(x), fill_value=0)
```

| 형태 | 설명 |
| --- | --- |
| **세로(long)** | `연령대 / 성별 / 인원수` 처럼 행이 길게 쌓인 형태 |
| **가로(wide)** | `연령대 \| 남성수 \| 여성수` 처럼 펼쳐진 표 |

- 📖 [pandas.pivot_table](https://pandas.pydata.org/docs/reference/api/pandas.pivot_table.html)

### 6-2. 희소 행렬(Sparse Matrix)

가로로 펼치면 **대부분의 값이 0**이고 극히 일부만 값을 갖는 **거대한 행렬**이 되기 쉽다. 0을 전부 저장하면 메모리 낭비이므로, **0이 아닌 값과 그 위치만** 저장해 절약한다.

| 형식 | 특징 | 언제 쓰나 |
| --- | --- | --- |
| **lil_matrix** | 값 **갱신(삽입/수정)이 빠름**, 연산은 느림 | 행렬을 **하나씩 채워 만들 때** |
| **csr_matrix** | **행(row) 접근**·연산이 빠름 | 다 만든 뒤 **연산**(행 기준) |
| **csc_matrix** | **열(column) 접근**·연산이 빠름 | 다 만든 뒤 **연산**(열 기준) |

```python
from scipy.sparse import csc_matrix

# 카테고리형으로 행/열 인덱스 준비
customer_id = pd.Categorical(cnt_tb['customer_id'])
people_num  = pd.Categorical(cnt_tb['people_num'])

# (값, (행번호, 열번호)) + shape 로 희소 행렬 생성
sparse_matrix = csc_matrix(
    (cnt_tb['rsv_cnt'], (customer_id.codes, people_num.codes)),
    shape=(len(customer_id.categories), len(people_num.categories)))
sparse_matrix.toarray()   # 일반 행렬로 펼쳐 확인
```

- 형식 간 변환: `tolil()`, `tocsr()`, `tocsc()`
- 📖 [scipy.sparse](https://docs.scipy.org/doc/scipy/reference/sparse.html)

---

## 🔬 3회차 — 데이터 세부내용 정제

> "각 **값 자체를 가공**하는" 단계. 수치·범주·일시·위치 데이터를 모델이 다루기 좋게 변환한다.

## 7. 수치 데이터 정제

### 7-1. 자료형 변환 — `astype`

수치열은 보통 자동으로 수치형이 되지만, 문자가 섞이거나 정수↔실수 변환이 필요하면 직접 바꾼다.

```python
df['value'].astype('int8')     # int8/16/32/64 (정수, 크기 선택)
df['value'].astype('float64')  # float16/32/64/128 (실수)
df.dtypes                      # 현재 자료형 확인
```

> 💡 작은 자료형(int8 등)을 쓰면 메모리를 아끼지만, 값 범위를 벗어나면 오버플로가 나니 주의.

### 7-2. 대수화(로그 변환) — 비선형 → 선형 ⭐

직선 하나로 안 맞는 **비선형 관계**를, 값에 로그를 씌워(`b = logₐx`) 선형 모델로도 다룰 수 있게 만든다.

> 🧮 **쉽게 이해하기 — 로그(log)는 "큰 숫자를 작게 줄여주는 도구"**
>
> 로그는 **자릿수 세기**라고 생각하면 쉽다. `log10`(밑이 10인 로그)으로 보면:
>
> - `log10(10) = 1`, `log10(100) = 2`, `log10(1000) = 3`, `log10(10000) = 4`
> - 즉 원래 값이 **10배씩 커져도** 로그 값은 **1씩만** 커진다. 큰 값일수록 팍팍 눌러준다.
>
> **왜 쓰나?** 데이터에 `100원`짜리와 `1,000,000원`짜리가 섞여 있으면 큰 값이 분석을 다 잡아먹는다.
> 로그를 씌우면 `2`와 `6`처럼 차이가 확 줄어서 **고만고만한 범위**로 모인다 → 모델이 다루기 편해짐.
>
> - 또 한쪽으로 길게 늘어진(한쪽에 몰린) 분포를 **고르게 펴주는** 효과도 있다.
> - "10대↔20대 차이"는 크게, "60대↔70대 차이"는 작게 — 큰 값일수록 차이를 줄여서 보고 싶을 때 적합.

**언제?** ① 한쪽으로 심하게 **치우친(skew)** 분포를 정규분포에 가깝게 펼 때 ② 값 범위(scale) 차이가 매우 클 때 ③ "10대↔20대"와 "60대↔70대"의 차이를 다르게 반영하고 싶을 때(로그는 큰 값일수록 차이를 압축).

```python
import numpy as np
# 교안: 1000으로 나누고 +1 후 log10 (x=0일 때 log(0)=-∞ 회피)
reserve_tb['total_price_log'] = reserve_tb['total_price'].apply(
    lambda x: np.log10(x / 1000 + 1))

# 일반적으로는 log1p(=log(1+x)) / 역변환 expm1 권장
df['가격_log'] = np.log1p(df['가격'])
원래값 = np.expm1(df['가격_log'])
```

> ⚠️ 로그는 **양수에만** 정의된다 → 0/음수가 있으면 `log1p`를 쓰거나 +1 등으로 보정.

### 7-3. 범주화(Binning / 이진화)

연속 수치를 **구간이나 참/거짓 플래그**로 바꾸는 것. 대수화만으로 표현이 어려운 **복잡한(계단식) 변화**에 사용.

```python
# 구간화: 나이를 10단위 범주로 (np.floor로 내림 → 카테고리)
customer_tb['age_rank'] = (np.floor(customer_tb['age'] / 10) * 10).astype('category')

# 이진화: 임계값 기준 True/False ("0~9세 플래그", "60세 이상 플래그" 등)
df['고령자'] = df['age'] >= 65

# pandas.cut: 경계를 직접 지정해 구간 라벨 붙이기
df['연령대'] = pd.cut(df['age'], bins=[0, 20, 40, 60, 120],
                    labels=['청년', '중년', '장년', '노년'])
```

> 💡 구간으로 묶으면 이상치 영향이 줄고 비선형 패턴을 단순화할 수 있지만, 너무 거칠게 나누면 정보가 손실된다.
> 📖 [pandas.cut](https://pandas.pydata.org/docs/reference/api/pandas.cut.html)

### 7-4. 정규화(Normalization / Scaling)

열마다 **값의 범위(스케일)를 통일**하는 변환. 단위·크기가 제각각이면(키 170 vs 연봉 5천만) 큰 값이 학습을 지배하므로, **거리 기반(KNN/K-means/SVM)·경사하강법 기반** 모델에서 특히 중요.

> 🧮 **쉽게 이해하기 — 왜 "범위를 맞춰" 줘야 하나?**
>
> 키(150~180, 차이 30 정도)와 연봉(3천만~1억, 차이 7천만)을 같이 쓰면, 숫자가 큰 연봉이 결과를 거의 다 결정한다.
> 키는 무시당하는 셈. 그래서 **단위가 다른 값들을 공통의 잣대로 맞추는** 게 정규화다. (예: "달리기 1등 vs 시험 1등"을 비교하려면 등수처럼 같은 잣대가 필요한 것과 같다.)

| 방법 | 식 | 결과 | 특징 |
| --- | --- | --- | --- |
| **표준화 (StandardScaler)** | (x − 평균) / 표준편차 | **평균 0, 분산 1** | 이상치에 상대적으로 덜 민감 |
| **Min-Max (MinMaxScaler)** | (x − min) / (max − min) | **최소 0, 최대 1** | 범위를 딱 맞춤, 이상치에 민감 |

> 🧮 **위 두 식, 말로 풀면**
>
> - **표준화 `(x − 평균) / 표준편차`** : "이 값은 평균에서 **표준편차 몇 개만큼** 떨어져 있나?"를 구하는 것.
>   결과가 `0`이면 평균과 같음, `+1`이면 평균보다 표준편차 1개만큼 큼, `−2`면 평균보다 2개만큼 작음.
>   예) 평균 50, 표준편차 10인 점수에서 내 점수 70 → `(70−50)/10 = +2` (평균보다 꽤 잘함).
> - **Min-Max `(x − min) / (max − min)`** : 가장 작은 값을 `0`, 가장 큰 값을 `1`로 두고 **0~1 사이로 비율 변환**.
>   예) 점수 범위 0~100점에서 80점 → `(80−0)/(100−0) = 0.8`. 시험 점수를 "0~1 비율"로 바꾸는 느낌.

```python
from sklearn.preprocessing import StandardScaler

reserve_tb['people_num'] = reserve_tb['people_num'].astype(float)  # 소수 대비 실수화
ss = StandardScaler()
result = ss.fit_transform(reserve_tb[['people_num', 'total_price']])
reserve_tb['people_num_normalized']  = [x[0] for x in result]
reserve_tb['total_price_normalized'] = [x[1] for x in result]
```

> ⚠️ 스케일러는 **학습 데이터로만 `fit`**, 테스트엔 `transform`만 (테스트 통계로 fit하면 누수).
> 📖 [sklearn preprocessing](https://scikit-learn.org/stable/modules/preprocessing.html)

### 7-5. 이상값(Outlier) 처리

대부분 값보다 극단적으로 크거나 작은 값. 정규화·모델 학습에 나쁜 영향을 주므로 정제 단계에서 제거한다.

**3-시그마 규칙**: 정규분포에서 값의 **99.73%가 평균 ±(표준편차×3)** 안에 있으므로, 그 범위를 벗어난 약 0.27%를 이상값으로 본다.

> 🧮 **쉽게 이해하기 — "시그마(σ)"는 표준편차의 다른 이름**
>
> 시그마(σ) = 표준편차. "평균을 한가운데 두고, 양옆으로 표준편차 몇 칸까지 보느냐"의 칸 수가 1·2·3 시그마다.
> 종 모양(정규분포) 그래프에서:
>
> - 평균 ±**1**칸 안에 약 **68%**
> - 평균 ±**2**칸 안에 약 **95%**
> - 평균 ±**3**칸 안에 약 **99.7%** ← 거의 다 들어옴
>
> 그래서 **평균에서 3칸(±3σ)보다 더 멀리 있는 값**은 "정상이라 보기엔 너무 드문 값"이라 이상값으로 간주한다.
> 예) 평균 50, 표준편차 10이면 정상 범위는 `50 ± 30` = `20~80`. → `200` 같은 값은 너무 멀어서 이상값.
>
> 아래 코드의 `|x − 평균| / 표준편차 <= 3` 은 "평균에서 표준편차 **3칸 이내**인 행만 남겨라"라는 뜻이다.
> (`| |` 는 절댓값 = 부호 떼고 거리만 보기. 위로 멀든 아래로 멀든 똑같이 "거리"로 따진다.)

```python
import numpy as np
# |x - 평균| / 표준편차 <= 3 인 행만 남김
reserve_tb = reserve_tb[
    (abs(reserve_tb['total_price'] - np.mean(reserve_tb['total_price']))
     / np.std(reserve_tb['total_price'])) <= 3
].reset_index()
```

### 7-6. 주성분 분석(PCA) — 차원 축소

입력 변수(차원)가 많을수록 학습에 필요한 데이터가 커진다. PCA는 변수 간 **상관관계를 이용해 차원을 줄여**(예: x,y 2차원 → z 1차원) 정보 손실을 최소화하며 압축한다.

> 🧮 **쉽게 이해하기 — "차원 축소"는 짐을 잘 싸는 것**
>
> "차원"은 그냥 **열(컬럼)의 개수**라고 보면 된다. 키·몸무게·허리둘레… 변수가 많을수록 차원이 높다.
> 그런데 키와 몸무게처럼 **서로 비슷하게 움직이는(상관관계 높은)** 변수들은 사실상 같은 얘기를 두 번 하는 셈이다.
>
> PCA는 이런 겹치는 정보를 **하나로 합쳐** 변수 개수를 줄인다.
> 비유하면, 입체(3D) 물건을 사진(2D) 한 장으로 찍는 것 — 약간의 정보는 잃지만 핵심 모양은 거의 살아 있다.
>
> - **장점**: 열이 줄어 학습이 가볍고 빨라짐.
> - **누적 기여율**: "사진이 원본을 몇 % 담고 있나"를 나타내는 점수. 90%면 원본의 90%를 보존했다는 뜻.

```python
from sklearn.decomposition import PCA

pca = PCA(n_components=2)                 # 주성분 2개로 축소
pca_values = pca.fit_transform(production_tb[['length', 'thickness']])
print('누적 기여율:', sum(pca.explained_variance_ratio_))   # 원본 정보 보존 비율
print('각 차원 기여율:', pca.explained_variance_ratio_)
```

> 💡 **기여율(explained_variance_ratio_)**: 각 주성분이 원본 데이터의 정보를 얼마나 설명하는지. 누적 기여율이 높을수록 압축 손실이 적다.

### 7-7. 결측값(Missing Value) 처리

| 방법 | 설명 | 코드 |
| --- | --- | --- |
| **행 제거** | 결측 레코드를 버림 | `df.dropna(subset=['thickness'], inplace=True)` |
| **고정값 대체** | 정해진 값으로 채움 | `df['thickness'].fillna(1, inplace=True)` |
| **평균값 대체** | 평균으로 채움 | `df['thickness'].fillna(df['thickness'].mean(), inplace=True)` |

```python
# 'None' 문자열을 먼저 진짜 결측(np.nan)으로 바꿔야 dropna/fillna가 동작
production_miss_num.replace('None', np.nan, inplace=True)
production_miss_num['thickness'] = production_miss_num['thickness'].astype('float64')
```

> 그 밖에 예측값 대체, 시간관계 보완, 다중대입법, 최대가능도, **KNN 보완**(→ 8-4) 등이 있다.

---

## 8. 범주 데이터 정제

### 8-1. 범주형(Categorical) 변환

범주형은 **가질 수 있는 값의 종류가 정해진** 데이터(성별, 등급 등). pandas `Categorical`은 값을 정수 코드로 내부 저장해 메모리를 아낀다.

```python
# 불리언: man이면 True
customer_tb['sex_is_man'] = (customer_tb['sex'] == 'man').astype('bool')

# 범주형: 카테고리 목록 지정
customer_tb['sex_c'] = pd.Categorical(customer_tb['sex'], categories=['man', 'woman'])
customer_tb['sex_c'].cat.codes        # 인덱스(코드)는 codes 에 저장
customer_tb['sex_c'].cat.categories   # 카테고리 목록은 categories 에 저장
```

### 8-2. 더미 변수화(One-Hot Encoding)

일부 머신러닝 함수는 범주형을 직접 못 받는다. 이때 범주값을 **여러 개의 0/1 플래그 열**로 바꾸는 것이 더미 변수화.

```python
customer_tb['sex'] = pd.Categorical(customer_tb['sex'])
dummy_vars = pd.get_dummies(customer_tb['sex'], drop_first=False)
#  → sex_man, sex_woman 두 열(각 행에 1/0)
```

> 💡 `drop_first=True`로 더미 열을 하나 줄이면(예: woman 열 제거, man=0이면 곧 woman) 학습 변수를 줄일 수 있다.
> 다만 정보가 줄어 **성능에 영향**을 줄 수 있으니 모델에 따라 선택한다.

### 8-3. 범주 그룹 단순화(집약)

데이터 수가 **극단적으로 적은 범주값**을 다른 범주와 묶는 것을 **범주값의 집약**이라 한다. (예: 60·70·80대 → "60 이상")

```python
customer_tb['age_rank'] = pd.Categorical(np.floor(customer_tb['age'] / 10) * 10)
customer_tb['age_rank'] = customer_tb['age_rank'].cat.add_categories(['60 이상'])
customer_tb.loc[customer_tb['age_rank'].isin([60.0, 70.0, 80.0]), 'age_rank'] = '60 이상'
customer_tb['age_rank'] = customer_tb['age_rank'].cat.remove_unused_categories()  # 안 쓰는 범주 제거
```

### 8-4. KNN 기반 결측 범주 보완

**KNN(K-최근접 이웃)**: 다른 변수들로 잰 **거리상 가까운 k개 이웃의 값**으로 대상 값을 예측하는 알고리즘. 범주형 결측을 채울 때 활용한다.

> 🧮 **쉽게 이해하기 — "끼리끼리"로 빈칸 채우기**
>
> "비슷한 것끼리 모인다"는 상식을 그대로 쓴 방법이다. 값이 비어 있는 데이터가 있으면,
> **그와 가장 가까운(비슷한) k명의 이웃**을 찾아 그 이웃들의 값으로 빈칸을 메운다.
>
> - 예) `length·thickness`가 비슷한 이웃 3명(k=3)이 모두 type `B`라면 → 빈칸도 `B`로 채움.
> - `k`는 **참고할 이웃 수**. 작으면 가까운 몇 명만 보고(예민함), 크면 넓게 보고 결정(안정적).
> "거리가 가깝다"는 건 키·몸무게 같은 숫자들이 서로 비슷하다는 뜻이다.

```python
from sklearn.neighbors import KNeighborsClassifier

production_missc_tb.replace('None', np.nan, inplace=True)
train = production_missc_tb.dropna(subset=['type'], inplace=False)        # 정상(비결손)
test  = production_missc_tb.loc[                                          # 결손
    production_missc_tb.index.difference(train.index), :]

kn = KNeighborsClassifier(n_neighbors=3)
kn.fit(train[['length', 'thickness']], train['type'])      # length·thickness로 type 학습
test['type'] = kn.predict(test[['length', 'thickness']])   # 결손 type 예측·보완
```

---

## 9. 일시(날짜·시간) 데이터 정제

### 9-1. 문자열 → 일시형 변환

문자열/UNIXTIME로 들어온 날짜는 **일시형(datetime64)**으로 바꿔야 날짜 연산이 가능하다.

```python
# format: %Y년 %m월 %d일 %H시 %M분 %S초
reserve_tb['reserve_datetime'] = pd.to_datetime(
    reserve_tb['reserve_datetime'], format='%Y-%m-%d %H:%M:%S')

# 시간 없이 날짜만 추출
pd.to_datetime(reserve_tb['checkin_date'], format='%Y-%m-%d').dt.date
```

### 9-2. 구성 요소 분리 / 포맷 변환 — `.dt`

```python
dt = reserve_tb['reserve_datetime'].dt
dt.year      # 연        dt.hour     # 시
dt.month     # 월        dt.minute   # 분
dt.day       # 일        dt.second   # 초
dt.dayofweek # 요일(월=0)
dt.strftime('%Y-%m-%d %H:%M:%S')   # 원하는 형식의 문자열로
```

### 9-3. 시간 간격(차이) 계산

```python
diff = reserve_tb['reserve_datetime'] - reserve_tb['checkin_datetime']
diff.dt.days                  # 일 차이
diff.dt.total_seconds() / 3600  # 시간 차이
diff.dt.total_seconds() / 60    # 분 차이
# 연/월 차이는 연·월을 각각 빼서 계산: (y1*12+m1) - (y2*12+m2)
```

### 9-4. 시간 증분(더하기) — `timedelta`

```python
import datetime
reserve_tb['reserve_datetime'] + datetime.timedelta(days=1)     # 1일 뒤
reserve_tb['reserve_datetime'] + datetime.timedelta(hours=1)    # 1시간 뒤
reserve_tb['reserve_datetime'] + datetime.timedelta(minutes=1)  # 1분 뒤
reserve_tb['reserve_datetime'] + datetime.timedelta(seconds=1)  # 1초 뒤
```

### 9-5. 계절 / 공휴일 등 파생 변수

```python
# 월 → 계절
def to_season(m):
    if   3 <= m <= 5:  return 'spring'
    elif 6 <= m <= 8:  return 'summer'
    elif 9 <= m <= 11: return 'autumn'
    else:              return 'winter'
reserve_tb['reserve_season'] = pd.Categorical(
    reserve_tb['reserve_datetime'].dt.month.apply(to_season),
    categories=['spring', 'summer', 'autumn', 'winter'])

# 공휴일 마스터(휴일 플래그 등)와 날짜 키로 결합
pd.merge(reserve_tb, holiday_mst, left_on='checkin_date', right_on='target_day')
```

- 📖 [pandas 시계열](https://pandas.pydata.org/docs/user_guide/timeseries.html)

---

## 10. 위치정보(좌표) 데이터 정제

### 10-1. 좌표계 변환

2010년 1월부터 공공측량은 **세계 측지계(WGS84)** 사용이 의무. 한국 측지계 데이터는 세계 측지계로 변환해 써야 한다. `pyproj`(EPSG 코드)로 변환.

```python
# pip install pyproj
import pyproj
epsg_world = pyproj.Proj('+init=EPSG:4326')   # 세계 측지계(WGS84)
epsg_korea = pyproj.Proj('+init=EPSG:4301')   # 교안 기준 측지계

home_position = customer_tb[['home_longitude', 'home_latitude']].apply(
    lambda x: pyproj.transform(epsg_korea, epsg_world, x[0], x[1]), axis=1)
```

> 참고: 위도/경도가 "도분초" 형태면 먼저 **도(度) 단위 소수**로 변환해야 한다(교안의 `convert_to_continuous`).

### 10-2. 두 지점 간 거리·방위각

위도·경도로 두 지점의 **거리와 방향(방위각, azimuth)**을 계산. 거리 공식은 정확도/거리에 따라 선택한다(2000km 이내 **휴베니**, 더 멀고 정밀하면 **빈센티/하버사인**).

> 🧮 **쉽게 이해하기 — 방위각(azimuth)은 "나침반 각도"**
>
> 방위각 = **북쪽을 0°로 두고 시계방향으로 잰 각도**. 어느 쪽을 향하는지를 숫자로 나타낸다.
>
> - `0°` = 북, `90°` = 동, `180°` = 남, `270°` = 서.
> - 예) A지점에서 B지점 방위각이 `80°`면 "거의 동쪽 방향"에 B가 있다는 뜻.
>
> 지구는 둥글어서 두 점 사이 거리를 자로 재듯 단순 계산할 수 없다. 그래서 휴베니·빈센티·하버사인 같은
> **지구 곡면을 감안한 공식**들이 따로 있고, 라이브러리(`pyproj`)가 알아서 계산해 준다. 공식 자체를 외울 필요는 없다.

```python
# pip install pyproj
import pyproj
g = pyproj.Geod(ellps='WGS84')   # WGS84 타원체 기준
# inv: 시작점·끝점의 (경도1, 위도1, 경도2, 위도2) → (정방위각, 역방위각, 거리[m])
home_to_hotel = home_and_hotel_points.apply(
    lambda x: g.inv(x[0], x[1], x[2], x[3]), axis=1)
```

- 📖 [pyproj 문서](https://pyproj4.github.io/pyproj/stable/)

---

## 🗺️ 전체 흐름 한눈에 보기

```text
[2회차] 데이터 구성 정제 — 모양·단위 바꾸기
  추출(isin/loc/query) → 집계(groupby) → 결합(merge/cross/self)
        → 분할(train/test, KFold) → 불균형보정(SMOTE)
        → 전개(pivot_table) → 희소행렬(scipy.sparse)

[3회차] 데이터 세부내용 정제 — 값 자체 가공하기
  수치 : 형변환 → 로그(대수화) → 범주화 → 정규화 → 이상값제거 → PCA → 결측처리
  범주 : 범주형변환 → 더미변수화 → 범주집약 → KNN보완
  일시 : 일시형변환 → 구성요소분리 → 시간차/증분 → 계절·공휴일
  위치 : 좌표계변환(WGS84) → 거리·방위각 계산
```

> 출처: 새싹 AI 교안 2·3회차 + pandas / scikit-learn / imbalanced-learn / scipy / pyproj 공식 문서 (2026-06).
