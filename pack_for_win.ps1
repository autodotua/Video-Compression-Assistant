pyinstaller main.py -F --icon ./icon.ico -w
# pyinstaller main.spec
Copy-Item "ff*.exe" -Destination "dist"
Copy-Item "icon.ico" -Destination "dist"
Move-Item -Path "./dist/main.exe" -Destination "./dist/vca.exe" -Force
#xcopy ff*.exe dist /y
# xcopy icon.ico dist /y
# xcopy ./dist/main.exe ./dist/vca.exe /y
# $WshShell = New-Object -comObject WScript.Shell
# $Shortcut = $WshShell.CreateShortcut(".\dist\vca.lnk")
# $Shortcut.TargetPath ="vca\vca.exe"
# $Shortcut.Save()
Remove-Item ./build -r -fo
Remove-Item ./__pycache__ -r -fo
[System.Console]::WriteLine('OK.')
[void][System.Console]::ReadKey(1)