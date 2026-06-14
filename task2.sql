use User_Actions

alter database User_Actions add filegroup User_Logs_frag
go
alter database User_Actions add file(
	name = 'User_Logs_frag_2025',
	filename = 'C:\education\SQL\LZ_6\User_Logs_frag_2025.ndf') to filegroup User_Logs_frag
go

create partition function pf_User_Logs_mounth(date)
as range right for values ('2025-02-01', '2025-03-01', '2025-04-01', '2025-05-01', '2025-06-01', '2025-07-01', '2025-08-01', '2025-09-01', '2025-10-01', '2025-11-01')
go

create partition scheme ps_User_Logs_frag
as partition pf_User_Logs_mounth to (
User_Logs_frag, User_Logs_frag, User_Logs_frag, User_Logs_frag, User_Logs_frag, User_Logs_frag, User_Logs_frag, User_Logs_frag, User_Logs_frag, User_Logs_frag, User_Logs_frag, User_Logs_frag)
go

create table Logs_frag(
	id int identity(100000000,1),
	username text not null,
	user_action text not null,
	action_date date not null,
	action_time time not null,
	action_result text not null,

	constraint pk_logs primary key clustered (id, action_date)
) on ps_User_Logs_frag(action_date)


insert into Logs_frag (username, user_action, action_date, action_time, action_result) 
	select username, user_action, action_date, action_time, action_result from User_Logs
