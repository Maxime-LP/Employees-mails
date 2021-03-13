CREATE TABLE employee(
    id_employee INT PRIMARY KEY,
    last_name varchar(40),
    first_name varchar(40),
    category varchar(40) NOT NULL
)

CREATE TABLE mailbox(
    mail_adress varchar(40) PRIMARY KEY,
    id_employee INT NOT NULL,
    
    CONSTRAINT FOREIGN KEY id_employee REFERENCES employee(id_employee) ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT FOREIGN KEY id_mail REFERENCES mail(id_mail) ON DELETE SET NULL ON UPDATE CASCADE
)

CREATE TABLE mail(
    id_mail INT PRIMARY KEY,
    mail_adress varchar(40),
    mail_date DATE,
    id_exp INT,
    id_rec INT,
    id_prec INT,
    id_resp INT,

    CONSTRAINT FOREIGN KEY mail_adress REFERENCES mailbox(mail_adress),
    CONSTRAINT FOREIGN KEY id_exp,id_rec REFERENCES employee(id_employee),
    CONSTRAINT FOREIGN KEY id_prec,id_resp REFERENCES mail(id_mail)
)