Param(
	[parameter(position=0, Mandatory=$true)]
	[string]$Envt)

##############################################
# Construction INVENT
$Process = "CORRECTIONS_ALBUMS_"+$Envt;
$version = '1.00';
$Start = (Get-Date);
$date	= (Get-Date).ToString("yyyyMMddHHmmss");
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

Write-Banner $Envt
Super-Title -Label ('START '+$Process) -Start $Start;

##############################################
$MySqlCon, $racine = ConnectEnvt -Envt $Envt
##############################################

Covers-ToMySQL -MySqlCon $MySqlCon -PathCover "E:\Download\coeur.jpg" -MD5 'YYYYYY';

##############################################
PurgeLog -Path $path_Out -NameLog $Process

##############################################
Disconnect-MySQL $MySqlCon
##############################################
Super-Title -Label 'END' -Start $Start;
Stop-Transcript | Out-Null
