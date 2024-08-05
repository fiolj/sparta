from pathlib import Path

pi = Path("../sparta-orig/doc")  # Input path
po = Path("newdoc/")             # Output path

if not po.exists():
  po.mkdir()

format_par = ["p", "b", "pre", "c", "h1", "h2", "h3", "h4", "h5", "h6"]  # format the entire paragraph
format_list = ["ul", "ol", "dl"]  #  lines of the paragraph as a list
format_parlist = ["l", "dt", "dd", "ulb", "ule", "olb", "ole", "dlb", "dle"]  # treat the paragraph as one entry in a list
# s = pi.read_text()

for line in pi.read_text():
  L = line.split(":")
  if len(L) > 1:



