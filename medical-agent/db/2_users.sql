CREATE USER 'ai_agent'@'%'
    IDENTIFIED BY 'ai_password';

GRANT SELECT ON hospital_db.* TO 'ai_agent'@'%';
GRANT SHOW VIEW ON hospital_db.* TO 'ai_agent'@'%';
REVOKE CREATE TEMPORARY TABLES ON *.* FROM 'ai_agent'@'%';

FLUSH PRIVILEGES;