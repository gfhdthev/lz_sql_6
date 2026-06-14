--информация о бэкапе
restore filelistonly 
from disk = 'C:\education\SQL\LZ_6\Backups\lz6.bak'
go

use master
go

create procedure dbo.sp_RestoreDatabaseFromBackup
    @BackupPath nvarchar(200)
as
begin
    declare @SQL nvarchar(max)
    set @SQL = N'
    restore database User_Actions from disk = ''' + @BackupPath + '''
    with 
        move ''User_Actions'' to ''C:\education\SQL\LZ_6\Data\User_Actions.mdf'',
        move ''User_Logs_frag_2025'' to ''C:\education\SQL\LZ_6\Data\User_Logs_frag_2025.ndf'',
        move ''User_Actions_log'' to ''C:\education\SQL\LZ_6\Data\User_Actions_log.ldf'',
        replace'
    exec (@SQL)
end
go

exec dbo.sp_RestoreDatabaseFromBackup @BackupPath = N'C:\education\SQL\LZ_6\Backups\lz6.bak'

-- Обработано 49208 страниц для базы данных "User_Actions", файл "User_Actions" для файла 1.
-- Обработано 43264 страниц для базы данных "User_Actions", файл "User_Logs_frag_2025" для файла 1.
-- Обработано 2 страниц для базы данных "User_Actions", файл "User_Actions_log" для файла 1.
-- RESTORE DATABASE успешно обработал 92474 страниц за 1.402 секунд (515.299 MБ/сек).
