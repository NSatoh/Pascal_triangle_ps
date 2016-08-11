import os

import color


def gen_nCr_mod(n, modulo):
    """
    Generate binary coefficient nCr

    :param int n:
    :param int modulo:
    :rtype: list[list[int]]
    :return: [[C(0,0)], [C(1,0), C(0,1)], ..., [C(n,0), C(n,1), ..., C(n,n)]]
    (nCr = output, then nCr[n][r] is C(n,r) )
    """
    nCr = [[1]]
    for i in range(1, n+1):
        iCr = [1]
        for r in range(1, i):
            iCr += [(nCr[i-1][r-1] + nCr[i-1][r]) % modulo]
        iCr += [1]
        nCr += [iCr]
    return nCr


# -- color settings --------------------------------------------
COLORS = [
    color.RED,
    color.GREEN,
    color.YELLOW,
    color.SLATEBLUE,
    color.GREEN,
    color.MAGENTA,
    color.CYAN,
    color.HOTPINK,
    color.TEAL,
    color.FORESTGREEN,
    color.DARKORCHID,
    color.SKYBLUE,
    color.BLACK
]


def pascal_triangle_coloring(row, modulo,
                             shape='rectangle',
                             scale=0.7, yscale=3**0.5, line_width=0.1,
                             color_list=COLORS,
                             coloring_flags=[False] + [True]*12,
                             print_background_triangle=False,
                             print_no_color=True,
                             print_sample=True, sample_scale=10):
    """
    Generate PS src

    :param int row: the number of rows of the triangle
    :param int modulo: modulo for coloring
    :param str shape: 'rectangle' or 'circle'
    :param float scale:
    :param float yscale:
    :param float line_width:
    :param list[Color] color_list: list of Colors class objects
    :param list[bool] coloring_flags: list of booleans
    :param bool print_background_triangle: if True, fill the background
                                           by color #0, and set variable
                                           print_no_color = False
                                           Automatically
    :param bool print_no_color: if False, don't output no-color cell
    :param bool print_sample: if True, output the color samples
    :param int sample_scale: length of edge of the color sample rectangles
    :rtype: str
    :return: postscript source
    """

    # postscript の仕様では, 1pt = 1/72 インチ
    # A4 だと, 0 < x < 595pt, 0 < y < 842pt くらい
    # そしてよくわからないが，座標では 左下(0,0) -- (501,709)右上 くらい
    ps_head =  r'%!PS-Adobe-3.0' + '\n'
    ps_head += r'/mm { 2.834646 mul } def  % inch -> mm' + '\n'
    ps_head += r'newpath' + '\n'

    ps_head += r'/gray {0.5 setgray } def' + '\n'

    for color in color_list:
        ps_head += color.as_ps_form() + '\n'

    rcomment = '%'
    ccomment = '%'

    if shape == 'rectangle':
        rcomment = ''
    elif shape == 'circle':
        ccomment = ''

    ps_head += '/colorbox {\n'
    ps_head += '  %%-- rectangle --\n'
    ps_head += '  {rcomment}moveto\n'.format(rcomment=rcomment)
    ps_head += '  {rcomment}0 {s} rlineto\n'.format(s=scale*yscale, rcomment=rcomment)
    ps_head += '  {rcomment}{ss} 0 rlineto\n'.format(ss=2*scale, rcomment=rcomment)
    ps_head += '  {rcomment}0 -{s} rlineto\n'.format(s=scale*yscale, rcomment=rcomment)
    ps_head += '  {rcomment}fill\n'.format(rcomment=rcomment)
    ps_head += '  %%-- circle --\n'
    ps_head += '  {ccomment}{s} 0 360 arc\n'.format(s=scale, ccomment=ccomment)
    ps_head += '  {ccomment}fill\n'.format(ccomment=ccomment)
    ps_head += '} def\n'

    ps_head += '/colorsample {\n'
    ps_head += '  0 {s} rlineto\n'.format(s=sample_scale//2)
    ps_head += '  {ss} 0 rlineto\n'.format(ss=2*sample_scale)
    ps_head += '  0 -{s} rlineto\n'.format(s=sample_scale//2)
    ps_head += '  fill\n'
    ps_head += '} def\n'

    ps_head += '/nocolorbox {\n'
    ps_head += '  %%-- rectangle --\n'
    ps_head += '  {rcomment}moveto\n'.format(rcomment=rcomment)
    ps_head += '  {rcomment}0 {s} rlineto\n'.format(s=scale*yscale, rcomment=rcomment)
    ps_head += '  {rcomment}{ss} 0 rlineto\n'.format(ss=2*scale, rcomment=rcomment)
    ps_head += '  {rcomment}0 -{s} rlineto\n'.format(s=scale*yscale, rcomment=rcomment)
    ps_head += '  {rcomment}stroke\n'.format(rcomment=rcomment)
    ps_head += '  %%-- circle --\n'
    ps_head += '  {ccomment}{s} 0 360 arc\n'.format(s=scale, ccomment=ccomment)
    ps_head += '  {ccomment}stroke\n'.format(ccomment=ccomment)
    ps_head += '} def\n'


    ps_body  = 'newpath\n'
    ps_body += '{lw} setlinewidth\n'.format(lw=line_width)
    ps_body += '% 原点を, 大体紙の中央一番上へ移動\n'
    ps_body += '250 700 translate\n'

    ps_body += '%****************** Pascal triangle -- {row} -- [color fill] ******************%\n'.format(row=row)
    ps_body += '% mod {modulo}\n'.format(modulo=modulo)

    color_num = 0
    color_dict = {}  # 直したい

    if print_background_triangle:
        color = color_list[color_num]
        ps_body += '% back-ground --> {color}\n'.format(color=color.name)
        color_dict['back-ground'] = color.name
        color_num += 1

    for r in range(modulo):
        if coloring_flags[r]:
            color = color_list[color_num]
            ps_body += '% {r} --> {color}\n'.format(r=r, color=color.name)
            color_dict[r] = color.name
            color_num += 1
        else:
            if print_background_triangle:
                ps_body += '% {r} --> back-ground\n'.format(r=r)
            else:
                ps_body += '% {r} --> no-color\n'.format(r=r)

    if print_sample:
        ps_body += '% -- color sample ---------------\n'
        ps_body += '/Times-Roman findfont {s} scalefont setfont\n'.format(s=int(sample_scale*0.6))
        x = row*scale + sample_scale
        y = 0
        for r in range(modulo):
            if coloring_flags[r]:
                color = color_dict[r]
                ps_body += 'black {x} {y} moveto (:{r}) show\n'.format(x=x+2*sample_scale,
                                                            y=y,
                                                            r=r)
                ps_body += '{color} {x} {y} moveto colorsample\n'.format(color=color,
                                                                  x=x,y=y)
                y -= sample_scale
            elif print_background_triangle:
                color = color_dict['back-ground']
                ps_body += 'black {x} {y} moveto (:{r}) show\n'.format(x=x+2*sample_scale,
                                                            y=y,
                                                            r=r)
                ps_body += '{color} {x} {y} moveto colorsample\n'.format(color=color,
                                                                  x=x,y=y)
                y -= sample_scale

    if print_background_triangle:
        print_no_color = False  # auto setting
        i, j = 0, 0
        ps_body += '{color} {x:<8.5f} {y:8<.5f} moveto\n'.format(color=color_dict['back-ground'],
                                                                 x=(-(i+1)+2*j)*scale,
                                                                 y=-i*scale*yscale)

        i, j = row-1, 0
        ps_body += '{x:<8.5f} {y:8<.5f} lineto\n'.format(color=color_dict['back-ground'],
                                                                 x=(-(i+1)+2*j)*scale,
                                                                 y=-i*scale*yscale)
        i, j = row-1, row-1
        ps_body += '{x:<8.5f} {y:8<.5f} lineto\n'.format(color=color_dict['back-ground'],
                                                                 x=(-(i+1)+2*j)*scale,
                                                                 y=-i*scale*yscale)
        ps_body += 'fill\n'

    nCr = gen_nCr_mod(row, modulo)

    for i in range(row):
        for j in range(i+1):
            iCj = nCr[i][j]
            if coloring_flags[iCj]:
                ps_body += '{color} {x:<8.5f} {y:8<.5f} colorbox\n'.format(color=color_dict[iCj],
                                                                 x=(-(i+1)+2*j)*scale,
                                                                 y=-i*scale*yscale)
            else:  # no-color
                if print_no_color:
                    ps_body += 'black {x:<8.5f} {y:8<.5f} nocolorbox\n'.format(x=(-(i+1)+2*j)*scale,
                                                                 y=-i*scale*yscale)

    ps_foot = 'showpage'
    return ps_head + ps_body + ps_foot


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
    if not os.path.isdir(out_directory):
      os.mkdir(out_directory)
    f = open(out_directory + '/' + file_name, 'w')

    ps = pascal_triangle_coloring(n, modulo,
                             shape=shape,
                             scale=0.5, yscale=3**0.5,
                             line_width=0.05,
                             print_background_triangle=bg_flag,
                             #print_no_color=False,
                             color_list=[color.BLACK]+COLORS,
                             coloring_flags=[False] + [True]*40,
                             print_sample=True
                                  )

    f.write(ps)
    f.close()

    print('success')
