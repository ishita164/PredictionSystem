create database geeklogin;

use geeklogin;

create table accounts(
id int not null auto_increment,
username varchar(50) not null,
password varchar(255) not null,
email varchar(100) not null,
primary key (id)
)engine=innoDB auto_increment=2 default charset=utf8;

select * 
from accounts;

