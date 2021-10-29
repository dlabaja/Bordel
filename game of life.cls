VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "ThisWorkbook"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = True
Dim list As New ArrayList

Sub Main()
    With ActiveSheet.UsedRange
        Range("B2:U21").RowHeight = 32
        Range("B2:U21").ColumnWidth = 6
    End With

    Dim rng As Range: Set rng = Application.Range("List1!B2:U21")
    Dim counter
    Set list = CreateObject("System.Collections.ArrayList")
    
    Do While True
    counter = counter + 1
    Range("A22").Value = counter
    For Each cell In rng.Cells
        With cell
            If cell.Interior.ColorIndex = 1 Then
                Call algorithm(Range(cell.Address(RowAbsolute:=False, ColumnAbsolute:=False)).Row, Range(cell.Address(RowAbsolute:=False, ColumnAbsolute:=False)).Column, False)
            Else
                Call algorithm(Range(cell.Address(RowAbsolute:=False, ColumnAbsolute:=False)).Row, Range(cell.Address(RowAbsolute:=False, ColumnAbsolute:=False)).Column, True)
            End If
        End With
    Next cell
    
    Dim i As Long
    For Each cell In rng.Cells
        With cell
            cell.Interior.ColorIndex = 0
        End With
    Next cell
    
    For i = 0 To list.count - 1
        If list.count >= 1 Then
            Range(list(i).Address).Interior.ColorIndex = 1
        End If
    Next i
    list.Clear
    Application.Wait Now + #12:00:03 AM#
    Loop
End Sub

Sub algorithm(ByVal x As Integer, ByVal y As Integer, ByVal isEmpty As Boolean)
    cellCount = 0
    If Cells((x - 1), (y - 1)).Interior.ColorIndex = 1 Then
           cellCount = cellCount + 1
    End If
    If Cells((x - 1), y).Interior.ColorIndex = 1 Then
           cellCount = cellCount + 1
    End If
    If Cells((x - 1), (y + 1)).Interior.ColorIndex = 1 Then
           cellCount = cellCount + 1
    End If
    If Cells(x, (y - 1)).Interior.ColorIndex = 1 Then
           cellCount = cellCount + 1
    End If

    If Cells(x, (y + 1)).Interior.ColorIndex = 1 Then
           cellCount = cellCount + 1
    End If
    If Cells((x + 1), (y - 1)).Interior.ColorIndex = 1 Then
           cellCount = cellCount + 1
    End If
    If Cells((x + 1), y).Interior.ColorIndex = 1 Then
           cellCount = cellCount + 1
    End If
    If Cells((x + 1), (y + 1)).Interior.ColorIndex = 1 Then
           cellCount = cellCount + 1
    End If
    
    If isEmpty = False Then
        If cellCount <= 1 Or cellCount >= 4 Then
            list.Remove Cells(x, y)
        Else
            list.Add Cells(x, y)
        End If
    End If
    If isEmpty = True Then
        If cellCount = 3 Then
            list.Add Cells(x, y)
        Else
            list.Remove Cells(x, y)
        End If
    End If


End Sub






