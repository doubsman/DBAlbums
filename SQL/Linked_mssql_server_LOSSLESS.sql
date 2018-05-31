USE [master]
GO

EXEC master.dbo.sp_addlinkedserver 
@server = N'HOMERSTATION'
,@srvproduct=N'MySQL'
,@provider=N'MSDASQL'
,@provstr=N'DRIVER={MySQL ODBC 5.3 ANSI Driver};SERVER=homerstation;DATABASE=Invent;PORT=3306;DATABASE=Invent; USER=AdmInvent;PASSWORD=JMctOz7a6TWnrJHB86pL;OPTION=134217728'
GO


