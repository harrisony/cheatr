import re
import cgi

EXPR_PATTERN = "\{\{(?P<expr>.*?)\}\}|\{\%(?P<tag>.*?)\%\}"

def render_view(template, context):
   def sub(match):
      if match.group('expr'):
         expr = match.group('expr').strip()
         try:
            x = eval(expr, {}, context)
         except:
            print "ExpressionError"
         return cgi.escape(str(x))
      elif match.group('tag'):
         print "Tag matched"
         tag = match.group('tag').strip().split()
         print tag[1]
         if tag[0] == 'include':
            try:
               return render_view(open(tag[1], 'rU').read(), context)
            except:
               print "IncludeError"
   return re.sub(EXPR_PATTERN, sub, template)
