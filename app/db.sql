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
    `ip` varchar(64) not null,
    primary key (`uid`),
    unique (`id`)
) ENGINE=InnoDB;

create table if not exists `xvzd_wargame`.`xvzd_message` (
    `no` bigint not null auto_increment,
    `recv_uid` bigint not null,
    `send_uid` bigint not null,
    `readed` tinyint(1),
    `title` varchar(128) not null,
    `content` text not null,
    `regdate` timestamp not null default current_timestamp,
    `ip` varchar(64) not null,
    primary key (`no`)
) ENGINE=InnoDB;

create table if not exists `xvzd_wargame`.`xvzd_notice` (
    `no` bigint not null auto_increment,
    `uid` bigint not null,
    `pinned` tinyint(1),
    `title` varchar(128) not null,
    `content` text not null,
    `regdate` timestamp not null default current_timestamp,
    `ip` varchar(64) not null,
    primary key (`no`)
) ENGINE=InnoDB;

create table if not exists `xvzd_wargame`.`xvzd_qna`
like `xvzd_wargame`.`xvzd_notice`;

create table if not exists `xvzd_wargame`.`xvzd_forum`
like `xvzd_wargame`.`xvzd_notice`;

/* Insert datas */
insert into `xvzd_wargame`.`xvzd_users` (id, name, password, ip)
select * from (
    select 'admin',
           'Xvezda',
           'fa449eec0fcabe9829db83e3810798f3f5e7b832ba79682cd4e474ddd51f5677b'
           '42a556cb8530d509f970b765e88b9052d77192d520acbf562178fd5aeb808ad',
           '127.0.0.1'
) as tmp where not exists (
    select `id` from `xvzd_wargame`.`xvzd_users` where id='admin'
);

insert into `xvzd_wargame`.`xvzd_notice` (pinned, title, content, uid, ip)
select * from (
    select 1,
           '[이벤트] 호스팅 서비스 오픈 이벤트 (9/1 ~ 9/30)',
           '이벤트 기간동안 가입하신 모든 분들께 30일간 Premium 패키지를 '
           '무료체험 하실 수 있는 기회를 드립니다!<br>지금 바로 가입하세요!',
           @adminUid,
           '127.0.0.1' union
    select 1,
           '게임 클리어 조건',
           '관리자는 QnA 게시판이 올라올때마다 최신 게시글을 체크합니다.<br>'
           '관리자에게 공지 게시판에 제목 "Hacked by &lt;여기에_아이디&gt;" '
           '(대소문자 구분x) 게시글을 올리게 만들면 개인쪽지로 플래그를 '
           '드립니다.',
           @adminUid,
           '127.0.0.1'
) as tmp where not exists (
    select no from `xvzd_wargame`.`xvzd_notice`
);

insert into `xvzd_wargame`.`xvzd_qna` (pinned, title, content, uid, ip)
select * from (
    select 1,
           '힌트',
           '<a href="https://github.com/Xvezda/xvzd-wargame" target="_blank">'
           'https://github.com/Xvezda/xvzd-wargame</a>',
           @adminUid,
           '127.0.0.1'
) as tmp where not exists (
    select no from `xvzd_wargame`.`xvzd_qna`
);

insert into `xvzd_wargame`.`xvzd_forum` (pinned, title, content, uid, ip)
select * from (
    select 1,
           '이곳은 자유롭게 글을 쓰실 수 있습니다.',
           '<img src="https://i.imgur.com/FGRGdLo.jpg" width="400" height="345">'
           '<p>주제가 없는 공개포럼 입니다.<br>아무주제나 편하게 써주세요 :D</p>',
           @adminUid,
           '127.0.0.1'
) as tmp where not exists (
    select no from `xvzd_wargame`.`xvzd_forum`
);

