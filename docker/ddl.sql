CREATE TABLE data_sync_schedule (
    id INT PRIMARY KEY AUTO_INCREMENT,

    table_name VARCHAR(100) NOT NULL UNIQUE COMMENT '대상 테이블명',
    sync_type VARCHAR(50) NOT NULL COMMENT '동기화 유형(FULL/INCREMENTAL)',
    cron_expression VARCHAR(50) COMMENT 'CRON 표현식',
    interval_minutes INT COMMENT '동기화 간격(분)',

    last_sync_at DATETIME COMMENT '마지막 동기화 시간',
    next_sync_at DATETIME COMMENT '다음 동기화 예정 시간',
    last_sync_status VARCHAR(20) COMMENT '마지막 동기화 상태(SUCCESS/FAILED/RUNNING)',
    last_sync_count INT DEFAULT 0 COMMENT '마지막 동기화 건수',
    last_error_message TEXT COMMENT '마지막 에러 메시지',

    is_enabled BOOLEAN DEFAULT TRUE COMMENT '활성화 여부',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    INDEX idx_table_name (table_name),
    INDEX idx_next_sync (next_sync_at),
    INDEX idx_is_enabled (is_enabled)
);

CREATE TABLE stocks (
    id INT PRIMARY KEY AUTO_INCREMENT,

    -- 기본 정보
    code VARCHAR(32) NOT NULL UNIQUE COMMENT '종목코드',
    name VARCHAR(256) NOT NULL COMMENT '종목명',

    -- 거래 정보
    list_count VARCHAR(20) COMMENT '상장주식수',
    audit_info VARCHAR(100) COMMENT '감리구분',
    reg_day VARCHAR(8) COMMENT '상장일(YYYYMMDD)',
    last_price VARCHAR(20) COMMENT '최종가격',
    state VARCHAR(256) COMMENT '종목상태',

    -- 시장 정보
    market_code VARCHAR(10) COMMENT '시장코드(0:거래소,1:코스닥)',
    market_name VARCHAR(50) COMMENT '시장명',

    -- 업종 정보
    up_name VARCHAR(100) COMMENT '업종명',
    up_size_name VARCHAR(100) COMMENT '업종규모명',

    -- 기타 정보
    company_class_name VARCHAR(100) COMMENT '기업구분명',
    order_warning VARCHAR(10) COMMENT '주문경고',
    nxt_enable VARCHAR(1) COMMENT '익일매매가능여부(Y/N)',

    -- 메타데이터
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '생성일시',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '수정일시',
    is_active BOOLEAN DEFAULT TRUE COMMENT '활성화여부',

    INDEX idx_code (code)
);

-- 섹터/업종 마스터 테이블
CREATE TABLE sectors (
    id INT PRIMARY KEY AUTO_INCREMENT,

    -- 섹터 정보
    code VARCHAR(50) NOT NULL UNIQUE COMMENT '섹터코드 (업종지수코드)',
    name VARCHAR(100) NOT NULL COMMENT '섹터명',

    -- 분류 정보
    market VARCHAR(20) COMMENT '시장구분 (KOSPI/KOSDAQ/KRX)',
    category VARCHAR(50) COMMENT '대분류 (WICS 등)',
    level INT DEFAULT 1 COMMENT '분류레벨 (1:대분류, 2:중분류, 3:소분류)',
    parent_id INT COMMENT '상위 섹터 ID',

    -- 통계 정보
    stock_count INT DEFAULT 0 COMMENT '속한 종목 수',

    -- 메타데이터
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '생성일시',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '수정일시',
    is_active BOOLEAN DEFAULT TRUE COMMENT '활성화여부',

    INDEX idx_code (code),
    INDEX idx_market (market),
    INDEX idx_category (category),
    INDEX idx_parent (parent_id),
    FOREIGN KEY (parent_id) REFERENCES sectors(id) ON DELETE SET NULL
);

-- 종목-섹터 매핑 테이블 (다대다 관계)
CREATE TABLE stock_sectors (
    id INT PRIMARY KEY AUTO_INCREMENT,

    stock_code VARCHAR(32) NOT NULL COMMENT '종목코드',
    sector_id INT NOT NULL COMMENT '섹터 ID',

    -- 메타데이터
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '생성일시',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '수정일시',

    UNIQUE KEY unique_stock_sector (stock_code, sector_id),
    INDEX idx_stock_code (stock_code),
    INDEX idx_sector_id (sector_id),
    FOREIGN KEY (sector_id) REFERENCES sectors(id) ON DELETE CASCADE
);

-- 일별 종목 거래 정보 테이블
CREATE TABLE stock_trading_daily (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,

    -- 기본 정보
    stock_code VARCHAR(32) NOT NULL COMMENT '종목코드',
    stock_name VARCHAR(256) NOT NULL COMMENT '종목명',
    trade_date DATE NOT NULL COMMENT '거래일자',

    -- 가격 정보
    current_price DECIMAL(15, 2) COMMENT '현재가',
    change_amount DECIMAL(15, 2) COMMENT '전일대비',
    change_rate DECIMAL(10, 2) COMMENT '등락률',

    -- 거래 정보
    trading_amount BIGINT COMMENT '거래대금',
    trading_volume BIGINT COMMENT '거래량',
    previous_trading_volume BIGINT COMMENT '전일거래량',

    -- 호가 정보
    sell_bid DECIMAL(15, 2) COMMENT '매도호가',
    buy_bid DECIMAL(15, 2) COMMENT '매수호가',

    -- 순위 정보
    current_rank INT COMMENT '현재순위',
    previous_rank INT COMMENT '전일순위',

    -- 메타데이터
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '생성일시',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '수정일시',

    -- 인덱스
    UNIQUE KEY unique_stock_date (stock_code, trade_date),
    INDEX idx_trade_date (trade_date),
    INDEX idx_stock_code (stock_code),
    INDEX idx_current_rank (current_rank),
    INDEX idx_trading_amount (trading_amount)
) COMMENT='일별 종목 거래 정보 (거래대금 순위 등)';

-- 투자자별 일별 매매 종목 테이블
CREATE TABLE investor_daily_trade (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,

    -- 요청 파라미터 (컨텍스트)
    start_date VARCHAR(8) NOT NULL COMMENT '시작일자(YYYYMMDD)',
    end_date VARCHAR(8) NOT NULL COMMENT '종료일자(YYYYMMDD)',
    trade_type VARCHAR(2) NOT NULL COMMENT '매매구분(1:순매도,2:순매수)',
    market_type VARCHAR(10) NOT NULL COMMENT '시장구분(001:코스피,101:코스닥)',
    investor_type VARCHAR(10) NOT NULL COMMENT '투자자구분(8000:개인,9000:외국인...)',
    exchange_type VARCHAR(2) NOT NULL COMMENT '거래소구분(1:KRX,2:NXT,3:통합)',

    -- 종목 정보
    stock_code VARCHAR(32) NOT NULL COMMENT '종목코드',
    stock_name VARCHAR(256) NOT NULL COMMENT '종목명',

    -- 거래 데이터
    net_sell_qty VARCHAR(30) COMMENT '순매도수량',
    net_sell_amt VARCHAR(30) COMMENT '순매도금액',
    est_avg_price VARCHAR(30) COMMENT '추정평균가',
    current_price VARCHAR(30) COMMENT '현재가',
    change_sign VARCHAR(5) COMMENT '대비기호',
    day_change VARCHAR(30) COMMENT '전일대비',
    avg_price_change VARCHAR(30) COMMENT '평균가대비',
    change_rate VARCHAR(20) COMMENT '대비율',
    period_trade_volume VARCHAR(30) COMMENT '기간거래량',

    -- 메타데이터
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '생성일시',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '수정일시',

    UNIQUE KEY idx_investor_trade_unique (stock_code, end_date, investor_type, market_type, trade_type),
    INDEX idx_stock_code (stock_code),
    INDEX idx_end_date (end_date),
    INDEX idx_investor_type (investor_type)
) COMMENT='투자자별 일별 매매 종목 정보';

-- 주식 기본 정보 테이블 (ka10001)
CREATE TABLE stock_basic_info (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,

    -- 종목 기본
    stock_code VARCHAR(32) NOT NULL UNIQUE COMMENT '종목코드',
    stock_name VARCHAR(256) COMMENT '종목명',
    setl_mm VARCHAR(20) COMMENT '결산월',
    fav VARCHAR(20) COMMENT '액면가',
    fav_unit VARCHAR(20) COMMENT '액면가단위',
    cap VARCHAR(20) COMMENT '자본금',
    flo_stk VARCHAR(20) COMMENT '상장주식',
    dstr_stk VARCHAR(20) COMMENT '유통주식',
    dstr_rt VARCHAR(20) COMMENT '유통비율',
    crd_rt VARCHAR(20) COMMENT '신용비율',

    -- 시가총액
    mac VARCHAR(30) COMMENT '시가총액',
    mac_wght VARCHAR(20) COMMENT '시가총액비중',
    for_exh_rt VARCHAR(20) COMMENT '외인소진률',
    repl_pric VARCHAR(20) COMMENT '대용가',

    -- 현재가 / 시세
    cur_prc VARCHAR(20) COMMENT '현재가',
    pre_sig VARCHAR(5) COMMENT '대비기호',
    pred_pre VARCHAR(20) COMMENT '전일대비',
    flu_rt VARCHAR(20) COMMENT '등락율',
    trde_qty VARCHAR(20) COMMENT '거래량',
    trde_pre VARCHAR(20) COMMENT '거래대비',
    open_pric VARCHAR(20) COMMENT '시가',
    high_pric VARCHAR(20) COMMENT '고가',
    low_pric VARCHAR(20) COMMENT '저가',
    upl_pric VARCHAR(20) COMMENT '상한가',
    lst_pric VARCHAR(20) COMMENT '하한가',
    base_pric VARCHAR(20) COMMENT '기준가',
    exp_cntr_pric VARCHAR(20) COMMENT '예상체결가',
    exp_cntr_qty VARCHAR(20) COMMENT '예상체결수량',

    -- 연중 최고/최저
    oyr_hgst VARCHAR(20) COMMENT '연중최고',
    oyr_lwst VARCHAR(20) COMMENT '연중최저',

    -- 250일 최고/최저
    hgst_250 VARCHAR(20) COMMENT '250일 최고가',
    hgst_250_pric_dt VARCHAR(8) COMMENT '250일 최고가일',
    hgst_250_pric_pre_rt VARCHAR(20) COMMENT '250일 최고가대비율',
    lwst_250 VARCHAR(20) COMMENT '250일 최저가',
    lwst_250_pric_dt VARCHAR(8) COMMENT '250일 최저가일',
    lwst_250_pric_pre_rt VARCHAR(20) COMMENT '250일 최저가대비율',

    -- 재무 지표
    per VARCHAR(20) COMMENT 'PER',
    eps VARCHAR(20) COMMENT 'EPS',
    roe VARCHAR(20) COMMENT 'ROE',
    pbr VARCHAR(20) COMMENT 'PBR',
    ev VARCHAR(20) COMMENT 'EV',
    bps VARCHAR(20) COMMENT 'BPS',
    sale_amt VARCHAR(20) COMMENT '매출액',
    bus_pro VARCHAR(20) COMMENT '영업이익',
    cup_nga VARCHAR(20) COMMENT '당기순이익',

    -- 메타데이터
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '생성일시',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '수정일시',

    INDEX idx_stock_code (stock_code)
) COMMENT='주식 기본 정보 (ka10001)';

-- 주식 분봉 차트 데이터 (ka10080)
CREATE TABLE stock_chart_minute (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,

    stock_code VARCHAR(32) NOT NULL COMMENT '종목코드',
    cntr_tm VARCHAR(14) NOT NULL COMMENT '체결시간 (YYYYMMDDHHMMSS)',

    -- OHLCV
    open_pric BIGINT COMMENT '시가',
    high_pric BIGINT COMMENT '고가',
    low_pric BIGINT COMMENT '저가',
    cur_prc BIGINT COMMENT '종가(현재가)',
    trde_qty BIGINT COMMENT '거래량',
    acc_trde_qty BIGINT COMMENT '누적거래량',

    -- 전일대비
    pred_pre BIGINT COMMENT '전일대비',
    pred_pre_sig VARCHAR(2) COMMENT '전일대비부호',

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '생성일시',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '수정일시',

    UNIQUE KEY idx_chart_minute_unique (stock_code, cntr_tm),
    INDEX idx_chart_minute_code_tm (stock_code, cntr_tm)
) COMMENT='주식 분봉 차트 데이터';

-- 주식 일봉 차트 데이터 (ka10081)
CREATE TABLE stock_chart_daily (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,

    stock_code VARCHAR(32) NOT NULL COMMENT '종목코드',
    dt VARCHAR(8) NOT NULL COMMENT '일자 (YYYYMMDD)',

    -- OHLCV
    open_pric BIGINT COMMENT '시가',
    high_pric BIGINT COMMENT '고가',
    low_pric BIGINT COMMENT '저가',
    cur_prc BIGINT COMMENT '종가(현재가)',
    trde_qty BIGINT COMMENT '거래량',
    trde_prica BIGINT COMMENT '거래대금',

    -- 전일대비
    pred_pre BIGINT COMMENT '전일대비',
    pred_pre_sig VARCHAR(2) COMMENT '전일대비부호',

    trde_tern_rt DECIMAL(10, 2) COMMENT '거래회전율',

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '생성일시',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '수정일시',

    UNIQUE KEY idx_chart_daily_unique (stock_code, dt),
    INDEX idx_chart_daily_dt (dt)
) COMMENT='주식 일봉 차트 데이터';

-- 주식 주봉 차트 데이터 (ka10082)
CREATE TABLE stock_chart_weekly (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,

    stock_code VARCHAR(32) NOT NULL COMMENT '종목코드',
    dt VARCHAR(8) NOT NULL COMMENT '주 시작일 (YYYYMMDD)',

    -- OHLCV
    open_pric BIGINT COMMENT '시가',
    high_pric BIGINT COMMENT '고가',
    low_pric BIGINT COMMENT '저가',
    cur_prc BIGINT COMMENT '종가(현재가)',
    trde_qty BIGINT COMMENT '거래량',
    trde_prica BIGINT COMMENT '거래대금',

    -- 전일대비
    pred_pre BIGINT COMMENT '전일대비',
    pred_pre_sig VARCHAR(2) COMMENT '전일대비부호',

    trde_tern_rt DECIMAL(10, 2) COMMENT '거래회전율',

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '생성일시',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '수정일시',

    UNIQUE KEY idx_chart_weekly_unique (stock_code, dt/s),
    INDEX idx_chart_weekly_dt (dt)
) COMMENT='주식 주봉 차트 데이터';

-- 주식 월봉 차트 데이터 (ka10083)
CREATE TABLE stock_chart_monthly (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,

    stock_code VARCHAR(32) NOT NULL COMMENT '종목코드',
    dt VARCHAR(8) NOT NULL COMMENT '월 시작일 (YYYYMMDD)',

    -- OHLCV
    open_pric BIGINT COMMENT '시가',
    high_pric BIGINT COMMENT '고가',
    low_pric BIGINT COMMENT '저가',
    cur_prc BIGINT COMMENT '종가(현재가)',
    trde_qty BIGINT COMMENT '거래량',
    trde_prica BIGINT COMMENT '거래대금',

    -- 전일대비
    pred_pre BIGINT COMMENT '전일대비',
    pred_pre_sig VARCHAR(2) COMMENT '전일대비부호',

    trde_tern_rt DECIMAL(10, 2) COMMENT '거래회전율',

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '생성일시',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '수정일시',

    UNIQUE KEY idx_chart_monthly_unique (stock_code, dt),
    INDEX idx_chart_monthly_dt (dt)
) COMMENT='주식 월봉 차트 데이터';
