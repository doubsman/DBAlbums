Param(
	[parameter(position=0, Mandatory=$false)][string]$Envt = 'LOSSLESS_TEST',
	[parameter(position=1, Mandatory=$false)][object]$Collections = @("CLASSIC","TECHNO","TRANCE","ROCK","REGGAE"),
	[parameter(position=2, Mandatory=$false)][string]$Mode = 'UPDATE' # Mise à jour de la base ("ADDNEW")
	)

##############################################
# Construction INVENT
$Process = "BUILD_INVENT_$Envt";
# Init Variables 
$version = '1.11';
$libversion = "INVENTAIRE COLLECTION $Envt";
$global:INVENTMODE = $Mode;
$Start = (Get-Date);
$date = (Get-Date).ToString("yyyyMMddHHmmss");
# file
$path = split-path $SCRIPT:MyInvocation.MyCommand.Path -parent
$path_Out = "$path\..\LOG";
$File_NAlbums = "$path_Out\$date`_$Process`_Albums.csv";
$File_NTracks = "$path_Out\$date`_$Process`_Tracks.csv";
$File_LogTrac = "$path_Out\$date`_$Process.log";


##############################################
# trace 
Start-Transcript $File_LogTrac | Out-Null


##############################################
. "$path\BUILD_INVENT_FUNCTIONS.ps1"
<#
http://www.yusufozturk.info/windows-powershell/adding-welcome-banner-to-your-powershell-scripts.html
# Install-Module -Name PSBanner function Write-Banner
	# default
	Write-Banner "Hello!"
	# change font name, size
	Write-Banner "Hello!" -FontName "Consolas" -FontSize 14
	# use fontstyles
	Write-Banner "Hello!" -Bold -Italic -Strikeout -Underline
	# use pipeline
	"Hello!" | Write-Banner
	# use emoji
	Write-Banner "??" -FontName "Segoe UI Emoji" -FontSize 20
	# vertical writing :)
	"??" -as [char[]] | Write-Banner
#>
$env:PSModulePath = $env:PSModulePath + ";C:\Program Files\WindowsPowerShell\Modules"
Import-Module PSBanner -PassThru
#import-module "C:\Program Files\WindowsPowerShell\Modules\PSBanner\0.4\PSBanner.psd1"  -PassThru


##############################################
Super-Title -Label "ENVT $Envt DEMARRAGE $libversion version (v$version)" -Start $Start;
Write-Banner $Envt


##############################################
Super-Title -Label 'CONNECT MYSQL' -Start $Start;
$MySqlCon, $racine = ConnectEnvt -Envt $Envt
<# Effacer base
$reqStr  = "TRUNCATE TABLE $Tbl_Albums;";
$rows = Execute-MySQLNonQuery -MySqlCon $MySqlCon -requete $reqStr
$reqStr  = "TRUNCATE TABLE $Tbl_Tracks;";
$rows = Execute-MySQLNonQuery -MySqlCon $MySqlCon -requete $reqStr
$reqStr  = "TRUNCATE TABLE $Tbl_Covers;";
$rows = Execute-MySQLNonQuery -MySqlCon $MySqlCon -requete $reqStr
$reqStr  = "TRUNCATE TABLE $Tbl_Errors;";
$rows = Execute-MySQLNonQuery -MySqlCon $MySqlCon -requete $reqStr
#>


##############################################
Super-Title -Label 'LOAD BASES ALBUMS' -Start $Start;
# Loading base ALBUMS
$SqlColllec = '"' + ($Collections -join '", "') + '"'
write-host("Category Update : " + $SqlColllec)
$reqStr  = "SELECT * FROM $Tbl_Albums WHERE Category IN ($SqlColllec);";
$Records = Execute-MySQLQuery -MySqlCon $MySqlCon -requete $reqStr;
If ($Records){
	$global:DBALBUMS = @() + $Records;
	Get-MySQLTDC -MySqlCon $MySqlCon -Group "Category" -Column "Family" -TableName $Tbl_Albums -TDCName "BASE ALBUMS" -LineSum | Out-Host;
	Get-MySQLTDC -MySqlCon $MySqlCon -Group "Category" -Column "Family" -TableName $Tbl_Albums -TDCName "SIZE   (GO)" -TDCSum 'ROUND(`Size`/1024,1)' -LineSum | Out-Host;
} Else {
	$global:DBALBUMS = @();
}

# base TRACKS
$reqStr  = "SELECT IFNULL(MAX(ID_TRACK),0) AS CPTIDTK FROM $Tbl_Tracks;";
$Records = Execute-MySQLQuery -MySqlCon $MySqlCon -requete $reqStr;
If ($Records){
	$global:cptIDTK = $Records.CPTIDTK;
	If ($global:cptIDTK -ne 0) {
		Get-MySQLTDC -MySqlCon $MySqlCon -Group "Category" -Column "Family" -TableName $Tbl_Tracks -TDCName "BASE TRACKS" -LineSum | Out-Host;
	}
}

##############################################
Super-Title -Label "BUILD ALBUMS LIST mode $global:INVENTMODE" -Start $Start;
Write-Host (' '*6+" Category |  Cpt  |State|  Ids  | Method| Name");
Write-Host (' '*6+"----------|-------|-----|-------|-------|"+'-'*111);
$A_List = $T_List = @();
ForEach ($Collection in $Collections){
	$reps = Get-ChildItem -LiteralPath "$racine\$Collection\" | Where-Object { $_.PSIsContainer } | Sort-Object Name | Select-Object Name,Fullname;
	ForEach ($rep in $reps){
		$Position = $rep.FullName.Split("\")[5];
		$Family = ($Families.GetEnumerator() | Where-Object { $Position -Match $_.Value}).Name;
		If ($Family){
			If (($Family -match 'Download') -and !($Collection -match 'TRANCE')) { 
				$Resultat = (Get-ListeAlb -pathAlbumsList $rep.Fullname -Family $Family);
				If ($Resultat[0]){
					$A_List += $Resultat[0];
					$T_List += $Resultat[1];
				}
			} Else { 
				$List_Reps = Get-ChildItem -LiteralPath $rep.Fullname | Where-Object { $_.PSIsContainer } | Sort-Object Name | Select-Object Name,Fullname;
				ForEach ($List_Rep in $List_Reps){
					$Resultat = (Get-ListeAlb -pathAlbumsList $List_Rep.Fullname -Family $Family);
					If ($Resultat[0]){
						$A_List += $Resultat[0];
						$T_List += $Resultat[1];
					}
				}
			}
		}
	}
}
Write-Host ("`r`n"+' '*6+"----------|------|-----|------|-------|"+'-'*111+"`n");
# pause de 5 secondes
Super-Waiting


##############################################
If (($global:INVENTMODE -eq 'UPDATE') -and ($A_List)){
	Super-Title -Label "VERIFICATION BASE $Envt" -Start $Start;
	$Diff_ABase = Compare-Object -referenceObject $global:DBALBUMS -differenceObject $A_List -Property ID_CD, Name, Path;
	# NEW
	$Diff_ABase | Select SideIndicator, ID_CD, Name, Path | ForEach-Object {if($_.SideIndicator -eq '=>'){ Write-Host ('      | (N) (ID-'+$_.Id_CD+') '+$_.Name)} };
	# ORPHELINS de la base ALBUMS
	$Diff_ABase | Select SideIndicator, ID_CD, Name, Path | ForEach-Object {if($_.SideIndicator -eq '<='){ Write-Host ('      | (S) (ID-'+$_.Id_CD+') '+$_.Name+' "'+$_.Path+'"') -foregroundcolor "yellow"} };
	# ID_CD OPRHELINS
	$OA_ListIDs = $Diff_ABase | Where-Object { $_.SideIndicator -eq '<='} | Select SideIndicator, ID_CD, Name, Path;
	# DOUBLONS
	$List_IDs = $A_List | Group-Object -property MD5 | Where-Object {$_.Count -gt 1};
	if ($List_IDs){
		$Doublons = $A_List | Where-Object {$List_IDs.Group.ID_CD -contains $_.ID_CD};
		$messAno = "DOUBLONS ALBUMS dans la base"
		Write-Host -foregroundcolor "yellow" ("`r`n"+' '*10+' | '+$messAno);
		$Doublons | Format-Table -Property @{Expression={      }},Name,Path | Out-Host
		ForEach ($Album_Result In $Doublons){
			Anno-toMySQL -MySqlCon $MySqlCon -ID_CD $Album_Result.ID_CD -Path $Album_Result.Path -Mess 'Doublons Albums' -Code 'DBL';
		}
	}
	Write-Host (' '*6+"| MODE '$global:INVENTMODE ': MISE A JOUR BASE $Tbl_Albums");
	ForEach ($OA_ALBUM In $OA_ListIDs){
		$reqStr  = "DELETE ALB FROM $Tbl_Albums AS ALB WHERE ALB.ID_CD="+$OA_ALBUM.ID_CD; 
		$rows = Execute-MySQLNonQuery -MySqlCon $MySqlCon -requete $reqStr
		Write-Host (' '*10+"| {0:0000} | Suppression : {1,-111}" -f $OA_ALBUM.ID_CD, $OA_ALBUM.Name);
	}
	# On met à jour la base DBCOVERS: ORPHELINS
	$reqStr  = "DELETE COV FROM $Tbl_Covers AS COV LEFT JOIN $Tbl_Albums AS ALB ON ALB.MD5=COV.MD5 WHERE ISNULL(ALB.MD5);"; 
	$rows = Execute-MySQLNonQuery -MySqlCon $MySqlCon -requete $reqStr	
	If ($rows -gt 0){
		Write-Host (' '*6+"| MODE '$global:INVENTMODE ': MISE A JOUR $Tbl_Covers ($rows ligne(s) supprimée(s)");
	}
	# On met à jour la base DBTRACKS: ORPHELINS
	$reqStr= "DELETE TRK FROM $Tbl_Tracks AS TRK LEFT JOIN $Tbl_Albums AS ALB ON ALB.ID_CD=TRK.ID_CD WHERE ISNULL(ALB.ID_CD);";
	$rows = Execute-MySQLNonQuery -MySqlCon $MySqlCon -requete $reqStr;
	If ($rows -gt 0){
		Write-Host (' '*6+"| MODE '$global:INVENTMODE ': MISE A JOUR $Tbl_Tracks ($rows ligne(s) supprimée(s)");
	}
}


##############################################
Super-Title -Label 'BUILD TDC' -Start $Start;
# NEWS ALBUMS
Write-Host (' '*2 + $Tbl_Albums.Padright(50,"_"));
# on affiche le table des compteurs NEW
If ($A_List | Where-Object {$_.Statut -eq "NEW"}){
	Get-PSArrayTDC -Collection $Collections -BASE ($A_List | Where-Object {$_.Statut -eq "NEW"}) -TabName 'NEW ALBUM(S)' | Out-Host;
	Get-PSArrayTDC -Collection $Collections -BASE $T_List -TabName 'NEW TRACK(S)' | Out-Host;
} Else {Write-Host (' '*6+'| NEW 0')};
# on affiche le table des compteurs UPDATE
If ($A_List | Where-Object {$_.Statut -eq "UPDATE"}){
	Get-PSArrayTDC -Collection $Collections -BASE ($A_List | Where-Object {$_.Statut -eq "UPDATE"}) -TabName 'UPDATE ALBUM(S)' | Out-Host;
} Else {Write-Host (' '*6+'| UPDATE 0')};
$NA_List = $A_List | Where-Object {($_.Statut -eq "UPDATE") -or ($_.Statut -eq "NEW")};
If ($NA_List){
	Get-MySQLTDC -MySqlCon $MySqlCon -Group "Statut" -Column "Category" -TableName $Tbl_Albums -TDCName "ALBUMS MYSQL" -LineSum | Out-Host;
	Get-MySQLTDC -MySqlCon $MySqlCon -Group "Category" -Column "Family" -TableName $Tbl_Tracks -TDCName "TRACKS MYSQL" -LineSum | Out-Host;
}

# FICHIERS CSV
If ($NA_List){
	$NA_List = $NA_List | Sort-Object  @{Expression='Category'; Descending=$true }, @{Expression='Position1'; Ascending=$true }, @{Expression='Position2'; Ascending=$true }, @{Expression='Name'; Ascending=$true };
	$NA_List | Export-Csv $File_NAlbums -NoTypeInformation -Encoding UTF8 -Delimiter ';' ;
	Write-Host (' '*7 + $File_NAlbums.Padright(50,"_"));
}
If ($T_List){
	$T_List | Export-Csv $File_NTracks -NoTypeInformation -Encoding UTF8 -Delimiter ';' 
	Write-Host (' '*7 + $File_NTracks.Padright(50,"_"));	
}

#
##############################################
Super-Title -Label 'BUILD COVER TO MySQL' -Start $Start;
$reqStr = "SELECT ALB.ID_CD, ALB.Name, ALB.MD5, ALB.Cover, ALB.Category FROM $Tbl_Albums AS ALB LEFT JOIN $Tbl_Covers AS COV ON ALB.MD5=COV.MD5 WHERE ISNULL(COV.MD5) AND Cover<>'No Picture' ORDER BY ALB.ID_CD";
$Records = Execute-MySQLQuery -MySqlCon $MySqlCon -requete $reqStr;
If ($Records){$ListMAJCover = @() + $Records};
$cpt = ($ListMAJCover | Measure-Object).Count;
ForEach ($MAJCover in $ListMAJCover){
	Write-Host (' '*6+"| {4,-16} | {0:0000} | ({1}) | {2:0000} | {5,-62}" -f $cpt, "C" , [int32]$MAJCover.ID_CD, $MAJCover.Name, $MAJCover.Category, $MAJCover.Cover);
	Covers-ToMySQL -MySqlCon $MySqlCon -PathCover $MAJCover.cover -MD5 $MAJCover.MD5;
	$cpt--
}
Write-Host ("`r`n");
#>


##############################################
Super-Title -Label 'PURJE LOGS' -Start $Start;
PurgeLog -Path $path_Out -NameLog $Process


##############################################
Super-Title -Label 'ANOMALIE(S) ANALYSE' -Start $Start;
$reqStr = "SELECT DISTINCT ID_CD,COD, MESS FROM $Tbl_Errors WHERE Date_insert>="+(Get-Date $Start).ToString("yyyyMMddHHmmss");
$Records = Execute-MySQLQuery -MySqlCon $MySqlCon -requete $reqStr;
$Records | Format-Table -Property @{Expression={mysql}},* -autoSize;


##############################################
Super-Title -Label 'DISCONNECT MYSQL' -Start $Start;
Disconnect-MySQL $MySqlCon


##############################################
Super-Title -Label ("...FIN...") -Start $Start;
# fin trace
Stop-Transcript | Out-Null
#Start $path_Out;

<#
FICHIER TROP LONG
# fichier trop >260 \\DOUBBIGSTATION\_LossLess
$folders = cmd /c dir E:\Work\TAG_bluid\TEST /s /-c /a:h /a:d
$folders = $folders -match "Répertoire"
$folders = $folders | %{$_.Replace(" Répertoire de ","")}

HTTP FOOBAR
http://127.0.0.1:8888/default/?cmd=Stop&param1=
http://127.0.0.1:8888/default/?cmd=PlayOrPause
http://127.0.0.1:8888/default/?cmd=CreatePlaylist&param1=playlist name&param2=insertion point index
#>
