Scenario 2

Install MySQL Pod

Follow instruction on folder database_mysql

kubectl apply -f ./database_mysql/mysql-deployment.yaml
kubectl apply -f ./database_mysql/mysql-pv.yaml

Install microservice deployment: 

kubectl apply -f simpleapp.yml

Check Mysql Instance

kubectl run -it --rm --image=mysql:5.6 --restart=Never mysql-client -- mysql -h mysql -ppassword

show databases;



DROP DATABASE IF EXISTS inventory;
create database inventory;
use inventory;
DROP TABLE IF EXISTS widgets;
DROP TABLE IF EXISTS users;
CREATE TABLE widgets (name VARCHAR(255), description VARCHAR(255));
CREATE TABLE users (id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255) NOT NULL, description VARCHAR(255) NOT NULL);

check number records vs request

select count(*) from users;