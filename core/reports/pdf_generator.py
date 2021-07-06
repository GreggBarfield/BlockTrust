import FoxitQPLDLL1811 as FoxitQuick

qp = FoxitQuick.PDFLibrary("C:\Program Files (x86)\Foxit Software\Quick PDF Library 18\DLL")
licenseKey = "jd4pi7ez76e5z89ad7em5jb7y"
if qp.UnlockKey(licenseKey) == 1:
  qp.DrawText(100, 700, "Hello world!!!")
  qp.SaveToFile("test_output.pdf")