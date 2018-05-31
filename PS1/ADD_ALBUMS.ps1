Param(
	[parameter(position=0, Mandatory=$true)]
	[string]$Envt,
	[parameter(position=1, Mandatory=$true)]
	[string]$AlbumReps)

##############################################
# Construction INVENT
$Process = "ADD_ALBUMS_"+$Envt;
$version = '1.00';
$date = (Get-Date).ToString("yyyyMMddHHmmss");
$Start = (Get-Date);
$path = split-path $SCRIPT:MyInvocation.MyCommand.Path -parent
$path_Out = "$path\..\LOG";
$File_LogTrac = "$path_Out\$date`_$Process.log";


##############################################
Start-Transcript $File_LogTrac | Out-Null
##############################################
. "$path\BUILD_INVENT_FUNCTIONS.ps1"
$env:PSModulePath = $env:PSModulePath + ";C:\Program Files\WindowsPowerShell\Modules"
Import-Module PSBanner -PassThru
#import-module "C:\Program Files\WindowsPowerShell\Modules\PSBanner\0.4\PSBanner.psd1"  -PassThru

Super-Title -Label ('START '+$Process) -Start $Start;

##############################################
$MySqlCon, $racine = ConnectEnvt -Envt $Envt
$nbupdate = ($AlbumReps.split(',')).Length;
$crupdate = 1;
$LossLess = ($Envt -match "LOSSLESS")
Foreach ($AlbumRep in $AlbumReps.split(',')){
	Super-Title -Label ("Analyse album ""$AlbumRep"" ($crupdate/$nbupdate)") -Start $Start;
	$crupdate ++
	Run-AddNewAlbum -AlbumRep $AlbumRep -LossLess $LossLess
}


##############################################
PurgeLog -Path $path_Out -NameLog $Process

##############################################
Disconnect-MySQL $MySqlCon
##############################################
Super-Title -Label 'END' -Start $Start;
Stop-Transcript | Out-Null
