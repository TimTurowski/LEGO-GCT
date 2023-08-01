import os
import datetime
from pikepdf import Pdf

start_time = datetime.datetime.now()

file2pages = {
    0: [0, 110], # 1st splitted PDF file will contain the pages from 0 to 9 (9 is not included)
    1: [110, 130], # 2nd splitted PDF file will contain the pages from 9 (9 is included) to 11
}

filename = "6490652.pdf"

pdf = Pdf.open(filename)

new_pdf_files = [ Pdf.new() for i in file2pages ]

"""Index für die Numerierung der PDF Teile"""
new_pdf_index = 0

for n, page in enumerate(pdf.pages):
    if n in list(range(*file2pages[new_pdf_index])):
        new_pdf_files[new_pdf_index].pages.append(page)
        print(f"[*] Assigning Page {n} to the file {new_pdf_index}")
    else:
        """file name setzen"""
        name, ext = os.path.splitext(filename)
        output_filename = f"{name}-{new_pdf_index}.pdf"
        """speichern"""
        new_pdf_files[new_pdf_index].save(output_filename)
        print(f"[+] File: {output_filename} saved.")

        """nächste datei"""
        new_pdf_index += 1
        # add the `n` page to the `new_pdf_index` file
        new_pdf_files[new_pdf_index].pages.append(page)
        print(f"[*] Assigning Page {n} to the file {new_pdf_index}")

# save the last PDF file
name, ext = os.path.splitext(filename)
output_filename = f"{name}-{new_pdf_index}.pdf"
new_pdf_files[new_pdf_index].save(output_filename)
print(f"[+] File: {output_filename} saved.")
print((datetime.datetime.now() - start_time).total_seconds())