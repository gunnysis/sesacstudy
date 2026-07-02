"""
This code sample shows Prebuilt Invoice operations with the Azure AI Document Intelligence client library. 
The async versions of the samples require Python 3.8 or later.

To learn more, please visit the documentation - Quickstart: Document Intelligence (formerly Form Recognizer) SDKs
https://learn.microsoft.com/azure/ai-services/document-intelligence/quickstarts/get-started-sdks-rest-api?pivots=programming-language-python
"""

from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest
import os
from dotenv import load_dotenv
import csv

"""
Remember to remove the key from your code when you're done, and never post it publicly. For production, use
secure methods to store and access your credentials. For more information, see 
https://docs.microsoft.com/en-us/azure/cognitive-services/cognitive-services-security?tabs=command-line%2Ccsharp#environment-variables-and-application-configuration
"""
load_dotenv()
endpoint = os.getenv("END_POINT")
key = os.getenv("API_KEY")

# Set up directories
uploads_dir = os.path.join("0702", "uploads")
os.makedirs(uploads_dir, exist_ok=True)

csv_dir = os.path.join("0702", "docs")
os.makedirs(csv_dir, exist_ok=True)
csv_file_path = os.path.join(csv_dir, "receipts_output.csv")

document_intelligence_client = DocumentIntelligenceClient(
    endpoint=endpoint, credential=AzureKeyCredential(key)
)

supported_extensions = ('.jpg', '.jpeg', '.png', '.pdf', '.tiff', '.bmp')
files_to_process = [f for f in os.listdir(uploads_dir) if f.lower().endswith(supported_extensions)]

if not files_to_process:
    print(f"업로드된 파일이 없습니다. '{uploads_dir}' 폴더에 분석할 영수증 이미지/PDF 파일을 넣어주세요.")
else:
    print(f"총 {len(files_to_process)}개의 파일을 분석합니다...")
    
    with open(csv_file_path, mode="w", newline="", encoding="utf-8-sig") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([
            "파일명", "영수증 번호", "공급자명", "공급자 주소", "공급자 수신인",
            "고객명", "고객 ID", "고객 주소", "고객 수신인",
            "청구서 번호", "청구일자", "총 청구금액", "결제 기한", "구매 주문서",
            "청구 주소", "청구 수신인", "배송 주소", "배송 수신인",
            "소계", "총 세금", "이전 미납 잔액", "청구 금액(Amount Due)",
            "서비스 시작일", "서비스 종료일", "서비스 주소", "서비스 수신인",
            "송금 주소", "송금 수신인",
            "품목 설명", "수량", "단위", "단가",
            "품목 코드", "품목 일자", "품목 세금", "품목 금액"
        ])
        
        for filename in files_to_process:
            file_path = os.path.join(uploads_dir, filename)
            print(f"분석 중: {filename}")
            
            with open(file_path, "rb") as f:
                poller = document_intelligence_client.begin_analyze_document(
                    "prebuilt-invoice", body=f
                )
            invoices = poller.result()
            
            for idx, invoice in enumerate(invoices.documents):
                row_base = [filename, idx + 1]
                
                def get_val(field_name, attr):
                    field = invoice.fields.get(field_name)
                    if field:
                        val = getattr(field, attr, None)
                        if val is not None:
                            if attr == 'value_currency':
                                return val.amount
                            return str(val)
                    return ""
                    
                row_base.extend([
                    get_val("VendorName", "value_string"),
                    get_val("VendorAddress", "value_address"),
                    get_val("VendorAddressRecipient", "value_string"),
                    get_val("CustomerName", "value_string"),
                    get_val("CustomerId", "value_string"),
                    get_val("CustomerAddress", "value_address"),
                    get_val("CustomerAddressRecipient", "value_string"),
                    get_val("InvoiceId", "value_string"),
                    get_val("InvoiceDate", "value_date"),
                    get_val("InvoiceTotal", "value_currency"),
                    get_val("DueDate", "value_date"),
                    get_val("PurchaseOrder", "value_string"),
                    get_val("BillingAddress", "value_address"),
                    get_val("BillingAddressRecipient", "value_string"),
                    get_val("ShippingAddress", "value_address"),
                    get_val("ShippingAddressRecipient", "value_string"),
                    get_val("SubTotal", "value_currency"),
                    get_val("TotalTax", "value_currency"),
                    get_val("PreviousUnpaidBalance", "value_currency"),
                    get_val("AmountDue", "value_currency"),
                    get_val("ServiceStartDate", "value_date"),
                    get_val("ServiceEndDate", "value_date"),
                    get_val("ServiceAddress", "value_address"),
                    get_val("ServiceAddressRecipient", "value_string"),
                    get_val("RemittanceAddress", "value_address"),
                    get_val("RemittanceAddressRecipient", "value_string")
                ])
                
                items = invoice.fields.get("Items")
                if items and items.value_array:
                    for item in items.value_array:
                        def get_item_val(item_field_name, attr):
                            field = item.value_object.get(item_field_name)
                            if field:
                                val = getattr(field, attr, None)
                                if val is not None:
                                    if attr == 'value_currency':
                                        return val.amount
                                    return str(val)
                            return ""
                        
                        row_item = [
                            get_item_val("Description", "value_string"),
                            get_item_val("Quantity", "value_number"),
                            get_item_val("Unit", "value_number"),
                            get_item_val("UnitPrice", "value_currency"),
                            get_item_val("ProductCode", "value_string"),
                            get_item_val("Date", "value_date"),
                            get_item_val("Tax", "value_string"),
                            get_item_val("Amount", "value_currency")
                        ]
                        writer.writerow(row_base + row_item)
                else:
                    writer.writerow(row_base + [""] * 8)
                    
    print(f"분석 완료! 결과가 {csv_file_path}에 저장되었습니다.")
