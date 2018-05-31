Param(
	[parameter(position=0, Mandatory=$true)]
	[string]$Envt,
	[parameter(position=1, Mandatory=$true)]
	[string]$Album_IDCD,
	[parameter(position=1, Mandatory=$true)]
	[string]$Logs
	)

##############################################
# Construction INVENT
$Process = "UPDATE_ALBUM_"+$Envt;
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
$date	= (Get-Date).ToString("yyyyMMddHHmmss");
$path = split-path $SCRIPT:MyInvocation.MyCommand.Path -parent
$path_Out = $Logs;
$File_LogTrac = "$path_Out\$date`_$Process.log";
$Table_Version = 20;
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


# Write-Host Waiting
Function Super-Title{
	param ([parameter(Mandatory = $True)][Datetime] $Start,
		   [parameter(Mandatory = $False)][String] $Label='',
		   [parameter(Mandatory = $False)][Int32]  $Width=154,
		   [parameter(Mandatory = $False)][String] $Deco1='*',
		   [parameter(Mandatory = $False)][String] $Deco2='-')

	#$Colors = @("DarkBlue","DarkGreen","DarkCyan","DarkRed","DarkMagenta","DarkYellow","Gray","Blue","Green","Cyan","Magenta","Yellow","White");
	#$foregroundcolor = Get-Random -Input $Colors;
	$Minute = [math]::Round(((Get-Date) - $Start).TotalMinutes,0);
	If ($Minute -eq 0){
		$Second = [math]::Round(((Get-Date) - $Start).TotalSeconds,0);
		$Length = [string]$Second + ' sec';
	} Else {
		$Length = [string]$Minute + ' min(s)';
	}
	$Tittle = $Deco1*$Width + "`n`r" + $Deco2*10 + ' ' + (Get-Date).tostring('HH:mm:ss') + " -- Durée: $Length -- $Label " + $Deco2*($Width-33-$Label.Length-$Length.Length) + "`n`r";
	Write-Host -foregroundcolor 'Green' $Tittle;
}


Super-Title -Label ('START '+$Process) -Start $Start;
##############################################
Start-Transcript $File_LogTrac | Out-Null
##############################################
. "$path\BUILD_INVENT_FUNCTIONS.ps1"
. "$path\Write-Banner.ps1"

Write-Banner $Envt

##############################################
$MySqlCon = Connect-MySQL -MySQLHost $serv -user $user -password $password -Database $db -port $port;
##############################################
$reqStr  = "SELECT IFNULL(MAX(ID_TRACK),0) AS CPTIDTK FROM $Tbl_Tracks;";
$Records = Execute-MySQLQuery -MySqlCon $MySqlCon -requete $reqStr;
$global:cptIDTK = $Records.CPTIDTK;
Run-UpdateAlbum($Album_IDCD)
##############################################
$nbfiles = (Get-ChildItem -LiteralPath ($path_Out) -file |  Where-Object { !($_.name.StartsWith('DB')) } | Measure-Object).count
If ($nbfiles -gt $Table_Version){
	Get-ChildItem -LiteralPath ($path_Out) -file |  Where-Object { !($_.name.StartsWith('DB')) } |  Where-Object { ($_.name -match $Process) } | Sort-Object LastWriteTime | Select -First ($nbfiles-$Table_Version) | %{Write-Host ('      | remove '+$_.fullname); Remove-Item $_.fullname}
}
##############################################
Disconnect-MySQL $MySqlCon
##############################################
Super-Title -Label 'END' -Start $Start;
Stop-Transcript | Out-Null
