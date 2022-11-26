(TeX-add-style-hook
 "exempel"
 (lambda ()
   (TeX-add-to-alist 'LaTeX-provided-package-options
                     '(("geometry" "hmargin=1cm")))
   (TeX-run-style-hooks
    "latex2e"
    "mall"
    "mall10"
    "xcolor"
    "blindtext"
    "geometry"
    "tabularx")
   (TeX-add-symbols
    "version"))
 :latex)

