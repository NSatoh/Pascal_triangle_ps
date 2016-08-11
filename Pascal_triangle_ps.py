import os
from time import clock

def gen_nCr(n, debug=False):
    '''
    @param int:  n
    @param bool: debug

    Generate binary coefficient nCr,
    @return list: [[C(0,0)], [C(1,0), C(0,1)], ..., [C(n,0), C(n,1), ..., C(n,n)]]
    (nCr = output, then nCr[n][r] is C(n,r) )
    '''
    t1 = clock()
    nCr = [[1]]
    for i in range(1,n+1):
        iCr = [1]
        for r in range(1,i):
            iCr += [nCr[i-1][r-1] + nCr[i-1][r]]
        iCr += [1]
        nCr += [iCr]
    t2 = clock()
    if debug:
        print('time @gen_nCr({n}): {t}'.format(n=n,t=t2-t1))
    return nCr

def gen_nCr_mod(n, modulo, debug=False):
    '''
    @param int:  n
    @param int:  modulo
    @param bool: debug

    Generate binary coefficient nCr,
    @return list: [[C(0,0)], [C(1,0), C(0,1)], ..., [C(n,0), C(n,1), ..., C(n,n)]]
    (nCr = output, then nCr[n][r] is C(n,r) )
    '''
    t1 = clock()
    nCr = [[1]]
    for i in range(1,n+1):
        iCr = [1]
        for r in range(1,i):
            iCr += [(nCr[i-1][r-1] + nCr[i-1][r]) % modulo]
        iCr += [1]
        nCr += [iCr]
    t2 = clock()
    if debug:
        print('time @gen_nCr_mod({n},{mod}): {t}'.format(n=n,mod=modulo,t=t2-t1))
    return nCr


#-- color settings for PS -------------------------------------
COLOR_format = '/{name} {{{r} {g} {b} setrgbcolor }} def'
class PsColor:

    def __init__(self, name, r, g, b):
        self.name = name
        self.r = r
        self.g = g
        self.b = b

    def PS_form(self):
        return COLOR_format.format(name=self.name,
                                   r=self.r,
                                   g=self.g,
                                   b=self.b)

RED     = PsColor(name='red',    r=1, g=0, b=0)
BLUE    = PsColor(name='blue',   r=0, g=0, b=1)
GREEN   = PsColor(name='green',  r=0, g=1, b=0)
MAGENTA = PsColor(name='magenta',r=1, g=0, b=1)
CYAN    = PsColor(name='cyan',   r=0, g=1, b=1)
YELLOW  = PsColor(name='yellow', r=1, g=1, b=0)
HOTPINK = PsColor(name='hotpink',r=1, g=0.412, b=0.706)
TEAL    = PsColor(name='teal',   r=0, g=0.5, b=0.5)
FORESTGREEN = PsColor(name='forestgreen', r=0.133, g=0.545, b=0.133)
DARKORCHID = PsColor(name='darkorchid', r=0.6, g=0.196, b=0.8)
SKYBLUE = PsColor(name='skyblue', r=0.529, g=0.808, b=0.922)
SLATEBLUE = PsColor(name='slateblue', r=0, g=0.5, b=1)
DARKORANGE = PsColor(name='darkorange', r=1, g=0.549, b=0)
BLACK   = PsColor(name='black',  r=0, g=0, b=0)
#GRAY   = PsColor(name='gray33',  r=0.33, g=0.33, b=0.33)
GRAY   = PsColor(name='gray80',  r=0.8, g=0.8, b=0.8)

#COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN,
#          HOTPINK, TEAL, FORESTGREEN, DARKORCHID, SKYBLUE,
#          BLACK]

COLORS = [RED, GREEN, YELLOW, SLATEBLUE, GREEN, MAGENTA, CYAN,
          HOTPINK, TEAL, FORESTGREEN, DARKORCHID, SKYBLUE,
          BLACK]


# tmp
COLORING_FLAGS = [False] + [True]*12

def Pascal_triangle_coloring(row, modulo,
                             shape='rectangle',
                             scale=0.7, yscale=3**0.5, line_width=0.1,
                             color_list=COLORS,
                             coloring_flags=COLORING_FLAGS,
                             print_background_triangle=False,
                             print_no_color=True,
                             print_sample=True, sample_scale=10):
    '''
    @param int: row --> the number of rows of the triangle
    @param int: modulo --> modulo for coloring
    @param str: shape --> 'rectangle' or 'circle'
    @param float: scale, yscale
    @param float: line_width
    @param list: color_list --> list of PsColors class objects
    @param list: coloring_flags --> list of booleans
    @param bool: print_background_triangle --> if True, fill the background
                                               by color #0, and set variable
                                               print_no_color = False
                                               Automatically
    @param bool: print_no_color --> if False, don't output no-color cell
    @param bool: print_sample --> if True, output the color samples
    @param int: sample_scale --> length of edge of the color sample rectangles

    Generate PS src
    '''
    # postscript の仕様では, 1pt = 1/72 インチ
    # A4 だと, 0 < x < 595pt, 0 < y < 842pt くらい
    # そしてよくわからないが，座標では 左下(0,0) -- (501,709)右上 くらい
    PS_head =  r'%!PS-Adobe-3.0' + '\n'
    PS_head += r'/mm { 2.834646 mul } def  % inch -> mm' + '\n'
    PS_head += r'newpath' + '\n'

    PS_head += r'/gray {0.5 setgray } def' + '\n'

    for color in color_list:
        PS_head += color.PS_form() + '\n'

    rcomment = '%'
    ccomment = '%'

    if shape == 'rectangle':
        rcomment = ''
    elif shape == 'circle':
        ccomment = ''

    PS_head += '/colorbox {\n'
    PS_head += '  %%-- rectangle --\n'
    PS_head += '  {rcomment}moveto\n'.format(rcomment=rcomment)
    PS_head += '  {rcomment}0 {s} rlineto\n'.format(s=scale*yscale, rcomment=rcomment) 
    PS_head += '  {rcomment}{ss} 0 rlineto\n'.format(ss=2*scale, rcomment=rcomment) 
    PS_head += '  {rcomment}0 -{s} rlineto\n'.format(s=scale*yscale, rcomment=rcomment) 
    PS_head += '  {rcomment}fill\n'.format(rcomment=rcomment)
    PS_head += '  %%-- circle --\n'
    PS_head += '  {ccomment}{s} 0 360 arc\n'.format(s=scale, ccomment=ccomment)
    PS_head += '  {ccomment}fill\n'.format(ccomment=ccomment)
    PS_head += '} def\n'

    PS_head += '/colorsample {\n'
    PS_head += '  0 {s} rlineto\n'.format(s=sample_scale//2) 
    PS_head += '  {ss} 0 rlineto\n'.format(ss=2*sample_scale) 
    PS_head += '  0 -{s} rlineto\n'.format(s=sample_scale//2)
    PS_head += '  fill\n'
    PS_head += '} def\n'

    PS_head += '/nocolorbox {\n'
    PS_head += '  %%-- rectangle --\n'
    PS_head += '  {rcomment}moveto\n'.format(rcomment=rcomment)
    PS_head += '  {rcomment}0 {s} rlineto\n'.format(s=scale*yscale, rcomment=rcomment) 
    PS_head += '  {rcomment}{ss} 0 rlineto\n'.format(ss=2*scale, rcomment=rcomment) 
    PS_head += '  {rcomment}0 -{s} rlineto\n'.format(s=scale*yscale, rcomment=rcomment) 
    PS_head += '  {rcomment}stroke\n'.format(rcomment=rcomment)
    PS_head += '  %%-- circle --\n'
    PS_head += '  {ccomment}{s} 0 360 arc\n'.format(s=scale, ccomment=ccomment)
    PS_head += '  {ccomment}stroke\n'.format(ccomment=ccomment)
    PS_head += '} def\n'


    PS  = 'newpath\n'
    PS += '{lw} setlinewidth\n'.format(lw=line_width) 
    # PS += '1 {yscale} scale\n'.format(yscale=yscale) # 線幅も影響を受けるのでよくない
    PS += '% 原点を, 大体紙の中央一番上へ移動\n'
    PS += '250 700 translate\n'# 

    PS += '%****************** Pascal triangle -- {row} -- [color fill] ******************%\n'.format(row=row)
    PS += '% mod {modulo}\n'.format(modulo=modulo)

    color_num = 0
    color_dict = {}# 直したい

    if print_background_triangle:
        color = color_list[color_num]
        PS += '% back-ground --> {color}\n'.format(color=color.name)
        color_dict['back-ground'] = color.name
        color_num += 1

    for r in range(modulo):
        if coloring_flags[r]:
            color = color_list[color_num]
            PS += '% {r} --> {color}\n'.format(r=r, color=color.name)
            color_dict[r] = color.name
            color_num += 1
        else:
            if print_background_triangle:
                PS += '% {r} --> back-ground\n'.format(r=r)
            else:
                PS += '% {r} --> no-color\n'.format(r=r)

    if print_sample:
        PS += '% -- color sample ---------------\n'
        PS += '/Times-Roman findfont {s} scalefont setfont\n'.format(s=int(sample_scale*0.6))
        x = row*scale + sample_scale
        y = 0
        for r in range(modulo):
            if coloring_flags[r]:
                color = color_dict[r]
                PS += 'black {x} {y} moveto (:{r}) show\n'.format(x=x+2*sample_scale,
                                                            y=y,
                                                            r=r)
                PS += '{color} {x} {y} moveto colorsample\n'.format(color=color,
                                                                  x=x,y=y)
                y -= sample_scale
            elif print_background_triangle:
                color = color_dict['back-ground']
                PS += 'black {x} {y} moveto (:{r}) show\n'.format(x=x+2*sample_scale,
                                                            y=y,
                                                            r=r)
                PS += '{color} {x} {y} moveto colorsample\n'.format(color=color,
                                                                  x=x,y=y)
                y -= sample_scale

    if print_background_triangle:
        print_no_color = False # auto setting
        i, j = 0, 0
        PS += '{color} {x:<8.5f} {y:8<.5f} moveto\n'.format(color=color_dict['back-ground'],
                                                                 x=(-(i+1)+2*j)*scale,
                                                                 y=-i*scale*yscale)

        i, j = row-1, 0
        PS += '{x:<8.5f} {y:8<.5f} lineto\n'.format(color=color_dict['back-ground'],
                                                                 x=(-(i+1)+2*j)*scale,
                                                                 y=-i*scale*yscale)
        i, j = row-1, row-1
        PS += '{x:<8.5f} {y:8<.5f} lineto\n'.format(color=color_dict['back-ground'],
                                                                 x=(-(i+1)+2*j)*scale,
                                                                 y=-i*scale*yscale)
        PS += 'fill\n'

    nCr = gen_nCr_mod(row,modulo)

    for i in range(row):
        for j in range(i+1):
            iCj = nCr[i][j]# % modulo
            if coloring_flags[iCj]:
                PS += '{color} {x:<8.5f} {y:8<.5f} colorbox\n'.format(color=color_dict[iCj],
                                                                 x=(-(i+1)+2*j)*scale,
                                                                 y=-i*scale*yscale)
            else:# no-color
                if print_no_color:
                    PS += 'black {x:<8.5f} {y:8<.5f} nocolorbox\n'.format(x=(-(i+1)+2*j)*scale,
                                                                 y=-i*scale*yscale)

    PS_foot = 'showpage'
    return PS_head + PS + PS_foot


if __name__ == '__main__':

    n = 300
    modulo = 5
    shape = 'circle'
    bg_flag = True
    if bg_flag:
        bg = '_bg'
    else:
        bg = ''
    out_directory = './out'
    file_name = 'Pascal_triangle_mod{modulo}_{n}_{shape}{bg}.ps'.format(modulo=modulo, n=n,
                                                                        shape=shape, bg=bg)
    os.mkdir(out_directory)
    f = open(out_directory + '/' + file_name, 'w')

    #ps = Pascal_triangle_coloring(600, 5,
    #                         #shape='rectangle',
    #                         scale=0.2, yscale=1.73, line_width=0.1,
    #                         color_list=[GRAY]+COLORS,
    #                         coloring_flags=[True]*5
    #                         #print_sample=True, sample_scale=10
    #                              )

    #ps = Pascal_triangle_coloring(600, 5,
    #                         shape='circle',
    #                         scale=0.2, yscale=1.73, line_width=0.1,
    #                         color_list=[GRAY]+COLORS,
    #                         coloring_flags=[True]*5
    #                         #print_sample=True, sample_scale=10
    #                              )

    ps = Pascal_triangle_coloring(n, modulo,
                             shape=shape,
                             scale=0.5, yscale=3**0.5,
                             line_width=0.05,
                             print_background_triangle=bg_flag,
                             #print_no_color=False,
                             color_list=[BLACK]+COLORS,
                             coloring_flags=[False] + [True]*40,
                             print_sample=True
                                  )

    f.write(ps)
    f.close()

    print('success')
