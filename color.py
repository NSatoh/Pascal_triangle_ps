class Color:

    def __init__(self, name, r, g, b):
        """
        :param str name: color name
        :param float r:
        :param float g:
        :param float b:
        """
        self.name = name
        self.r = r
        self.g = g
        self.b = b


RED         = Color(name='red', r=1, g=0, b=0)
BLUE        = Color(name='blue', r=0, g=0, b=1)
GREEN       = Color(name='green', r=0, g=1, b=0)
MAGENTA     = Color(name='magenta', r=1, g=0, b=1)
CYAN        = Color(name='cyan', r=0, g=1, b=1)
YELLOW      = Color(name='yellow', r=1, g=1, b=0)
HOTPINK     = Color(name='hotpink', r=1, g=0.412, b=0.706)
TEAL        = Color(name='teal', r=0, g=0.5, b=0.5)
FORESTGREEN = Color(name='forestgreen', r=0.133, g=0.545, b=0.133)
DARKORCHID  = Color(name='darkorchid', r=0.6, g=0.196, b=0.8)
SKYBLUE     = Color(name='skyblue', r=0.529, g=0.808, b=0.922)
SLATEBLUE   = Color(name='slateblue', r=0, g=0.5, b=1)
DARKORANGE  = Color(name='darkorange', r=1, g=0.549, b=0)
BLACK       = Color(name='black', r=0, g=0, b=0)
GRAY80      = Color(name='gray80', r=0.8, g=0.8, b=0.8)
