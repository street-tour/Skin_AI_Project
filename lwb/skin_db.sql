use skin;

-- 제품
CREATE TABLE `product` (
	`product_no`   INT          NOT NULL COMMENT '제품번호', -- 제품번호
	`category`     VARCHAR(30)  NULL     COMMENT '카테고리', -- 카테고리
	`url`          VARCHAR(200) NULL     COMMENT 'url', -- url
	`product_name` VARCHAR(300) NULL     COMMENT '제품명' -- 제품명
)
COMMENT '제품';

ALTER TABLE product
MODIFY column category VARCHAR(300);

-- 제품
ALTER TABLE `product`
	ADD CONSTRAINT `PK_product` -- 제품 기본키
	PRIMARY KEY (
	`product_no` -- 제품번호
	);

ALTER TABLE `product`
	MODIFY COLUMN `product_no` INT NOT NULL AUTO_INCREMENT COMMENT '제품번호';

-- 성분
CREATE TABLE `ingredient` (
	`ingredient_no` INT         NOT NULL COMMENT '성분번호', -- 성분번호
	`product_no`    INT         NOT NULL COMMENT '제품번호', -- 제품번호
	`ingredient`    VARCHAR(100) NULL     COMMENT '성분', -- 성분
	`count`         INT         NULL     COMMENT '성분수' -- 성분수
)
COMMENT '성분';

-- 성분
ALTER TABLE `ingredient`
	ADD CONSTRAINT `PK_ingredient` -- 성분 기본키
	PRIMARY KEY (
	`ingredient_no` -- 성분번호
	);

ALTER TABLE `ingredient`
	MODIFY COLUMN `ingredient_no` INT NOT NULL AUTO_INCREMENT COMMENT '성분번호';

-- 병원
CREATE TABLE `hospital` (
	`hospital_no`   INT          NOT NULL COMMENT '병원번호', -- 병원번호
	`hospital_name` VARCHAR(100) NOT NULL COMMENT '병원이름', -- 병원이름
	`doctor_name`   VARCHAR(30)  NOT NULL COMMENT '의사이름', -- 의사이름
	`address`       VARCHAR(200) NOT NULL COMMENT '주소', -- 주소
	`number`        VARCHAR(30)  NULL     COMMENT '전화번호', -- 전화번호
	`dermatologist` VARCHAR(10)  NOT NULL COMMENT '피부과전문의' -- 피부과전문의
)
COMMENT '병원';

-- 병원
ALTER TABLE `hospital`
	ADD CONSTRAINT `PK_hospital` -- 병원 기본키
	PRIMARY KEY (
	`hospital_no` -- 병원번호
	);

ALTER TABLE `hospital`
	MODIFY COLUMN `hospital_no` INT NOT NULL AUTO_INCREMENT COMMENT '병원번호';

-- 회원
CREATE TABLE `member` (
	`memberid` VARCHAR(30)  NOT NULL COMMENT '회원아이디', -- 회원아이디
	`passwd`   VARCHAR(200) NOT NULL COMMENT '패스워드', -- 패스워드
	`email`    VARCHAR(50)  NOT NULL COMMENT '이메일', -- 이메일
	`usertype` VARCHAR(20)  NULL     DEFAULT ('user') COMMENT '사용자구분', -- 사용자구분
	`regdate`  DATE         NULL     DEFAULT (CURDATE()) COMMENT '등록일자', -- 등록일자
	`active`   BOOLEAN      NULL     DEFAULT (TRUE) COMMENT '회원상태', -- 회원상태
	`gender`   VARCHAR(20)  NOT NULL COMMENT '성별', -- 성별
	`skintype` VARCHAR(20)  NOT NULL COMMENT '피부타입', -- 피부타입
	`age`      INT          NOT NULL COMMENT '나이', -- 나이
	`address`  VARCHAR(400) NULL     COMMENT '주소' -- 주소
)
COMMENT '회원';

-- 회원
ALTER TABLE `member`
	ADD CONSTRAINT `PK_member` -- 회원 기본키
	PRIMARY KEY (
	`memberid` -- 회원아이디
	);

-- 첨부파일
CREATE TABLE `attachment` (
	`attachno`      INT          NOT NULL COMMENT '첨부파일번호', -- 첨부파일번호
	`boardno`       INT          NOT NULL COMMENT '글번호', -- 글번호
	`userfilename`  VARCHAR(100) NOT NULL COMMENT '사용자파일이름', -- 사용자파일이름
	`savedfilename` VARCHAR(100) NOT NULL COMMENT '저장된파일이름', -- 저장된파일이름
	`downloadcnt`   INT          NULL     DEFAULT (0) COMMENT '다운로드횟수' -- 다운로드횟수
)
COMMENT '첨부파일';

-- 첨부파일
ALTER TABLE `attachment`
	ADD CONSTRAINT `PK_attachment` -- 첨부파일 기본키
	PRIMARY KEY (
	`attachno` -- 첨부파일번호
	);

-- 게시판
CREATE TABLE `board` (
	`boardno`    INT           NOT NULL COMMENT '글번호', -- 글번호
	`title`      VARCHAR(100)  NOT NULL COMMENT '제목', -- 제목
	`writer`     VARCHAR(30)   NOT NULL COMMENT '작성자', -- 작성자
	`content`    VARCHAR(2000) NULL     COMMENT '글내용', -- 글내용
	`writedate`  DATETIME      NULL     DEFAULT (NOW()) COMMENT '작성일자', -- 작성일자
	`modifydate` DATETIME      NULL     DEFAULT (NOW()) COMMENT '수정일자', -- 수정일자
	`deleted`    BOOLEAN       NULL     DEFAULT (FALSE) COMMENT '삭제여부' -- 삭제여부
)
COMMENT '게시판';

-- 게시판
ALTER TABLE `board`
	ADD CONSTRAINT `PK_board` -- 게시판 기본키
	PRIMARY KEY (
	`boardno` -- 글번호
	);

-- 피부검사
CREATE TABLE `skin_test` (
	`testno`    INT         NOT NULL COMMENT '검사번호', -- 검사번호
	`model`     VARCHAR(50) NOT NULL COMMENT '모델', -- 모델
	`result`    VARCHAR(10) NOT NULL COMMENT '결과값', -- 결과값
	`modeldate` DATETIME    NOT NULL DEFAULT (NOW()) COMMENT '검사일자', -- 검사일자
	`memberid`  VARCHAR(30) NULL     COMMENT '회원아이디' -- 회원아이디
)
COMMENT '피부검사';

-- 피부검사
ALTER TABLE `skin_test`
	ADD CONSTRAINT `PK_skin_test` -- 피부검사 기본키
	PRIMARY KEY (
	`testno` -- 검사번호
	);

ALTER TABLE `skin_test`
	MODIFY COLUMN `testno` INT NOT NULL AUTO_INCREMENT COMMENT '검사번호';

-- 추천화장품
CREATE TABLE `cosmetic_recommendation` (
	`recommendno` INT NOT NULL COMMENT '추천번호', -- 추천번호
	`testno`      INT NULL     COMMENT '검사번호', -- 검사번호
	`product_no`  INT NULL     COMMENT '제품번호' -- 제품번호
)
COMMENT '추천화장품';

-- 추천화장품
ALTER TABLE `cosmetic_recommendation`
	ADD CONSTRAINT `PK_cosmetic_recommendation` -- 추천화장품 기본키
	PRIMARY KEY (
	`recommendno` -- 추천번호
	);

ALTER TABLE `cosmetic_recommendation`
	MODIFY COLUMN `recommendno` INT NOT NULL AUTO_INCREMENT COMMENT '추천번호';

-- 질병검사
CREATE TABLE `disease_test` (
	`testno`   INT          NOT NULL COMMENT '검사번호', -- 검사번호
	`memberid` VARCHAR(30)  NOT NULL COMMENT '회원아이디', -- 회원아이디
	`result`   VARCHAR(100) NOT NULL COMMENT '결과값', -- 결과값
	`testdate` DATETIME     NOT NULL DEFAULT (NOW()) COMMENT '검사일자' -- 검사일자
)
COMMENT '질병검사';

-- 질병검사
ALTER TABLE `disease_test`
	ADD CONSTRAINT `PK_disease_test` -- 질병검사 기본키
	PRIMARY KEY (
	`testno` -- 검사번호
	);

ALTER TABLE `disease_test`
	MODIFY COLUMN `testno` INT NOT NULL AUTO_INCREMENT COMMENT '검사번호';

-- 성분
ALTER TABLE `ingredient`
	ADD CONSTRAINT `FK_product_TO_ingredient` -- 제품 -> 성분
	FOREIGN KEY (
	`product_no` -- 제품번호
	)
	REFERENCES `product` ( -- 제품
	`product_no` -- 제품번호
	);

-- 첨부파일
ALTER TABLE `attachment`
	ADD CONSTRAINT `FK_board_TO_attachment` -- 게시판 -> 첨부파일
	FOREIGN KEY (
	`boardno` -- 글번호
	)
	REFERENCES `board` ( -- 게시판
	`boardno` -- 글번호
	);

-- 게시판
ALTER TABLE `board`
	ADD CONSTRAINT `FK_member_TO_board` -- 회원 -> 게시판
	FOREIGN KEY (
	`writer` -- 작성자
	)
	REFERENCES `member` ( -- 회원
	`memberid` -- 회원아이디
	);

-- 피부검사
ALTER TABLE `skin_test`
	ADD CONSTRAINT `FK_member_TO_skin_test` -- 회원 -> 피부검사
	FOREIGN KEY (
	`memberid` -- 회원아이디
	)
	REFERENCES `member` ( -- 회원
	`memberid` -- 회원아이디
	);

-- 추천화장품
ALTER TABLE `cosmetic_recommendation`
	ADD CONSTRAINT `FK_skin_test_TO_cosmetic_recommendation` -- 피부검사 -> 추천화장품
	FOREIGN KEY (
	`testno` -- 검사번호
	)
	REFERENCES `skin_test` ( -- 피부검사
	`testno` -- 검사번호
	);

-- 추천화장품
ALTER TABLE `cosmetic_recommendation`
	ADD CONSTRAINT `FK_product_TO_cosmetic_recommendation` -- 제품 -> 추천화장품
	FOREIGN KEY (
	`product_no` -- 제품번호
	)
	REFERENCES `product` ( -- 제품
	`product_no` -- 제품번호
	);

-- 질병검사
ALTER TABLE `disease_test`
	ADD CONSTRAINT `FK_member_TO_disease_test` -- 회원 -> 질병검사
	FOREIGN KEY (
	`memberid` -- 회원아이디
	)
	REFERENCES `member` ( -- 회원
	`memberid` -- 회원아이디
	);
    