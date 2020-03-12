pyinstaller main.spec
# xcopy ff*.exe dist /y
# xcopy icon.ico dist /y
# $WshShell = New-Object -comObject WScript.Shell
# $Shortcut = $WshShell.CreateShortcut(".\dist\vca.lnk")
# $Shortcut.TargetPath ="vca\vca.exe"
# $Shortcut.Save()
[System.Console]::Write('OK.')
[void][System.Console]::ReadKey(1)