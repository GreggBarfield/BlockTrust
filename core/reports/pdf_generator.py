from . import FoxitQPLDLL1811 as FoxitQuick
from .. import config
from ..utilities.aws import aws

def get_url(file_id, expires_in=3600):
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
            "Key":  + str(int(file_id))
        },
        ExpiresIn=expires_in,
    )
def get_pdf_url(folder_name,file_id,expires_in=3600):
  """Gets a signed URL to a file by the ID.

  Params:
      folder_name: s3 folder's name : background/ or reported_certificates/ 
      file_id: The file's ID

      expires_in: The number of seconds before the link is no longer available
          (default 1 hour (3600))
  """
  key= "animal_certificates/"+str(folder_name)+"/"+str(file_id)+".pdf"
  return aws.get_s3_client().generate_presigned_url(
      ClientMethod="get_object",
      Params={
          "Bucket": config.AWS_S3_BUCKET,
          "Key": key
      },
      ExpiresIn=expires_in,
  )
# def local_generate():
#   medical_data={'type': 'matches_by_eids', 'params': {'eids': [982000418411463], 'ljoin_account_links': True, 'types': ['Medical']}, 'result': {'matches': [{'id': 1791334, 'account': 4, 'account_link': None, 'eid': 982000418411463, 'lat': None, 'lon': None, 'time': 1519365600, 'created': 1604985815, 'type': 20, 'raw_identifier': None, 'data': {'product': 'Cavalry 9', 'location': 'Left & Right Neck'}, 'visibility': True, 'account_links.id': None, 'account_links.account': None, 'account_links.uid_type': None, 'account_links.uid': None, 'account_links.company': None, 'account_links.sector': None}, {'id': 1791335, 'account': 4, 'account_link': None, 'eid': 982000418411463, 'lat': None, 'lon': None, 'time': 1519365600, 'created': 1604985815, 'type': 20, 'raw_identifier': None, 'data': {'product': 'Pyramid 5+Presponse SQ', 'location': 'Left & Right Neck'}, 'visibility': True, 'account_links.id': None, 'account_links.account': None, 'account_links.uid_type': None, 'account_links.uid': None, 'account_links.company': None, 'account_links.sector': None}, {'id': 1791336, 'account': 4, 'account_link': None, 'eid': 982000418411463, 'lat': None, 'lon': None, 'time': 1519365600, 'created': 1604985815, 'type': 20, 'raw_identifier': None, 'data': {'product': 'Safe-Guard Suspension', 'location': 'Mouth'}, 'visibility': True, 'account_links.id': None, 'account_links.account': None, 'account_links.uid_type': None, 'account_links.uid': None, 'account_links.company': None, 'account_links.sector': None}, {'id': 1791337, 'account': 4, 'account_link': None, 'eid': 982000418411463, 'lat': None, 'lon': None, 'time': 1519365600, 'created': 1604985815, 'type': 20, 'raw_identifier': None, 'data': {'product': 'Cylence', 'location': 'Back'}, 'visibility': True, 'account_links.id': None, 'account_links.account': None, 'account_links.uid_type': None, 'account_links.uid': None, 'account_links.company': None, 'account_links.sector': None}, {'id': 1791338, 'account': 4, 'account_link': None, 'eid': 982000418411463, 'lat': None, 'lon': None, 'time': 1519365600, 'created': 1604985815, 'type': 20, 'raw_identifier': None, 'data': {'product': 'Component E-C', 'location': 'Right Ear'}, 'visibility': True, 'account_links.id': None, 'account_links.account': None, 'account_links.uid_type': None, 'account_links.uid': None, 'account_links.company': None, 'account_links.sector': None}, {'id': 1791339, 'account': 4, 'account_link': None, 'eid': 982000418411463, 'lat': None, 'lon': None, 'time': 1519365600, 'created': 1604985815, 'type': 20, 'raw_identifier': None, 'data': {'product': 'Knife'}, 'visibility': True, 'account_links.id': None, 'account_links.account': None, 'account_links.uid_type': None, 'account_links.uid': None, 'account_links.company': None, 'account_links.sector': None}, {'id': 1791340, 'account': 4, 'account_link': None, 'eid': 982000418411463, 'lat': None, 'lon': None, 'time': 1521090000, 'created': 1604985815, 'type': 20, 'raw_identifier': None, 'data': {'product': 'Cavalry 9', 'location': 'Left & Right Neck'}, 'visibility': True, 'account_links.id': None, 'account_links.account': None, 'account_links.uid_type': None, 'account_links.uid': None, 'account_links.company': None, 'account_links.sector': None}, {'id': 1791341, 'account': 4, 'account_link': None, 'eid': 982000418411463, 'lat': None, 'lon': None, 'time': 1521090000, 'created': 1604985815, 'type': 20, 'raw_identifier': None, 'data': {'product': 'Pyramid 5+Presponse SQ', 'location': 'Left & Right Neck'}, 'visibility': True, 'account_links.id': None, 'account_links.account': None, 'account_links.uid_type': None, 'account_links.uid': None, 'account_links.company': None, 'account_links.sector': None}], 'blocked_matches': []}}
#   qp =FoxitQuick.PDFLibrary("C:\Program Files (x86)\Foxit Software\Quick PDF Library 18\DLL")
#   licenseKey = "jd4pi7ez76e5z89ad7em5jb7y"
#   if qp.UnlockKey(licenseKey) == 1:
#     qp.LoadFromFile("Blank_Health_Track_Certificate_no_grid.pdf","")
#     # qp.SetTextSize(5)
#     qp.SetPageSize("Letter Landscape")
#     # print(medical_data['result'],type(medical_data['result']))
#     row_c = len(medical_data['result']['matches'])
#     print("ROW_C",row_c)
  
#     medical_table=qp.CreateTable(row_c,4)
#     qp.SetTableBorderColor(medical_table, 0, 0.34, 0.204, 0)
#     qp.SetTableBorderWidth(medical_table, 0, 0.2)
#     qp.SetTableRowHeight(medical_table,1, row_c,16)
#     qp.SetTableColumnWidth(medical_table, 1, 4, 160)
#     qp.SetTableCellBackgroundColor(medical_table, 1, 1, 1, 4, 0.847, 0.176, 0.223)
#     qp.SetTableCellAlignment(medical_table, 1, 1, 1, 4, 0)
    
#     qp.SetTableCellContent(medical_table, 1, 1, "<b>Date</b>")
#     qp.SetTableCellContent(medical_table, 1, 2, "<b>Product Name</b>")
#     qp.SetTableCellContent(medical_table, 1, 3, "<b>Location</b>")
#     qp.SetTableCellContent(medical_table, 1, 4, "<b>Admin Route</b>")
#     row_counter=2
    
#     for match_row in medical_data['result']['matches']:
#       print(match_row['data'].keys())
#       data_obj = match_row['data']
#       key=match_row['data'].keys()
#       if 'product' in key:
#         product= str(data_obj['product'])
#       else:
#         product="NA"
#       if 'location' in key:
#         location= str(data_obj['location'])
#       else:
#         location="NA"
#       # create_row(qp,medical_table,row_counter,match_row['time'],data_obj['product'],data_obj['location'],'')
#       qp.SetTableCellContent(medical_table, row_counter, 1, str(match_row['time']))
#       qp.SetTableCellContent(medical_table, row_counter, 2,product)
#       qp.SetTableCellContent(medical_table, row_counter, 3, location)
#       qp.SetTableCellContent(medical_table, row_counter, 4,'')
#       row_counter+=1
#     qp.DrawTableRows(medical_table, 47, 463, 400, 1, 0)
#     qp.SaveToFile("test.pdf")

# local_generate()

def generate_pdf(medical_data,eid):
  print("In generater--------------------",medical_data)
  qp = FoxitQuick.PDFLibrary("C:\Program Files (x86)\Foxit Software\Quick PDF Library 18\DLL")
  licenseKey = "jd4pi7ez76e5z89ad7em5jb7y"
  print("qp-----")
  if qp.UnlockKey(licenseKey) == 1:
    qp.LoadFromFile("Blank_Health_Track_Certificate_no_grid.pdf","")
    # qp.SetTextSize(5)
    qp.SetPageSize("Letter Landscape")
    # print(medical_data['result'],type(medical_data['result']))
    row_c = len(medical_data['result']['matches'])
    print("ROW_C",row_c)
  
    medical_table=qp.CreateTable(row_c,4)
    qp.SetTableBorderColor(medical_table, 0, 0.34, 0.204, 0)
    qp.SetTableBorderWidth(medical_table, 0, 0.2)
    qp.SetTableRowHeight(medical_table,1, row_c,16)
    qp.SetTableColumnWidth(medical_table, 1, 4, 160)
    qp.SetTableCellBackgroundColor(medical_table, 1, 1, 1, 4, 0.847, 0.176, 0.223)
    qp.SetTableCellAlignment(medical_table, 1, 1, 1, 4, 0)
    
    qp.SetTableCellContent(medical_table, 1, 1, "<b>Date</b>")
    qp.SetTableCellContent(medical_table, 1, 2, "<b>Product Name</b>")
    qp.SetTableCellContent(medical_table, 1, 3, "<b>Location</b>")
    qp.SetTableCellContent(medical_table, 1, 4, "<b>Admin Route</b>")
    row_counter=2
    
    for match_row in medical_data['result']['matches']:
      print(match_row['data'].keys())
      data_obj = match_row['data']
      key=match_row['data'].keys()
      if 'product' in key:
        product= str(data_obj['product'])
      else:
        product="NA"
      if 'location' in key:
        location= str(data_obj['location'])
      else:
        location="NA"
      # create_row(qp,medical_table,row_counter,match_row['time'],data_obj['product'],data_obj['location'],'')
      qp.SetTableCellContent(medical_table, row_counter, 1, str(match_row['time']))
      qp.SetTableCellContent(medical_table, row_counter, 2,product)
      qp.SetTableCellContent(medical_table, row_counter, 3, location)
      qp.SetTableCellContent(medical_table, row_counter, 4,'')
      row_counter+=1
    qp.DrawTableRows(medical_table, 47, 463, 400, 1, 0)
    qp.SaveToFile(get_pdf_url("reported_certificates/",str(eid)))
    print("success!!!!")

#   print(str(medical_data))
  # licenseKey = "jd4pi7ez76e5z89ad7em5jb7y"
  # if qp.UnlockKey(licenseKey) == 1:
  #   qp.LoadFromFile(get_url("animal_certificates/Blank_Health_Track_Certificate_no_grid.pdf"), "")
  #   qp.DrawText(100, 700, "Hello world!!!?")
  #   qp.SetPageSize("Letter Landscape")


  #   tableID = qp.CreateTable(5, 5)


  #   qp.SetTableBorderColor(tableID, 0, 0.3, 0.204, 0)
  #   qp.SetTableBorderWidth(tableID, 0, 0.2)


  #   qp.SetTableRowHeight(tableID, 1, 5, 0)
  #   qp.SetTableColumnWidth(tableID, 1, 5, 100)


  #   qp.SetTableCellBackgroundColor(tableID, 1, 1, 1, 5, 0.3, 0.7, 1.0)
  #   qp.SetTableCellAlignment(tableID, 1, 1, 1, 5, 4)


  #   qp.SetTableCellContent(tableID, 1, 1, "<b>This Week</b>")
  #   qp.SetTableCellContent(tableID, 1, 2, "<b>Last Week</b>")
  #   qp.SetTableCellContent(tableID, 1, 3, "<b>Artist Name</b>")
  #   qp.SetTableCellContent(tableID, 1, 4, "<b>Peak</b>")
  #   qp.SetTableCellContent(tableID, 1, 5, "<b>Weeks On</b>")


  #   qp.SetTableCellContent(tableID, 2, 1, "1")
  #   qp.SetTableCellContent(tableID, 2, 2, "1")
  #   qp.SetTableCellContent(tableID, 2, 3, "<b>The Black Eyed Peas</b><br>Boom Boom Pow")
  #   qp.SetTableCellContent(tableID, 2, 4, "<b>1</b>")
  #   qp.SetTableCellContent(tableID, 2, 5, "<b>11</b>")



  #   qp.SetTableCellContent(tableID, 3, 1, "2")
  #   qp.SetTableCellContent(tableID, 3, 2, "3")
  #   qp.SetTableCellContent(tableID, 3, 3, "<b>Missy Higgins</b><br>Life is a rainbow")
  #   qp.SetTableCellContent(tableID, 3, 4, "<b>2</b>")
  #   qp.SetTableCellContent(tableID, 3, 5, "<b>8</b>")



  #   qp.SetTableCellContent(tableID, 4, 1, "3")
  #   qp.SetTableCellContent(tableID, 4, 2, "2")
  #   qp.SetTableCellContent(tableID, 4, 3, "<b>Silverchair</b><br>The Door")
  #   qp.SetTableCellContent(tableID, 4, 4, "<b>3</b>")
  #   qp.SetTableCellContent(tableID, 4, 5, "<b>7</b>")



  #   qp.SetTableCellContent(tableID, 5, 1, "4")
  #   qp.SetTableCellContent(tableID, 5, 2, "4")
  #   qp.SetTableCellContent(tableID, 5, 3, "<b>Rolling Stones</b><br>Sweet Virginia")
  #   qp.SetTableCellContent(tableID, 5, 4, "<b>4</b>")
  #   qp.SetTableCellContent(tableID, 5, 5, "<b>19</b>")



  #   qp.SetOrigin(1)
  #   qp.DrawTableRows(tableID, 50, 50, 400, 1, 0)

  #   qp.SaveToFile("test_output.pdf")