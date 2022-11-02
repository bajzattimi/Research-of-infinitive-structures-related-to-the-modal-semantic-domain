import re

a = """[/N][All]:
[/Supl][/Adj][_Comp/Adj][Poss.1Sg][All]
[/Supl][/Adj][_Comp/Adj][Poss.3Sg][All]
[/Num][_Ord/Adj][All]
[/Adj][_Comp/Adj][All]
[/Adj][All]
[/Adj][All][Punct]
[/Adj][AnP][All]
[/Adj|Pro][All]
[/Adj|Pred][All]
[/Adj][_Comp/Adj][_Design/Adj][All]
[/Adj|Attr|Pro][All]
[/Adj|Unit][All]
[/Adj|col][All]
[/Adj][Fam.Pl][All]
[/Adj|nat][All]
[/Det|Pro][All]
[/Adj][Poss.1Pl][All]
[/Adj][Poss.1Sg][All]
[/Adj][Poss.2Sg][All]
[/Adj][Poss.3Pl][All]
[/Adj][Poss.3Sg][All]
[/Adj][Poss.3Sg][All][Punct]
[/Adj|Pro][AnP][All]
[/Adj|Pro][Poss.3Sg][All]
[/N|Acron][Poss.1Pl][All]
[/N][AnP][All]
[/N][AnP][All][Punct]
[/N][All]
[N][All]
[/N][All][Hyph:Slash]
[/N][All][Punct]
[/N][Poss.1Pl][All]
[/N][Poss.1Pl][AnP][All]
[/N][Poss.1Pl][All][Punct]
[/N][Poss.1Sg][All]
[/N][Poss.1Sg][All][Punct]
[/N][Poss.2Pl][All]
[/N][Poss.2Sg][All]
[/N][Poss.2Sg][All][Punct]
[/N][Poss.3Pl][All]
[/N][Poss.3Pl][All][Punct]
[/N][Poss.3Pl][AnP][All]
[/N][Poss.3Sg][All]
[/N][Poss.3Sg][All][Hyph:Slash]
[/N][Poss.3Sg][All][Punct]
[/N][Poss.3Sg][AnP][All]
[/Supl][/Adj][_Comp/Adj][All]
[/Supl][/Adj][All]
[/Supl][/Adj][_Comp/Adj][_Design/Adj][Poss.3Sg][All]



[/N][Cau]:
[/Supl][/Adj][_Comp/Adj][Poss.3Sg][Cau]
[/Num][_Ord/Adj][Cau]
[/Num|Digit][_Ord/Adj][Cau]
[/Adj][_Comp/Adj][Cau]
[/Adj][Cau]
[/Adj][Cau][Punct]
[/Adj|Pro][Cau]
[/Adj|Pred][Cau]
[/Adj][_Comp/Adj][_Design/Adj][Cau]
[/Adj|Attr|Pro][Cau]
[/Adj|Unit][Cau]
[/Adj|col][Cau]
[/Adj|nat][Cau]
[/Det|Pro][Cau]
[/Adj][Poss.1Pl][Cau]
[/Adj][Poss.1Sg][Cau]
[/Adj][Poss.2Pl][Cau]
[/Adj][Poss.2Sg][Cau]
[/Adj][Poss.3Pl][Cau]
[/Adj][Poss.3Pl][Cau][Punct]
[/Adj][Poss.3Sg][Cau]
[/Adj|Pro][AnP][Cau]
[/N][AnP][Cau]
[/N][AnP][Cau][Punct]
[/N][Cau]
[/N][Cau][Hyph:Slash]
[/N][Cau][Punct]
[/N][Poss.1Pl][Cau]
[/N][Poss.1Pl][Cau][Punct]
[/N][Poss.1Sg][Cau]
[/N][Poss.1Sg][Cau][Punct]
[/N][Poss.2Pl][Cau]
[/N][Poss.2Sg][Cau]
[/N][Poss.2Sg][Cau][Punct]
[/N][Poss.3Pl][Cau]
[/N][Poss.3Pl][Cau][Punct]
[/N][Poss.3Sg][AnP][Cau]
[/N][Poss.3Sg][Cau]
[/N][Poss.3Sg][Cau][Punct]


[/N][Del]:
[/Supl][/Adj][Del]
[/Supl][/Adj][_Comp/Adj][Poss.3Sg][Del]
[/Supl][/Adj][_Comp/Adj][Poss.3Pl][Del]
[/Num][_Ord/Adj][Del]
[/Num|Digit][_Ord/Adj][Poss.3Sg][Del]
[/Num|Digit][_Ord/Adj][Del]
[/Adj][_Comp/Adj][Del]
[/Adj][Del]
[/Adj|Attr][Del]
[/Adj|Pro][Del]
[/Adj|Pred][Del]
[/Adj][_Comp/Adj][_Design/Adj][Del]
[/Adj|Attr|Pro][Del]
[/Adj|Unit][Del]
[/Adj|col][Del]
[/Adj][Del][Punct]
[/Adj|nat][Del]
[/Det|Pro][Del]
[/Adj][Poss.1Pl][Del]
[/Adj][Poss.1Pl][Del][Punct]
[/Adj][Poss.2Pl][Del]
[/Adj][Poss.2Sg][Del]
[/Adj][Poss.1Sg][Del]
[/Adj][Poss.3Pl][Del]
[/Adj][Poss.3Sg][Del]
[/Adj|Pro][AnP][Del]
[/Adj|Pro][Del]
[/Adj|Pro][Del][Punct]
[/Adj|Pro][Poss.3Sg][Del]
[/N][AnP][Del]
[/N][AnP][Del][Punct]
[/N][Del]
[/N][Del][Hyph:Slash]
[/N][Del][Punct]
[/N][_Comp/Adj][Del]
[/N][Poss.1Pl][Del]
[/N][Poss.1Pl][Del][Hyph:Slash]
[/N][Poss.1Pl][Del][Punct]
[/N][Poss.1Sg][AnP][Del]
[/N][Poss.1Sg][Del]
[/N][Poss.1Sg][Del][Punct]
[/N][Poss.2Pl][Del]
[/N][Poss.2Sg][AnP][Del]
[/N][Poss.2Sg][Del]
[/N][Poss.3Pl][AnP][Del]
[/N][Poss.3Pl][Del]
[/N][Poss.3Pl][Del][Punct]
[/N][Poss.3Sg][Del]
[/N][Poss.3Sg][Del][Punct]
[/Supl][/Adj][_Comp/Adj][Del]
[/Supl][/Adj][_Comp/Adj][_Design/Adj][Poss.3Sg][Del]

[/N][EssFor:képp]:
[/Adj][_Comp/Adj][EssFor:képp]
[/Adj][EssFor:képp]
[/Adj|Pro][EssFor:képp]
[/Adj|Pred][EssFor:képp]
[/Adj|Attr|Pro][EssFor:képp]
[/Adj|Unit][EssFor:képp]
[/Adj|col][EssFor:képp]
[/Adj|nat][EssFor:képp]
[/Det|Pro][EssFor:képp]
[/N][EssFor:képp]
[/N][EssFor:képp][Punct]
[/N][Poss.3Sg][EssFor:képp]

[/N][EssFor:képpen]:
[/Adj][_Comp/Adj][EssFor:képpen]
[/Adj][EssFor:képpen]
[/Adj|Pro][EssFor:képpen]
[/Adj|Pred][EssFor:képpen]
[/Adj|Attr|Pro][EssFor:képpen]
[/Adj|Unit][EssFor:képpen]
[/Adj|col][EssFor:képpen]
[/Adj|nat][EssFor:képpen]
[/Det|Pro][EssFor:képpen]
[/N][EssFor:képpen]
[/N][EssFor:képpen][Punct]
[/N][Poss.3Sg][EssFor:képpen]


[/N][Ess]:
[/Adj][_Comp/Adj][Ess]
[/Adj][Ess]
[/Adj|Pro][Ess]
[/Adj|Pred][Ess]
[/Adj|Attr|Pro][Ess]
[/Adj|Unit][Ess]
[/Adj|col][Ess]
[/Adj][Ess][Punct]
[/Adj|nat][Ess]
[/Det|Pro][Ess]
[/N][Ess]
[/N][Ess][Punct]
[/N][Poss.1Pl][Ess]
[/N][Poss.1Sg][Ess]
[/N][Poss.2Pl][Ess]
[/N][Poss.2Sg][Ess]
[/N][Poss.3Pl][Ess]
[/N][Poss.3Sg][Ess]


[/N][Ine]:
[/Supl][/Adj][Ine]
[/Num][_Ord/Adj][Ine]
[/Adj][_Comp/Adj][Ine]
[/Adj][Ine]
[/Adj][AnP][Ine]
[/Adj|Attr][Ine]
[/Adj|Pro][Ine]
[/Adj|Pred][Ine]
[/Adj][_Comp/Adj][_Design/Adj][Ine]
[/Adj|Attr|Pro][Ine]
[/Adj|Unit][Ine]
[/Adj|col][Ine]
[/Adj|nat][Ine]
[/Adj][Ine][Punct]
[/Det|Pro][Ine]
[/Adj][Poss.1Pl][Ine]
[/Adj][Poss.1Sg][AnP][Ine]
[/Adj][Poss.2Pl][Ine]
[/Adj][Poss.2Sg][Ine]
[/Adj][Poss.1Sg][Ine]
[/Adj][Poss.3Pl][Ine]
[/Adj][Poss.3Sg][Ine]
[/Adj][Poss.3Sg][Ine][Punct]
[/Adj|Pro][AnP][Ine]
[/Adj|Pro][Ine]
[/Adj|Pro][Poss.3Sg][Ine]
[/N][AnP][Ine]
[/N][AnP][Ine][Punct]
[/N][AnP][Ine][Punct][Hyph:Slash]
[/N][Ine]
[/N][Ine][Hyph:Slash]
[/N][Ine][Punct]
[/N][Ine][Nom]
[/N][Ine][Punct][Hyph:Slash]
[/N][Ine][Punct][Punct]
[/N][Poss.1Pl][Ine]
[/N][Poss.1Pl][Ine][Punct]
[/N][Poss.1Sg][AnP][Ine]
[/N][Poss.1Sg][Ine]
[/N][Poss.1Sg][Ine][Punct]
[/N][Poss.1Sg][Ine][Punct][Punct]
[/N][Poss.2Pl][Ine]
[/N][Poss.3Pl][Ine]
[/N][Poss.3Pl][Ine][Punct]
[/N][Poss.2Sg][Ine]
[/N][Poss.2Sg][Ine][Hyph:Slash]
[/N][Poss.2Sg][Ine][Punct]
[/N][Poss.2Sg][Ine][Punct][Hyph:Slash]
[/N][Poss.2Sg][AnP][Ine]
[/N][Poss.3Sg][Ine]
[/N][Poss.3Sg][Ine][Prs.NDef.3Sg]
[/N][Poss.3Sg][Ine][Punct]
[/N][Poss.3Sg][AnP][Ine]
[/Num|Digit][_Ord/Adj][Ine]
[/Supl][/Adj][_Comp/Adj][Ine]
[/Supl][/Adj][_Comp/Adj][_Design/Adj][Poss.3Sg][Ine]
[/Supl][/Num][_Ord/Adj][_Comp/Adj][Ine]

[/N][Ins]:
[/Supl][/Adj][Ins]
[/Supl][/Adj][_Comp/Adj][Ins]
[/Supl][/Adj][_Comp/Adj][Poss.3Sg][Ins]
[/Supl][/Adj][_Comp/Adj][_Design/Adj][Ins]
[/Supl][/Adj][_Comp/Adj][_Design/Adj][Poss.3Sg][Ins]
[/Num][_Ord/Adj][Poss.3Sg][Ins]
[/Num][_Ord/Adj][Ins]
[/Num|Digit][_Ord/Adj][AnP][Ins]
[/Num|Digit][_Ord/Adj][Poss.3Sg][Ins]
[/Num|Digit][_Ord/Adj][Ins]
[/N|Acron][Ins]
[/Adj][_Comp/Adj][Ins]
[/Adj][Ins]
[/Adj][AnP][Ins]
[/Adj|Attr][Ins]
[/Adj|Attr][Ins][Punct]
[/Adj|Pro][Ins]
[/Adj|Pred][Ins]
[/Adj][_Comp/Adj][_Design/Adj][Ins]
[/Adj|Attr|Pro][Ins]
[/Adj|Unit][Ins]
[/Adj|col][Ins]
[/Adj|nat][Ins]
[/Adj][Ins][Punct]
[/Det|Pro][Ins]
[/Adj][Poss.1Pl][Ins]
[/Adj][Poss.1Sg][Ins]
[/Adj][Poss.3Pl][Ins]
[/Adj][Poss.3Pl][Ins][Punct]
[/Adj][Poss.3Sg][Ins]
[/Adj][Poss.3Sg][Ins][Punct]
[/Adj][Poss.2Pl][Ins]
[/Adj][Poss.2Sg][Ins]
[/Adj][Poss.2Sg][Ins][Punct]
[/Adj|Pro][AnP][Ins]
[/Adj|Pro][Ins][Punct]
[/Adj|Pro][Ins]
[/Adj|Pro][Poss.3Pl][Ins]
[/Adj|Pro][Poss.3Sg][Ins]
[/N][AnP][Ins]
[/N][AnP][Ins][Punct]
[/N][Ins]
[/N][Ins][Hyph:Slash]
[/N][Ins][Punct]
[/N][Ins][Punct][Hyph:Slash]
[/N][Poss.1Pl][Ins]
[/N][Poss.1Pl][Ins][Punct]
[/N][Poss.1Sg][AnP][Ins]
[/N][Poss.1Sg][Ins][Hyph:Slash]
[/N][Poss.1Sg][Ins]
[/N][Poss.1Sg][Ins][Punct]
[/N][Poss.2Pl][Ins]
[/N][Poss.2Pl][Ins][Punct]
[/N][Poss.2Sg][Ins]
[/N][Poss.2Sg][Ins][Punct]
[/N][Poss.3Pl][Ins]
[/N][Poss.3Pl][Ins][Punct]
[/N][Poss.3Pl][AnP][Ins]
[/N][Poss.3Sg][Ins]
[/N][Poss.3Sg][Ins][Punct]
[/N][Poss.3Sg][AnP][Ins]
[/Supl][/N][Poss.3Sg][Ins]

[/N][Loc]:
[/Adj][_Comp/Adj][Loc]
[/Adj][Loc]
[/Adj|Pro][Loc]
[/Adj|Pred][Loc]
[/Adj|Attr|Pro][Loc]
[/Adj|Unit][Loc]
[/Adj|col][Loc]
[/Adj|nat][Loc]
[/Det|Pro][Loc]
[/N][Loc]
[/N][Loc][Punct]

[/N][Supe]:
[/Supl][/Adj][_Comp/Adj][Poss.1Sg][Supe]
[/Supl][/Adj][_Comp/Adj][Poss.3Pl][Supe]
[/Supl][/Adj][_Comp/Adj][Supe]
[/Supl][/Adj][_Comp/Adj][Poss.3Sg][Supe]
[/Num][_Ord/Adj][AnP][Supe]
[/Num][_Ord/Adj][Supe]
[/Num|Digit][_Ord/Adj][Supe]
[/Num|Digit][_Ord/Adj][Poss.3Sg][Supe]
[/Adj][_Comp/Adj][Supe]
[/Adj][Supe]
[/Adj][AnP][Supe]
[/Adj][AnP][Supe][Punct]
[/Adj|Attr][Supe]
[/Adj|Pro][Supe]
[/Adj|Pred][Supe]
[/Adj|Attr|Pro][Supe]
[/Adj|Unit][Supe]
[/Adj|col][Supe]
[/Adj|nat][Supe]
[/Det|Pro][Supe]
[/Adj][Poss.1Pl][Supe]
[/Adj][Poss.1Sg][Supe]
[/Adj][Poss.2Sg][Fam.Pl][Supe]
[/Adj][Poss.2Sg][Supe]
[/Adj][Poss.3Pl][Supe]
[/Adj][Poss.3Sg][Supe]
[/Adj][Poss.3Sg][Supe][Punct]
[/Adj][Poss.2S][Supe]
[/Adj|Pro][Poss.3Sg][Supe]
[/Adj][Supe][Hyph:Slash]
[/Adj][Supe][Punct]
[/Adj|Pro][Supe][Punct]
[/N][AnP][Supe]
[/N][AnP][Supe][Punct]
[/N][Poss.1Pl][AnP][Supe]
[/N][Poss.1Pl][Supe]
[/N][Poss.1Pl][Supe][Punct]
[/N][Poss.1Sg][Supe]
[/N][Poss.1Sg][Supe][Hyph:Slash]
[/N][Poss.1Sg][Supe][Punct]
[/N][Poss.2Pl][Supe]
[/N][Poss.2Sg][Supe]
[/N][Poss.2Sg][Supe][Punct]
[/N][Poss.3Pl][Supe]
[/N][Poss.3Pl][Supe][Punct]
[/N][Poss.3Sg][AnP][Supe]
[/N][Poss.3Sg][Supe]
[/N][Poss.3Sg][Supe][Hyph:Slash]
[/N][Poss.3Sg][Supe][Punct]

[/N][Temp]:
[/Num|Digit][_Ord/Adj][Temp]
[/Adj][_Comp/Adj][Temp]
[/Adj][Temp]
[/Adj|Pro][Temp]
[/Adj|Pred][Temp]
[/Adj|Attr|Pro][Temp]
[/Adj|Unit][Temp]
[/Adj|col][Temp]
[/Adj|nat][Temp]
[/Det|Pro][Temp]
[/Adj][Poss.1Pl][Temp]
[/N][AnP][Temp]
[/N][Poss.1Pl][Temp]
[/N][Poss.1Sg][Temp]
[/N][Poss.2Sg][Temp]
[/N][Poss.3Sg][Temp]
[/N][Poss.3Sg][Temp][Punct]
[/N][Poss.3Pl][Temp]
[/Supl][/Adj][_Comp/Adj][Temp]

[/N][Ter]:
[/N][Ter][Nom]
[/Supl][/Adj][Poss.1Pl][Ter]
[/Supl][/Adj][_Comp/Adj][Ter]
[/Num][_Ord/Adj][Ter]
[/Num][_Ord/Adj][AnP][Ter]
[/Num|Digit][_Ord/Adj][Ter]
[/Num|Digit][_Ord/Adj][AnP][Ter]
[/Num|Digit][_Ord/Adj][Poss.3Sg][Ter]
[/Adj][_Comp/Adj][Ter]
[/Adj][Ter]
[/Adj][AnP][Ter]
[/Adj|Pro][Ter]
[/Adj|Pred][Ter]
[/Adj|Attr|Pro][Ter]
[/Adj|Unit][Ter]
[/Adj|col][Ter]
[/Adj|nat][Ter]
[/Det|Pro][Ter]
[/Adj][Poss.3Sg][Ter]
[/Adj][Ter][Punct]
[/N][AnP][Ter]
[/N][AnP][Ter][Punct]
[/N][Poss.1Pl][Ter]
[/N][Poss.1Sg][Ter]
[/N][Poss.2Sg][Ter]
[/N][Poss.3Pl][Ter]
[/N][Poss.3Sg][AnP][Ter]
[/N][Poss.3Sg][Ter]
[/N][Poss.3Sg][Ter][Punct]
[/N][Poss.3Sg][Ter][Punct][Hyph:Slash]


[/N][Pl][Transl]:
[/Supl][/Adj][_Comp/Adj][Pl][Transl]
[/Adj][_Comp/Adj][Pl][Transl]
[/Adj][Pl][Transl]
[/Adj|Pro][Pl][Transl]
[/Adj|Pred][Pl][Transl]
[/Adj|Attr|Pro][Pl][Transl]
[/Adj][_Comp/Adj][Pl][Transl]
[/Adj|Unit][[Pl][Transl]
[/Adj|col][Pl][Transl]
[/Adj|nat][Pl][Transl]
[/Det|Pro][Pl][Transl]
[/Adj][Pl.Poss.3Pl][Transl]
[/N][Farm.Pl][Transl]
[/Adj][Pl.Poss.3Sg][Transl]
[/Adj|Pro][Pl][Transl]
[/N][Pl.Poss.1Pl][Transl]
[/N][Pl.Poss.1Sg][Transl]
[/N][Pl.Poss.2Sg][Transl]
[/N][Pl.Poss.3Pl][Transl]
[/N][Pl.Poss.3Sg][Transl]
[/Num][_Ord/Adj][Pl][Transl]

[/N][Pl][Ela]:
[/Supl][/Adj][_Comp/Adj][Pl.Poss.3Sg][Ela]
[/Adj][_Comp/Adj][Pl][Ela]
[/Adj][Pl][Ela]]
[/Adj|Attr][Pl][Ela][Punct]
[/Adj|Attr][Pl.Poss.2Pl][Ela]
[/Adj|Attr][Pl.Poss.3Sg][Ela]
[/Adj|Pro][Pl][Ela]
[/Adj|Pred][Pl][Ela]
[/Adj][_Comp/Adj][Pl][Ela]
[/Adj][_Comp/Adj][Pl][Ela][Punct]
[/Adj|Attr|Pro][Pl][Ela]
[/Adj|Unit][[Pl][Ela]
[/Adj|col][Pl][Ela]
[/Adj|nat][Pl][Ela]
[/Adj][Pl][AnP][Ela]
[/Adj][Pl][Ela]
[/Adj][Pl][Ela][Punct]
[/Det|Pro][Pl][Ela]
[/Adj][Pl.Poss.1Pl][Ela]
[/Adj][Pl.Poss.1Sg][Ela]
[/Adj][Pl.Poss.2Sg][Ela]
[/Adj][Pl.Poss.3Pl][Ela]
[/Adj][Pl.Poss.3Sg][Ela]
[/N][Farm.Pl][Ela]
[/Adj|Pro][Pl][Ela]
[/N][Fam.Pl][Ela]
[/N][Pl][AnP][Ela]
[/N][Pl][Ela]
[/N][Pl][Ela][Punct]
[/N][Pl.Poss.1Pl][Ela]
[/N][Pl.Poss.1Pl][Ela][Punct]
[/N][Pl.Poss.1Sg][Ela]
[/N][Pl.Poss.2Pl][Ela]
[/N][Pl.Poss.2Sg][Ela]
[/N][Pl.Poss.3Pl][Ela][Punct]
[/N][Pl.Poss.3Pl][Ela]
[/N][Pl.Poss.3Sg][Ela]
[/N][Pl.Poss.3Sg][Ela][Punct]

[/N][Pl][Acc]:
[/Supl][/Adj][_Comp/Adj][Pl.Poss.1Sg][Acc]
[/Supl][/Adj][_Comp/Adj][Pl.Poss.3Pl][Acc]
[/Supl][/Adj][_Comp/Adj][Pl.Poss.3Sg][Acc]
[/Supl][/Adj][_Comp/Adj][Pl][Acc]
[/Supl][/Adj][_Comp/Adj][Pl][Acc][Punct]
[/Supl][/Adj][_Comp/Adj][Pl.Poss.1Pl][Acc]
[/Num][_Ord/Adj][Pl.Poss.3Sg][Acc]
[/Num][_Ord/Adj][Pl][Acc]
[/Num][Pl][AnP][Acc]
[/N][Poss.3Sg][Fam.Pl][Acc]
[/N][Poss.2Sg][Fam.Pl][Acc]
[/Adj][_Comp/Adj][Pl][Acc]
[/Adj][Pl][Acc]]
[/Adj|Attr][Pl][Acc][Punct]
[/Adj|Attr][Pl.Poss.2Pl][Acc]
[/Adj|Attr][Pl.Poss.3Sg][Acc]
[/Adj|Pro][Pl][Acc]
[/Adj|Pred][Pl][Acc]
[/Adj][_Comp/Adj][Pl][Acc]
[/Adj][_Comp/Adj][Pl][Acc][Punct]
[/Adj|Attr|Pro][Pl][Acc]
[/Adj|Unit][[Pl][Acc]
[/Adj|col][Pl][Acc]
[/Adj][Fam.Pl][Acc]
[/Adj][Fam.Pl][Acc][Punct]
[/Adj][Fam.Pl][AnP][Acc]
[/Adj|nat][Pl][Acc]
[/Adj][Pl][Acc]
[/Adj][Pl][Acc][Hyph:Slash]
[/Adj][Pl][Acc][Punct]
[/Adj][Pl][AnP][Acc]
[/Det|Pro][Pl][Acc]
[/Adj][Pl.Poss.1Pl][Acc]
[/Adj][Pl.Poss.1Pl][Acc][Punct]
[/Adj][Pl.Poss.1Sg][Acc]
[/Adj][Pl.Poss.1Sg][Acc][Punct]
[/Adj][Pl.Poss.2Pl][Acc]
[/Adj][Pl.Poss.2Pl][AnP.Pl][Acc]
[/Adj][Pl.Poss.2Sg][Acc]
[/Adj][Pl.Poss.2Sg][Acc][Punct]
[/Adj][Pl.Poss.3Pl][Acc]
[/Adj][Pl.Poss.3Pl][Acc][Punct]
[/Adj][Pl.Poss.3Sg][Acc]
[/Adj][Pl.Poss.3Sg][Acc][Punct]
[/N][Farm.Pl][Acc]
[/Adj|Pro][Pl][Acc][Punct]
[/Adj|Pro][Pl][AnP][Acc]
[/N|Acron][Pl][Acc]
[/N][AnP.Pl][Acc]
[/N][Fam.Pl][Acc]
[/N][Fam.Pl][Acc][Punct]
[/N][Fam.Pl][AnP][Acc]
[/N][Pl][AnP.Pl][Acc]
[/N][Pl][Acc]
[/N][Pl][Acc][Hyph:Slash]
[/N][Pl][Acc][Punct]
[/N][Pl][Acc][Punct][Hyph:Slash]
[/N][Pl][AnP][Acc]
[/N][Fam.Pl][AnP.Pl][Acc]
[/N][Pl.Poss.1Pl][Acc]
[/N][Pl.Poss.1Pl][Acc][Punct]
[/N][Pl.Poss.1Sg][Acc]
[/N][Pl.Poss.1Sg][Acc][Punct]
[/N][Pl.Poss.1Pl][AnP][Acc]
[/N][Pl.Poss.2Pl][Acc]
[/N][Pl.Poss.2Pl][Acc][Punct]
[/N][Pl.Poss.2Sg][Acc]
[/N][Pl.Poss.2Sg][Acc][Hyph:Slash]
[/N][Pl.Poss.2Sg][Acc][Punct]
[/N][Pl.Poss.3Pl][Acc]
[/N][Pl.Poss.3Pl][Acc][Punct]
[/N][Pl.Poss.3Pl][AnP][Acc]
[/N][Pl.Poss.3Sg][Acc]
[/N][Pl.Poss.3Sg][Acc][Hyph:Slash]
[/N][Pl.Poss.3Sg][Acc][Punct]
[/N][Pl.Poss.3Sg][Acc][Punct][Hyph:Slash]
[/N][Pl.Poss.3Sg][AnP][Acc]
[/N][Poss.1Sg][Fam.Pl][Acc]
[/N][Poss.1Sg][Fam.Pl][AnP][Acc]
[/Supl][/Num][_Ord/Adj][Pl][Acc]

[/N][Pl][Dat]:
[/Supl][/Adj][_Comp/Adj][Pl.Poss.3Sg][Dat]
[/Supl][/Adj][_Comp/Adj][Pl.Poss.1Pl][Dat]
[/Supl][/Adj][_Comp/Adj][Pl][Dat]
[/Adj][_Comp/Adj][Pl][Dat]
[/Adj][Pl][Dat]
[/Adj|Pro][Pl][Dat]
[/Adj|Pred][Pl][Dat]
[/Adj|Attr|Pro][Pl][Dat]
[/Adj|Unit][[Pl][Dat]
[/Adj|col][Pl][Dat]
[/Adj][Fam.Pl][Dat]
[/Adj|nat][Pl][Dat]
[/N][Poss.3Sg][Fam.Pl][Dat]
[/Adj][Pl][AnP][Dat]
[/Adj][Pl][Dat]
[/Adj][Pl][Dat][Punct]
[/Det|Pro][Pl][Dat]
[/Adj][Pl.Poss.1Pl][Dat]
[/Adj][Pl.Poss.1Pl][Dat][Hyph:Slash]
[/Adj][Pl.Poss.1Pl][Dat][Punct]
[/Adj][Pl.Poss.1Sg][Dat]
[/Adj][Pl.Poss.2Pl][Dat]
[/Adj][Pl.Poss.2Sg][Dat]
[/Adj][Pl.Poss.2Sg][Dat][Punct]
[/Adj][Pl.Poss.3Pl][Dat]
[/Adj][Pl.Poss.3Pl][Dat][Punct]
[/Adj][Pl.Poss.3Sg][Dat]
[/N][Farm.Pl][Dat]
[/Adj|Pro][Pl][Dat]
[/Adj|Pro][Pl][Dat][Punct]
[/N][AnP.Pl][Dat]
[/N][Fam.Pl][Dat]
[/N][Fam.Pl][AnP][Dat]
[/N][Pl][AnP][Dat]
[/N][Pl][Dat]
[/N][Pl][Dat][Punct]
[/N][Pl.Poss.1Sg][Dat]
[/N][Pl.Poss.1Pl][Dat]
[/N][Pl.Poss.1Pl][Dat][Punct]
[/N][Pl.Poss.1Sg][Dat][Punct]
[/N][Pl.Poss.2Pl][Dat]
[/N][Pl.Poss.2Sg][Dat]
[/N][Pl.Poss.2Sg][Dat][Punct]
[/N][Pl.Poss.3Pl][Dat]
[/N][Pl.Poss.3Pl][Dat][Punct]
[/N][Pl.Poss.3Sg][Dat]
[/N][Pl.Poss.3Sg][Dat][Punct]
[/N][Poss.1Pl][AnP.Pl][Dat]
[/N][Poss.1Sg][Fam.Pl][Dat]
[/N][Poss.2Sg][Fam.Pl][Dat]

[/N][Pl][Subl]:
[/Supl][/Adj][Pl][Subl]
[/Supl][/Adj][_Comp/Adj][Pl][Subl]
[/Num][_Ord/Adj][Pl][Subl]
[/Adj][_Comp/Adj][Pl][Subl]
[/Adj][Pl][Subl]
[/Adj|Attr][Pl.Poss.2Pl][Subl]
[/Adj|Pro][Pl][Subl]
[/Adj|Pred][Pl][Subl]
[/Adj|Attr|Pro][Pl][Subl]
[/Adj][_Comp/Adj][Pl.Poss.3Sg][Subl]
[/Adj][_Comp/Adj][Pl][Subl]
[/Adj|Unit][[Pl][Subl]
[/Adj|col][Pl][Subl]
[/Adj|nat][Pl][Subl]
[/Adj][Pl][AnP.Pl][Subl]
[/Det|Pro][Pl][Subl]
[/Adj][Pl.Poss.1Pl][Subl]
[/Adj][Pl.Poss.2Sg][Subl]
[/Adj][Pl.Poss.3Pl][Subl]
[/Adj][Pl.Poss.3Sg][Subl]
[/N][Farm.Pl][Subl]
[/Adj][Pl][Subl][Punct]
[/Adj|Pro][Pl][AnP][Subl]
[/Adj|Pro][Pl][Subl]
[/N|Acron][Pl][Subl]
[/N][AnP.Pl][Subl]
[/N][Fam.Pl][AnP][Subl]
[/N][Pl][AnP][Subl]
[/N][Fam.Pl][Subl]
[/N][Pl.Poss.1Pl][Subl]
[/N][Pl.Poss.1Pl][Subl][Punct]
[/N][Pl.Poss.1Sg][Subl]
[/N][Pl.Poss.1Sg][Subl][Punct]
[/N][Pl.Poss.2Pl][Subl]
[/N][Pl.Poss.2Pl][Subl][Punct]
[/N][Pl.Poss.2Sg][Subl]
[/N][Pl.Poss.3Pl][Subl]
[/N][Pl.Poss.3Pl][Subl][Punct]
[/N][Pl.Poss.3Sg][Subl]
[/N][Pl.Poss.3Sg][Subl][Hyph:Slash]
[/N][Pl.Poss.3Sg][Subl][Punct]
[/N][Pl][Subl]
[/N][Pl][Subl][Punct]


[/N][Pl][EssFor:ként]:
[/Supl][/Adj][_Comp/Adj][Pl.Poss.3Sg][EssFor:ként]
[/Supl][/Adj][_Comp/Adj][Pl][EssFor:ként]
[/Num][_Ord/Adj][Pl][EssFor:ként]
[/Adj][_Comp/Adj][Pl][EssFor:ként]
[/Adj][Pl][EssFor:ként]
[/Adj|Pro][Pl][EssFor:ként]
[/Adj|Pred][Pl][EssFor:ként]
[/Adj|Attr|Pro][Pl][EssFor:ként]
[/Adj|Unit][[Pl][EssFor:ként]
[/Adj|col][Pl][EssFor:ként]
[/Adj|nat][Pl][EssFor:ként]
[/Adj][Pl][EssFor:ként]
[/Det|Pro][Pl][EssFor:ként]
[/Adj][Pl.Poss.1Sg][EssFor:ként]
[/Adj][Pl.Poss.2Sg][EssFor:ként]
[/Adj][Pl.Poss.3Pl][EssFor:ként]
[/Adj][Pl.Poss.3Sg][EssFor:ként]
[/N][Farm.Pl][EssFor:ként]
[/N][Fam.Pl][EssFor:ként]
[/N][Pl.Poss.1Sg][EssFor:ként]
[/N][Pl.Poss.1Pl][EssFor:ként]
[/N][Pl][EssFor:ként]
[/N][Pl.Poss.2Sg][EssFor:ként]
[/N][Pl.Poss.2Pl][EssFor:ként]
[/N][Pl.Poss.3Pl][EssFor:ként]
[/N][Pl.Poss.3Sg][EssFor:ként]

[/N][Pl][Ill]:
[/Adj][_Comp/Adj][Pl][Ill]
[/Adj][Pl][Ill]
[/Adj|Pro][Pl][Ill]
[/Adj|Pred][Pl][Ill]
[/Adj|Attr|Pro][Pl][Ill]
[/Adj|Unit][[Pl][Ill]
[/Adj|col][Pl][Ill]
[/Adj][Fam.Pl][Ill]
[/Adj|nat][Pl][Ill]
[/Adj][Pl][AnP][Ill]
[/Adj][Pl][Ill]
[/Adj][Pl][Ill][Punct]
[/Det|Pro][Pl][Ill]
[/Adj][Pl.Poss.1Sg][Ill]
[/Adj][Pl.Poss.3Sg][Ill]
[/N][Farm.Pl][Ill]
[/Adj|Pro][Pl][AnP][Ill]
[/Adj|Pro][Pl][Ill]
[/N][AnP.Pl][Ill]
[/N][Fam.Pl][Ill]
[/N][Pl][AnP][Ill]
[/N][Pl][Ill]
[/N][Pl][Ill][Punct]
[/N][Pl.Poss.1Pl][Ill]
[/N][Pl.Poss.1Pl][Ill][Punct]
[/N][Pl.Poss.1Sg][Ill]
[/N][Pl.Poss.1Sg][Ill][Punct]
[/N][Pl.Poss.2Pl][Ill]
[/N][Pl.Poss.2Sg][Ill]
[/N][Pl.Poss.3Pl][Ill]
[/N][Pl.Poss.3Pl][Ill][Punct]
[/N][Pl.Poss.3Sg][Ill]
[/N][Pl.Poss.3Sg][Ill][Punct]

[/N][Pl][Abl]:
[/Supl][/Adj][_Comp/Adj][Pl.Poss.3Sg][Abl]
[/Supl][/Adj][_Comp/Adj][Pl][Abl]
[/Adj][_Comp/Adj][Pl][Abl]
[/Adj][Pl][Abl]
[/Adj][AnP.Pl][Abl]
[/Adj|Attr][Pl.Poss.2Sg][Abl]
[/Adj|Pro][Pl][Abl]
[/Adj|Pred][Pl][Abl]
[/Adj][_Comp/Adj][Pl][Abl][Punct]
[/Adj|Attr|Pro][Pl][Abl]
[/Adj|Unit][[Pl][Abl]
[/Adj|col][Pl][Abl]
[/Adj|nat][Pl][Abl]
[/Adj][Pl][AnP][Abl]
[/Det|Pro][Pl][Abl]
[/Adj][Pl.Poss.1Pl][Abl]
[/Adj][Pl.Poss.2Sg][Abl
[/Adj][Pl.Poss.3Sg][Abl]
[/Adj][Pl.Poss.3Sg][Abl][Punct]
[/Adj][Pl.Poss.1Sg][Abl][Punct]
[/N][Farm.Pl][Abl]
[/Adj][Poss.1Sg][Fam.Pl][AnP][Abl]
[/Adj|Pro][Pl][AnP][Abl]
[/N][Fam.Pl][Abl]
[/N][Pl][Abl]
[/N][Pl][Abl][Punct]
[/N][Pl][AnP][Abl]
[/N][Pl.Poss.1Sg][Abl]
[/N][Pl.Poss.1Sg][Abl][Punct]
[/N][Pl.Poss.1Pl][Abl]
[/N][Pl.Poss.2Pl][Abl]
[/N][Pl.Poss.2Sg][Abl]
[/N][Pl.Poss.2Sg][Abl][Punct]
[/N][Pl.Poss.3Pl][Abl]
[/N][Pl.Poss.3Pl][Abl][Punct]
[/N][Pl.Poss.3Sg][Abl]
[/N][Pl.Poss.3Sg][Abl][Punct]
[/N][Poss.1Sg][Fam.Pl][Abl]

[/N][Pl][Ade]:
[/Supl][/Adj][_Comp/Adj][Pl.Poss.3Sg][Ade]
[/Supl][/Adj][_Comp/Adj][Pl][Ade]
[/Adj][_Comp/Adj][Pl][Ade]
[/Adj][Pl][Ade]
[/Adj|Attr][Pl.Poss.1Pl][Ade][Punct]
[/Adj|Pro][Pl][Ade]
[/Adj|Pred][Pl][Ade]
[/Adj|Attr|Pro][Pl][Ade]
[/Adj|Unit][[Pl][Ade]
[/Adj|col][Pl][Ade]
[/Adj|nat][Pl][Ade]
[/Adj][Pl][Ade]
[/Adj][Pl][AnP][Ade]
[/Det|Pro][Pl][Ade]
[/Adj][Pl.Poss.1Sg][Ade]
[/N][Farm.Pl][Ade]
[/N][Fam.Pl][Ade]
[/N][Pl][Ade]
[/N][Pl][Ade][Punct]
[/N][Pl][AnP][Ade]
[/N][Pl.Poss.1Pl][Ade]
[/N][Pl.Poss.1Sg][Ade]
[/N][Pl.Poss.3Pl][Ade]
[/N][Pl.Poss.2Sg][Ade]
[/N][Pl.Poss.2Pl][Ade]
[/N][Pl.Poss.3Sg][Ade]
[/N][Poss.1Sg][Fam.Pl][Ade]

[/N][Pl][All]:
[/Supl][/Adj][_Comp/Adj][Pl.Poss.3Sg][All]
[/Supl][/Adj][_Comp/Adj][Pl][All]
[/Adj][_Comp/Adj][Pl][All]
[/Adj][Pl][All]
[/Adj|Pro][Pl][All]
[/Adj|Pred][Pl][All]
[/Adj|Attr|Pro][Pl][All]
[/Adj|Unit][[Pl][All]
[/Adj|col][Pl][All]
[/Adj|nat][Pl][All]
[/Adj][Pl][All]
[/Adj][Pl][All][Punct]
[/Adj][Pl][AnP][All]
[/Det|Pro][Pl][All]
[/Adj][Pl.Poss.1Pl][All]
[/Adj][Pl.Poss.1Sg][All]
[/Adj][Pl.Poss.3Pl][All]
[/Adj][Pl.Poss.3Sg][All]
[/N][Farm.Pl][All]
[/Adj|Pro][Pl][All]
[/Adj|Pro][Pl][AnP][All]
[/N|Acron][Pl][All]
[/N][Fam.Pl][All]
[/N][Fam.Pl][AnP][All]
[/N][AnP.Pl][All]
[/N][Pl][AnP][All]
[/N][Pl][All]
[/N][Pl][All][Hyph:Slash]
[/N][Pl][All][Punct]
[/N][Pl.Poss.1Pl][All]
[/N][Pl.Poss.1Pl][All][Punct]
[/N][Pl.Poss.1Sg][All]
[/N][Pl.Poss.2Pl][All]
[/N][Pl.Poss.2Sg][All]
[/N][Pl.Poss.3Pl][All]
[/N][Pl.Poss.3Pl][All][Punct]
[/N][Pl.Poss.3Sg][All]
[/N][Pl.Poss.3Sg][All][Punct]
[/N][Poss.1Sg][Fam.Pl][All]
[/N][Poss.3Sg][Fam.Pl][All]

[/N][Pl][Cau]:
[/Adj][_Comp/Adj][Pl][Cau]
[/Adj][Pl][Cau]
[/Adj|Pro][Pl][Cau]
[/Adj|Pred][Pl][Cau]
[/Adj|Attr|Pro][Pl][Cau]
[/Adj|Unit][[Pl][Cau]
[/Adj|col][Pl][Cau]
[/Adj|nat][Pl][Cau]
[/Adj][Pl][Cau]
[/Det|Pro][Pl][Cau]
[/Adj][Pl.Poss.1Pl][Cau]
[/Adj][Pl.Poss.3Pl][Cau]
[/Adj][Pl.Poss.3Sg][Cau]
[/N][Farm.Pl][Cau]
[/Adj|Pro][Pl][Cau]
[/N][Fam.Pl][Cau]
[/N][Pl][AnP][Cau]
[/N][Pl][Cau]
[/N][Pl][Cau][Punct]
[/N][Pl.Poss.1Sg][Cau]
[/N][Pl.Poss.1Pl][Cau]
[/N][Pl.Poss.1Pl][Cau][Punct]
[/N][Pl.Poss.2Pl][Cau]
[/N][Pl.Poss.2Sg][Cau]
[/N][Pl.Poss.3Pl][Cau]
[/N][Pl.Poss.3Sg][Cau][Punct]
[/N][Pl.Poss.3Sg][Cau]
[/N][Pl.Poss.3Pl][Cau][Punct]
[/Supl][/Adj][_Comp/Adj][Pl][Cau]


[/N][Pl][Del]:
[/Supl][/Adj][_Comp/Adj][Pl][Del]
[/Adj][_Comp/Adj][Pl][Del]
[/Adj][Pl][Del]
[/Adj|Attr][Pl.Poss.3Sg][Del]
[/Adj|Pro][Pl][Del]
[/Adj|Pred][Pl][Del]
[/Adj|Attr|Pro][Pl][Del]
[/Adj|Unit][[Pl][Del]
[/Adj|col][Pl][Del]
[/Adj|nat][Pl][Del]
[/Adj][Pl][AnP][Del]
[/Adj][Pl][Del]
[/Adj][Pl][Del][Punct]
[/Det|Pro][Pl][Del]
[/Adj][Pl.Poss.1Pl][Del]
[/Adj][Pl.Poss.1Sg][Del]
[/Adj][Pl.Poss.3Pl][Del]
[/Adj][Pl.Poss.3Sg][Del]
[/Adj][Pl.Poss.2Sg][Del]
[/N][Farm.Pl][Del]
[/Adj|Pro][Pl][AnP][Del]
[/Adj|Pro][Pl][Del]
[/N][AnP.Pl][Del]
[/N][Fam.Pl][Del]
[/N][Pl][AnP][Del]
[/N][Pl.Poss.1Sg][Del]
[/N][Pl.Poss.1Sg][Del][Punct]
[/N][Pl][Del]
[/N][Pl][Del][Punct]
[/N][Pl.Poss.1Pl][Del]
[/N][Pl.Poss.1Pl][Del][Punct]
[/N][Pl.Poss.2Pl][Del]
[/N][Pl.Poss.2Sg][Del]
[/N][Pl.Poss.3Pl][Del]
[/N][Pl.Poss.3Pl][Del][Punct]
[/N][Pl.Poss.3Sg][Del]
[/N][Pl.Poss.3Sg][Del][Punct]
[/N][Poss.1Sg][Fam.Pl][Del]

[/N][Pl][EssFor:képp]:
[/Adj][_Comp/Adj][Pl][EssFor:képp]
[/Adj][Pl][EssFor:képp]
[/Adj|Pro][Pl][EssFor:képp]
[/Adj|Pred][Pl][EssFor:képp]
[/Adj|Attr|Pro][Pl][EssFor:képp]
[/Adj|Unit][[Pl][EssFor:képp]
[/Adj|col][Pl][EssFor:képp]
[/Adj|nat][Pl][EssFor:képp]
[/Det|Pro][Pl][EssFor:képp]
[/N][Farm.Pl][EssFor:képp]

[/N][Pl][EssFor:képpen]:
[/Adj][_Comp/Adj][Pl][EssFor:képpen]
[/Adj][Pl][EssFor:képpen]
[/Adj|Pro][Pl][EssFor:képpen]
[/Adj|Pred][Pl][EssFor:képpen]
[/Adj|Attr|Pro][Pl][EssFor:képpen]
[/Adj|Unit][[Pl][EssFor:képpen]
[/Adj|col][Pl][EssFor:képpen]
[/Adj|nat][Pl][EssFor:képpen]
[/Det|Pro][Pl][EssFor:képpen]
[/N][Farm.Pl][EssFor:képpen]

[/N][Pl][Ess]:
[/Adj][_Comp/Adj][Pl][Ess]
[/Adj][Pl][Ess]
[/Adj|Pro][Pl][Ess]
[/Adj|Pred][Pl][Ess]
[/Adj|Attr|Pro][Pl][Ess]
[/Adj|Unit][[Pl][Ess]
[/Adj|col][Pl][Ess]
[/Adj|nat][Pl][Ess]
[/Det|Pro][Pl][Ess]
[/N][Farm.Pl][Ess]
[/N][Pl.Poss.1Pl][Ess]
[/N][Pl][Ess]
[/N][Pl.Poss.3Pl][Ess]
[/N][Pl.Poss.3Sg][Ess]


[/N][Pl][Ine]:
[/Adj][_Comp/Adj][Pl][Ine]
[/Adj][Pl][Ine]
[/Adj|Pro][Pl][Ine]
[/Adj|Pred][Pl][Ine]
[/Adj|Attr|Pro][Pl][Ine]
[/Adj][_Comp/Adj][Pl][Ine][Punct]
[/Adj|Unit][[Pl][Ine]
[/Adj|col][Pl][Ine]
[/Adj][Fam.Pl][Ine]
[/Adj|nat][Pl][Ine]
[/Adj][Pl][Ine]
[/Adj][Pl][Ine][Punct]
[/Det|Pro][Pl][Ine]
[/N][Farm.Pl][Ine]
[/Adj|Pro][Pl][Ine]
[/Adj|Pro][Pl][Ine][Punct]
[/N|Acron][Pl][Ine]
[/N][AnP.Pl][Ine]
[/N][Fam.Pl][Ine]
[/N][Pl][AnP][Ine]
[/N][Pl][Ine]
[/N][Pl][Ine][Hyph:Slash]
[/N][Pl][Ine][Punct]
[/N][Pl.Poss.1Sg][Ine]
[/N][Pl.Poss.1Sg][Ine][Punct]
[/N][Pl.Poss.1Pl][Ine]
[/N][Pl.Poss.1Pl][Ine][Punct]
[/N][Pl.Poss.2Pl][Ine]
[/N][Pl.Poss.2Sg][Ine]
[/N][Pl.Poss.2Sg][Ine][Punct]
[/N][Pl.Poss.3Pl][Ine]
[/N][Pl.Poss.3Pl][Ine][Punct]
[/N][Pl.Poss.3Sg][Ine][Punct]
[/N][Pl.Poss.3Sg][Ine]
[/N][Poss.2Sg][Fam.Pl][Ine]
[/Supl][/Adj][_Comp/Adj][Pl][Ine]
[/Supl][/Adj][_Comp/Adj][Pl.Poss.1Pl][Ine]

[/N][Pl][Ins]:
[/Supl][/Adj][_Comp/Adj][Pl.Poss.2Pl][Ins]
[/Supl][/Adj][_Comp/Adj][Pl.Poss.3Sg][Ins]
[/Supl][/Adj][_Comp/Adj][Pl.Poss.3Pl][Ins]
[/Supl][/Adj][_Comp/Adj][Pl][Ins]
[/Supl][/Adj][_Comp/Adj][Pl][AnP][Ins]
[/Num][_Ord/Adj][Pl][Ins]
[/Adj][_Comp/Adj][Pl][Ins]
[/Adj][Pl][Ins]
[/Adj|Attr][Pl.Poss.3Sg][Ins][Punct]
[/Adj|Pro][Pl][Ins]
[/Adj|Pred][Pl][Ins]
[/Adj|Attr|Pro][Pl][Ins]
[/Adj][_Comp/Adj][Pl][Ins]
[/Adj][_Comp/Adj][Pl.Poss.3Sg][Ins]
[/Adj|Unit][[Pl][Ins]
[/Adj|col][Pl][Ins]
[/Adj][Fam.Pl][Ins]
[/Adj|nat][Pl][Ins]
[/Adj][Pl][AnP][Ins]
[/Adj][Pl][AnP][Ins][Punct]
[/Adj][Pl][Ins]
[/Adj][Pl][Ins][Punct]
[/Det|Pro][Pl][Ins]
[/Adj][Pl.Poss.1Pl][Ins]
[/Adj][Pl.Poss.1Pl][Ins][Punct]
[/Adj][Pl.Poss.1Sg][Ins]
[/Adj][Pl.Poss.3Pl][Ins]
[/Adj][Pl.Poss.3Pl][Ins][Punct]
[/Adj][Pl.Poss.3Sg][Ins]
[/Adj][Pl.Poss.3Sg][Ins][Hyph:Slash]
[/Adj][Pl.Poss.3Sg][Ins][Punct]
[/Adj][Pl.Poss.2Sg][Ins][Punct]
[/N][Farm.Pl][Ins]
[/Adj|Pro][Pl][Ins]
[/Adj|Pro][Pl][Ins][Punct]
[/Adj|Pro][Pl.Poss.1Pl][Ins]
[/Adj|Pro][Pl][AnP][Ins]
[/N][AnP.Pl][Ins]
[/N][Pl][AnP][Ins]
[/N][Pl][AnP.Pl][Ins]
[/N][Fam.Pl][Ins]
[/N][Fam.Pl][Ins][Punct]
[/N][Pl][Ins]
[/N][Pl][Ins][Hyph:Slash]
[/N][Pl][Ins][Punct]
[/N][Pl.Poss.1Pl][Ins]
[/N][Pl.Poss.1Pl][Ins][Punct]
[/N][Pl.Poss.1Sg][Ins]
[/N][Pl.Poss.1Sg][Ins][Punct]
[/N][Pl.Poss.2Pl][Ins]
[/N][Pl.Poss.2Sg][Ins]
[/N][Pl.Poss.2Sg][Ins][Punct]
[/N][Pl.Poss.3Pl][AnP][Ins]
[/N][Pl.Poss.3Pl][Ins][Hyph:Slash]
[/N][Pl.Poss.3Pl][Ins]
[/N][Pl.Poss.3Pl][Ins][Punct]
[/N][Pl.Poss.3Sg][Ins][Punct]
[/N][Pl.Poss.3Sg][Ins]
[/N][Poss.1Sg][Fam.Pl][Ins]

[/N][Pl][Loc]:
[/Adj][_Comp/Adj][Pl][Loc]
[/Adj][Pl][Loc]
[/Adj|Pro][Pl][Loc]
[/Adj|Pred][Pl][Loc]
[/Adj|Attr|Pro][Pl][Loc]
[/Adj|Unit][[Pl][Loc]
[/Adj|col][Pl][Loc]
[/Adj|nat][Pl][Loc]
[/Det|Pro][Pl][Loc]
[/N][Farm.Pl][Loc]

[/N][Pl][Supe]:
[/Supl][/Adj][_Comp/Adj][Pl][Supe]
[/Num][_Ord/Adj][Pl][AnP][Supe]
[/Adj][_Comp/Adj][Pl][Supe]
[/Adj][Pl][Supe]
[/Adj|Pro][Pl][Supe]
[/Adj|Pred][Pl][Supe]
[/Adj|Attr|Pro][Pl][Supe]
[/Adj][_Comp/Adj][Pl][Supe]
[/Adj|Unit][[Pl][Supe]
[/Adj|col][Pl][Supe]
[/Adj|nat][Pl][Supe]
[/Adj][Pl][AnP][Supe]
[/Det|Pro][Pl][Supe]
[/Adj][Pl.Poss.1Sg][Supe]
[/Adj][Pl.Poss.2Pl][Supe]
[/Adj][Pl.Poss.2Sg][Supe]
[/N][Farm.Pl][Supe]
[/Adj][Pl.Poss.3Sg][Supe]
[/Adj][Pl][Supe][Punct]
[/Adj|Pro][Pl][Supe][Punct]
[/Adj|Pro][Pl][Supe]
[/N][Fam.Pl][AnP][Supe]
[/N][AnP.Pl][Supe]
[/N][Pl][AnP][Supe]
[/N][Fam.Pl][Supe]
[/N][Fam.Pl][Supe][Punct]
[/N][Pl.Poss.1Pl][Supe]
[/N][Pl.Poss.1Pl][Supe][Punct]
[/N][Pl.Poss.1Sg][Supe]
[/N][Pl.Poss.1Sg][Supe][Punct]
[/N][Pl.Poss.2Pl][Supe]
[/N][Pl.Poss.2Sg][Supe]
[/N][Pl.Poss.3Pl][AnP][Supe]
[/N][Pl.Poss.3Pl][Supe]
[/N][Pl.Poss.3Pl][Supe][Punct]
[/N][Pl.Poss.3Sg][Supe]
[/N][Pl.Poss.3Sg][Supe][Punct]
[/N][Pl][Supe][Punct]
[/N][Pl][Supe]
[/N][Pl][Supe][Punct][Hyph:Slash]
[/N][Poss.1Sg][Fam.Pl][Supe]

[/N][Pl][Temp]:

[/Adj][_Comp/Adj][Pl][Temp]
[/Adj][Pl][Temp]
[/Adj|Pro][Pl][Temp]
[/Adj|Pred][Pl][Temp]
[/Adj|Attr|Pro][Pl][Temp]
[/Adj|Unit][[Pl][Temp]
[/Adj|col][Pl][Temp]
[/Adj|nat][Pl][Temp]
[/Det|Pro][Pl][Temp]
[/N][Farm.Pl][Temp]
[/N][Pl.Poss.1Pl][Temp]
[/N][Pl.Poss.3Sg][Temp]
[/N][Pl][Temp]
[/N][Pl][Temp][Punct]

[/N][Pl][Ter]:
[/Supl][/Adj][Pl][Ter]
[/Supl][/Adj][_Comp/Adj][Pl][Ter]
[/Adj][_Comp/Adj][Pl][Ter]
[/Adj][Pl][Ter]
[/Adj][AnP.Pl][Ter]
[/Adj][Pl][Ter]
[/Adj|Pro][Pl][Ter]
[/Adj|Pred][Pl][Ter]
[/Adj|Attr|Pro][Pl][Ter]
[/Adj][_Comp/Adj][Pl][Ter]
[/Adj|Unit][[Pl][Ter]
[/Adj|col][Pl][Ter]
[/Adj|nat][Pl][Ter]
[/Det|Pro][Pl][Ter]
[/Adj][Pl.Poss.2Sg][AnP][Ter]
[/N][Farm.Pl][Ter]
[/Adj][Pl][Ter][Punct]
[/Adj|Pro][Pl][Ter]
[/N][Pl.Poss.1Pl][Ter]
[/N][Pl.Poss.2Sg][Ter]
[/N][Pl.Poss.1Sg][Ter]
[/N][Pl.Poss.3Sg][Ter]
[/N][Pl.Poss.3Pl][Ter]
[/N][Pl][Ter]
[/N][Pl][Ter][Punct]

[/Adj|Pro|Int][Acc]:
[/Adj|Pro|Int][Poss.1Pl][Acc][Punct]
[/Adj|Pro|Int][Poss.1Pl][AnP][Acc]
[/Adj|Pro|Int][Poss.1Sg][Acc]
[/Adj|Pro|Int][AnP][Acc]


[/Adj|Pro|Int][Pl][Nom]:
[/Adj|Pro|Int][Pl][Nom][Punct]
[/Adj|Pro|Int][Pl.Poss.3Sg][Nom]
[/Adj|Pro|Rel][Pl][AnP][Nom]

[/Adj|Pro|Int][Pl][Supe]:
[/Adj|Pro|Int][Pl][AnP][Supe]

[/Adj|Pro|Int][Pl][Acc]:
[/Adj|Pro|Int][Pl][AnP][Acc]
[/Adj|Pro|Rel][Pl][Acc]

[/Adj|Pro|Int][Nom]:
[/Adj|Pro|Int][Nom][Punct]
[/Adj|Pro|Int][Poss.1Sg][Nom]
[/Adj|Pro|Int][Poss.2Sg][Nom]
[/Adj|Pro|Rel][Nom][Punct]

[/Adj|Pro|Int][Ins]:
[/Adj|Pro|Int][Poss.2Sg][Ins]

[/Adj|Pro|Rel][Nom]:
[/Adj|Pro|Rel][AnP][Nom]
[/Adj|Attr|Pro|Rel][Nom]

[/Adv]:
[/Adv]
[/Adv|Abbr]
[/Adv|Abbr][Punct]
[/Adv|Acronx]
[/Adv][Hyph:Hyph]
[/Adv][Hyph:Slash]
[/Adv][Nom]
[/Adv|Pro][Hyph:Slash]
[/Adv][Punct]
[/Adv][Punct][Hyph:Slash]
[/Adv][Punct][Punct]

[/Adv|Pro][1Sg]:
[/Adv|Pro][1Sg][Punct]

[/Adv|Pro][2Sg]:
[/Adv|Pro][2Sg][Punct]

[/Adv|Pro|Int]:
[/Adv|Pro|Int][Punct]

[/CmpdPfx]:
[/CmpdPfx][Hyph:Hyph]
[/CmpdPfx][Hyph:Slash]

[/Det|Art.Def]:
[/Det|Art.Def][Punct]

[/Det|Pro][Abl]:
[/Det|Pro][Abl][Punct]

[/Det|Pro][Acc]:
[/Det|Pro][Acc][Hyph:Slash]
[/Det|Pro][Acc][Punct]

[/Det|Pro][All]:
[/Det|Pro][All][Punct]

[/Det|Pro][Cau]:
[/Det|Pro][AnP][Cau]
[/Det|Pro][Cau][Punct]

[/Det|Pro][Nom]:
[/Det|Pro][AnP][Nom]
[/Det|Pro][Nom][Punct]
[/Det|Pro][Punct]

[/Det|Pro][Subl]:
[/Det|Pro][AnP][Subl]

[/Det|Pro][Dat]:
[/Det|Pro][Dat][Hyph:Slash]
[/Det|Pro][Dat][Punct]

[/Det|Pro|def]:
[/Det|Pro|def][Hyph:Slash]
[/Det|Pro|def][Punct]

[/Det|Pro][Del]:
[/Det|Pro][Del][Punct]

[/Det|Pro][Ela]:
[/Det|Pro][Ela][Punct]

[/Det|Pro][Ill]:
[/Det|Pro][Ill][Punct]

[/Det|Pro][Subl]:
[/Det|Pro][Subl][Punct]

[/Det|Pro][Ins]:
[/Det|Pro][Ins][Punct]

[/Det|Pro][Supe]:
[/Det|Pro][Supe][Punct]

[/Det|Pro][Pl][Acc]:
[/Det|Pro][Pl][Acc][Punct]
[/Det|Pro][Pl][AnP][Acc]

[/Det|Pro][Pl][Del]:
[/Det|Pro][Pl][AnP][Del]

[/Det|Pro][Pl][Nom]:
[/Det|Pro][Pl][AnP][Nom]
[/Det|Pro][Pl][Nom][Punct]

[/Det|Pro][Pl][Subl]:
[/Det|Pro][Pl][AnP][Subl]
[/Det|Pro][Pl][Subl][Punct]

[/Det|Pro][Pl][Dat]:
[/Det|Pro][Pl][Dat][Punct]

[/Det|Pro][Pl][Del]:
[/Det|Pro][Pl][Del][Punct]

[/Det|Pro][Pl][Ela]:
[/Det|Pro][Pl][Ela][Punct]

[/Det|Pro][Pl][Ine]:
[/Det|Pro][Pl][Ine][Punct]

[/Det|Pro][Pl][Ins]:
[/Det|Pro][Pl][Ins][Punct]

[/Det|Pro][Pl][Supe]:
[/Det|Pro][Pl][Supe][Punct]

[/Det|Pro|Rel]:
[/Det|Pro|Rel][Punct]


[/Det|Pro|(Post)]:
[/Det|Pro|(Post)][Hyph:Slash]
[/N|Pro|(Post)][Nom][Hyph:Slash]

[/Post]:
[/Supl][/Post|(Abl)][_Comp/Post|(Abl)][Del]
[/Supl][/Post|(Abl)][_Comp/Post|(Abl)][Subl]
[/Supl][/Post|(All)][_Comp/Post|(All)][Subl]
[/Post][1Pl]
[/Post][1Pl][Punct]
[/Post][1Sg]
[/Post][1Sg][Hyph:Slash]
[/Post][1Sg][Punct]
[/Post][2Pl]
[/Post][2Pl][Punct]
[/Post][2Sg]
[/Post][2Sg][Punct]
[/Post][3Pl]
[/Post][3Pl][Punct]
[/Post][3Sg]
[/Post][3Sg][Hyph:Slash]
[/Post][3Sg][Punct]
[/Post][Abl]
[/Post|(Abl)]
[/Post|(All)]
[/Post][Del]
[/Post|(Ela)]
[/Post][Hyph:Hyph]
[/Post][Hyph:Slash]
[/Post][Ine]
[/Post|(Ins)]
[/Post|(Poss)]
[/Post|(Poss)][Poss.1Pl][Punct]
[/Post|(Poss)][Poss.1Sg][Punct]
[/Post|(Poss)][Poss.2Pl]
[/Post|(Poss)][Poss.2Pl][Punct]
[/Post|(Poss)][Poss.2Sg][Punct]
[/Post|(Poss)][Poss.3Pl][Punct]
[/Post|(Poss)][Poss.3Sg]
[/Post|(Poss)][Poss.3Sg][Hyph:Slash]
[/Post|(Poss)][Poss.3Sg][Punct]
[/Post|(Poss)][Prs.NDef.1Pl]
[/Post|(Poss)][Prs.NDef.1Sg]
[/Post|(Poss)][Prs.NDef.2Pl]
[/Post|(Poss)][Prs.NDef.2Sg]
[/Post|(Poss)][Prs.NDef.3Pl]
[/Post|(Poss)][Prs.NDef.3Sg]
[/Post|(Poss)][Prs.NDef.3Sg][Punct]
[/Post|(Poss)][Punct]
[/Post|(Poss)][Punct][Hyph:Slash]
[/Post][Punct]
[/Post][Subl]
[/Post|(Subl)]
[/Post|(Supe)]
[/Post|(Supe)][1Sg]
[/Post|(Supe)][2Sg]
[/Post|(Supe)][3Pl]
[/Post|(Supe)][3Sg]
[/Post|(Supe)][Del]
[/Post|(Supe)][Punct]
[/Post|(Supe)][Subl]
[/Post][Ter]

[Hyph:Slash]:
[Hyph:Slash][Punct]

[/Inj-Utt]:
[/Inj-Utt][Hyph:Slash]
[/Inj-Utt][Punct]
[/Inj-Utt][QPtcl]

[/Det|Q]:
[/Det|Q.NDef][Punct]

[/N|Pro][1Pl][Abl]:
[/N|Pro][1Pl][Abl][Punct]

[/N|Pro][1][Pl][Acc]:
[/N|Pro][1][Pl][Acc][Punct]

[/N|Pro][1Pl][Acc]:
[/N|Pro][1Pl][Acc][Punct]
[/N|Pro][1Pl][AnP][Acc]

[/N|Pro][1Pl][Dat]:
[/N|Pro][1Pl][AnP][Dat]

[/N|Pro][1Pl][Ela]:
[/N|Pro][1Pl][AnP][Ela]

[/N|Pro][1Pl][Ill]:
[/N|Pro][1Pl][AnP][Ill]

[/N|Pro][1Pl][Ins]:
[/N|Pro][1Pl][AnP][Ins]
[/N|Pro][1Pl][Ins][Punct]

[/N|Pro][1Pl][Transl]:
[/N|Pro][1Pl][AnP][Transl]

[/N|Pro][1Pl][All]:
[/N|Pro][1Pl][All][Punct]

[/N|Pro][1Pl][Dat]:
[/N|Pro][1Pl][Dat][Punct]

[/N|Pro][1Pl][Nom]:
[/N|Pro][1Pl][Nom][Punct]

[/N|Pro][1Sg][Acc]:
[/N|Pro][1Sg][Acc][Punct]
[/N|Pro][1Sg][AnP][Acc]

[/N|Pro][1Sg][Pl][Acc]:
[/N|Pro][1Sg][AnP.Pl][Acc]

[/N|Pro][1Sg][Pl][Transl]:
[/N|Pro][1Sg][AnP.Pl][Transl]

[/N|Pro][1Sg][All]:
[/N|Pro][1Sg][AnP][All]

[/N|Pro][1Sg][AnP][Dat]:
[/N|Pro][1Sg][Dat]

[/N|Pro][1Sg][Del]:
[/N|Pro][1Sg][AnP][Del]

[/N|Pro][1Sg][Supe]:
[/N|Pro][1Sg][AnP][Supe]
[/N|Pro][1Sg][Supe][Punct]

[/N|Pro][1Sg][Ela]:
[/N|Pro][1Sg][AnP][Ela]

[/N|Pro][1Sg][Ill]:
[/N|Pro][1Sg][AnP][Ill]

[/N|Pro][1Sg][Ine]:
[/N|Pro][1Sg][AnP][Ine]

[/N|Pro][1Sg][Ins]:
[/N|Pro][1Sg][AnP][Ins]

[/N|Pro][1Sg][Nom]:
[/N|Pro][1Sg][AnP][Nom]
[/N|Pro][1Sg][Nom][Punct]

[/N|Pro][1Sg][Transl]:
[/N|Pro][1Sg][AnP][Transl]

[/N|Pro][1Sg][Cau]:
[/N|Pro][1Sg][Cau][Punct]

[/N|Pro][1Sg][Dat]:
[/N|Pro][1Sg][Dat][Punct]

[/N|Pro][1Sg][Del]:
[/N|Pro][1Sg][Del][Punct]

[/N|Pro][1Sg][Ela]:
[/N|Pro][1Sg][Ela][Punct]

[/N|Pro][1Sg][Ine]:
[/N|Pro][1Sg][Ine][Punct]

[/N|Pro][1Sg][Ins]:
[/N|Pro][1Sg][Ins][Punct]

[/N|Pro][1Sg][Subl]:
[/N|Pro][1Sg][Subl][Punct]

[/N|Pro][2][Pl][Acc]:
[/N|Pro][2][Pl][Acc][Punct]

[/N|Pro][2Pl][Acc]:
[/N|Pro][2Pl][Acc][Punct]
[/N|Pro][2Pl][AnP][Acc]

[/N|Pro][2Pl][Dat]:
[/N|Pro][2Pl][AnP][Dat]

[/N|Pro][2Pl][Transl]:
[/N|Pro][2Pl][AnP][Transl]

[/N|Pro][2Pl][Ins]:
[/N|Pro][2Pl][Ins][Punct]

[/N|Pro][2Pl][Subl]:
[/N|Pro][2Pl][Subl][Punct]

[/N|Pro][2Sg][Acc]:
[/N|Pro][2Sg][Acc][Punct]
[/N|Pro][2Sg][AnP][Acc]

[/N|Pro][2Sg][Dat]:
[/N|Pro][2Sg][AnP][Dat]
[/N|Pro][2Sg][Dat][Punct]

[/N|Pro][2Sg][Nom]:
[/N|Pro][2Sg][AnP][Nom][Punct]
[/N|Pro][2Sg][Nom][Hyph:Slash]
[/N|Pro][2Sg][Nom][Punct]

[/N|Pro][2Sg][Transl]:
[/N|Pro][2Sg][AnP][Transl]

[/N|Pro][2Sg][Del]:
[/N|Pro][2Sg][Del][Punct]

[/N|Pro][2Sg][Ine]:
[/N|Pro][2Sg][Ine][Punct]

[/N|Pro][2Sg][Ins]:
[/N|Pro][2Sg][Ins][Punct]

[/N|Pro][2Sg][Supe]:
[/N|Pro][2Sg][Supe][Punct]

[/N|Pro][3Pl][Acc]:
[/N|Pro][3Pl][Acc][Hyph:Slash]
[/N|Pro][3Pl][Acc][Punct]

[/N|Pro][3Pl][AnP][Acc]:
[/N|Pro][3Pl][AnP][Acc][Punct]

[/N|Pro][3Pl][Dat]:
[/N|Pro][3Pl][AnP][Dat]

[/N|Pro][3Pl][Ela]:
[/N|Pro][3Pl][AnP][Ela]

[/N|Pro][3Pl][Ins]:
[/N|Pro][3Pl][AnP][Ins]

[/N|Pro][3Pl][Nom]:
[/N|Pro][3Pl][AnP][Nom]

[/N|Pro][3Pl][Transl]:
[/N|Pro][3Pl][AnP][Transl]

[/N|Pro][3Pl][Cau]:
[/N|Pro][3Pl][Cau][Punct]

[/N|Pro][3Pl][Dat]:
[/N|Pro][3Pl][Dat][Punct]

[/N|Pro][3Pl][Del]:
[/N|Pro][3Pl][Del][Punct]

[/N|Pro][3Pl][Ela]:
[/N|Pro][3Pl][Ela][Punct]

[/N|Pro][3Pl][Ins]:
[/N|Pro][3Pl][Ins][Punct]

[/N|Pro][3Pl][Nom]:
[/N|Pro][3Pl][Nom][Punct]

[/N|Pro][3Pl][Subl]:
[/N|Pro][3Pl][Subl][Punct]

[/N|Pro][3Pl][Supe]:
[/N|Pro][3Pl][Supe][Punct]

[/N|Pro][3Sg][Acc]:
[/N|Pro][3Sg][Acc][Punct]
[/N|Pro][3][S][g][Acc]
[/N|Pro][3Sg][AnP][Acc]

[/N|Pro][3Sg][All]:
[/N|Pro][3Sg][All][Punct]

[/N|Pro][3Sg][Abl]:
[/N|Pro][3Sg][AnP][Abl]

[/N|Pro][3Sg][All]:
[/N|Pro][3Sg][AnP][All]

[/N|Pro][3Sg][Dat]:
[/N|Pro][3Sg][AnP][Dat]
[/N|Pro][3Sg][Dat][Hyph:Slash]
[/N|Pro][3Sg][Dat][Punct]

[/N|Pro][3Sg][Ela]:
[/N|Pro][3Sg][AnP][Ela]
[/N|Pro][3Sg][Ela][Punct]


[/N|Pro][3Sg][Ill]:
[/N|Pro][3Sg][AnP][Ill]

[/N|Pro][3Sg][Ine]:
[/N|Pro][3Sg][AnP][Ine]
[/N|Pro][3Sg][Ine][Punct]


[/N|Pro][3Sg][Ins]:
[/N|Pro][3Sg][AnP][Ins]
[/N|Pro][3Sg][Ins][Punct]


[/N|Pro][3Sg][Nom]:
[/N|Pro][3Sg][AnP][Nom]
[/N|Pro][3Sg][Nom]
[/N|Pro][3Sg][Nom][Punct]

[/N|Pro][3Sg][Subl]:
[/N|Pro][3Sg][AnP][Subl]

[/N|Pro][3Sg][Supe]:
[/N|Pro][3Sg][AnP][Supe]
[/N|Pro][3Sg][Supe][Punct]

[/N|Pro][3Sg][Transl]:
[/N|Pro][3Sg][AnP][Transl]

[/N|Pro][3Sg][Cau]:
[/N|Pro][3Sg][Cau][Punct]

[/N|Pro][3Sg][Del]:
[/N|Pro][3Sg][Del][Punct]

[/N|Pro][Nom]:
[/N|Pro|Abbr][Nom][]
[/N|Pro][Nom][Hyph:Hyph]
[/N|Pro][Nom][Hyph:Slash]
[/N|Pro][Nom][Punct]
[/N|Pro][Nom][Punct][Punct]
[/N|Pro][Poss.1Pl][Nom]
[/N|Pro][Poss.1Sg][Nom]
[/N|Pro][Poss.1Sg][Nom][Punct]
[/N|Pro][Poss.2Pl][Nom]
[/N|Pro][Poss.2Sg][Nom]
[/N|Pro][Poss.3Pl][Nom]
[/N|Pro][Poss.3Sg][Nom]


[/N|Pro][Abl]:
[/N|Pro][Abl][Punct]
[/N|Pro][Poss.2Pl][Abl]
[/N|Pro][Poss.3Sg][Abl]

[/N|Pro][Acc]:
[/N|Pro][Acc][Punct]
[/N|Pro][Poss.1Sg][Acc]
[/N|Pro][Poss.2Pl][Acc]
[/N|Pro][Poss.2Sg][Acc]
[/N|Pro][Poss.3Pl][Acc][Punct]
[/N|Pro][Poss.3Sg][Acc]


[/N|Pro][Abl][1Pl]:
[/N|Pro][Abl][1Pl][Punct]

[/N|Pro][Abl][1Sg]:
[/N|Pro][Abl][1Sg][Punct]

[/N|Pro][Abl][2Pl]:
[/N|Pro][Abl][2Pl][Punct]

[/N|Pro][Abl][2Sg]:
[/N|Pro][Abl][2Sg][Punct]

[/N|Pro][Abl][3Pl]:
[/N|Pro][Abl][3Pl][Punct]

[/N|Pro][Abl][3Sg]:
[/N|Pro][Abl][3Sg][Punct]

[/N|Pro][Ade][1Pl]:
[/N|Pro][Ade][1Pl][Punct]

[/N|Pro][Ade][1Sg]:
[/N|Pro][Ade][1Sg][Punct]

[/N|Pro][Ade][2Sg]:
[/N|Pro][Ade][2Sg][Punct]

[/N|Pro][Ade][3Pl]:
[/N|Pro][Ade][3Pl][Punct]

[/N|Pro][Ade][3Sg]:
[/N|Pro][Ade][3Sg][Punct]

[/N|Pro][Ade]:
[/N|Pro][Ade][Punct]

[/N|Pro][All][1Pl]:
[/N|Pro][All][1Pl][Punct]

[/N|Pro][All][1Sg]:
[/N|Pro][All][1Sg][Punct]

[/N|Pro][All][2Pl]:
[/N|Pro][All][2Pl][Punct]

[/N|Pro][All][2Sg]:
[/N|Pro][All][2Sg][Punct]

[/N|Pro][All][3Pl]:
[/N|Pro][All][3Pl][Punct]

[/N|Pro][All]:
[/N|Pro][All][Punct]
[/N|Pro][Poss.3Sg][All]

[/N|Pro][AnP][1Sg][Acc]:
[/N|Pro][AnP][1Sg][Acc][Hyph:Slash]
[/N|Pro][AnP][1Sg][Acc][Punct]

[/N|Pro][AnP][1Sg][Ade]:
[/N|Pro][AnP][1Sg][Ade][Punct]

[/N|Pro][AnP][2Sg][Acc]:
[/N|Pro][AnP][2Sg][Acc][Hyph:Slash]

[/N|Pro][AnP][2Sg][Nom]:
[/N|Pro][AnP][2Sg][Nom][Punct]

[/N|Pro][AnP][3Pl][Nom]:
[/N|Pro][AnP][3Pl][Nom][Punct]

[/N|Pro][AnP.Pl][1Pl][Acc]:
[/N|Pro][AnP.Pl][1Pl][Acc][Punct]

[/N|Pro][Cau][3Sg]:
[/N|Pro][Cau][3Sg][Punct][Hyph:Slash]

[/N|Pro][Cau]:
[/N|Pro][Cau][Punct]
[/N|Pro][Poss.1Sg][Cau]


[/N|Pro][Dat][1Pl]:
[/N|Pro][Dat][1Pl][Punct]

[/N|Pro][Dat][1Sg]:
[/N|Pro][Dat][1Sg][Punct]

[/N|Pro][Dat][2Pl]:
[/N|Pro][Dat][2Pl][Punct]

[/N|Pro][Dat][2Sg]:
[/N|Pro][Dat][2Sg][Punct]

[/N|Pro][Dat][3Pl][Punct]:
[/N|Pro][Dat][3Pl]

[/N|Pro][Dat]:
[/N|Pro][Poss.1Sg][Dat]
[/N|Pro][Dat][Punct]
[/N|Pro][Poss.2Sg][Dat]
[/N|Pro][Poss.3Sg][Dat]
[/N|Pro][Poss.3Pl][Dat]


[/N|Pro][Del][1Pl]:
[/N|Pro][Del][1Pl][Punct]

[/N|Pro][Del][1Sg]:
[/N|Pro][Del][1Sg][Punct]

[/N|Pro][Del][2Sg]:
[/N|Pro][Del][2Sg][Punct]

[/N|Pro][Del][3Pl]:
[/N|Pro][Del][3Pl][Punct]

[/N|Pro][Del][3Sg]:
[/N|Pro][Del][3Sg][Hyph:Slash]
[/N|Pro][Del][3Sg][Punct]

[/N|Pro][Del]:
[/N|Pro][Del][Punct]
[/N|Pro][Poss.3Sg][Del]

[/N|Pro][Ela][1Pl]:
[/N|Pro][Ela][1Pl][Punct]

[/N|Pro][Ela][1Sg]:
[/N|Pro][Ela][1Sg][Punct]

[/N|Pro][Ela][3Pl]:
[/N|Pro][Ela][3Pl][Punct]

[/N|Pro][Ela][3Sg]:
[/N|Pro][Ela][3Sg][Hyph:Slash]
[/N|Pro][Ela][3Sg][Punct]

[/N|Pro][Ela]:
[/N|Pro][Ela][Punct]
[/N|Pro][Poss.1Pl][Ela]
[/N|Pro][Poss.3Sg][Ela]
[/N|Pro][Poss.1Sg][Ela]
[/N|Pro][Poss.2Sg][Ela]

[/N|Pro][Ill]:
[/N|Pro][Poss.2Sg][Ill]
[/N|Pro][Poss.3Sg][Ill]


[/N|Pro][Ine][1Pl]:
[/N|Pro][Ine][1Pl][Punct]

[/N|Pro][Ine][1Sg]:
[/N|Pro][Ine][1Sg][Punct]

[/N|Pro][Ine][2Sg]:
[/N|Pro][Ine][2Sg][Punct]

[/N|Pro][Ine][3Pl]:
[/N|Pro][Ine][3Pl][Punct]

[/N|Pro][Ine][3Sg]:
[/N|Pro][Ine][3Sg][Hyph:Slash]
[/N|Pro][Ine][3Sg][Punct]
[/N|Pro][Ine][3Sg][Punct][Hyph:Slash]

[/N|Pro][Ine]:
[/N|Pro][Ine][Punct]
[/N|Pro][Poss.1Sg][Ine]
[/N|Pro][Poss.3Sg][Ine]

[/N|Pro][Ins][1Pl]:
[/N|Pro][Ins][1Pl][Punct]

[/N|Pro][Ins][1Sg]:
[/N|Pro][Ins][1Sg][Punct]

[/N|Pro][Ins][2Pl]:
[/N|Pro][Ins][2Pl][Punct]

[/N|Pro][Ins][2Sg]:
[/N|Pro][Ins][2Sg][Punct]
[/N|Pro][Ins][2Sg][Punct][Hyph:Slash]

[/N|Pro][Ins][3Pl]:
[/N|Pro][Ins][3Pl][Punct]

[/N|Pro][Ins][3Sg]:
[/N|Pro][Ins][3Sg][Punct]

[/N|Pro][Ins]:
[/N|Pro][Ins][Punct]
[/N|Pro][Poss.2Pl][Ins]
[/N|Pro][Poss.2Sg][Ins]
[/N|Pro][Poss.3Pl][Ins]
[/N|Pro][Poss.3Sg][Ins]

[/N|Pro|Int][Acc]:
[/N|Pro|Int][Acc][Hyph:Slash]
[/N|Pro|Int][Acc][Punct][Punct]

[/N|Pro|Int][Cau]:
[/N|Pro|Int][Cau][Hyph:Slash]

[/N|Pro|Int][Ela]:
[/N|Pro|Int][Ela][Hyph:Slash]
[/N|Pro|Int][Ela][Punct]

[/N|Pro|Int][Ine]:
[/N|Pro|Int][Ine][Punct]

[/N|Pro|Int][Nom]:
[/N|Pro|Int][Nom][Hyph:Hyph]
[/N|Pro|Int][Nom][Punct]

[/N|Pro|Int][Poss.1Pl][Acc]:
[/N|Pro|Int][Poss.1Pl][Acc][Punct]

[/N|Pro][Pl][Abl]:
[/N|Pro][Pl][Abl][Punct]

[/N|Pro][Pl][Acc]:
[/N|Pro][Pl][Acc][Punct]
[/N|Pro][Poss.3Sg][Fam.Pl][Acc]

[/N|Pro][Pl][Ade]:
[/N|Pro][Pl][Ade][Punct]

[/N|Pro][Pl][All][Punct]:
[/N|Pro][Pl][All]

[/N|Pro][Pl][Cau]:
[/N|Pro][Pl][Cau][Punct]


[/N|Pro][Pl][Dat]:
[/N|Pro][Pl][Dat][Hyph:Slash]

[/N|Pro][Pl][Dat]:
[/N|Pro][Pl][Dat][Punct]

[/N|Pro][Pl][Del]:
[/N|Pro][Pl][Del][Punct]

[/N|Pro][Pl][Ela]:
[/N|Pro][Pl][Ela][Punct]

[/N|Pro][Pl][Ine]:
[/N|Pro][Pl][Ine][Punct]

[/N|Pro][Pl][Ins]:
[/N|Pro][Pl][Ins][Punct]

[/N|Pro][Pl][Nom]:
[/N|Pro][Pl.Poss.1Pl][Nom]
[/N|Pro][Pl][Nom][Hyph:Slash]
[/N|Pro][Pl][Nom][Punct]
[/N|Pro][Poss.3Sg][Fam.Pl][Nom]

[/N|Pro][Ade]:
[/N|Pro][Poss.1Pl][Ade]
[/N|Pro][Poss.2Sg][Ade]
[/N|Pro][Poss.3Sg][Ade]


[/N|Pro][Pl][Subl]:
[/N|Pro][Pl][Subl][Punct]
[/N|Pro][Poss.3Sg][Subl]

[/N|Pro][EssFor:ként]:
[/N|Pro][Poss.3Sg][EssFor:ként]

[/N|Pro][Supe]:
[/N|Pro][Poss.3Sg][Supe]
[/N|Pro][Poss.3Sg][Supe][Punct]

[/N|Pro][Transl]:
[/N|Pro][Poss.3Sg][Transl]

[/N|Pro|Rel][Acc]:
[/N|Pro|Rel][Acc][Punct]

[/N|Pro|Rel][All]:
[/N|Pro|Rel][All][Hyph:Slash]

[/N|Pro|Rel][Ine]:
[/N|Pro|Rel][Ine][Punct]

[/N|Pro|Rel][Nom]:
[/N|Pro|Rel][Nom][Hyph:Hyph]
[/N|Pro|Rel][Nom][Punct]

[/N|Pro|Rel][Pl][Nom]:
[/N|Pro|Rel][Pl][Nom][Hyph:Slash]

[/N|Pro|Rel][Poss.1Pl][Acc]:
[/N|Pro|Rel][Poss.1Pl][Acc][Punct]

[/N|Pro][Subl][1Sg]:
[/N|Pro][Subl][1Sg][Punct]

[/N|Pro][Subl][2Sg]:
[/N|Pro][Subl][2Sg][Punct]
[/N|Pro][Supe][2Sg][Punct]

[/N|Pro][Subl][3Pl]:
[/N|Pro][Subl][3Pl][Hyph:Slash]
[/N|Pro][Subl][3Pl][Punct]

[/N|Pro][Subl]:
[/N|Pro][Subl][Punct]

[/N|Pro][Supe][1Pl]:
[/N|Pro][Supe][1Pl][Punct]

[/N|Pro][Supe][1Sg]:
[/N|Pro][Supe][1Sg][Punct]
[/N|Pro][Supe][1Sg][Punct][Punct]

[/N|Pro][Supe][3Pl]:
[/N|Pro][Supe][3Pl][Punct]

[/N|Pro][Supe]:
[/N|Pro][Supe][Punct]

[/N|Pro][Temp]:
[/N|Pro][Temp][Punct]

[/N|Pro][Ter]:
[/N|Pro][Ter][Punct]

[/N][Subl]:
[/N][Subl][Hyph:Slash]
[/N][Subl][Punct]

[/N][Supe]:
[/N][Supe][Hyph:Slash]
[/N][Supe][Punct]
[/N][Supe][Punct][Hyph:Slash]

[/N][Temp]:
[/N][Temp][Punct]

[/N][Ter]:
[/N][Ter][Hyph:Slash]
[/N][Ter][Punct]

[/N][_Tmp_Loc/Adv]:
[/N][_Tmp_Loc/Adv][Punct]

[/Num][_Comp/Num][Nom]:
[/Num][_Comp/Num][_Frac/Num][Nom]
[/Num][_Comp/Num][Nom][Hyph:Hyph]
[/Num][_Comp/Num][Poss.1Pl][Nom]
[/Num][_Comp/Num][Poss.2Pl][Nom]
[/Num][_Comp/Num][Poss.2Sg][Nom]
[/Num][_Comp/Num][Poss.3Pl][Nom]

[/Num][_Comp/Num][Subl]:
[/Num][_Comp/Num][_Frac/Num][Poss.3Sg][Subl]

[/Num][_Comp/Num][Ins]:
[/Num][_Comp/Num][Poss.2Pl][Ins]

[/Num][_Comp/Num][Supe]:
[/Num][_Comp/Num][Poss.2Sg][Supe]

[/Num][_Comp/Num][Del]:
[/Num][_Comp/Num][Poss.3Sg][Del]

[/Num][Acc]:
[/Num|Abbr][Acc]
[/Num][Acc][Punct]
[/Num|Digit][Acc]
[/Num|Digit][Acc][Punct]
[/Num|Digit][_Frac/Num][Acc]
[/Num|Digit][Poss.1Sg][Acc]
[/Num|Digit][Poss.3Sg][Acc]
[/Num][_Frac/Num][Acc]
[/Num][_Frac/Num][Poss.3Pl][Acc]
[/Num][_Frac/Num][Poss.3Sg][Acc]
[/Num][Poss.3Pl][Acc]
[/Num][Poss.2Pl][Acc]
[/Num][Poss.3Sg][Acc][Punct]
[/Num][Poss.3Sg][Acc]
[/Num][Poss.1Pl][Acc]
[/Num|Roman][Acc]
[/Num|Roman][_Ord/Adj][Acc]
[/Num|Roman][Poss.3Sg][Acc]

[/Num][AnP][Nom]:
[/Num][Poss.1Pl][AnP][Nom]

[/Num][Nom]:
[/Num|Abbr][Nom]
[/Num|Attr][Nom]
[/Num|Attr][Nom][Hyph:Hyph]
[/Num|Digit][_Frac/Num][Nom]
[/Num|Digit][Nom]
[/Num|Digit][Nom][Hyph:Hyph]
[/Num|Digit][Nom][Hyph:Slash]
[/Num|Digit][Nom][Punct]
[/Num|Digit][Nom][Punct][Hyph:Slash]
[/Num|Digit][Nom][Punct][Punct]
[/Num|Digit][Poss.2Sg][Nom]
[/Num|Digit][Poss.1Sg][Nom]
[/Num|Digit][Poss.3Sg][Nom]
[/Num][_Frac/Num][Nom]
[/Num][_Frac/Num][Poss.3Pl][Nom]
[/Num][_Frac/Num][Poss.3Sg][Nom]
[Num][Nom]
[/Num][Nom][Hyph:Hyph]
[/Num][Nom][Hyph:Slash]
[/Num][Nom][Punct]
[/Num][Poss.3Sg][Nom]
[/Num][Poss.3Pl][Nom]
[/Num][Poss.2Sg][Nom]
[/Num][Poss.2Pl][Nom]
[/Num][Poss.1Sg][Nom]
[/Num][Poss.1Pl][Nom]
[/Num|Roman][Nom]
[/Num|Roman][Nom][Hyph:Hyph]
[/Num|Roman][Nom][Hyph:Slash]
[/Num|Roman][Nom][Punct]
[/Num|Roman][Nom][Punct][Hyph:Slash]

[/Num][Abl]:
[/Num|Digit][Abl]
[/Num][_Frac/Num][Abl]
[/Num][_Frac/Num][Poss.3Sg][Abl]
[/Num][Poss.1Pl][Abl]
[/Num][Poss.2Pl][Abl]
[/Num][Poss.3Pl][Abl]
[/Num][Poss.3Sg][Abl]
[/Num|Roman][Abl]

[/Num][Ade]:
[/Num|Digit][Ade]
[/Num|Digit][Poss.3Sg][Ade]
[/Num][_Frac/Num][Poss.3Sg][Ade]
[/Num][Poss.1Pl][Ade]
[/Num|Roman][Ade]

[/Num][All]:
[/Num|Digit][All]
[/Num|Digit][All][Punct]
[/Num|Digit][Poss.3Sg][All]
[/Num][_Frac/Num][Poss.3Sg][All]
[/Num][Poss.3Sg][All]
[/Num][Poss.1Pl][All]
[/Num|Roman][All]
[/Num|Roman][_Ord/Adj][All]

[/Num][AnP][Acc]:
[/Num|Digit][AnP][Acc]
[/Num][Poss.1Pl][AnP][Acc]

[/Num][AnP][Abl]:
[/Num][_Frac/Num][AnP][Abl]

[/Num][AnP][Ill]:
[/Num|Digit][AnP][Ill]


[/Num][Ter]:
[/Num|Digit][AnP][Ter]
[/Num|Digit][Ter]
[/Num][_Frac/Num][Poss.3Sg][Ter]
[/Num][_Frac/Num][Ter]
[/Num][Poss.3Sg][Ter]
[/Num][Poss.2Sg][Ter]
[/Num|Roman][Ter]
[/Num][Ter]

[/Num][AnP][Ter]:
[/Num][_Frac/Num][AnP][Ter]

[/Num][Cau]:
[/Num|Digit][Cau]
[/Num][_Frac/Num][Poss.3Sg][Cau]
[/Num|Digit][Poss.3Sg][Cau]
[/Num][Poss.2Pl][Cau]


[/Num][Dat]:
[/Num|Digit][Dat]
[/Num|Digit][Dat][Punct]
[/Num][_Frac/Num][Dat]
[/Num][_Frac/Num][Poss.3Sg][Dat]
[/Num][Poss.1Pl][Dat]
[/Num][Poss.1Sg][Dat]
[/Num][Poss.3Pl][Dat]
[/Num][Poss.3Sg][Dat]
[/Num|Roman][Dat]
[/Num|Roman][_Ord/Adj][Dat]

[/Num][Del]:
[/Num|Digit][Del]
[/Num|Digit][Poss.1Sg][Del]
[/Num][_Frac/Num][Del]
[/Num][Poss.1Pl][Del]
[/Num|Roman][Del]

[/Num][EssFor:ként]:
[/Num][Poss.3Sg][EssFor:ként]

[/Num][Ela]:
[/Num|Digit][Ela]
[/Num|Digit][Ela][Punct]
[/Num][_Frac/Num][Poss.1Pl][Ela]
[/Num][_Frac/Num][Poss.3Pl][Ela]
[/Num][_Frac/Num][Poss.3Sg][Ela]
[/Num|Digit][Poss.3Sg][Ela]
[/Num][Ela][Punct]
[/Num][_Frac/Num][Ela]
[/Num][Poss.1Pl][Ela]
[/Num][Poss.3Sg][Ela]
[/Num][Poss.3Pl][Ela]
[/Num|Roman][_Ord/Adj][Ela]
[/Num|Roman][Ela]

[/Num][AnP][Ela]:
[/Num][Poss.2Sg][AnP][Ela]

[/Num][Subl]:
[/Num|Digit][_Frac/Num][Poss.3Sg][Subl]
[/Num][_Frac/Num][Poss.3Sg][Subl]
[/Num][_Frac/Num][Subl]
[/Num|Digit][Subl]
[/Num|Digit][Subl][Punct]
[/Num][Poss.2Pl][Subl]
[/Num][Poss.3Pl][Subl]
[/Num][Poss.3Sg][Subl]
[/Num][Poss.1Pl][Subl]
[/Num|Roman][_Ord/Adj][Subl]
[/Num|Roman][Subl]
[/Num][Subl][Punct]

[/Num][Ill]:
[/Num|Digit][Ill]
[/Num|Digit][Ill][Punct]
[/Num][Ill][Punct]
[/Num][_Frac/Num][Ill]
[/Num|Digit][Poss.1Sg][Ill]
[/Num][_Frac/Num][Poss.3Sg][Ill]
[/Num][Poss.3Sg][Ill]
[/Num|Roman][Ill]
[/Num|Roman][_Ord/Adj][Ill]


[/Num][Ine]:
[/Num|Digit][Ine]
[/Num|Digit][Ine][Punct]
[/Num][_Frac/Num][Ine]
[/Num][_Frac/Num][Poss.3Sg][Ine]
[/Num|Digit][Poss.2Sg][Ine]
[/Num|Digit][Poss.3Sg][Ine]
[/Num][Poss.3Sg][Ine]
[/Num|Roman][Ine]
[/Num|Roman][_Ord/Adj][Ine]
[/Num|Roman][Poss.3Sg][Ine]

[/Num][Ins]:
[/Num|Digit][Ins]
[/Num|Digit][Poss.1Pl][Ins]
[/Num|Digit][Poss.1Sg][Ins]
[/Num|Digit][Poss.3Sg][Ins]
[/Num][_Frac/Num][Ins]
[/Num][_Frac/Num][Poss.1Pl][Ins]
[/Num][_Frac/Num][Poss.3Sg][Ins]
[/Num][Poss.2Pl][Ins]
[/Num][Poss.3Pl][Ins]
[/Num][Poss.3Sg][Ins]
[/Num][Poss.1Pl][Ins]
[/Num|Roman][Ins]

[/Num][Supe]:
[/Num|Digit][Poss.3Pl][Supe]
[/Num|Digit][Poss.3Sg][Supe]
[/Num|Digit][Supe]
[/Num][_Frac/Num][Supe]
[/Num][_Frac/Num][Poss.3Sg][Supe]
[/Num][Poss.1Pl][Supe]
[/Num][Poss.1Sg][Supe]
[/Num][Poss.3Pl][Supe]
[/Num][Poss.3Sg][Supe]
[/Num|Roman][Supe]
[/Num][Supe][Punct]

[/Num][Dat]:
[/Num][Poss.2Pl][Dat]

[/Num][AnP][Supe]:
[/Num][_Frac/Num][AnP][Supe]

[/Num][Temp]:
[/Num|Digit][Temp]
[/Num][Temp][Punct]

[/Num][Pl][Acc]:
[/Num|Digit][Pl][Acc]
[/Num|Digit][Pl.Poss.3Pl][Acc]
[/Num][_Frac/Num][Pl][Acc]
[/Num][Pl.Poss.3Pl][Acc]
[/Num][Pl.Poss.3Sg][Acc]
[/Num|Roman][Pl][Acc]

[/Num][Pl][Ine]:
[/Num][Pl][Ine][Punct]
[/Num][Pl.Poss.3Sg][Ine]

[/Num][Pl][Ins]:
[/Num|Digit][Pl][Ins]
[/Num][Pl.Poss.1Pl][Ins]
[/Num][Pl.Poss.3Sg][Ins]

[/Num][Pl][Nom]:
[/Num][Pl.Poss.3Pl][Nom]
[/Num|Digit][Pl][Nom]
[/Num|Digit][Pl.Poss.3Pl][Nom]
[/Num|Digit][Pl.Poss.3Sg][Nom]
[/Num][_Frac/Num][Pl][Nom]
[/Num][Fam.Pl][Nom]
[/Num][Pl.Poss.2Sg][Nom]
[/Num][Pl.Poss.3Sg][Nom]

[/Num][Pl][Subl]:
[/Num|Digit][Pl][Subl]
[/Num][Pl.Poss.3Sg][Subl]

[/Num][Pl][Abl]:
[/Num][Pl.Poss.1Sg][Abl]
[/Num][Pl.Poss.3Sg][Abl]

[/Num][Pl][Del]:
[/Num][Pl.Poss.3Pl][Del]
[/Num][Pl.Poss.3Sg][Del]

[/Num][Pl][All]:
[/Num][Pl.Poss.3Sg][All]

[/Num][Pl][Dat]:
[/Num][Pl.Poss.3Sg][Dat]

[/Num][Pl][Ela]:
[/Num][Pl.Poss.3Sg][Ela]

[/Num][Pl][Ill]:
[/Num][Pl.Poss.3Sg][Ill]

[/Num][Pl][Supe]:
[/Num][Pl.Poss.3Sg][Supe]
[/Num][Pl.Poss.3Sg][Supe][Punct]

[/Num|Pro][Acc]:
[/Num|Pro][Poss.1Pl][Acc]
[/Num|Pro][Poss.3Pl][Acc]
[/Num|Pro][Poss.3Sg][Acc]
[/Num|Pro][Acc][Punct]

[/Num|Pro][Nom]:
[/Num|Pro][Poss.1Pl][Nom]
[/Num|Pro][Poss.3Pl][Nom]

[/Num|Pro][Dat]:
[/Num|Pro][Poss.3Pl][Dat]

[/Num|Pro|Int][_Frac/Num][Subl]:
[/Num|Pro|Int][_Frac/Num][Poss.3Sg][Subl]

[/Num|Pro|Int][Subl]:
[/Num|Pro|Int][Subl][Punct]

[/Num|Pro][Cau]:
[/Num|Pro][Cau][Punct]

[/Num|Pro][Ins]:
[/Num|Pro][Ins][Punct]

[/Num|Pro|Int][Nom]:
[/Num|Pro|Int][Nom][Punct]

[/Num|Pro][Subl]:
[/Num|Pro][Subl][Punct]

[/Prev]:
[/Prev][Hyph:Hyph]
[/Prev][Hyph:Slash]
[/Prev][Punct]

[/Supl][/Adj][_Comp/Adj][Nom]:
[/Supl][/Adj][_Comp/Adj][AnP][Nom]
[/Supl][/Adj][_Comp/Adj][_Design/Adj][Nom]
[/Supl][/Adj][_Comp/Adj][Nom]
[/Supl][/Adj][_Comp/Adj][Nom][Punct]
[/Supl][/Adj][_Comp/Adj][Poss.1Sg][Nom]
[/Supl][/Adj][_Comp/Adj][Poss.3Sg][Nom]

[/Supl][/Num][_Comp/Num][Acc]:
[/Supl][/Num][_Comp/Num][Acc][Punct]

[/Supl][/Num][_Comp/Num][Acc]:
[/Supl][/Num][_Comp/Num][Poss.1Pl][Acc]
[/Supl][/Num][_Comp/Num][Poss.3Pl][Acc]
[/Supl][/Num][_Comp/Num][Poss.3Sg][Acc]

[/Supl][/Num][_Comp/Num][Ade]:
[/Supl][/Num][_Comp/Num][Poss.1Pl][Ade]
[/Supl][/Num][_Comp/Num][Poss.3Sg][Ade]

[/Supl][/Num][_Comp/Num][All]:
[/Supl][/Num][_Comp/Num][Poss.1Pl][All]

[/Supl][/Num][_Comp/Num][Ins]:
[/Supl][/Num][_Comp/Num][Poss.1Pl][Ins]
[/Supl][/Num][_Comp/Num][Poss.3Pl][Ins]
[/Supl][/Num][_Comp/Num][Poss.3Sg][Ins]

[/Supl][/Num][_Comp/Num][Nom]:
[/Supl][/Num][_Comp/Num][Poss.1Pl][Nom]
[/Supl][/Num][_Comp/Num][Poss.2Pl][Nom]
[/Supl][/Num][_Comp/Num][Poss.3Sg][Nom]
[/Supl][/Num][_Comp/Num][Poss.3Pl][Nom]

[/Supl][/Num][_Comp/Num][Dat]:
[/Supl][/Num][_Comp/Num][Poss.2Pl][Dat]
[/Supl][/Num][_Comp/Num][Poss.3Pl][Dat]
[/Supl][/Num][_Comp/Num][Poss.3Sg][Dat]

[/Supl][/Num][_Comp/Num][Abl]:
[/Supl][/Num][_Comp/Num][Poss.3Pl][Abl]

[/Supl][/Num][_Comp/Num][Del]:
[/Supl][/Num][_Comp/Num][Poss.3Pl][Del]

[/Supl][/Num][_Comp/Num][Ela]:
[/Supl][/Num][_Comp/Num][Poss.3Pl][Ela]

[/Supl][/Num][_Comp/Num][Subl]:
[/Supl][/Num][_Comp/Num][Poss.3Pl][Subl]

[/V][_AdvPerfPtcp/Adv]:
[/V][_AdvPerfPtcp/Adv][Punct]

[/V][_AdvPtcp/Adv]:
[/V][_AdvPtcp/Adv][Punct]
[/V][_Caus/V][_AdvPtcp/Adv][Punct]

[/V][Inf]:
[/V][_Caus/V][_Caus/V][Inf]
[/V][_Caus/V][_Freq/V][Inf]
[/V][_Caus/V][Inf]
[/V][_Caus/V][Inf][Punct]
[/V][_Freq/V][Inf]
[V][Inf]
[/V][Inf][Hyph:Hyph]
[/V][Inf][Hyph:Slash]
[/V][Inf][Punct]

[/V][Prs.Def.1Sg]:
[/V][_Caus/V][_Caus/V][Prs.Def.1Sg]
[/V][_Caus/V][Prs.Def.1Sg]
[/V][_Freq/V][Prs.Def.1Sg]
[/V][Prs.Def.1Sg][Hyph:Slash]
[/V][Prs.Def.1Sg][Punct]
[/V][Prs.Def.1Sg][Punct][Hyph:Slash]

[/V][Prs.NDef.3Sg]
[/V][_Caus/V][_Caus/V][Prs.NDef.3Sg]
[/V][_Caus/V][Prs.NDef.3Sg]
[/V][_Caus/V][Prs.NDef.3Sg][Punct]
[/V][_Freq/V][Prs.NDef.3Sg]
[/V][Prs.NDef.3Sg][Hyph:Hyph]
[/V][Prs.NDef.3Sg][Hyph:Slash]
[/V][Prs.NDef.3Sg][Punct]
[/V][Prs.NDef.3Sg][Punct][Hyph:Slash]
[/V][Prs.NDef.3Sg][Punct][Punct]

[/V][Sbjv.Def.3Sg]:
[/V][_Caus/V][_Caus/V][Sbjv.Def.3Sg]
[/V][_Caus/V][Sbjv.Def.3Sg]
[/V][_Freq/V][Sbjv.Def.3Sg]
[/V][Sbjv.Def.3Sg][Hyph:Slash]
[/V][Sbjv.Def.3Sg][Punct]

[/V][Cond.NDef.2Sg]:
[/V][_Caus/V][Cond.NDef.2Sg][Punct]
[/V][Cond.Def.2Sg][Punct]
[/V][Cond.NDef.2Sg][Hyph:Slash]
[/V][_Caus/V][Cond.NDef.2Sg]


[/V][_Mod/V][Cond.Def.3Pl]:
[/V][_Caus/V][_Mod/V][Cond.Def.3Pl]

[/V][_Mod/V][Prs.Def.1Pl]:
[/V][_Caus/V][_Mod/V][Prs.Def.1Pl]
[/V][_Caus/V][Prs.Def.1Pl]
[/V][_Mod/V][Prs.Def.1Pl][Punct]


[/V][_Mod/V][Prs.Def.1Sg]:
[/V][_Caus/V][_Mod/V][Prs.Def.1Sg]
[/V][_Mod/V][Prs.Def.1Sg][Punct]

[/V][_Mod/V][Prs.Def.3Pl]:
[/V][_Caus/V][_Mod/V][Prs.Def.3Pl]
[/V][_Freq/V][Prs.Def.3Pl]

[/V][Prs.Def.3Pl]:
[/V][_Caus/V][Prs.Def.3Pl]
[/V][Prs.Def.3Pl][Hyph:Slash]
[/V][Prs.Def.3Pl][Punct]


[/V][_Mod/V][Prs.Def.3Sg]:
[_Caus/V][_Mod/V][Prs.Def.3Sg]
[/V][_Mod/V][Prs.Def.3Sg][Punct]

[/V][Prs.Def.3Sg]:
[/V][_Caus/V][Prs.Def.3Sg][Punct]
[/V][/V][_Caus/V][Prs.Def.3Sg]
[/V][_Freq/V][Prs.Def.3Sg]
[/V][Prs.Def.3Sg][Hyph:Slash]
[/V][Prs.Def.3Sg][Punct]

[/V][_Mod/V][Pst.Def.2Sg]:
[/V][_Caus/V][_Mod/V][Pst.Def.2Sg]


[/V][Pst.Def.2Sg]:
[/V][_Caus/V][Pst.Def.2Sg][Punct]
[/V][_Caus/V][Pst.Def.2Sg]
[/V][Pst.Def.2Sg][Punct]


[/V][_Mod/V][Sbjv.Def.1Pl]:
[/V][_Caus/V][_Mod/V][Sbjv.Def.1Pl]

[/V][_Caus/V][Sbjv.Def.1Pl]:
[/V][Sbjv.Def.1Pl]
[/V][_Freq/V][Sbjv.Def.1Pl]
[/V][Sbjv.Def.1Pl][Punct]

[/V][_Mod/V][Sbjv.Def.3Sg]:
[/V][_Caus/V][_Mod/V][Sbjv.Def.3Sg]
[/V][_Mod/V][Sbjv.Def.3Sg][Punct]

[/V][_Mod/V][Sbjv.NDef.3Pl]:
[/V][_Caus/V][_Mod/V][Sbjv.NDef.3Pl]
[/V][_Mod/V][Sbjv.NDef.3Pl][Punct]


[/V][Sbjv.NDef.3Pl]:
[/V][_Caus/V][Sbjv.NDef.3Pl]
[/V][Sbjv.NDef.3Pl][Punct]

[/V][Prs.Def.2Pl]:
[/V][_Caus/V][Prs.Def.2Pl]
[/V][Prs.Def.2Pl][Punct]

[/V][Prs.Def.2Sg]:
[/V][_Caus/V][Prs.Def.2Sg]
[/V][Prs.Def.2Sg][Punct]
[/V][Prs.Def.2Sg][Hyph:Slash]

[/V][Prs.NDef.1Pl]:
[/V][_Caus/V][Prs.NDef.1Pl]
[/V][Prs.NDef.1Pl][Hyph:Slash]
[/V][Prs.NDef.1Pl][Punct]

[/V][Prs.NDef.1Sg]:
[/V][_Caus/V][Prs.NDef.1Sg]
[/V][_Caus/V][Prs.NDef.1Sg][Punct]
[/V][Prs.NDef.1Sg][Hyph:Slash]
[/V][Prs.NDef.1Sg][Punct]

[/V][Prs.NDef.2Pl]:
[/V][_Caus/V][Prs.NDef.2Pl]
[/V][Prs.NDef.2Pl][Punct]

[/V][Prs.NDef.2Sg]:
[/V][_Caus/V][Prs.NDef.2Sg]
[/V][Prs.NDef.2Sg][Hyph:Slash]
[/V][Prs.NDef.2Sg][Punct]


[/V][Prs.NDef.3Pl]:
[/V][_Caus/V][Prs.NDef.3Pl]
[/V][Prs.NDef.3Pl][Hyph:Slash]
[/V][Prs.NDef.3Pl][Punct]

[/V][Pst.1Sg›2]:
[/V][_Caus/V][Pst.1Sg›2]

[/V][Pst.Def.1Pl]:
[/V][_Caus/V][Pst.Def.1Pl]
[/V][Pst.Def.1Pl][Punct]

[/V][Pst.Def.1Sg]:
[/V][_Caus/V][Pst.Def.1Sg]
[/V][_Caus/V][Pst.Def.1Sg][Punct]
[/V][Pst.Def.1Sg][Hyph:Slash]
[/V][Pst.Def.1Sg][Punct]

[/V][Pst.Def.3Pl]:
[/V][_Caus/V][Pst.Def.3Pl]
[/V][_Freq/V][Pst.Def.3Pl]
[/V][Pst.Def.3Pl][Hyph:Slash]

[/V][Pst.Def.3Sg]:
[/V][_Caus/V][Pst.Def.3Sg]
[/V][_Freq/V][Pst.Def.3Sg]
[/V][Pst.Def.3Sg][Hyph:Slash]
[/V][Pst.Def.3Sg][Punct][Punct]

[/V][Pst.NDef.1Sg]:
[/V][_Caus/V][Pst.NDef.1Sg]
[/V][_Freq/V][Pst.NDef.1Sg]
[/V][Pst.NDef.1Sg][Hyph:Slash]
[/V][Pst.NDef.1Sg][Punct]

[/V][Pst.NDef.3Pl]:
[/V][_Caus/V][Pst.NDef.3Pl]
[/V][_Freq/V][Pst.NDef.3Pl]
[/V][Pst.NDef.3Pl][Hyph:Slash]
[/V][Pst.NDef.3Pl][Punct]

[/V][Pst.NDef.3Sg]:
[/V][_Caus/V][Pst.NDef.3Sg]
[/V][_Freq/V][Pst.NDef.3Sg]
[/V][Pst.NDef.3Sg][Hyph:Slash]
[/V][Pst.NDef.3Sg][Punct]

[/V][Sbjv.Def.1Sg]:
[/V][_Caus/V][Sbjv.Def.1Sg]
[/V][Sbjv.Def.1Sg][Punct]

[/V][Sbjv.Def.2Sg]:
[/V][_Caus/V][Sbjv.Def.2Sg]
[/V][_Freq/V][Sbjv.Def.2Sg]
[/V][Sbjv.Def.2Sg][Punct]

[/V][Sbjv.Def.3Pl]:
[/V][_Caus/V][Sbjv.Def.3Pl]
[/V][_Freq/V][Sbjv.NDef.3Pl]
[/V][Sbjv.Def.3Pl][Hyph:Slash]
[/V][Sbjv.Def.3Pl][Punct]

[/V][Sbjv.NDef.1Pl]:
[/V][_Caus/V][Sbjv.NDef.1Pl]
[/V][_Freq/V][Sbjv.NDef.1Pl]
[/V][Sbjv.NDef.1Pl][Punct]

[/V][Sbjv.NDef.2Sg]:
[/V][_Caus/V][Sbjv.NDef.2Sg]
[/V][Sbjv.NDef.2Sg][Punct]

[/V][Sbjv.NDef.3Sg]:
[/V][_Caus/V][Sbjv.NDef.3Sg]
[/V][_Freq/V][Sbjv.NDef.3Sg]
[/V][Sbjv.NDef.3Sg][Hyph:Slash]
[/V][Sbjv.NDef.3Sg][Punct]

[/V][Cond.Def.1Pl]:
[/V][Cond.Def.1Pl][Hyph:Slash]
[/V][Cond.Def.1Pl][Punct]
[/V][_Caus/V][Cond.Def.1Pl]

[/V][Inf.1Pl]:
[/V][_Caus/V][Inf.1Pl]
[/V][Inf.1Pl][Punct]

[/V][Inf.1Sg]:
[/V][_Caus/V][Inf.1Sg]
[/V][Inf.1Sg][Punct]

[/V][Inf.2Sg]:
[/V][_Caus/V][Inf.2Sg]
[/V][Inf.2Sg][Punct]
[/V][_Freq/V][Inf.2Sg]

[/V][Inf.3Pl]:
[/V][Inf.3Pl][Punct]

[/V][Inf.3Sg]:
[/V][Inf.3Sg][Punct]

[/V][Cond.Def.1Sg]:
[/V][Cond.Def.1Sg][Hyph:Slash]
[/V][Cond.Def.1Sg][Punct]
[/V][_Caus/V][Cond.Def.1Sg]

[/V][Cond.Def.3Pl]:
[/V][Cond.Def.3Pl][Punct]
[/V][_Caus/V][Cond.Def.3Pl]

[/V][Cond.Def.3Sg]:
[/V][Cond.Def.3Sg][Hyph:Slash]
[/V][Cond.Def.3Sg][Punct]
[/V][_Freq/V][Cond.Def.3Sg]
[/V][_Caus/V][Cond.Def.3Sg]

[/V][Cond.NDef.1Pl]:
[/V][Cond.NDef.1Pl][Punct]
[/V][_Caus/V][Cond.NDef.1Pl]

[/V][Cond.NDef.1Sg]:
[/V][Cond.NDef.1Sg][Punct]
[/V][_Freq/V][Cond.NDef.1Sg]

[/V][Cond.NDef.3Pl]:
[/V][Cond.NDef.3Pl][Punct]

[/V][Cond.NDef.3Sg]:
[/V][Cond.NDef.3Sg][Hyph:Slash]
[/V][Cond.NDef.3Sg][Punct]
[/V][Cond.NDef.3Sg][Punct][Hyph:Slash]
[/V][Cond.NDef.3Sg][Punct][Punct]
[/V][_Freq/V][Cond.NDef.3Sg]
[/V][_Caus/V][Cond.NDef.3Sg]

[/V][_AdvPtcp/Adv]:
[/V][_Freq/V][_AdvPtcp/Adv]

[/V][_Mod/V][Prs.Def.1Sg]:
[/V][_Freq/V][_Mod/V][Prs.Def.1Sg]

[/V][_Mod/V][Prs.NDef.2Pl]:
[/V][_Freq/V][_Mod/V][Prs.NDef.2Pl][Punct]
[/V][_Mod/V][Prs.NDef.2Pl][Punct]

[/V][Prs.NDef.1Pl]:
[/V][_Freq/V][Prs.NDef.1Pl]

[/V][Prs.NDef.1Sg]:
[/V][_Freq/V][Prs.NDef.1Sg]
[/V][_Freq/V][Prs.NDef.1Sg][Punct]

[/V][Prs.NDef.2Sg]:
[/V][_Freq/V][Prs.NDef.2Sg]

[/V][Prs.NDef.3Pl]:
[/V][_Freq/V][Prs.NDef.3Pl]

[/V][Pst.NDef.1Pl]:
[/V][_Freq/V][Pst.NDef.1Pl]
[/V][Pst.NDef.1Pl][Hyph:Slash]
[/V][Pst.NDef.1Pl][Punct]

[/V][Pst.NDef.2Sg]:
[/V][_Freq/V][Pst.NDef.2Sg]
[/V][Pst.NDef.2Sg][Punct]

[/V][Sbjv.Def.1Pl]:
[/V][_Freq/V][Sbjv.Def.1Pl]

[/V][_Mod/V][Cond.NDef.3Sg]:
[/V][_Mod/V][Cond.NDef.3Sg][Punct]

[/V][_Mod/V][Prs.Def.2Pl]:
[/V][_Mod/V][Prs.Def.2Pl][Punct]

[/V][_Mod/V][Prs.NDef.1Pl]:
[/V][_Mod/V][Prs.NDef.1Pl][Punct]

[/V][_Mod/V][Prs.NDef.2Sg]:
[/V][_Mod/V][Prs.NDef.2Sg][Punct]

[/V][_Mod/V][Prs.NDef.3Pl]:
[/V][_Mod/V][Prs.NDef.3Pl][Punct]

[/V][_Mod/V][Prs.NDef.3Sg]:
[/V][_Mod/V][Prs.NDef.3Sg][Punct]

[/V][_Mod/V][Pst.NDef.3Sg]:
[/V][_Mod/V][Pst.NDef.3Sg][Punct]

[/V][_Mod/V][Sbjv.Def.3Pl]:
[/V][_Mod/V][Sbjv.Def.3Pl][Punct]

[/V][_Mod/V][Sbjv.NDef.1Sg]:
[/V][_Mod/V][Sbjv.NDef.1Sg][Punct]

[/V][_Mod/V][Sbjv.NDef.3Sg]:
[/V][_Mod/V][Sbjv.NDef.3Sg][Punct]

[/V][Prs.1Sg›2]:
[/V][Prs.1Sg›2][Punct]

[/V][Pst.NDef.2Pl]:
[/V][Pst.NDef.2Pl][Punct]

[/V]:
[/V][Punct]

[/V][Prs.Def.1Pl]:
[/V][Prs.Def.1Pl][Hyph:Slash]
[/V][Prs.Def.1Pl][Punct]

[/V][Sbjv.Def.2Pl]:
[/V][Sbjv.Def.2Pl][Punct]

[/V][Sbjv.NDef.1Sg]:
[/V][Sbjv.NDef.1Sg][Punct]

[/V][Sbjv.NDef.2Pl]:
[/V][Sbjv.NDef.2Pl][Punct]

[/CNj]:
[/Cnj|Abbr]
[/Cnj|Abbr][Punct]
[/Cnj][Hyph:Slash]
[/Cnj][Punct]
[/Cnj][QPtcl]

[/Adv][_Manner/Adv]:
[/Adj|Attr][_Manner/Adv]
[/Adj][_Mannder/Adv]
[/Adj][_Comp/Adj][_Manner/Adv]
[/Supl][/Supl][/Adj][_Comp/Adj][_Manner/Adv]
[/Supl][/Adj][_Manner/Adv]
[/Supl][/Adj][_Comp/Adj][_Manner/Adv]
[/Num][_Manner/Adv]
[/Num][_Comp/Num][_Manner/Adv]
[/Num][_Comp/Adj][_Manner/Adv]
[/Num][_Comp/Adj][_Manner/Adv]
[/Adj][_Comp/Adj][_Manner/Adv]
[/Adj][_Manner/Adv]
[/Adj|Attr][_Manner/Adv]
[/Adj][_Comp/Adj][_Manner/Adv]
[/Num|Pro][_Manner/Adv]
[/Adj][_Comp/Adj][_Manner/Adv][Punct]
[/Adj][_Manner/Adv]:
[/Adj][_Manner:0/Adv][Punct]
[/Adj][_Manner/Adv][Hyph:Hyph]
[/Adj][_Manner/Adv][Punct]
[/Adj|Pred][_Manner/Adv]
[/Num|Digit][_Manner/Adv]
[/Supl][/Adj][_Comp/Adj][_Manner/Adv][Punct]


[/Adv][_Advz:lAg/Adv]:
[/Adj][_Advz:lAg/Adv]


[/Adv][_Distr:nként/Adv]:
[/Num][_Distr:nként/Adv]
[/N][_Distr:nként/Adv]
[/Adj][_Distr:nként/Adv]
[/N][_Distr:nként/Adv][Punct]
[/Num|Digit][_Distr:nként/Adv]


[/Adv][_Aggreg/Adv]:
[/Supl][/Num][_Comp/Num][_Aggreg/Adv]
[/Num|Digit][_Aggreg/Adv]
[/Num][_Aggreg/Adv]
[/Num|Pro][_Aggreg/Adv]
[/Num][_Aggreg/Adv][Punct]
[/Num|Pro][_Aggreg/Adv][Punct]



[/Adv][_Mlt-Iter/Adv]:
[/Num][_Mlt-Iter/Adv]
[/Num][_Mlt-Iter/Adv]
[/Num][_Comp/Num][_Ord/Adj][_Mlt-Iter/Adv]
[/Num][_Comp/Num][_Mlt-Iter/Adv]
[/Num][_Comp/Num][_Frac/Num][_Mlt-Iter/Adv]
[/Num|Attr][_Mlt-Iter/Adv]
[/Num|Pro][_MltIter/Adv]
[/Num|Digit][_Mlt-Iter/Adv]
[/Num][_Mlt-Iter/Adv][Punct]
[/Num|Digit][_Frac/Num][_Mlt-Iter/Adv]
[/Num|Digit][_Ord/Adj][_Mlt-Iter/Adv]
[/Supl][/Num][_Comp/Num][_Mlt-Iter/Adv][Punct]


[/Adv][Adj]:
[/Supl][/Adv]
[/Supl][/Adv][_Comp/Adv]
[/Adv|(Adj)]
[/Adv|AdjMod]
[/Adv|AdjMod][Punct]


[/Adv][Subl]:
[/Supl][/Adv][_Comp/Adv][Subl]
[/Num][_Mlt-Iter/Adv][Subl]
[/Num][_Mlt-Iter/Adv][Subl]
[/Num][_Comp/Num][_Ord/Adj][_Mlt-Iter/Adv][Subl]
[/Num][_Comp/Num][_Frac/Num][_Mlt-Iter/Adv][Subl]
[/Num|Attr][_Mlt-Iter/Adv][Subl]
[/Adv][_Comp/Adv][Subl]
[/Num|Digit][_Ord/Adj][_Mlt-Iter/Adv][Subl]
[/Num][_Frac/Num][_Mlt-Iter/Adv][Subl]


[/Adv][Del]:
[/Supl][/Adv][Del]
[/Supl][/Adv][_Comp/Adv][Del]
[/Adv][_Comp/Adv][Del]

"""

print('^(', '"\n    - "'.join((i.strip()) for i in a.split('\n')), ')$', sep='')
