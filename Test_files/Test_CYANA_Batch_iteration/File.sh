#!/bin/bash

/home/ubuntu/programs/cyana-3.98.11/cyana << EOF > Zoolander_OVW_1_log.txt
read seq Zoolander_SEQ_ORI4.seq
read aco Zoolander_ACO_noloops.aco
read aco Zoolander_ACO_loops5.aco append
read lol Zoolander_LOL_ORI_0.lol
read upl Zoolander_UPL_ORI_0.upl
read upl Zoolander_UPL_regula_nometLEU_noNH3LYS.upl append
read upl Zoolander_UPL_regula_LK_metcarb.upl append
read pcs Zoolander_PCS_numbatpcs_ori4_tol20.pcs
weight_upl = 0.1
anneal_weight_upl := 1.0, 1.0, 1.0, 1.0
weight_pcs = 0.3
anneal_weight_pcs := 1.0, 1.0, 1.0, 1.0
weight_aco = 5.0
anneal_weight_aco := 1.0, 1.0, 1.0, 1.0
weight_vdw = 2.0
anneal_weight_vdw := 0.25, 0.25, 0.25, 1.0
seed       = 1215
nproc=16
calc_all structures=3000 steps=25000
overview Zoolander_OVW_1.ovw structures=10 range=3-238 pdb
exit
EOF


/home/ubuntu/programs/cyana-3.98.11/cyana << EOF > Zoolander_OVW_1_log.txt
read seq Zoolander_SEQ_ORI4.seq
read aco Zoolander_ACO_noloops.aco
read aco Zoolander_ACO_loops5.aco append
read lol Zoolander_LOL_ORI_0.1.lol
read upl Zoolander_UPL_ORI_0.1.upl
read upl Zoolander_UPL_regula_nometLEU_noNH3LYS.upl append
read upl Zoolander_UPL_regula_LK_metcarb.upl append
read pcs Zoolander_PCS_numbatpcs_ori4_tol20.pcs
weight_upl = 0.1
anneal_weight_upl := 1.0, 1.0, 1.0, 1.0
weight_pcs = 0.3
anneal_weight_pcs := 1.0, 1.0, 1.0, 1.0
weight_aco = 5.0
anneal_weight_aco := 1.0, 1.0, 1.0, 1.0
weight_vdw = 2.0
anneal_weight_vdw := 0.25, 0.25, 0.25, 1.0
seed       = 1215
nproc=16
calc_all structures=3000 steps=25000
overview Zoolander_OVW_1.ovw structures=10 range=3-238 pdb
exit
EOF


/home/ubuntu/programs/cyana-3.98.11/cyana << EOF > Zoolander_OVW_1_log.txt
read seq Zoolander_SEQ_ORI4.seq
read aco Zoolander_ACO_noloops.aco
read aco Zoolander_ACO_loops5.aco append
read lol Zoolander_LOL_ORI_0.2.lol
read upl Zoolander_UPL_ORI_0.2.upl
read upl Zoolander_UPL_regula_nometLEU_noNH3LYS.upl append
read upl Zoolander_UPL_regula_LK_metcarb.upl append
read pcs Zoolander_PCS_numbatpcs_ori4_tol20.pcs
weight_upl = 0.1
anneal_weight_upl := 1.0, 1.0, 1.0, 1.0
weight_pcs = 0.3
anneal_weight_pcs := 1.0, 1.0, 1.0, 1.0
weight_aco = 5.0
anneal_weight_aco := 1.0, 1.0, 1.0, 1.0
weight_vdw = 2.0
anneal_weight_vdw := 0.25, 0.25, 0.25, 1.0
seed       = 1215
nproc=16
calc_all structures=3000 steps=25000
overview Zoolander_OVW_1.ovw structures=10 range=3-238 pdb
exit
EOF

