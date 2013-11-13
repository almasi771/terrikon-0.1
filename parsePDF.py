from xhtml2pdf import pisa
from StringIO import StringIO

def main():
	data = list(csv.reader(open("/Users/administrator/Dropbox/backup/Projects/terrikon_04/uploads/terrikon_test_file.csv"), delimiter= ','))
	#'hello'+'world'+'.pdf', "wb"

	'''
	pdf = pisa.CreatePDF(
		"Hello <strong> World </strong>",
		file("/Users/administrator/Dropbox/backup/Projects/terrikon_04/uploads/	"+"new_file.pdf", "wb"))		
	'''
if __name__ == '__main__':
	pisa.showLogging()
	main()