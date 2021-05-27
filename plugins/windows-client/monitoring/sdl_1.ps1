$totalRam = (Get-CimInstance Win32_PhysicalMemory | Measure-Object -Property capacity -Sum).Sum
$Total_Ram_in_GB = [math]::Round((Get-CimInstance -ClassName Win32_ComputerSystem).totalphysicalmemory / (1024 * 1024 * 1024),2)
while($true) {
    $date = Get-Date -format "dd-MMM-yyyy hh:mm tt"
    $date_ = Get-Date -format "dd-MM-yyyy HH:mm:ss"
    $cpuTime = [math]::Round((Get-Counter '\Processor(_Total)\% Processor Time').CounterSamples.CookedValue.ToString("#,0.000"),0)
    $availMem = (Get-Counter '\Memory\Available MBytes').CounterSamples.CookedValue
    $availMem_in_GB = [math]::Round((Get-Counter '\Memory\Available MBytes').CounterSamples.CookedValue/1024,0)
    $Ram_Usage_in_Percentage = (100-104857600 * $availMem / $totalRam).ToString("#,0.0")
    $Total_Ram_in_GB = [math]::Round((Get-CimInstance -ClassName Win32_ComputerSystem).totalphysicalmemory / (1024 * 1024 * 1024),0)
    $MemUsage_in_GB = $Total_Ram_in_GB - $availMem_in_GB
    $disks = Get-WmiObject -ComputerName $Env:COMPUTERNAME win32_logicaldisk -Filter "DriveType='3'"
    $final = ""
    foreach($disk in $disks){
        $driveLetter = ($disk | Select-Object DeviceId).DeviceId
        $Used = [math]::Round($disk.Size/1gb-$disk.FreeSpace/1gb,0)
        $Total = [math]::Round($disk.Size/1gb,0)
        $UsedPercent = [math]::Round(($Used / $Total ) * 100,0)
        $diskUsage = "$driveLetter $Used GB Out of $Total GB ($UsedPercent%)"
        $final = $final + $diskUsage + ","
    }
    Invoke-WebRequest -Uri "https://write-url-here/postsystems/" -Method Post -UseBasicParsing -Body @{
		host_name = $env:computername
		cpu_usage = "$cpuTime %"
		disk_usage = $final
		ram_usage = "$MemUsage_in_GB GB out of $Total_Ram_in_GB GB ($Ram_Usage_in_Percentage%)"
		current_time = $date 
        time_ = $date_
	}
    Start-Sleep -s 5
}