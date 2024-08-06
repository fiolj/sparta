from pathlib import Path
parentdir = Path("../..")
pi = parentdir / "sparta-orig/doc"  # Input path
po = parentdir / "sparta/ newdoc"             # Output path

if not po.exists():
  po.mkdir()

format_par = ["p", "b", "pre", "c", "h1", "h2", "h3", "h4", "h5", "h6"]  # format the entire paragraph
format_list = ["ul", "ol", "dl"]  # lines of the paragraph as a list
format_parlist = ["l", "dt", "dd", "ulb", "ule", "olb", "ole", "dlb", "dle"]  # treat the paragraph as one entry in a list
format_linepar = ["all(p)", "all(c)", "all(b)", "all(l)"]  # applied to each line of the paragraph

cmd_special = [
  "line",  # insert a horizontal line = <HR>
  "image",  # insert an image = <IMG SRC = "file">
  "link"  # insert a named link that can be referred to elsewhere
]

# s = pi.read_text()
fi = pi / "Section_accelerate.txt"
for line in fi.read_text().splitlines():
  L = line.split(":")
  # print(line)
  if len(L) > 1:
    print(L)
