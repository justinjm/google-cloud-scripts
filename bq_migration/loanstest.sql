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
  ,default           BIT 
  ,purpose           VARCHAR(18)
  ,zip_code          VARCHAR(5)
  ,addr_state        VARCHAR(2)
  ,open_accts        INTEGER 
  ,credit_debt       INTEGER 
);

INSERT INTO test.loan(id,member_id,loan_amnt,term_in_months,interest_rate,payment,grade,sub_grade,employment_length,home_owner,income,verified,default,purpose,zip_code,addr_state,open_accts,credit_debt) VALUES (123688,123685,1800,36,17.22,64.38,'G','G3',1,0,1896,0,0,'debt_consolidation','853xx','AZ',3,702);
INSERT INTO test.loan(id,member_id,loan_amnt,term_in_months,interest_rate,payment,grade,sub_grade,employment_length,home_owner,income,verified,default,purpose,zip_code,addr_state,open_accts,credit_debt) VALUES (139940,139937,500,36,9.01,15.91,'B','B2',1,0,2000,0,1,'other','727xx','AR',2,0);
INSERT INTO test.loan(id,member_id,loan_amnt,term_in_months,interest_rate,payment,grade,sub_grade,employment_length,home_owner,income,verified,default,purpose,zip_code,addr_state,open_accts,credit_debt) VALUES (288342,288338,500,36,8,15.67,'A','A3',1,0,3300,0,1,'educational','303xx','GA',3,0);
INSERT INTO test.loan(id,member_id,loan_amnt,term_in_months,interest_rate,payment,grade,sub_grade,employment_length,home_owner,income,verified,default,purpose,zip_code,addr_state,open_accts,credit_debt) VALUES (228954,228911,1600,36,7.43,49.72,'A','A2',1,0,3500,0,1,'other','069xx','CT',2,506);
INSERT INTO test.loan(id,member_id,loan_amnt,term_in_months,interest_rate,payment,grade,sub_grade,employment_length,home_owner,income,verified,default,purpose,zip_code,addr_state,open_accts,credit_debt) VALUES (267670,252052,1525,36,10.71,49.72,'B','B5',1,0,3600,0,1,'moving','109xx','NY',5,3757);