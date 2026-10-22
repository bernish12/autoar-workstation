try {
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    
    $docPath = "D:\new web record file\Smart_Wireless_Ultrasonic_Thickness_Gauging_Project_Report_Rohini_College.docx"
    $pdfPath = "D:\new web record file\Smart_Wireless_Ultrasonic_Thickness_Gauging_Project_Report_Rohini_College.pdf"
    Write-Host "Opening docx: $docPath"
    $doc = $word.Documents.Open($docPath)
    Write-Host "Exporting to PDF: $pdfPath"
    $doc.SaveAs([ref]$pdfPath, [ref]17)
    $doc.Close()

    $docCopyPath = "C:\final doc\Smart_Wireless_Ultrasonic_Thickness_Gauging_Project_Report_Rohini_College.docx"
    $pdfCopyPath = "C:\final doc\Smart_Wireless_Ultrasonic_Thickness_Gauging_Project_Report_Rohini_College.pdf"
    Write-Host "Opening copy docx: $docCopyPath"
    $doc2 = $word.Documents.Open($docCopyPath)
    Write-Host "Exporting copy PDF: $pdfCopyPath"
    $doc2.SaveAs([ref]$pdfCopyPath, [ref]17)
    $doc2.Close()

    $word.Quit()
    Write-Host "SUCCESS: Both PDFs generated successfully!"
} catch {
    Write-Error $_.Exception.Message
    if ($word) { $word.Quit() }
}
