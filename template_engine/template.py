import re
import cgi
from TemplateException import TemplateException

class Node(object):
   def render(self, context, response):
      raise NotImplementedError

class GroupNode(Node):
   def __init__(self):
      super(GroupNode, self).__init__()
      self.children = []
   def render(self, context, response):
      for child in self.children:
         child.render(context, response)
   def add_child(self,node):
      self.children.append(node)
      
class ExprNode(Node):
   def __init__(self, expr):
      super(ExprNode, self).__init__()
      self.expr = expr
   def render(self, context, response):
      try:
         output = str(eval(self.expr, {}, context))
         response.write(cgi.escape(output))
      except:
         response.write(self.expr + " does not exist.")

class HTMLNode(Node):
   def __init__(self, content):
      super(HTMLNode, self).__init__()
      self.content = content
   def render(self, context, response):
      response.write(self.content)

class IncludeNode(Node):
   def __init__(self, filepath):
      super(IncludeNode, self).__init__()
      self.filepath = filepath
      self.root = compile_template(self.filepath)
   def render(self, context, response):
      self.root.render(context, response)

class IfNode(Node):
   def __init__(self, predicate, group):
      super(IfNode, self).__init__()
      self.predicate = predicate
      self.group = group
   def render(self, context, response):
      if eval(self.predicate,{},context):
         self.group.render(context, response)

class ForNode(Node):
   def __init__(self, items, collection, group):
      super(IfNode, self).__init__()
      self.items = items
      self.collection = collection
      self.group = group
   def render(self, context, response):
      if eval(self.predicate,{},context):
         self.group.render(context, response)

class TokenStream(object):
   def __init__(self,token_list):
      self.token_list = token_list
      self.index = 0
   def next(self):
      self.index += 1
      return self.token_list[self.index-1]
   def peek(self):
      return self.token_list[self.index]
   def valid(self):
      return self.index < len(self.token_list)

def render_template(filepath,context, response):
   root = compile_template(filepath)
   root.render(context, response)

def compile_template(filepath):
   try:
      template_file = open(filepath, 'rU')
      contents = template_file.read()
      template_file.close()
      return parse_template(contents)
   except IOError:
      raise TemplateException("IncludeException: " + filepath + " not found")
   except Exception:
      import traceback
      e = traceback.format_exc()
      print e
      raise #TemplateException("IncludeException: " + filepath + " ")

def parse_template(contents):
   tokens = tokenize(contents)
   return parse_group(tokens)

PATTERN = "\{\{(?P<expr>.*?)\}\}|\{\%(?P<tag>.*?)\%\}"
FORPATTERN = "(?P<items>.*?)\s+in\s+(?P<collection>.*)"

def tokenize(contents):
   tokens = []
   upto = 0
   for match in re.finditer(PATTERN, contents):
      tokens.append((contents[upto:match.start()],"html"))
      if match.group('expr'):
         expr = match.group('expr').strip()
         tokens.append((expr,"expr"))
      elif match.group('tag'):
         tag,arg = match.group('tag').strip().split(" ",1)
         if tag == 'include':
            tokens.append((arg,"include"))
         elif tag == 'if':
            tokens.append((arg,"if"))
         elif tag == 'end':
            tokens.append((arg,"end"))
         elif tag == 'for':
            items,collection = re.search(FORPATTERN,arg).groups()
            tokens.append((items,collection,"for"))
      upto = match.end()
   tokens.append((contents[upto:],"html"))
   tokens = TokenStream(tokens)
   return tokens

def parse_group(tokens):
   group = GroupNode()
   while tokens.valid():
      if tokens.peek()[1] == "html":
         group.add_child(HTMLNode(tokens.next()[0]))
      elif tokens.peek()[1] == "expr":
         group.add_child(ExprNode(tokens.next()[0]))
      elif tokens.peek()[1] == "include":
         group.add_child(IncludeNode(tokens.next()[0]))
      elif tokens.peek()[1] == "if":
         group.add_child(parse_if(tokens))
      else:
         break
   return group

def parse_if(tokens):
   if_token = tokens.next()
   group = parse_group(tokens)
   if tokens.valid():
      endif_token = tokens.next()
      if endif_token[1] != "end" or endif_token[0] != "if":
         raise TemplateException("EndTagException: Mismatched End Tag")
   else:
      raise TemplateException("EndTagException: Missing {% end if %}")
   return IfNode(if_token[0], group)

def parse_for(tokens):
   for_token = tokens.next()
   group = parse_group(tokens)
   if tokens.valid():
      endfor_token = tokens.next()
      if endfor_token[1] != "end" or endfor_token[0] != "for":
         raise TemplateException("EndTagException: Mismatched End Tag")
   else:
      raise TemplateException("EndTagException: Missing {% end for %}")
   return ForNode(for_token[0], group)
