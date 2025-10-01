from pathlib import Path
import argparse
import pymupdf
import sys
import os

def printError(msg):
    print("\033[91merror:\033[0m " + msg)

def deleteDuplicateSlides(args):
    filepaths = [str(path) for path in Path(args.filename).rglob('*.pdf')]

    print(f"Identified {len(filepaths)} PDF{'' if len(filepaths) == 1 else 's'}.\n")

    if len(filepaths) == 0:
        printError("file \033[4m" + args.filename + "\033[0m doesn't exist.")
        return

    for filepath in filepaths:
        outputname = args.outputname

        print(f"Processing \033[4m{os.path.basename(filepath)}\033[0m.\n")

        # removing duplicates
        doc = pymupdf.open(filepath)
        prev_text = ''

        for i in range(len(doc)-1, -1, -1):
            current_text = doc[i].get_text().encode("utf8")

            if current_text == prev_text:
                doc.delete_page(i)
            
            prev_text = current_text

        # saving file
        if args.replace:
            # renaming original so new one can hive its name
            os.rename(filepath, filepath[0:-4] + "-original.pdf")
            outputname = filepath[0:-4] + "-no-duplicates.pdf"
        elif not outputname:
            outputname = filepath[0:-4] + "-no-duplicates.pdf"
        elif not outputname.endswith('.pdf'):
            if len(filepaths) > 1:
                outputname = filepath + outputname + '.pdf'
            else:
                outputname += ".pdf"

        doc.save(outputname)
        
        # deleting original and renaming new one if replace option was chosen
        if args.replace:
            oldname = outputname
            new_name = oldname[0:-18] + '.pdf'
            outputname = new_name

            os.rename(oldname, new_name)
            os.remove(filepath[0:-4] + "-original.pdf")

        print("Saved output to \033[4m" + outputname + "\033[0m.\n")
   
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