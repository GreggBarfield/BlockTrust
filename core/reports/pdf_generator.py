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
