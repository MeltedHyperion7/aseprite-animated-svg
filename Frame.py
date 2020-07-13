import xml.dom.minidom as md

from n_dim_matrix import n_dim_matrix

class Frame:
    def __init__(self, file_name: str):
        self.document = md.parse(file_name)
        
        document_width = int(self.document.firstChild.getAttribute('width'))
        document_height = int(self.document.firstChild.getAttribute('height'))
        
        pixels = self.document.getElementsByTagName('rect')

        self.scale = int(pixels[0].getAttribute('width'))
        self.width = document_width // self.scale
        self.height = document_height // self.scale

        self.grid = n_dim_matrix((self.height, self.width), fill=None)

        for pixel in pixels:
            x = int(pixel.getAttribute('x'))
            y = int(pixel.getAttribute('y'))

            row = y // self.scale
            col = x // self.scale

            self.grid[row][col] = pixel