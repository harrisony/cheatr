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
   def __init__(self, filepath, scope):
      super(IncludeNode, self).__init__()
      self.filepath = filepath
      self.root = compile_template(self.filepath, scope)
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
   def __init__(self, item, collection, group):
      super(ForNode, self).__init__()
      self.item = item
      self.collection = collection
      self.group = group
   def render(self, context, response):
      collection = eval(self.collection, {}, context)
      if self.item:
         for item in collection:
            context[self.item] = item
            self.group.render(context, response)
      
class Token(object):
   def __init__(self, type, args):
      self.type = type
      self.args = args
   def arg(self, item=0):
      try:
         return self.args[item]
      except:
         raise
         
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

class Scope(object):
   def __init__(self, parent, filepath):
      self.filepath = filepath
      self.parent = parent
   def valid_path(self, include_path):
      if self.filepath == include_path:
         return False
      elif self.parent:
         return self.parent.valid_path(include_path)
      else:
         return True
         
      
def render_template(filepath,context, response):
   root = compile_template(filepath, Scope(None, filepath))
   root.render(context, response)

def compile_template(filepath, scope):
   try:
      template_file = open(filepath, 'rU')
      contents = template_file.read()
      template_file.close()
      return parse_template(contents, scope)
   except IOError:
      raise TemplateException("IncludeException: " + filepath + " not found")
   except Exception:
      import traceback
      e = traceback.format_exc()
      print e
      raise #TemplateException("IncludeException: " + filepath + " ")

def parse_template(contents, scope):
   tokens = tokenize(contents)
   return parse_group(tokens, scope)

PATTERN = "\{\{(?P<expr>.*?)\}\}|\{\%(?P<tag>.*?)\%\}"
FORPATTERN = "(?P<items>.*?)\s+in\s+(?P<collection>.*)"

def tokenize(contents):
   tokens = []
   upto = 0
   for match in re.finditer(PATTERN, contents):
      tokens.append(Token("html", (contents[upto:match.start()],)))
      if match.group('expr'):
         expr = match.group('expr').strip()
         tokens.append(Token("expr", (expr,)))
      elif match.group('tag'):
         tag,arg = match.group('tag').strip().split(" ",1)
         if tag == 'include':
            tokens.append(Token("include",(arg.split()[0],)))
         elif tag == 'if':
            tokens.append(Token("if",(arg,)))
         elif tag == 'end':
            tokens.append(Token("end",(arg,)))
         elif tag == 'for':
            items,collection = re.search(FORPATTERN,arg).groups()
            tokens.append(Token("for", (items,collection)))
      upto = match.end()
   tokens.append(Token("html", (contents[upto:],)))
   tokens = TokenStream(tokens)
   return tokens

def parse_group(tokens, scope):
   group = GroupNode()
   while tokens.valid():
      if tokens.peek().type == "html":
         group.add_child(HTMLNode(tokens.next().arg()))
      elif tokens.peek().type == "expr":
         group.add_child(ExprNode(tokens.next().arg()))
      elif tokens.peek().type == "include":
         group.add_child(parse_include(tokens.next().arg(), scope))
      elif tokens.peek().type == "if":
         group.add_child(parse_if(tokens, scope))
      elif tokens.peek().type == "for":
         group.add_child(parse_for(tokens, scope))
      else:
         break
   return group

def parse_include(filepath, scope):   
   if scope.valid_path(filepath):
      
      return IncludeNode(filepath, scope)
   else:
      return HTMLNode("SCREW YOU, YOU INFINITE LOOPER! I SPENT VALUABLE TIME TRYING TO STOP YOUR BLOODY INFINITE LOOP! >:C")
   
def parse_if(tokens, scope):
   if_token = tokens.next()
   group = parse_group(tokens, scope)
   if tokens.valid():
      endif_token = tokens.next()
      if endif_token.type != "end" or endif_token.arg() != "if":
         raise TemplateException("EndTagException: Mismatched End Tag")
   else:
      raise TemplateException("EndTagException: Missing {% end if %}")
   return IfNode(if_token.arg(), group)

def parse_for(tokens, scope):
   for_token = tokens.next()
   group = parse_group(tokens, scope)
   if tokens.valid():
      endfor_token = tokens.next()
      if endfor_token.type != "end" or endfor_token.arg() != "for":
         raise TemplateException("EndTagException: Mismatched End Tag")
   else:
      raise TemplateException("EndTagException: Missing {% end for %}")
   return ForNode(for_token.arg(), for_token.arg(1), group)
