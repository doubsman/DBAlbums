UPDATE ALBUMS 
SET `ADD` = strftime('%Y-%m-%d %H:%M:%S', `ADD`), 
	`MODIFIED` =  strftime('%Y-%m-%d %H:%M:%S', `MODIFIED`);