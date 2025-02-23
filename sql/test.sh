docker exec -it fact-checker-sql-container mysql -uadmin -paddmin_pass
USE fact_checking_db;
SHOW TABLES;