pyinstaller main.py -F --icon ./icon.ico -w
# pyinstaller main.spec
xcopy ff*.exe dist /y
xcopy icon.ico dist /y
# $WshShell = New-Object -comObject WScript.Shell
# $Shortcut = $WshShell.CreateShortcut(".\dist\vca.lnk")
# $Shortcut.TargetPath ="vca\vca.exe"
# $Shortcut.Save()
Remove-Item ./build -r -fo
Remove-Item ./__pycache__ -r -fo
[System.Console]::WriteLine('OK.')
[void][System.Console]::ReadKey(1)