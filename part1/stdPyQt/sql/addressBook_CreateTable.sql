-- MySQL용
CREATE TABLE addressbook (
  Idx int NOT NULL AUTO_INCREMENT,
  FullName varchar(50) NOT NULL COMMENT '이름',
  PhoneNum varchar(20) NOT NULL COMMENT '핸드폰 번호',
  Email varchar(120) DEFAULT NULL COMMENT '이메일 NULL 허용',
  Address varchar(250) DEFAULT NULL COMMENT '주소 NULL 허용',
  PRIMARY KEY (Idx)
) COMMENT='주소록 테이블';
