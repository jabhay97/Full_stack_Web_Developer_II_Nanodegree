from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi # For Post
from database_setup import Base, Company, Product
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine('sqlite:///companyproduct.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/company"):
                comps = session.query(Company).all()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                for company in comps:
                    output += company.name
                    output += "</br>"
                    output += "<a href ='#' ><b>Edit</b></a> "
                    output += "</br>"
                    output += "<a href =' #'><b>Delete</b></a>"
                    output += "</br>"
                    output += "</br>"
                output += "</body></html>"
                self.wfile.write(output)
                return
        except IOError:
            self.send_error(404, 'Requested File Not Found: %s' % self.path)


def main():
    try:
        server = HTTPServer(('', 8080), webserverHandler)
        print 'Running successfully. Try opening localhost:8080/company'
        server.serve_forever() # To answer all requests
    except KeyboardInterrupt:
        print 'Ctrl-C Pressed, Server Shutting Down'
        server.socket.close()

if __name__ == '__main__':
    main()
