(TeX-add-style-hook
 "installationsmanual"
 (lambda ()
   (TeX-run-style-hooks
    "latex2e"
    "TDP003mall"
    "TDP003mall10"
    "subcaption"
    "float"
    "graphicx")
   (TeX-add-symbols
    "version")
   (LaTeX-add-labels
    "fig:settingJson"))
 :latex)

