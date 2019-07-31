set @adminUid = 1;

/* Create user */
create user if not exists 'xvzd'@'%' identified by 'xvzd';
grant all privileges on `xvzd_wargame`.* to 'xvzd'@'%';

/* Create database */
create database if not exists `xvzd_wargame`
character set utf8mb4 collate utf8mb4_unicode_ci;

create table if not exists `xvzd_wargame`.`xvzd_users` (
    `uid` bigint not null auto_increment,
    `id` varchar(128) not null,
    `name` varchar(128) not null,
    `password` varchar(128) not null,
    primary key (`uid`),
    unique (`id`)
) ENGINE=InnoDB;
create table if not exists `xvzd_wargame`.`xvzd_notice` (
    `no` bigint not null auto_increment,
    `uid` bigint not null,
    `title` varchar(128) not null,
    `content` text not null,
    primary key (`no`)
) ENGINE=InnoDB;

/* Insert datas */
insert into `xvzd_wargame`.`xvzd_users` (id, name, password)
select * from (
    select 'admin',
           'Xvezda',
           'fa449eec0fcabe9829db83e3810798f3f5e7b832ba79682cd4e474ddd51f5677b'
           '42a556cb8530d509f970b765e88b9052d77192d520acbf562178fd5aeb808ad'
) as tmp where not exists (
    select `id` from `xvzd_wargame`.`xvzd_users` where id='admin'
) limit 1;

insert into `xvzd_wargame`.`xvzd_notice` (title, content, uid)
select * from (
    select '+++ THIS IS YOUR MAIN GOAL +++',
           'Admin checks every submits on support board.<br>'
           'Make admin to submit support board with title "Hacked by <name>"'
           ' and content with login cookie flag. <br><br>'
           '#JavaScript #XSS #CSRF #Bypass',
           1
) as tmp where not exists (
    select * from `xvzd_wargame`.`xvzd_notice`
) limit 1;
