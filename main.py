import pymupdf
import sys
import os

def printError(msg):
    print("\033[91merror:\033[0m " + msg)

def deleteDuplicateSlides(input_path, output_path = None):
    if not os.path.exists(input_path):
        printError("file \033[4m" + input_path + "\033[0m doesn't exist.")
        return

    # removing duplicates
    doc = pymupdf.open(input_path)
    prev_text = ''

    for i in range(len(doc)-1, -1, -1):
        current_text = doc[i].get_text().encode("utf8")

        if current_text == prev_text:
            doc.delete_page(i)
        
        prev_text = current_text

    # saving file
    if not output_path:
        output_path = input_path[0:-4] + "-no-duplicates.pdf"
    elif not output_path.endswith('.pdf'):
        output_path += ".pdf"

    doc.save(output_path)
    print("Saved output to \033[4m" + output_path + "\033[0m.")
   
if __name__ == "__main__":
    arguments = sys.argv
    if len(arguments) == 1:
        printError("no file name provided.")
    elif len(arguments) == 2:
        deleteDuplicateSlides(arguments[1])
    elif len(arguments) == 3:
        deleteDuplicateSlides(arguments[1], arguments[2])
    else:
        printError("too many arguments.")