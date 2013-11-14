from xhtml2pdf import pisa     
# Define your data
sourceHtml = "<html><body><p>To PDF or not to PDF<p></body></html>"
outputFilename = "test_xhtml2pdf.pdf"

# Utility function
def convertHtmlToPdf(sourceHtml, outputFilename):
    # open output file for writing (truncated binary)
    resultFile = open(outputFilename, "w+b")

    # convert HTML to PDF
    pisaStatus = pisa.CreatePDF(
            sourceHtml,                # the HTML to convert
            dest=resultFile)           # file handle to recieve result

    # close output file
    resultFile.close()                 # close output file

    # return True on success and False on errors
    return pisaStatus.err

# Main program
if __name__=="__main__":
    pisa.showLogging()
    convertHtmlToPdf(sourceHtml, outputFilename)