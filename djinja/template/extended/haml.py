from hamlpy.nodes import TagNode, RootNode, TAG
from hamlpy.nodes import create_node as _create_node
from hamlpy import hamlpy


def create_node(haml_line):
    stripped_line = haml_line.strip()

    if not stripped_line:
        return None

    if stripped_line[0] == TAG:
        return JinjaTagNode(haml_line)

    return _create_node(haml_line)


class JinjaTagNode(TagNode):
    self_closing = TagNode.self_closing
    self_closing.update({
        'macro': 'endmacro',
        'call': 'endcall',
        'trans': 'endtrans'
    })

    may_contain = dict((key, [val]) for key, val in TagNode.may_contain.iteritems())
    may_contain.update({
        'if': ['else', 'elif'],
        'for': ['empty'],
        'with': ['with'],
        'trans': ['pluralize']
    })

    def should_contain(self, node):
        return isinstance(node, TagNode) and node.tag_name in self.may_contain.get(self.tag_name, [])


class Compiler(hamlpy.Compiler):
    def process_lines(self, haml_lines):
        root = RootNode()
        for line in haml_lines:
            haml_node = create_node(line)
            root.add_node(haml_node)
        return root.render()
