Param(
	[parameter(position=0, Mandatory=$true)]
	[string]$Envt,
	[parameter(position=1, Mandatory=$true)]
	[string]$listID_CD)

##############################################
# Construction INVENT
$Process = "UPDATE_ALBUMS_"+$Envt;
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

$ban = Write-Banner $Envt
write-host($ban)
Super-Title -Label ('START '+$Process) -Start $Start;

##############################################
$MySqlCon, $racine = ConnectEnvt -Envt $Envt
$nbupdate = ($listID_CD.split(',')).Length;
$crupdate = 1;
$LossLess = ($Envt -match "LOSSLESS")
Foreach ($ID_CD in $listID_CD.split(',')){
	Super-Title -Label ("uptade album ID=$ID_CD ($crupdate/$nbupdate)") -Start $Start;
	$crupdate ++
	Run-UpdateAlbum -ID_CD $ID_CD -LossLess $LossLess
}

##############################################
PurgeLog -Path $path_Out -NameLog $Process

##############################################
Disconnect-MySQL $MySqlCon

##############################################
Super-Title -Label 'END' -Start $Start;
Stop-Transcript | Out-Null