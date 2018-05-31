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

$LossLess = ($Envt -match "LOSSLESS")
$reqStr  = "SELECT DISTINCT ID_CD FROM DBTRACKS WHERE LENGTH(TAG_Genres)=70;";
$Records = Execute-MySQLQuery -MySqlCon $MySqlCon -requete $reqStr;
$Records = @('997', '4640', '3607', '3608', '3609', '3610', '3611', '3612', '3613', '3614', '3962', '3668')
ForEach ($row in $Records){
	#Super-Title -Label ("uptade album ID="+$row.ID_CD) -Start $Start;
	#Run-UpdateAlbum -ID_CD $row.ID_CD -LossLess $LossLess -Force $True
	Super-Title -Label ("uptade album ID="+$row) -Start $Start;
	Run-UpdateAlbum -ID_CD $row -LossLess $LossLess -Force $True
}

##############################################
PurgeLog -Path $path_Out -NameLog $Process

##############################################
Disconnect-MySQL $MySqlCon
##############################################
Super-Title -Label 'END' -Start $Start;
Stop-Transcript | Out-Null
