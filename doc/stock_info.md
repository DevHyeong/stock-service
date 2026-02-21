

# 📑 키움 REST API: 주식기본정보요청 (ka10001)

본 API는 특정 종목의 코드(`stk_cd`)를 입력하여 해당 종목의 **현재가, 시세, 재무지표(PER, PBR 등), 상장 정보** 등을 한 번에 가져오는 가장 기본적인 API입니다.

## 1. 기본 호출 규격

* **Method**: `POST`
* **API ID**: `ka10001`
* **URL**: `https://api.kiwoom.com/api/dostk/stkinfo`
* **Content-Type**: `application/json;charset=UTF-8`

---

## 2. 요청 파라미터 (Request)

### Header

| Element | 설명 | 필수 | 비고 |
| --- | --- | --- | --- |
| `api-id` | TR명 | Y | `ka10001` |
| `authorization` | 접근토큰 | Y | `Bearer {access_token}` 형식 |
| `cont-yn` | 연속조회여부 | N | 응답 Header의 값을 세팅 |
| `next-key` | 연속조회키 | N | 응답 Header의 값을 세팅 |

### Body

| Element | 한글명 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- | --- |
| `stk_cd` | 종목코드 | String | Y | KRX(039490), NXT(039490_NX) 등 |

---

## 3. 응답 데이터 (Response) 주요 항목

응답은 단일 객체 형태로 반환되며, 주요 필드는 다음과 같습니다.

### ① 종목 및 상장 정보

* `stk_nm`: 종목명
* `mac`: 시가총액 / `mac_wght`: 시가총액비중
* `flo_stk`: 상장주식수 / `dstr_stk`: 유통주식수 (`dstr_rt`: 유통비율)
* `fav`: 액면가 (`fav_unit`: 액면가단위)

### ② 현재가 및 시세 정보

* `cur_prc`: 현재가
* `open_pric`: 시가 / `high_pric`: 고가 / `low_pric`: 저가
* `upl_pric`: 상한가 / `lst_pric`: 하한가
* `flu_rt`: 등락율 / `pred_pre`: 전일대비 (`pre_sig`: 대비기호)
* `trde_qty`: 거래량

### ③ 재무 지표 (외부 벤더 제공)

> **주의:** 아래 항목은 일주일에 한 번 또는 실적 발표 시즌에 업데이트됩니다.

* `per`: PER / `pbr`: PBR / `roe`: ROE / `ev`: EV
* `eps`: EPS / `bps`: BPS
* `sale_amt`: 매출액 / `bus_pro`: 영업이익 / `cup_nga`: 당기순이익

### ④ 기간 최고/최저가

* `250hgst`: 250일 최고가 (`250hgst_pric_dt`: 최고가일)
* `250lwst`: 250일 최저가 (`250lwst_pric_dt`: 최저가일)
* `oyr_hgst`: 연중 최고가 / `oyr_lwst`: 연중 최저가

---

## 4. 데이터 예시 (Example)

### Request

```json
{
    "stk_cd": "005930"
}

```

### Response

```json
{
    "stk_cd": "005930",
    "stk_nm": "삼성전자",
    "cur_prc": "60500",
    "flu_rt": "+0.83",
    "per": "12.5",
    "pbr": "1.1",
    "return_code": 0,
    "return_msg": "정상적으로 처리되었습니다"
}

```

---

## 5. 개발 참고사항

1. **데이터 업데이트 주기**: PER, ROE 등 재무 데이터는 실시간이 아니며 외부 공급사 사정에 따라 주 단위로 갱신될 수 있음을 사용자에게 고지해야 합니다.
2. **거래소 구분**: 종목코드 뒤에 `_NX`(NXT 거래소) 등을 붙여 호출할 수 있으므로, 다중 거래소 지원 시 파라미터 처리에 유의하십시오.
3. **에러 핸들링**: `return_code`가 `0`이 아닌 경우 `return_msg`를 통해 실패 사유를 확인할 수 있습니다.