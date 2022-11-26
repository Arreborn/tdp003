(TeX-add-style-hook
 "gruppkontrakt"
 (lambda ()
   (TeX-run-style-hooks
    "latex2e"
    "mall"
    "mall10")
   (TeX-add-symbols
    "version"))
 :latex)

