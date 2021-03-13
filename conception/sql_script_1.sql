
CREATE TABLE employee (
                id_employee INTEGER NOT NULL,
                last_name VARCHAR NOT NULL,
                first_name VARCHAR,
                category VARCHAR NOT NULL,
                CONSTRAINT id_employee PRIMARY KEY (id_employee)
);


CREATE TABLE mailbox (
                mail_adress VARCHAR NOT NULL,
                id_employee INTEGER NOT NULL,
                CONSTRAINT mail_adress PRIMARY KEY (mail_adress)
);


CREATE TABLE mail (
                id_mail INTEGER NOT NULL,
                mail_date DATE NOT NULL,
                mail_rec VARCHAR NOT NULL,
                mail_exp VARCHAR NOT NULL,
                id_prec INTEGER,
                id_resp INTEGER,
                CONSTRAINT id_mail PRIMARY KEY (id_mail)
);


ALTER TABLE mailbox ADD CONSTRAINT mailbox_employee_fk
FOREIGN KEY (id_employee)
REFERENCES employee (id_employee)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE mail ADD CONSTRAINT mailbox_mail_fk
FOREIGN KEY (mail_exp)
REFERENCES mailbox (mail_adress)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE mail ADD CONSTRAINT mailbox_mail_fk1
FOREIGN KEY (mail_rec)
REFERENCES mailbox (mail_adress)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE mail ADD CONSTRAINT mail_mail_fk
FOREIGN KEY (id_prec)
REFERENCES mail (id_mail)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE mail ADD CONSTRAINT mail_mail_fk1
FOREIGN KEY (id_resp)
REFERENCES mail (id_mail)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;
