CREATE_SCHEMA = """
CREATE SCHEMA IF NOT EXISTS `mydb`;
"""

Create_users_Table = """
CREATE TABLE IF NOT EXISTS mydb.Users( 
        name VARCHAR(45) NOT NULL, 
        email Varchar(120) Not NULL,   
        type VARCHAR(45) NOT NULL,
        password VARCHAR(45) NULL,  
        UNIQUE INDEX email_UNIQUE (email), 
        CHECK (type in ('Recruiter','Client','Administration')),
        PRIMARY KEY (email)   );
  """
Create_recruiter_Table = """
CREATE TABLE IF NOT EXISTS mydb.Recruiter(
  RID INT NOT NULL AUTO_INCREMENT,
  RName VARCHAR(45) NOT NULL,
  REmail VARCHAR(45) NOT NULL,
  CompanyName VARCHAR(45) NOT NULL,
  CompanyLocation VARCHAR(45) NOT NULL,
  RGender VARCHAR(2) NOT NULL,
   PRIMARY KEY (RID),
   UNIQUE (REmail)
   );
  """
Create_client_Table = """
CREATE TABLE IF NOT EXISTS mydb.Client (
  CID INT NOT NULL AUTO_INCREMENT,
  CName VARCHAR(45) NOT NULL,
  CEmail VARCHAR(45) NOT NULL,
  CAge INT NOT NULL,
  CLocation VARCHAR(45) NOT NULL,
  CGender VARCHAR(2) NOT NULL,
  CExp INT NOT NULL,
  CSkills VARCHAR(45) NOT NULL,
  CQualification VARCHAR(45) NOT NULL,
  UNIQUE (CEmail),
  PRIMARY KEY (CID)
  );
  """

Create_Job_Table = """
CREATE TABLE IF NOT EXISTS mydb.Job (
  RID INT NOT NULL,
  JID INT NOT NULL AUTO_INCREMENT,
  JobRole VARCHAR(45) NOT NULL,
  JobType VARCHAR(45) NOT NULL,
  Qualification VARCHAR(45) NOT NULL,
  MinExp INT NOT NULL,
  Salary INT NOT NULL,
  FOREIGN KEY (RID) REFERENCES mydb.Recruiter(RID),
  PRIMARY KEY (JID)
  );
  """

Create_Application_Table="""
CREATE TABLE IF NOT EXISTS mydb.Application(
    AID INT NOT NULL AUTO_INCREMENT,
    RID INT NOT NULL,
    JID INT NOT NULL,
    CID INT NOT NULL,
    PRIMARY KEY(AID),
    FOREIGN KEY(RID) REFERENCES mydb.Recruiter(RID),
    FOREIGN KEY(JID) REFERENCES mydb.Job(JID),
    FOREIGN KEY(CID) REFERENCES mydb.Client(CID)
);
"""

Create_DELJOB_Table="""
CREATE TABLE IF NOT EXISTS mydb.DELJOB(
    JID int,
    RID int,
    JObRole varchar(45),
    Deleted_At datetime
);
"""

Create_DELAPP_Table="""
CREATE TABLE IF NOT EXISTS mydb.DELAPP(
    CID int,
    JID int,
    Deleted_At datetime
);
"""

CREATE_Admin="""
INSERT INTO users 
VALUE("BhaveshPatil", "ADMIN", "Administration", "password")
"""

JobTrig1="""
CREATE TRIGGER jobTrig1
BEFORE DELETE ON Job FOR EACH ROW
BEGIN
INSERT INTO DelJob
SET JID=OLD.JID,
RID=OLD.RID,
JOBRole=OLD.JOBrole,
Deleted_AT=NOW();
END
"""

JobTrig2="""
CREATE TRIGGER jobTrig2
AFTER INSERT ON Job FOR EACH ROW
BEGIN
INSERT INTO NewJob
SET JID=NEW.JID,
RID=NEW.RID,
JOBRole=NEW.JOBrole,
Created_AT=NOW();
END
"""

AppTrig="""
CREATE TRIGGER appTrig
BEFORE DELETE ON application FOR EACH ROW
BEGIN
INSERT INTO DelAPP
SET CID=OLD.CID,
JID=OLD.JID,
Deleted_AT=NOW();
END
"""

totalAPP="""
CREATE PROCEDURE no_of_app()
BEGIN
SELECT COUNT(JID) AS No_Of_JobApplications
FROM application;
END
"""

totalJOB="""
CREATE PROCEDURE no_of_job()
BEGIN
SELECT COUNT(JID) AS No_Of_Jobs
FROM job;
END
"""

totalUSERS="""
CREATE PROCEDURE no_of_users()
BEGIN
SELECT COUNT(email) AS No_Of_Users
FROM users;
END
"""

Log_View="""
CREATE VIEW log AS
SELECT email,password
FROM users
"""