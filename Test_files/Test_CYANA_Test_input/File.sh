#!/bin/bash


/Applications/cyana-3.98.12/cyana << EOF > Zoolander_OVW_1_log.txt
read seq SEQ.seq
read aco ACO.aco
read lol LOL.lol
read upl UPL.upl
read pcs PCS.pcs
weight_upl = 1.0
anneal_weight_upl := 1.0, 1.0, 1.0, 1.0
weight_pcs = 0.1
anneal_weight_pcs := 1.0, 1.0, 1.0, 1.0
weight_aco = 5.0
anneal_weight_aco := 1.0, 1.0, 1.0, 1.0
weight_vdw = 2.0
anneal_weight_vdw := 0.25, 0.25, 0.25, 1.0
seed       = 1215
nproc=4
info:=NORMAL
calc_all structures=3000 steps=25000
overview Zoolander_OVW_1.ovw structures=10 range=3-238 pdb
exit
EOF

/Applications/cyana-3.98.12/cyana << EOF > Zoolander_OVW_2_log.txt
read seq SEQ.seq
read aco ACO.aco
read lol LOL.lol
read upl UPL.upl
weight_upl = 1.0
anneal_weight_upl := 1.0, 1.0, 1.0, 1.0
weight_pcs = 0.1
anneal_weight_pcs := 1.0, 1.0, 1.0, 1.0
weight_aco = 5.0
anneal_weight_aco := 1.0, 1.0, 1.0, 1.0
weight_vdw = 2.0
anneal_weight_vdw := 0.25, 0.25, 0.25, 1.0
seed       = 1215
nproc=4
info:=NORMAL
calc_all structures=3000 steps=25000
overview Zoolander_OVW_2.ovw structures=10 range=3-238 pdb
exit
EOF


/Applications/cyana-3.98.12/cyana << EOF > Zoolander_OVW_3_log.txt
read seq SEQ.seq
read aco ACO.aco
read lol LOL.lol
read upl UPL.upl
read pcs PCS.pcs
read pcs PCS_2.pcs
weight_upl = 1.0
anneal_weight_upl := 1.0, 1.0, 1.0, 1.0
weight_pcs = 0.1
anneal_weight_pcs := 1.0, 1.0, 1.0, 1.0
weight_aco = 5.0
anneal_weight_aco := 1.0, 1.0, 1.0, 1.0
weight_vdw = 2.0
anneal_weight_vdw := 0.25, 0.25, 0.25, 1.0
seed       = 1215
nproc=4
info:=NORMAL
calc_all structures=3000 steps=25000
overview Zoolander_OVW_3.ovw structures=10 range=3-238 pdb
exit
EOF
