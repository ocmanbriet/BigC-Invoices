from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
from .models import Orders, CompanyName
import zipfile
import os
# unique_company_names = Orders.objects.values_list('company_name', flat=True).distinct()

def pdf_process(request):
    # orders = Orders.objects.all()

    # zip_buffer = BytesIO()
    # with zipfile.ZipFile(zip_buffer, 'w') as zipf:


    unique_company_names = Orders.objects.values_list('company_name', flat=True).distinct()
    z = 0
    print(unique_company_names)

    for company_name in unique_company_names:
        # Step 2: Create a folder for each company
        folder_name = f"All_Invoices/{company_name}"
        os.makedirs(folder_name, exist_ok=True)

        # Retrieve orders for the current company
        orders = Orders.objects.filter(company_name=company_name)

        # Step 3: Generate and save invoices in the folder
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w') as zipf:
            for blog in orders:
                z += 1
                template = get_template('invoice.html')
                prods = fix_prod(blog.order_id)

                html_content = template.render({
                    'customer_name':blog.customer_name, 
                    'order_id':blog.order_id, 
                    'prods':prods, 
                    'subtotal_inc_tax':blog.subtotal_inc_tax, 
                    'shipping_cost_ex_tax':blog.shipping_cost_ex_tax,
                    'ship_method': blog.ship_method,
                    'order_date': blog.order_date,
                    'shipping_phone':blog.shipping_phone,
                    'shipping_email':blog.shipping_email,
                    'shipping_tax_id':blog.shipping_tax_id,
                    'shipping_street_1':blog.shipping_street_1,
                    'shipping_street_2':blog.shipping_street_2,
                    'shipping_suburb':blog.shipping_suburb,
                    'shipping_state':blog.shipping_state,
                    'shipping_zip':blog.shipping_zip,
                    'shipping_country':blog.shipping_country,
                    'shipping_first_name':blog.shipping_first_name,
                    'shipping_last_name':blog.shipping_last_name,
                    'shipping_cost_inc_tax':blog.shipping_cost_inc_tax,
                    'subtotal_inc_tax':blog.subtotal_inc_tax,
                    'order_total_inc_tax':blog.order_total_inc_tax,
                    'store_credit_redeemed':blog.store_credit_redeemed,
                    'tax_total':blog.tax_total,
                    'billing_phone':blog.shipping_phone,
                    'billing_email':blog.shipping_email,
                    'billing_tax_id':blog.shipping_tax_id,
                    'billing_street_1':blog.shipping_street_1,
                    'billing_street_2':blog.shipping_street_2,
                    'billing_suburb':blog.shipping_suburb,
                    'billing_state':blog.shipping_state,
                    'billing_zip':blog.shipping_zip,
                    'billing_country':blog.billing_country,
                    'billing_tax_id':blog.billing_tax_id,
                    'billing_payment_method':blog.payment_method,
                    'billing_first_name':blog.billing_first_name,
                    'billing_last_name':blog.billing_last_name,
                    'customer_message':blog.customer_message,
                    'company_name':blog.company_name,
                    })

                buffer = BytesIO()
                pdf = pisa.pisaDocument(BytesIO(html_content.encode('UTF-8')), buffer)
                if not pdf.err:
                    pdf_data = buffer.getvalue()

                    # Save the PDF in the company's folder
                    pdf_file_path = os.path.join(folder_name, f'{blog.order_id}.pdf')
                    with open(pdf_file_path, 'wb') as pdf_file:
                        pdf_file.write(pdf_data)

                    # Add the PDF to the zip file
                    zipf.write(pdf_file_path, os.path.basename(pdf_file_path))
                print("***********************", z , "-", blog.order_id)
        zip_buffer.seek(0)
        # with open(os.path.join(folder_name, 'invoices.zip'), 'wb') as zip_file:
        #     zip_file.write(zip_buffer.read())

    response = HttpResponse(zip_buffer.getvalue(), content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="blog_pdfs.zip'

    return response


import re
def index(request):
    #     # fix_prod()
    # i = 0
    # nulls = []
    # orders = Orders.objects.all()
    # for order in orders:
    #     print(i)
    #     i += 1
    #     try:
    #         comp = CompanyName.objects.filter(order_id = order.order_id)[0]
    #         order.company_name = comp.company_name
    #         order.save()
    #         print("***********************", order.id)
    #     except:
    #         nulls.append(order.id)

    #     print(order.id)





    return render(request, 'index.html')


def fix_prod(id):
    # id = 44947
    json_data = []
    order = Orders.objects.get(order_id=id)

    product_records = re.split(r'(?=Product ID:)', order.product_details)
    for product_record in product_records:
        data = product_record.split(",")
        y = 1
        js = {}
        for i in data:
            if 'Nicotine Level' not in i:
                target = ''
                j = i.split(":")
                x = 0
                for k in j:
                    if x == 1:
                        target = k
                    x += 1
                if y== 1:
                    js['product_id'] = target
                if y== 2:
                    js['product_qty'] = target
                if y== 3:
                    js['product_sku'] = target
                if y== 4:
                    js['product_name'] = target
                if y== 5:
                    js['product_weight'] =target
                if y== 6:
                    js['product_variation'] = target
                if y== 7:
                    js['product_unit_price'] = target
                if y== 8:
                    target = target.replace('|', '')
                    js['product_total_price'] = target

                y += 1
        if js['product_id'] != '':
            json_data.append(js)        
        # print('\n\n')
    # print(json_data)
    return json_data
    








































# from django.http import HttpResponse
# import io
# import zipfile
# from reportlab.pdfgen import canvas
# from .models import *

# def generate_pdf_content(text):
#     buffer = io.BytesIO()
#     p = canvas.Canvas(buffer)
#     p.drawString(100, 100, text)
#     p.showPage()
#     p.save()
#     buffer.seek(0)
#     return buffer.read()

# def index(request):
#     Orders = Orders.objects.all()

#     zip_buffer = io.BytesIO()
#     with zipfile.ZipFile(zip_buffer, 'w') as zipf:
#         for i, blog in enumerate(Orders, 1):
#             pdf_content = generate_pdf_content(blog.name)
#             zipf.writestr(f'blog_{i}.pdf', pdf_content)
#             print("********************************", i)

#     response = HttpResponse(zip_buffer.getvalue(), content_type='application/zip')
#     response['Content-Disposition'] = 'attachment; filename="blog_pdfs.zip"'

#     return response

# # def index(request):
# #     for i in range(100):
# #         Orders.objects.create(name = i, description = "Hiiiiii")
# #     return HttpResponse('Done')

