import http.server
import socketserver
import os
import sys

PORT = 8546

class SPARequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Translate the URL path to a local file system path
        local_path = self.translate_path(self.path)
        
        # If the path does not exist, serve index.html to let client-side JS handle it
        if not os.path.exists(local_path):
            self.path = '/index.html'
            
        return super().do_GET()

if __name__ == '__main__':
    # Determine directory to serve
    # If run from root, serve site-generator/dist
    # If run from site-generator, serve dist
    # If run from dist, serve current directory
    cwd = os.getcwd()
    target_dir = 'dist'
    
    if os.path.basename(cwd) == 'Google Review':
        target_dir = 'site-generator/dist'
    elif os.path.basename(cwd) == 'dist':
        target_dir = '.'
        
    if os.path.exists(target_dir):
        os.chdir(target_dir)
        print(f"Serving folder: {os.path.abspath('.')}")
    else:
        print(f"Warning: Target directory '{target_dir}' not found. Serving current folder.")

    Handler = SPARequestHandler
    # Allow port reuse to avoid address already in use errors on rapid restarts
    socketserver.TCPServer.allow_reuse_address = True
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"SPA Testing Server started on: http://localhost:{PORT}/")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")
