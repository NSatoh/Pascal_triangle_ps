import os

import color
import postscript


def gen_nCr_mod(n, modulo):
    """
    Generate binary coefficient nCr

    :param int n:
    :param int modulo:
    :rtype: list[list[int]]
    :return: [[C(0,0)], [C(1,0), C(1,1)], ..., [C(n,0), C(n,1), ..., C(n,n)]]
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
                             scale=0.7, yscale=3**0.5,
                             line_width=0.1,
                             color_list=COLORS,
                             coloring_flags=[False] + [True]*12,
                             print_background_triangle=False,
                             print_no_color=True,
                             print_color_sample=True,
                             sample_length=10):
    """
    Generate PostScript src

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
    :param bool print_color_sample: if True, output the color samples
    :param int sample_length: length of edge of the color sample rectangles
    :rtype: str
    :return: PostScript source
    """

    if print_background_triangle:
        print_no_color = False  # auto setting

    ps = postscript.PostScript()

    # postscript の仕様では, 1pt = 1/72 インチ
    # A4 だと, 0 < x < 595pt, 0 < y < 842pt くらい
    # そしてよくわからないが，座標では 左下(0,0) -- (501,709)右上 くらい
    ps.header.comment('inch -> mm')
    ps.header.definition('mm', '2.834646 mul')

    for c in color_list:
        ps.header.color_definition(c)

    if shape is 'rectangle':
        ps.header.definition('colorbox', [
            'moveto',
            '0 {s} rlineto'.format(s=scale * yscale),
            '{ss} 0 rlineto'.format(ss=2 * scale),
            '0 -{s} rlineto'.format(s=scale * yscale),
            'fill',
        ])
        ps.header.definition('nocolorbox', [
            'moveto',
            '0 {s} rlineto'.format(s=scale * yscale),
            '{ss} 0 rlineto'.format(ss=2 * scale),
            '0 -{s} rlineto'.format(s=scale * yscale),
            'stroke',
        ])
    elif shape is 'circle':
        ps.header.definition('colorbox', [
            '{s} 0 360 arc'.format(s=scale),
            'fill',
        ])
        ps.header.definition('nocolorbox', [
            '{s} 0 360 arc'.format(s=scale),
            'stroke',
        ])
    else:
        pass

    ps.header.definition('colorsample', [
        '0 {s} rlineto'.format(s=sample_length // 2),
        '{ss} 0 rlineto'.format(ss=2 * sample_length),
        '0 -{s} rlineto'.format(s=sample_length // 2),
        'fill'
    ])

    ps.body.new_path()
    ps.body.set_line_width(line_width)

    ps.body.comment('原点を, 大体紙の中央一番上へ移動')
    ps.body.translate(250, 700)

    ps.body.comment('****************** Pascal triangle -- {row} -- [color fill] ******************'.format(row=row))
    ps.body.comment('mod {modulo}'.format(modulo=modulo))
    ps.body.comment('print save mode --> {flag}'.format(flag=print_background_triangle))

    for r in range(modulo):
        color_name = color_list[r].name if coloring_flags[r] else 'no-color'
        ps.body.comment('{r} --> {color}'.format(r=r, color=color_name))

    if print_color_sample:
        ps.body.comment('-- color sample ---------------')
        ps.body.set_font('Times-Roman', point=int(sample_length * 0.6))

        x = row*scale + sample_length
        y = 0
        for r in range(modulo):
            ps.body.set_color(color.BLACK)
            ps.body.draw_string(x=x + 2*sample_length, y=y, string=':{r}'.format(r=r))
            ps.body.set_color(color_list[r])
            ps.body.move_to(x, y)
            ps.body.call('colorsample')
            y -= sample_length

    if print_background_triangle:
        remainder0_color_number = 0

        i, j = 0, 0
        x = (-(i+1) + 2*j) * scale
        y = -i * scale * yscale
        triangle_vertex1 = (round(x, 5), round(y, 5))

        i, j = row-1, 0
        x = (-(i+1) + 2*j) * scale
        y = -i * scale * yscale
        triangle_vertex2 = (round(x, 5), round(y, 5))

        i, j = row-1, row-1
        x = (-(i+1) + 2*j) * scale
        y = -i * scale * yscale
        triangle_vertex3 = (round(x, 5), round(y, 5))

        ps.body.set_color(color_list[remainder0_color_number])
        ps.body.fill_triangle(triangle_vertex1, triangle_vertex2, triangle_vertex3)

    nCr = gen_nCr_mod(row, modulo)

    for i in range(row):
        for j in range(i+1):
            iCj = nCr[i][j]
            x = (-(i+1) + 2*j) * scale
            y = -i * scale * yscale
            if coloring_flags[iCj]:
                ps.body.set_color(color_list[iCj])
                ps.body.append_content('{x} {y} colorbox'.format(x=round(x, 5), y=round(y, 5)))
            else:  # no-color
                if print_no_color:
                    ps.body.set_color(color.BLACK)
                    ps.body.append_content('{x} {y} nocolorbox'.format(x=round(x, 5), y=round(y, 5)))

    ps.footer.show_page()

    return ps.get_source()


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
    file_name = 'Pascal_triangle_mod{modulo}_{n}_{shape}{bg}.ps'.format(modulo=modulo, n=n, shape=shape, bg=bg)
    if not os.path.isdir(out_directory):
        os.mkdir(out_directory)
    f = open(out_directory + '/' + file_name, 'w')

    ps_src = pascal_triangle_coloring(n, modulo,
                                      shape=shape,
                                      scale=0.5, yscale=3**0.5,
                                      line_width=0.05,
                                      print_background_triangle=bg_flag,
                                      #print_no_color=False,
                                      color_list=[color.BLACK]+COLORS,
                                      coloring_flags=[False] + [True]*40,
                                      print_color_sample=True
                                      )

    f.write(ps_src)
    f.close()

    print('success')
