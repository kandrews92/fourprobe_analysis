Sub ConvertToXlsx
    Dim strPath As String
    Dim strFile As String
    Dim wbk As Workbook
    ' Path must end in trailing backslash
    strPath = "C:\Documents\wayne\research\scripts\analysis\fourprobe\"
    strFile = Dir(strPath & "*.xls")
    Do While strFile <> ""
        If Right(strFile, 3) = "xls" Then
            Set wbk = Workbooks.Open(Filename:=strPath & strFile)
            wbk.SaveAs Filename:=strPath & strFile & "x", _
                FileFormat:=xlOpenXMLWorkbook
            wbk.Close SaveChanges:=False
        End If
        strFile = Dir
    Loop
End Sub

Call :ConvertToXlsx

:EOF