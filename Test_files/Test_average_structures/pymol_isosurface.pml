#PyMOL macro for tensor with values:
#alpha: 42.657 beta: 93.561 gamma: 99.920 Ax: 69.408 Rh: 25.017 x: -3.898 y: 30.564 z: -18.051
#Corresponding potential file should be in ./pymol_isosurface.pml.xplor
load ./pymol_isosurface.pml.xplor, isomap, 1, xplor
isosurface iso1, isomap, 7.1668
isosurface iso2, isomap, -7.1668
isosurface iso3, isomap, 1.7917
isosurface iso4, isomap, -1.7917
set transparency, 0.5, iso1
set transparency, 0.5, iso2
set transparency, 0.7, iso3
set transparency, 0.7, iso4
set surface_color, blue, iso1
set surface_color, red, iso2
set surface_color, blue, iso3
set surface_color, red, iso4
color blue, iso1
color red, iso2
color blue, iso3
color red, iso4
load ./pymol_isosurface.pml.pdb
bond (name OX) and (object pymol_isosurface.pml) and (residue 9000), (name OO) and (object pymol_isosurface.pml) and (residue 9000)
bond (name OY) and (object pymol_isosurface.pml) and (residue 9000) , (name OO) and (object pymol_isosurface.pml) and (residue 9000)
bond (name OZ) and (object pymol_isosurface.pml) and (residue 9000) , (name OO) and (object pymol_isosurface.pml) and (residue 9000)
bond (name OX) and (object pymol_isosurface.pml) and (residue 9001) , (name OO) and (object pymol_isosurface.pml) and (residue 9001)
bond (name OY) and (object pymol_isosurface.pml) and (residue 9001) , (name OO) and (object pymol_isosurface.pml) and (residue 9001)
bond (name OZ) and (object pymol_isosurface.pml) and (residue 9001) , (name OO) and (object pymol_isosurface.pml) and (residue 9001)
bond (name OX) and (object pymol_isosurface.pml) and (residue 9002) , (name OO) and (object pymol_isosurface.pml) and (residue 9002)
bond (name OY) and (object pymol_isosurface.pml) and (residue 9002) , (name OO) and (object pymol_isosurface.pml) and (residue 9002)
bond (name OZ) and (object pymol_isosurface.pml) and (residue 9002) , (name OO) and (object pymol_isosurface.pml) and (residue 9002)
bond (name OX) and (object pymol_isosurface.pml) and (residue 9003) , (name OO) and (object pymol_isosurface.pml) and (residue 9003)
bond (name OY) and (object pymol_isosurface.pml) and (residue 9003) , (name OO) and (object pymol_isosurface.pml) and (residue 9003)
bond (name OZ) and (object pymol_isosurface.pml) and (residue 9003) , (name OO) and (object pymol_isosurface.pml) and (residue 9003)
unbond (name OX) and (object pymol_isosurface.pml), (name OY) and (object pymol_isosurface.pml)
unbond (name OX) and (object pymol_isosurface.pml), (name OZ) and (object pymol_isosurface.pml)
unbond (name OY) and (object pymol_isosurface.pml), (name OZ) and (object pymol_isosurface.pml)
set_bond stick_radius, 0.1, (name OX) and (object pymol_isosurface.pml) , (name OO) and (object pymol_isosurface.pml)
set_bond stick_radius, 0.1, (name OY) and (object pymol_isosurface.pml) , (name OO) and (object pymol_isosurface.pml)
set_bond stick_radius, 0.1, (name OZ) and (object pymol_isosurface.pml) , (name OO) and (object pymol_isosurface.pml)
set_bond stick_color, red, (name OX) and (object pymol_isosurface.pml) , (name OO) and (object pymol_isosurface.pml)
set_bond stick_color, green, (name OY) and (object pymol_isosurface.pml) , (name OO) and (object pymol_isosurface.pml)
set_bond stick_color, blue, (name OZ) and (object pymol_isosurface.pml) , (name OO) and (object pymol_isosurface.pml)
color yellow, (name OO) and (object pymol_isosurface.pml)
color red, (name OX) and (object pymol_isosurface.pml)
color green, (name OY) and (object pymol_isosurface.pml)
color blue, (name OZ) and (object pymol_isosurface.pml)
show sticks, object pymol_isosurface.pml
label (name OX) and (object pymol_isosurface.pml), 'X'
label (name OY) and (object pymol_isosurface.pml), 'Y'
label (name OZ) and (object pymol_isosurface.pml), 'Z'
label (name OO) and (object pymol_isosurface.pml), 'O'
show labels, object pymol_isosurface.pml
