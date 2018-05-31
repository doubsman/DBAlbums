Param(
	[parameter(position=0, Mandatory=$true)]
	[string]$Envt,
	[parameter(position=1, Mandatory=$true)]
	[string]$listID_CD)

##############################################
# Construction INVENT
$Process = "UPDATE_ALBUMS_"+$Envt;
$version = '1.00';
$Start = (Get-Date);
# environnement
Switch ($Envt){
		{$_ -eq "LOSSLESS"} {
			$ErrorActionPreference = "Continue";
			$serv = "homerstation";
			$user = "AdmInvent";
			$db = "Invent";
			$password = "JMctOz7a6TWnrJHB86pL";
		}
		{$_ -eq "MP3"} {
			$ErrorActionPreference = "Continue";
			$serv = 'homerstation'
			$user = 'admInventMP3'
			$db = "InventMP3";
			$password = 'nuDbC6spVZxtkKC8'
		}
		{$_ -eq "MP3_TEST"} {
			$ErrorActionPreference = "Stop";
			$serv = "doubbigstation";
			$user = "admInvent";
			$db = "MP3";
			$password = "MwRbBR2HA8PFQjuu";
		}
		default { # TEST
			$ErrorActionPreference = "Stop";
			$serv = 'doubbigstation'
			$user = 'admInvent'
			$db = "Invent";
			$password = 'MwRbBR2HA8PFQjuu'
		}
}
# files
$date = (Get-Date).ToString("yyyyMMddHHmmss");
$path = split-path $SCRIPT:MyInvocation.MyCommand.Path -parent
$path_Out = "$path\..\Logs";
$File_LogTrac = "$path_Out\$date`_$Process.log";
$Table_Version = 20;
$global:cptIDTK = 0;
# base de données  
$port = "3306";
$Tbl_Albums = "DBALBUMS";
$Tbl_Tracks = "DBTRACKS";
$Tbl_Covers = "DBCOVERS";
$Tbl_Errors = "DBERRORS";
# globaux
$path = split-path $SCRIPT:MyInvocation.MyCommand.Path -parent
$global:AlBumArtDownloader = 'C:\Program Files\AlbumArtDownloader\AlbumArt.exe';
$global:Compteur = 0;
$global:FileDllTag = "$path\taglib-sharp.dll";
$global:MaskMusic = @('.flac','.ape','.wma','.mp3','.wv','.aac','.mpc');
$global:MaskCover = @('.jpg','.jpeg','.png','.bmp','.tif','.bmp');
$global:CoverAlbum = @('cover.jpg','Cover.jpg','cover.jpeg','cover.png','front.jpg','folder.jpg','folder.jpeg');


##############################################
Start-Transcript $File_LogTrac | Out-Null
##############################################
. "$path\BUILD_INVENT_FUNCTIONS.ps1"
. "$path\Write-Banner.ps1"
Write-Banner $Envt
Super-Title -Label ('START '+$Process) -Start $Start;

##############################################
$MySqlCon = Connect-MySQL -MySQLHost $serv -user $user -password $password -Database $db -port $port;
$nbupdate = ($listID_CD.split(',')).Length;
$crupdate = 1;
$LossLess = ($Envt -match "LOSSLESS")
Foreach ($ID_CD in $listID_CD.split(',')){
	Super-Title -Label ("uptade album ID=$ID_CD ($crupdate/$nbupdate)") -Start $Start;
	$crupdate ++
	Run-UpdateAlbum -ID_CD $ID_CD -LossLess $LossLess
}

##############################################
$nbfiles = (Get-ChildItem -LiteralPath ($path_Out) -file |  Where-Object { ($_.name -match $Process) } | Measure-Object).count
If ($nbfiles -gt $Table_Version){
	Get-ChildItem -LiteralPath ($path_Out) -file | Where-Object { ($_.name -match $Process) } | Sort-Object LastWriteTime | Select -First ($nbfiles-$Table_Version) | %{Write-Host ('      | remove '+$_.fullname); Remove-Item $_.fullname}
}
##############################################
Disconnect-MySQL $MySqlCon
##############################################
Super-Title -Label 'END' -Start $Start;
Stop-Transcript | Out-Null
