def comment(content):
    """
    :param str content: comment content
    :rtype: str
    :return:
    """
    return '% ' + content


def definition(key, value):
    """
    :param str key:
    :param str|int|float value:
    :rtype: str
    :return:
    """
    return '/{key} {{{value}}} def'.format(key=key, value=value)


def set_line_width(width):
    """
    :param int|float width:
    :rtype: str
    :return:
    """
    return '{width} setlinewidth'.format(width=width)


def set_rgb_color(r, g, b):
    """
    :param int|float r:
    :param int|float g:
    :param int|float b:
    :rtype: str
    :return:
    """
    return '{r} {g} {b} setrgbcolor'.format(r=r, g=g, b=b)


def translate(x, y):
    """
    :param int|float x:
    :param int|float y:
    :rtype: str
    :return:
    """
    return '{x} {y} translate'.format(x=x, y=y)


def move_to(x, y):
    """
    :param int|float x:
    :param int|float y:
    :rtype: str
    :return:
    """
    return '{x} {y} moveto'.format(x=x, y=y)


def line_to(x, y):
    """
    :param int|float x:
    :param int|float y:
    :rtype: str
    :return:
    """
    return '{x} {y} lineto'.format(x=x, y=y)


def r_line_to(dx, dy):
    """
    :param int|float dx:
    :param int|float dy:
    :rtype: str
    :return:
    """
    return '{dx} {dy} rlineto'.format(dx=dx, dy=dy)


def fill():
    """
    :rtype: str
    :return:
    """
    return 'fill'


def stroke():
    """
    :rtype: str
    :return:
    """
    return 'stroke'


def show(string):
    """
    :param str string:
    :rtype: str
    :return:
    """
    return '({string}) show'.format(string=string)


def set_font(font_name, point):
    """
    :param str font_name:
    :param int point:
    :rtype: str
    :return:
    """
    return '/{font_name} findfont {point} scalefont setfont'.format(font_name=font_name, point=point)


def new_path():
    """
    :rtype: str
    :return:
    """
    return 'newpath'


def show_page():
    """
    :rtype: str
    :return:
    """
    return 'showpage'
