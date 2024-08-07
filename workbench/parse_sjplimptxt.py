from pathlib import Path
import re
parentdir = Path().home() / "Trabajos/dsmc"  # Parent directory
pi = parentdir / "sparta/doc"  # Input path
po = parentdir / "sparta/docs"             # Output path

repar = re.compile(r"(?s)((?:[^\n][\n]?)+)")  # Matches a paragraph
recmd = re.compile(r".*:\S+$")

if not po.exists():
  po.mkdir()

cmd_par = ["p", "b", "pre", "c", "h1", "h2", "h3", "h4", "h5", "h6"]  # cmd the entire paragraph
cmd_list = ["ul", "ol", "dl"]  # lines of the paragraph as a list
cmd_parlist = ["l", "dt", "dd", "ulb", "ule", "olb", "ole", "dlb", "dle"]  # treat the paragraph as one entry in a list
cmd_linepar = ["all(p)", "all(c)", "all(b)", "all(l)"]  # applied to each line of the paragraph

# cmd_special = [
#   "line",
#   "image",  # insert an image = <IMG SRC = "file">
#   "link"  # insert a named link that can be referred to elsewhere
# ]

cmd_args = ["link", "tb", "image"]
cmds = cmd_par + cmd_list + cmd_parlist + cmd_linepar + ['line']

scmds = "|".join(cmds).replace("(", r"\(").replace(")", r"\)")
recmds = re.compile("(:(("+scmds+"|,"+")+)$)")
# recmdargs = re.compile(':('+'|'.join(cmd_args)+r')\([^\)]+\)')
recmdargs = re.compile('(:('+'|'.join(cmd_args)+r')\([^\)]+\))')
recmds = re.compile("(:(("+scmds+"|," + '('+'|'.join(cmd_args)+r')\([^\)]+\)' + ")+)$)")

# fi = pi / "Section_accelerate.txt"
fi = pi / "Section_howto.txt"
# fi = pi / "fix.txt"


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
  # if not m:
  #   m = recmdargs.search(paragraph)
  if m:
    parrafo = paragraph[:m.start()]
    cmd = paragraph[m.start()+1:m.end()].split(",")
    return parrafo, cmd
  else:
    return paragraph, []


def read_txtfile(fi):
  """Read txt file and prepare content for processing

  Parameters
  ----------
  fi : Path, string or file-object

  Returns
  -------

  string: cleaned-up contents of file
  """

  # s = Path(fi).read_text().replace(':link(', '\n:link(')
  s = Path(fi).read_text()
  s = recmdargs.sub(r"\1\n", s)  # Add empty line after these commands
  # s = recmds.sub(r"\1\n\n\n", s)  # Add empty line after these commands
  return s


if __name__ == '__main__':

  s = read_txtfile(fi)
  for m in repar.finditer(s):
    par, cmds = get_par_cmds(m.group().rstrip())

    if len(cmds) >= 1:
      print(cmds)
