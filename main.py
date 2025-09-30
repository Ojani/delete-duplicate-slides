from pathlib import Path
import argparse
import pymupdf
import sys
import os

def printError(msg):
    print("\033[91merror:\033[0m " + msg)

def deleteDuplicateSlides(args):
    if not os.path.exists(args.filename):
        printError("file \033[4m" + args.filename + "\033[0m doesn't exist.")
        return

    # removing duplicates
    doc = pymupdf.open(args.filename)
    prev_text = ''

    for i in range(len(doc)-1, -1, -1):
        current_text = doc[i].get_text().encode("utf8")

        if current_text == prev_text:
            doc.delete_page(i)
        
        prev_text = current_text

    # saving file
    if args.replace:
        # renaming original so new one can hive its name
        os.rename(args.filename, args.filename[0:-4] + "-original.pdf")
        args.outputname = args.filename[0:-4] + "-no-duplicates.pdf"
    elif not args.outputname:
        args.outputname = args.filename[0:-4] + "-no-duplicates.pdf"
    elif not args.outputname.endswith('.pdf'):
        args.outputname += ".pdf"

    doc.save(args.outputname)
    
    # deleting original and renaming new one if replace option was chosen
    if args.replace:
        oldname = args.outputname
        new_name = oldname[0:-18] + '.pdf'
        args.outputname = new_name

        os.rename(oldname, new_name)
        os.remove(args.filename[0:-4] + "-original.pdf")

    print("Saved output to \033[4m" + args.outputname + "\033[0m.")
   
if __name__ == "__main__":
    argparser = argparse.ArgumentParser(
                    prog='dds (Delete Duplicate Slides)',
                    description='deletes pdfs with duplicate text content, leaving the most recent page by default.')
    
    argparser.add_argument('filename')
    argparser.add_argument('-o', '--outputname')
    # When can be used no output name is provided so that instead of appending
    # "-no-duplicates" to the output, it replaces the original file
    argparser.add_argument('-r', '--replace', action='store_true')
    args = argparser.parse_args()

    args.filename = str(Path(args.filename).resolve())

    deleteDuplicateSlides(args)