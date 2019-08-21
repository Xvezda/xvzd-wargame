/* Copyright (C) 2019 Xvezda <https://xvezda.com/> */
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
           '127.0.0.1' union
    select 'yabiru-bot',
           'ayibur',
           'fa449eec0fcabe9829db83e3810798f3f5e7b832ba79682cd4e474ddd51f5677b'
           '42a556cb8530d509f970b765e88b9052d77192d520acbf562178fd5aeb808ad',
           '127.0.0.1' union
    select 'guest',
           'guest',
           'fa449eec0fcabe9829db83e3810798f3f5e7b832ba79682cd4e474ddd51f5677b'
           '42a556cb8530d509f970b765e88b9052d77192d520acbf562178fd5aeb808ad',
           '127.0.0.1'
) as tmp where not exists (
    select `id` from `xvzd_wargame`.`xvzd_users` where id='admin'
);
set @adminUid = (select `uid` from `xvzd_wargame`.`xvzd_users` where id='admin');
set @botUid = (select `uid` from `xvzd_wargame`.`xvzd_users` where name='ayibur');
set @guestUid = (select `uid` from `xvzd_wargame`.`xvzd_users` where id='guest');

insert into `xvzd_wargame`.`xvzd_notice` (pinned, title, content, uid, regdate, ip)
select * from (
    select 1,
           '[이벤트] 호스팅 서비스 오픈 이벤트 (9/1 ~ 9/30)',
           '이벤트 기간동안 가입하신 모든 분들께 30일간 Premium 패키지를 '
           '무료체험 하실 수 있는 기회를 드립니다!<br>지금 바로 가입하세요!',
           @adminUid,
           timestamp('2019-08-15 00:00:00'),
           '127.0.0.1' union
    select 0,
           '[서비스점검] 서비스를 점검 합니다. (8/1 ~ 8/2)',
           '사이트의 보안취약점을 발견하여 잠시 서비스를 중단합니다.<br>'
           '고객 여러분의 양해를 바랍니다.<br><br>'
           '--- 수정 ---<br>점검이 완료 되었습니다.',
           @adminUid,
           timestamp('2019-08-01 13:00:00'),
           '127.0.0.1'
) as tmp where not exists (
    select no from `xvzd_wargame`.`xvzd_notice`
);

insert into `xvzd_wargame`.`xvzd_qna` (pinned, title, content, uid, regdate, ip)
select * from (
    select 1,
           '서비스 관련 질문은 이곳에 해주세요',
           '실시간 알림으로 24시간 답변드리고 있습니다!',
           @adminUid,
           timestamp('2019-08-01 00:00:00'),
           '127.0.0.1' union
    select 1,
           'JUST ANOTHER HINT',
           '<a href="https://github.com/Xvezda/xvzd-wargame/blob/master/'
           'app/common/lib/security.py" target="_blank">'
           'Source code</a><br><br>'
           '<p class="text-muted">There is another hidden hint here.</p>'
           '<!-- Hint: CSRF, XSS, HTML5, Bypass, Gadget -->',
           @adminUid,
           now(),
           '127.0.0.1' union
    select 0,
           'Is mayonnaise an instrument?',
           '._.',
           @guestUid,
           timestamp('2019-08-03 23:23:23'),
           '127.0.0.1'
) as tmp where not exists (
    select no from `xvzd_wargame`.`xvzd_qna`
);

insert into `xvzd_wargame`.`xvzd_forum` (pinned, title, content, uid, regdate, ip)
select * from (
    select 1,
           '이곳은 자유롭게 글을 쓰실 수 있습니다.',
           '<img src="https://i.imgur.com/FGRGdLo.jpg" width="400" height="345">'
           '<p>주제가 없는 공개포럼 입니다.<br>아무주제나 편하게 써주세요 :D</p>',
           @adminUid,
           timestamp('2019-08-01 00:00:00'),
           '127.0.0.1' union
    select 0,
           '본인 방금 Pwn2Own우승하는 상상함 ㅋㅋㅋ',
           '<img src="https://i.imgur.com/hsoVAVU.png">'
           '<p>웹 브라우저들 차례차례 익스짜서 1등하는거지 ㅋㅋㅋㅋㅋㅋ</p>'
           '<p>객체들 놀라서 도망치려고 하지만 내 사거리에서 벗어나는 건 불가능 '
           'ㅋㅋㅋ 메모리 릭으로 다 죽어나고ㅋㅋㅋ</p>'
           '<img src="https://i.imgur.com/7a5pFfl.png">'
           '<p>뒤늦게 샌드박스로 막으려 하지만 어림도 없지 ㅋㅋㅋ '
           '바로 샌드박스 이스케이프해서 루트쉘따기!! ㅋㅋㅋ</p>'
           '<p>아 생각만 해도 기분좋네 ㅋㅋㅋㅋㅋ</p>',
           @guestUid,
           timestamp('2019-08-01 11:11:11'),
           '127.0.0.1' union
    select 0,
           'Hello Webhackers',
           '<sVg/OnLoAd="confirm(\'Do you like meu?\')'
           '?location.href=\'https://rubiya.kr/\''
           ':this.parentElement.removeChild(this)">'
           '<p>:D</p>',
           @botUid,
           timestamp('2019-08-01 12:34:56'),
           '127.0.0.1'
) as tmp where not exists (
    select no from `xvzd_wargame`.`xvzd_forum`
);

