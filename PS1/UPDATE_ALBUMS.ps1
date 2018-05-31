Param(
	[parameter(position=0, Mandatory=$True)][string]$Envt,
	[parameter(position=1, Mandatory=$True)][string]$TypeOpe,
	[parameter(position=2, Mandatory=$True)][string]$AlbumInfos,
	[parameter(position=3, Mandatory=$False)][string]$Category,
	[parameter(position=4, Mandatory=$False)][string]$Family,
	[parameter(position=4, Mandatory=$False)][switch]$Force
	)

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
if ($Force){
	$BForce = $True
} else {
	$BForce = $False
}
$LossLess = ($Envt -match "LOSSLESS")
$listacti = $TypeOpe.replace('"','').split('|')
$listinfo = $AlbumInfos.replace('"','').split('|')
$nbupdate = $listinfo.Length;
$listcate = $Category.replace('"','').split('|')
$listfami = $Family.replace('"','').split('|')
$counters = 0
Foreach ($AlbumRep in $listinfo){
	if ($listacti[$counters] -eq 'ADD'){
		$apath = $listinfo[$counters]
		$acate = $listcate[$counters]
		$afami = $listfami[$counters]
		$counters++
		Super-Title -Label ("ADD   : $acate $afami $apath ($counters/$nbupdate)") -Start $Start;
		Run-AddNewAlbum -AlbumRep $apath -LossLess $LossLess -Category $acate -Family $afami
	}
	if (($listacti[$counters] -eq 'UPDATE') -or ($listacti[$counters] -eq 'DELETE')){
		$aidcd = $listinfo[$counters]
		$counters++
		Super-Title -Label ("UPDATE: $aidcd ($counters/$nbupdate)") -Start $Start;
		Run-UpdateAlbum -ID_CD $aidcd -LossLess $LossLess -Force $BForce
	}
	
}


##############################################
PurgeLog -Path $path_Out -NameLog $Process

##############################################
Disconnect-MySQL $MySqlCon
##############################################
Super-Title -Label 'END' -Start $Start;
Stop-Transcript | Out-Null
