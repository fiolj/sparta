from pathlib import Path
import re
parentdir = Path().home() / "Trabajos/dsmc"  # Parent directory
pi = parentdir / "sparta/doc"  # Input path
po = parentdir / "sparta/newdoc"             # Output path

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
recmds = re.compile(f"({srecmds}$)",flags=re.M)
repar = re.compile(r"(?s)((?:[^\n][\n]?)+)")  # Matches a paragraph


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

apply_cmds = {
  'p':lambda x:x,
  'b':lambda x:x,
  'line': lambda x: "------",
  
}  
if __name__ == '__main__':

  fi = pi / "Section_accelerate.txt"
  fi = pi / "Section_howto.txt"
  # fi = pi / "fix.txt"
  # fi = pi / "variable.txt"
  # for fi in pi.glob("*.txt"):
  #   s = read_sjptxt(fi)
  s = read_sjptxt(fi)
  ss = ""

  for m in repar.finditer(s):
    par, cmds = get_par_cmds(m.group().rstrip())
    # ss = ""
    
    # ss += apply_cmd_par(s)
    if len(cmds) >= 1:
      print(cmds)

