import re
import cgi
from TemplateException import TemplateException

class Node(object):
   def __init__(self, parent):
      self.parent = parent
   def render(self, context, response):
      raise NotImplementedError

class GroupNode(Node):
   def __init__(self, parent):
      super(GroupNode, self).__init__(parent)
      self.children = []
   def render(self, context, response):
      for child in self.children:
         child.render(context, response)
   def add_child(self,node):
      self.children.append(node)
      
class ExprNode(Node):
   def __init__(self, parent, expr):
      super(ExprNode, self).__init__(parent)
      self.expr = expr
   def render(self, context, response):
      try:
         output = str(eval(self.expr, {}, context))
         response.write(cgi.escape(output))
      except:
         response.write(self.expr + " does not exist.")

class HTMLNode(Node):
   def __init__(self, parent, content):
      super(HTMLNode, self).__init__(parent)
      self.content = content
   def render(self, context, response):
      response.write(self.content)

class IncludeNode(Node):
   def __init__(self, parent, filepath):
      super(IncludeNode, self).__init__(parent)
      self.filepath = filepath
      self.root = compile_template(self.filepath)
   def render(self, context, response):
      self.root.render(context, response)

def compile_template(filepath):
   root = GroupNode(None)
   try:
      contents = open(filepath, 'rU')
      parse_template(contents.read(), root)
      contents.close()
      return root
   except IOError:
      raise
   except:
      raise# TemplateException("IncludeException: " + filepath)

PATTERN = "\{\{(?P<expr>.*?)\}\}|\{\%(?P<tag>.*?)\%\}"

def parse_template(contents, parent):
   upto = 0
   for match in re.finditer(PATTERN, contents):   
      parent.add_child(HTMLNode(parent, contents[upto:match.start()]))
      if match.group('expr'):
         expr = match.group('expr').strip()
         parent.add_child(ExprNode(parent, expr))
      elif match.group('tag'):
         tag = match.group('tag').strip().split()
         if tag[0] == 'include':
            parent.add_child(IncludeNode(parent, tag[1]))      
      upto = match.end()
   parent.add_child(HTMLNode(parent, contents[upto:]))

def render_template(filepath,context, response):
   root = compile_template(filepath)
   root.render(context, response)
