SET IDENTITY_INSERT [dbo].[DBALBUMS] ON
INSERT INTO [dbo].[DBALBUMS] ([ID_CD]
		   ,[MD5]
           ,[Family]
           ,[Category]
           ,[Position1]
           ,[Position2]
           ,[Name]
           ,[Label]
           ,[ISRC]
           ,[Year]
           ,[Qty_CD]
           ,[Qty_Cue]
           ,[Qty_CueERR]
           ,[Qty_repMusic]
           ,[Qty_Tracks]
           ,[Qty_audio]
           ,[Typ_Audio]
           ,[Qty_repCover]
           ,[Qty_covers]
           ,[Cover]
           ,[Path]
           ,[Size]
           ,[Duration]
           ,[Length]
           ,[Typ_Tag]
           ,[Date_Insert]
           ,[Date_Modifs]
           ,[RHDD_Modifs]
           ,[Score]
           ,[Statut])
SELECT * 
FROM openquery([HOMERSTATION], 'SELECT * FROM Invent.DBALBUMS')
SET IDENTITY_INSERT dbo.[DBALBUMS] OFF;
GO
SET IDENTITY_INSERT dbo.[DBTRACKS] ON;
INSERT INTO [dbo].[DBTRACKS]
           ([ID_CD],[ID_TRACK]
           ,[Family]
           ,[Category]
           ,[Position1]
           ,[Position2]
           ,[REP_Album]
           ,[REP_Track]
           ,[FIL_Track]
           ,[TAG_Exten]
           ,[TAG_Album]
           ,[TAG_Albumartists]
           ,[TAG_Year]
           ,[TAG_Disc]
           ,[TAG_Track]
           ,[ODR_Track]
           ,[TAG_Artists]
           ,[TAG_Title]
           ,[TAG_Genres]
           ,[TAG_Duration]
           ,[TAG_length]
           ,[Score]
           ,[Date_Insert]
           ,[Statut])
SELECT * 
FROM openquery([HOMERSTATION], 'SELECT * FROM Invent.DBTRACKS')
SET IDENTITY_INSERT dbo.[DBTRACKS] OFF;
GO
INSERT INTO [dbo].[DBCOVERS]
           ([MD5]
           ,[Cover64]
           ,[MiniCover64])
SELECT * 
FROM openquery([HOMERSTATION], 'SELECT * FROM Invent.DBCOVERS')




