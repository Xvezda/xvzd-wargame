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
    `name` varchar(32) not null,
    `password` varchar(128) not null,
    primary key (`uid`),
    unique (`id`)
) ENGINE=InnoDB;
create table if not exists `xvzd_wargame`.`xvzd_notice` (
    `no` bigint not null auto_increment,
    `uid` bigint not null,
    `pinned` tinyint(1),
    `title` varchar(128) not null,
    `content` text not null,
    `regdate` timestamp not null default current_timestamp,
    primary key (`no`)
) ENGINE=InnoDB;
create table if not exists `xvzd_wargame`.`xvzd_support`
like `xvzd_wargame`.`xvzd_notice`;

/* Insert datas */
insert into `xvzd_wargame`.`xvzd_users` (id, name, password)
select * from (
    select 'admin',
           'Xvezda',
           'fa449eec0fcabe9829db83e3810798f3f5e7b832ba79682cd4e474ddd51f5677b'
           '42a556cb8530d509f970b765e88b9052d77192d520acbf562178fd5aeb808ad'
) as tmp where not exists (
    select `id` from `xvzd_wargame`.`xvzd_users` where id='admin'
);

insert into `xvzd_wargame`.`xvzd_notice` (pinned, title, content, uid)
select * from (
    select 1,
           '+++ THIS IS YOUR MAIN GOAL +++',
           'Admin checks every submits on support board.<br>'
           'Make admin to submit on notice board with title "Hacked by '
           "&lt;your_id_here&gt;\" and contents with admin's login cookie flag."
           '<br><br>'
           '#JavaScript #XSS #CSRF #Bypass',
           @adminUid union
    select 0,
           'HINT FOR YOU',
           '<a href="https://github.com/Xvezda/xvzd-wargame" target="_blank">'
           'https://github.com/Xvezda/xvzd-wargame</a><br>'
           'Here is all source code of this website :)<br><br>'
           '+Tip)<br>'
           'If you are not friendly with js, then use jQuery instead. :D',
           @adminUid
) as tmp where not exists (
    select no from `xvzd_wargame`.`xvzd_notice`
);
