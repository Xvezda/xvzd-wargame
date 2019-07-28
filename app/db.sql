create user if not exists 'xvzd'@'%' identified by 'xvzd';
grant all privileges on xvzd_wargame.* to 'xvzd'@'%';
create database if not exists xvzd_wargame;
create table if not exists `xvzd_wargame`.`xvzd_users` (
    `uid` bigint not null auto_increment,
    `id` varchar(128) not null,
    `name` varchar(128) not null,
    `password` varchar(128) not null,
primary key (`uid`));
