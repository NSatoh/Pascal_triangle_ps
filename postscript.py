import postscript_command as cmd


class PostScriptContent:

    def __init__(self):
        self.content = []

    def append_content(self, content):
        """
        append content

        :param str|list[str] content:
        :rtype: PostScriptContent
        :return:
        """
        if isinstance(content, list):
            self.content.extend(content)
        else:
            self.content.append(content)
        return self

    def comment(self, content):
        """
        append comment

        :param str content:
        :rtype: PostScriptContent
        :return:
        """
        return self.append_content(cmd.comment(content))

    def definition(self, key, value):
        """
        append definition command

        :param str key:
        :param str|int|float|list[str] value:
        :rtype: PostScriptContent
        :return:
        """
        definition_cmd = cmd.define_procedure if isinstance(value, list) else cmd.define_value
        return self.append_content(definition_cmd(key, value))

    def call(self, key):
        """
        append `call defined object` command

        :param str key:
        :rtype: PostScriptContent
        :return:
        """
        return self.append_content(key)

    def set_line_width(self, width):
        """
        append set_line_width command

        :param int|float width:
        :rtype: PostScriptContent
        :return:
        """
        return self.append_content(cmd.set_line_width(width))

    # TODO: 必要かどうか
    def move_to(self, x, y):
        """
        append `move to` command

        :param int|float x:
        :param int|float y:
        :rtype: PostScriptContent
        :return:
        """
        return self.append_content(cmd.move_to(x, y))

    def translate(self, x, y):
        """
        append translate command

        :param int|float x:
        :param int|float y:
        :rtype: PostScriptContent
        :return:
        """
        return self.append_content(cmd.translate(x, y))

    def set_font(self, font_name, point):
        """
        append font setting command

        :param str font_name:
        :param int point:
        :rtype: PostScriptContent
        :return:
        """
        return self.append_content(cmd.set_font(font_name, point))

    def color_definition(self, color):
        """
        append color definition

        :param color.Color color:
        :rtype: PostScriptContent
        :return:
        """
        color_cmd = cmd.set_rgb_color(color.r, color.g, color.b)
        return self.definition(color.name, color_cmd)

    def set_color(self, color):
        """
        append `set color` command(macro)

        :param color.Color color:
        :rtype: PostScriptContent
        :return:
        """
        return self.append_content(color.name)

    def draw_string(self, x, y, string):
        """
        append `draw string` command

        :param int|float x:
        :param int|float y:
        :param str string:
        :rtype: PostScriptContent
        :return:
        """
        return self.append_content([
            cmd.move_to(x, y),
            cmd.show(string)
        ])

    def fill_rectangle(self, width, height):
        """
        append `fill rectangle` command

        :param int|float width:
        :param int|float height:
        :rtype: PostScriptContent
        :return:
        """
        return self.append_content([
            cmd.r_line_to(width, 0),
            cmd.r_line_to(0, height),
            cmd.r_line_to(-width, 0),
            cmd.fill()
        ])

    def fill_triangle(self, v1, v2, v3):
        """
        append `fill triangle` command

        :param (int|float, int|float) v1: vertex coordinate (x, y)
        :param (int|float, int|float) v2: vertex coordinate (x, y)
        :param (int|float, int|float) v3: vertex coordinate (x, y)
        :rtype: PostScriptContent
        :return:
        """
        return self.append_content([
            cmd.move_to(v1[0], v1[1]),
            cmd.line_to(v2[0], v2[1]),
            cmd.line_to(v3[0], v3[1]),
            cmd.fill()
        ])

    def new_path(self):
        """
        append `new path` command

        :rtype: PostScriptContent
        :return:
        """
        return self.append_content(cmd.new_path())

    def show_page(self):
        """
        append `show page` command

        :rtype: PostScriptContent
        :return:
        """
        return self.append_content(cmd.show_page())

    def get_source(self):
        """
        :rtype: str
        :return: source
        """
        return '\n'.join(self.content)


class PostScript:

    def __init__(self):
        self.header = PostScriptContent()
        self.body = PostScriptContent()
        self.footer = PostScriptContent()

        self.header.append_content('%!PS-Adobe-3.0')

    def get_header_source(self):
        """
        :rtype: str
        :return: header source
        """
        return self.header.get_source()

    def get_body_source(self):
        """
        :rtype: str
        :return: body source
        """
        return self.body.get_source()

    def get_footer_source(self):
        """
        :rtype: str
        :return: footer source
        """
        return self.footer.get_source()

    def get_source(self):
        """
        :rtype: str
        :return: source
        """
        return '\n'.join([
            self.get_header_source(),
            self.get_body_source(),
            self.get_footer_source()
        ])
