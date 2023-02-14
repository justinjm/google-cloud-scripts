-- create schemas
CREATE SCHEMA test;
go

-- create table
CREATE TABLE test.loans(
   id                INT  PRIMARY KEY 
  ,member_id         INT 
  ,loan_amnt         INT 
  ,term_in_months    INT 
  ,interest_rate     NUMERIC(5,2)
  ,payment           NUMERIC(7,2)
  ,grade             VARCHAR(1)
  ,sub_grade         VARCHAR(2)
  ,employment_length INT 
  ,home_owner        INT 
  ,income            NUMERIC(9,2)
  ,verified          INT 
  ,"default"         INT
  ,purpose           VARCHAR(18)
  ,zip_code          VARCHAR(5)
  ,addr_state        VARCHAR(2)
  ,open_accts        INT 
  ,credit_debt       INT
);

