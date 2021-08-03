import struct
from obj import Obj
    
def char(c):
    return struct.pack('=c', c.encode('ascii'))
    
def word(w):
    #short
    return struct.pack('=h', w)

def dword(dw):
    #long
    return struct.pack('=l', dw)

def color(r, g, b):
    return bytes([b, g, r])
    
black = color(0, 0, 0)
white = color(255, 255, 255)

class Renderer(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.currentColor = white
        self.clear()
        
    def clear(self):
        self.framebuffer = [
            [black for x in range(self.width)]
            for y in range(self.height)
            ]
        
    def write(self, filename):
        f = open(filename, 'bw')
        
        #File header
        f.write(char('B'))
        f.write(char('M'))
        f.write(dword(14 + 40 + 3*(self.width * self.height)))
        f.write(dword(0))
        f.write(dword(14 + 40))
        
        
        #Info Header
        f.write(dword(40))
        f.write(dword(self.width))
        f.write(dword(self.height))
        f.write(word(1))
        f.write(word(24))
        f.write(dword(0))
        f.write(dword((self.width * self.height) * 3))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        
        #Mapa Bits
        for y in range(self.height):
            for x in range(self.width):
                f.write(self.framebuffer[y][x])
        
        f.close()
        
    def render(self):
        self.write('3DRender.bmp')
        
    def point(self, x, y, color = None):
        self.framebuffer[y][x] = color or self.currentColor

    def line(self, x0, y0, x1, y1):
        dy = abs(y1 - y0)
        dx = abs(x1 - x0)
        
        steep = dy > dx
        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1
        
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
            
        dy = abs(y1 - y0)
        dx = abs(x1 - x0)
        
        offset = 0 * 2 * dx
        threshold = 0.5
        y = y0
        
        # y = mx + b
        points = []
        for x in range(x0, x1 + 1):
            if steep:
                points.append((y, x))
            else:
                points.append((x, y))
                
            offset += dy * 2 
            if offset >= threshold:
                y += 1 if y0 < y1 else -1
                threshold += 1 * 2 * dx
            
        for point in points:        
            r.point(*point)
    
    def load(self, filename, translate, scale):
        model = Obj(filename)
        
        for face in model.faces:
            vcount = len(face)
            for j in range(vcount):
                f1 = face[j][0]
                f2 = face[(j + 1) % vcount][0]
                
                v1 = model.vertices[f1 - 1]
                v2 = model.vertices[f2 - 1]
                
                x1 = round((v1[0] + translate[0]) * scale[0])
                y1 = round((v1[1] + translate[1]) * scale[1])
                x2 = round((v2[0] + translate[0]) * scale[0]) 
                y2 = round((v2[1] + translate[1]) * scale[1])
                
                if y1 < 350 and x1 < 440 and y2 > -180:
                    self.currentColor = color(28, 193, 28)
               # elif y2 - y1 < -3 or x2 - x1 < 3:
                #    self.currentColor = color(28, 193, 28)
                else:
                    self.currentColor = color(252, 144, 36)
                self.line(x1, y1, x2, y2)
                     
r = Renderer(800, 600)
#r.currentColor = color(252, 144, 36)
r.load('./models/pumpkin.obj', [0.8, -0.7], [500, 500])
r.render()