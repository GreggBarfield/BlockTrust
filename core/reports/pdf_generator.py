import FoxitQPLDLL1811 as FoxitQuick
from .. import config
from ..utilities.aws import aws
class PDFGenerator:
  def __init__(self, db):
        self._db = db

  def get_url(self, file_id, expires_in=3600):
      """Gets a signed URL to a file by the ID.

      Params:
          id: The file's ID
          expires_in: The number of seconds before the link is no longer available
              (default 1 hour (3600))
      """
      return aws.get_s3_client().generate_presigned_url(
          ClientMethod="get_object",
          Params={
              "Bucket": config.AWS_S3_BUCKET,
              "Key": "animal_certificates/" + str(int(file_id))
          },
          ExpiresIn=expires_in,
      )
  def generate_pdf(self):
    qp = FoxitQuick.PDFLibrary(PDFGenerator.get_url("foxitDLL/"))
    licenseKey = "jd4pi7ez76e5z89ad7em5jb7y"
    if qp.UnlockKey(licenseKey) == 1:
      qp.LoadFromFile(PDFGenerator.get_url("Blank_Health_Track_Certificate_no_grid.pdf"), "")
      qp.DrawText(100, 700, "Hello world!!!?")
      qp.SetPageSize("Letter Landscape")
  

      tableID = qp.CreateTable(5, 5)


      qp.SetTableBorderColor(tableID, 0, 0.3, 0.204, 0)
      qp.SetTableBorderWidth(tableID, 0, 0.2)


      qp.SetTableRowHeight(tableID, 1, 5, 0)
      qp.SetTableColumnWidth(tableID, 1, 5, 100)


      qp.SetTableCellBackgroundColor(tableID, 1, 1, 1, 5, 0.3, 0.7, 1.0)
      qp.SetTableCellAlignment(tableID, 1, 1, 1, 5, 4)


      qp.SetTableCellContent(tableID, 1, 1, "<b>This Week</b>")
      qp.SetTableCellContent(tableID, 1, 2, "<b>Last Week</b>")
      qp.SetTableCellContent(tableID, 1, 3, "<b>Artist Name</b>")
      qp.SetTableCellContent(tableID, 1, 4, "<b>Peak</b>")
      qp.SetTableCellContent(tableID, 1, 5, "<b>Weeks On</b>")


      qp.SetTableCellContent(tableID, 2, 1, "1")
      qp.SetTableCellContent(tableID, 2, 2, "1")
      qp.SetTableCellContent(tableID, 2, 3, "<b>The Black Eyed Peas</b><br>Boom Boom Pow")
      qp.SetTableCellContent(tableID, 2, 4, "<b>1</b>")
      qp.SetTableCellContent(tableID, 2, 5, "<b>11</b>")



      qp.SetTableCellContent(tableID, 3, 1, "2")
      qp.SetTableCellContent(tableID, 3, 2, "3")
      qp.SetTableCellContent(tableID, 3, 3, "<b>Missy Higgins</b><br>Life is a rainbow")
      qp.SetTableCellContent(tableID, 3, 4, "<b>2</b>")
      qp.SetTableCellContent(tableID, 3, 5, "<b>8</b>")



      qp.SetTableCellContent(tableID, 4, 1, "3")
      qp.SetTableCellContent(tableID, 4, 2, "2")
      qp.SetTableCellContent(tableID, 4, 3, "<b>Silverchair</b><br>The Door")
      qp.SetTableCellContent(tableID, 4, 4, "<b>3</b>")
      qp.SetTableCellContent(tableID, 4, 5, "<b>7</b>")



      qp.SetTableCellContent(tableID, 5, 1, "4")
      qp.SetTableCellContent(tableID, 5, 2, "4")
      qp.SetTableCellContent(tableID, 5, 3, "<b>Rolling Stones</b><br>Sweet Virginia")
      qp.SetTableCellContent(tableID, 5, 4, "<b>4</b>")
      qp.SetTableCellContent(tableID, 5, 5, "<b>19</b>")



      qp.SetOrigin(1)
      qp.DrawTableRows(tableID, 50, 50, 400, 1, 0)

      qp.SaveToFile("test_output.pdf")