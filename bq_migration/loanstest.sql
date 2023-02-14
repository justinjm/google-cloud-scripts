-- create schemas
CREATE SCHEMA test;
go

-- create table
CREATE TABLE test.loans(
   id                INTEGER  PRIMARY KEY 
  ,member_id         INTEGER 
  ,loan_amnt         INTEGER 
  ,term_in_months    INTEGER 
  ,interest_rate     NUMERIC(5,2)
  ,payment           NUMERIC(7,2)
  ,grade             VARCHAR(1)
  ,sub_grade         VARCHAR(2)
  ,employment_length INTEGER 
  ,home_owner        BIT 
  ,income            NUMERIC(9,2)
  ,verified          BIT 
  ,`default`           BIT 
  ,purpose           VARCHAR(18)
  ,zip_code          VARCHAR(5)
  ,addr_state        VARCHAR(2)
  ,open_accts        INTEGER 
  ,credit_debt       INTEGER 
);
