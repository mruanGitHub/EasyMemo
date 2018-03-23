#NoEnv
SendMode Input
SetWorkingDir %A_WorkingDir%
#SingleInstance Force

; Show the Input Box to the user
Loop
{
   inputbox, text, Diary (Your input will be appended in %A_WorkingDir%\diary.txt),,,750,150
   ; Format the time-stamp
   current=%A_DD%/%A_MM%/%A_YYYY%, %A_Hour%:%A_Min%
   ; Write this data to the diary.txt file
   myVar := text
   
   if ErrorLevel  ;Concel pressed
      break
   else if myVar <> 
   {
      fileappend, %current% - %text%`n, %A_WorkingDir%\diary.txt
      Process, Exist, SmallEditor.exe ; check to see if program is running
      If (ErrorLevel > 0) ; If program is not running -> Run
      {
  	 Process, Close, %ErrorLevel%
         Run, SmallEditor.exe diary.txt
      }
   }
}
return

;Ctrl + Alt + A
;^!A::
^M::
Loop
{
   inputbox, text, Diary (Your input will be appended in %A_WorkingDir%\diary.txt),,,750,150
   ; Format the time-stamp
   current=%A_DD%/%A_MM%/%A_YYYY%, %A_Hour%:%A_Min%
   ; Write this data to the diary.txt file
   myVar := text
   
   if ErrorLevel  ;Concel pressed
      break
   else if myVar <> 
   {
      fileappend, %current% - %text%`n, %A_WorkingDir%\diary.txt
      Process, Exist, SmallEditor.exe ; check to see if program is running
      If (ErrorLevel > 0) ; If program is not running -> Run
      {
  	 Process, Close, %ErrorLevel%
         Run, SmallEditor.exe diary.txt
      }
   }
}

return

^E::
IfNotExist, diary.txt
   FileAppend,,diary.txt

;StartClose("SmallEditor.exe diary.txt")
StartClose("SmallEditor.exe")

;Run, SmallEditor diary.txt

return

StartClose(exe)
{
Process, Exist, %exe% ; check to see if program is running
;msgbox %ErrorLevel%
If (ErrorLevel = 0) ; If program is not running -> Run
    Run, %exe% diary.txt
Else ; If program is running, ErrorLevel = process id for the target program -> Close
{
    Process, Close, %ErrorLevel%
    Run, %exe% diary.txt
}
}

;Esc:: ExitApp
