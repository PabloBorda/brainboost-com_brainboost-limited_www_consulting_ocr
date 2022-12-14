import os
import cherrypy


config = {
    'global' : {
        'server.socket_host' : '127.0.0.1',
        'server.socket_port' : 8080
    }
}




class FileReceiver():
    
    
    @cherrypy.expose
    def test_form(self):
        return '''
            <form method="post" action="http://127.0.0.1:8080/receive_file" enctype="multipart/form-data">
                <label>Digitzs Receipt Upload</label>
                <input type="text" name="reference" />
                <input type="file" name="ufile" />
                <input type="submit" />
            </form>
        '''
        
    
    
    @cherrypy.expose 
    def receive_file(self,reference,ufile=None):

        upload_path = os.path.dirname('receipts/')

        upload_filename = reference+'_'+ufile.filename

        upload_file = os.path.normpath(
            os.path.join(upload_path, upload_filename))
        size = 0
        with open(upload_file, 'wb') as out:
            while True:
                data = ufile.file.read(8192)
                if not data:
                    break
                out.write(data)
                size += len(data)
        out = '''
File received.
Filename: {}

''' .format(ufile.filename)
        return out




if __name__ == '__main__':
    cherrypy.quickstart(FileReceiver(), '/', config)
