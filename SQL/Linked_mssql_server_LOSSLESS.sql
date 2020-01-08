USE [master]
GO

EXEC master.dbo.sp_addlinkedserver 
@server = N'HOMERSTATION'
,@srvproduct=N'MySQL'
,@provider=N'MSDASQL'
,@provstr=N'DRIVER={MySQL ODBC 8.0 ANSI Driver};SERVER=homerstation;DATABASE=DBALBUMS;PORT=3307; USER=AdmInvent;PASSWORD=JMctOz7a6TWnrJHB86pL;OPTION=134217728'
GO


