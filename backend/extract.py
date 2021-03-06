import logging
import os.path
import zipfile
from os import rename
import shutil
from adobe.pdfservices.operation.auth.credentials import Credentials
from adobe.pdfservices.operation.exception.exceptions import ServiceApiException, ServiceUsageException, SdkException
from adobe.pdfservices.operation.pdfops.options.extractpdf.extract_pdf_options import ExtractPDFOptions
from adobe.pdfservices.operation.pdfops.options.extractpdf.extract_element_type import ExtractElementType
from adobe.pdfservices.operation.execution_context import ExecutionContext
from adobe.pdfservices.operation.io.file_ref import FileRef
from adobe.pdfservices.operation.pdfops.extract_pdf_operation import ExtractPDFOperation

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
def save(sf,df):
    abs_path=os.path.abspath(df)
    dir=os.path.dirname(abs_path)
    if not os.path.exists(dir):
        os.mkdir(dir)
    if not os.path.exists(abs_path):
        shutil.move(sf,abs_path)
        return
def extract(NAME):
    try:
        # get base path.
        base_path = ""
        # print(base_path)
        # print("Here")

        # Initial setup, create credentials instance.
        credentials = Credentials.service_account_credentials_builder() \
            .from_file(base_path + "pdfservices-api-credentials.json") \
            .build()

        # Create an ExecutionContext using credentials and create a new operation instance.
        execution_context = ExecutionContext.create(credentials)
        extract_pdf_operation = ExtractPDFOperation.create_new()

        # Set operation input from a source file.
        source = FileRef.create_from_local_file(base_path + f"{NAME}.pdf")
        extract_pdf_operation.set_input(source)

        # Build ExtractPDF options and set them into the operation
        extract_pdf_options: ExtractPDFOptions = ExtractPDFOptions.builder() \
            .with_element_to_extract(ExtractElementType.TEXT) \
            .build()
        extract_pdf_operation.set_options(extract_pdf_options)

        # Execute the operation.
        result: FileRef = extract_pdf_operation.execute(execution_context)

        # Save the result to the specified location.
        #result.save_as(base_path + f"{NAME}.zip")
        save(result._file_path,base_path + f"{NAME}.zip")
        # Extract zip
        with zipfile.ZipFile(f"{base_path}{NAME}.zip", 'r') as zip_ref:
            zip_ref.extractall(f"{base_path}")
        zip_ref.close()
        # Rename json
        src = f"{base_path}structuredData.json"
        os.rename(src, f"{base_path}{NAME}.json")
    except (ServiceApiException, ServiceUsageException, SdkException):
        logging.exception("Exception encountered while executing operation")
