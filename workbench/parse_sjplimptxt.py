from pathlib import Path
import re
parentdir = Path().home() / "Trabajos/dsmc"  # Parent directory
pi = parentdir / "sparta/doc"  # Input path
po = parentdir / "sparta/docs"             # Output path

# recmd = re.compile(r".*:\S+$")

if not po.exists():
  po.mkdir()

cmd_par = ["p", "b", "pre", "c", "h1", "h2", "h3", "h4", "h5", "h6"]  # cmd the entire paragraph
cmd_lst = ["ul", "ol", "dl"]  # lines of the paragraph as a lst
cmd_parlst = ["l", "dt", "dd", "ulb", "ule", "olb", "ole", "dlb", "dle"]  # treat the paragraph as one entry in a lst
cmd_linepar = ["all(p)", "all(c)", "all(b)", "all(l)"]  # applied to each line of the paragraph
cmd_indep = ['line']            # Commands independent of paragraphs
cmd_args = ["link", "tb", "image"]                      # Commands that take arguments
cmds = cmd_par + cmd_lst + cmd_parlst + cmd_linepar + cmd_indep  # All commands with no arguments

scmds = "|".join(cmds).replace("(",r"\(").replace(")",r"\)")
scmdargs = '('+'|'.join(cmd_args)+r')\([^\)]+\)'

# Regular expressions
srecmds = f":({scmds}|{scmdargs}|,)+"
# recmdargs = re.compile(f"({scmdargs}$)",flags=re.M)
recmds = re.compile(f"({srecmds}$)",flags=re.M)
repar = re.compile(r"(?s)((?:[^\n][\n]?)+)")  # Matches a paragraph

rebraceS = re.compile('([[])([^]]+:)[]]',re.M)
rebrace = re.compile('([{[])([^]}]+)[]}]',re.M)

def apply_inmrkp(s):
  """Convert markup to rst

  Convert [blah:] -> heading-6
  Convert [blah] -> **blah**
  Convert {blah} -> *blah*

  Parameters
  ----------
  s : string
  

  Returns
  -------
  
  string
  """
  def repl(m):
    dmrkup = {'[':"**", '{':'*'}
    delim = dmrkup[m.group(1)]
    return f"{delim}{m.group(2).strip()}{delim}"

  s1= rebraceS.sub(r"\2"+":h6\n\n",s)
  s1= rebrace.sub(repl,s1)
  return s1


def read_sjptxt(fi):
  """Read txt file and preprocess the contents

  

  Parameters
  ----------
  fi : pathlib Path, file object or string
  

  Returns
  -------
  
  string: Contents of file
  """
  s = Path(fi).read_text()
  s = recmds.sub(r"\1\n",s)     # Add newline after each command
  s = s.replace("\\\n","")      # Remove continuation lines
  return s

def get_par_cmds(paragraph):
  """Return the paragraph and commands

  Parameters
  ----------
  paragraph : text to analyze
   

  Returns
  -------
   
  tuple: (paragraph,[cmds])
  """

  m = recmds.search(paragraph)
  if m:
    parrafo = paragraph[:m.start()]
    cmd = paragraph[m.start()+1:m.end()].split(",")
    return parrafo, cmd
  else:
    return paragraph,[]

def fmt_literal(s):
  """format paragraph as code

  Parameters
  ----------
  s : paragraph
  

  Returns
  -------
  
  string: formatted paragraph as code
  """
  ss = "::\n\n   "
  L = s.splitlines()
  ss += "\n   ".join(L)
  return f"\n{ss}\n"


apply_cmds = {
  'p':lambda x:f"{x}",
  'b':lambda x:f"{x}",
  'c':lambda x:f"{x}",
  # We use "standard" order for sections
  'h1':lambda x:f"\n{len(x)*'#'}\n{x}\n{len(x)*'#'}\n",
  'h2':lambda x:f"\n{len(x)*'*'}\n{x}\n{len(x)*'*'}\n",
  'h3':lambda x:f"\n{x}\n{len(x)*'='}\n",
  'h4':lambda x:f"\n{x}\n{len(x)*'-'}\n",
  'h5':lambda x:f"\n{x}\n{len(x)*'^'}\n",
  'h6':lambda x:f"\n{x}\n{len(x)*'\"'}\n",
  'pre':fmt_literal,
  'ulb':lambda x: f"{x}\n",
  'ule':lambda x: f"{x}\n\n",
  'olb':lambda x: f"{x}\n",
  'ole':lambda x: f"{x}\n\n",
  'l': lambda x: f"- {x}",
  'line': lambda x: "\n--------------\n",
  'all(p)': lambda x: '\n\n'.join(x.splitlines())+'\n',
  'all(b)':lambda x:f"{x}\n",
  'all(l)': lambda x: '\n-'.join(x.splitlines())+'\n',
  # 'link':lambda x:x,
}


if __name__ == '__main__':

  fn = "Section_accelerate.txt"
  fn = "Section_howto.txt"
  fn = "fix.txt"
  fn = "variable.txt"
  fn = "write_restart.txt"
  # for fi in pi.glob("*.txt"):
  #   s = read_sjptxt(fi)
  fi = pi/fn
  s = read_sjptxt(fi)
  s = apply_inmrkp(s)

  ss = ""

  for m in repar.finditer(s):
    par, commds = get_par_cmds(m.group().rstrip())
    # if len(commds) >= 1:
    #   print(f"++{par}++")
    #   print(commds)
    ppar = par.rstrip()
    for c in commds:
      if c in cmds:
        ppar = apply_cmds[c](ppar)
    
    # for c in commds:
    #   if c in cmds:
    #     ppar = apply_cmds[c](ppar)
    #   else:
    #     ppar = par
    ss += f"{ppar}\n"
    # # ss += apply_cmd_par(s)
    (po / fn).with_suffix('.rst').write_text(ss)

