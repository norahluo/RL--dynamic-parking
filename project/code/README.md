# CS 285

## Policy Gradient
```
cd Documents/Codes/Course/CS285/project/code
```

## basic policy gradient
finished
```
python cs285/scripts/run_parking.py -dsa --policy beta --exp_name b
python cs285/scripts/run_parking.py -dsa -rtg --policy beta --exp_name b_rtg
python cs285/scripts/run_parking.py -rtg --policy beta --exp_name b_rtg_sa
python cs285/scripts/run_parking.py -dsa --exp_name n
python cs285/scripts/run_parking.py -dsa -rtg --exp_name n_rtg
python cs285/scripts/run_parking_actor_critic.py -ntu 1 -ngsptu 1 --policy beta --exp_name b_ntu_1_ngsptu_1
python cs285/scripts/run_parking_actor_critic.py -ntu 10 -ngsptu 1 --policy beta --exp_name b_ntu_10_ngsptu_1
python cs285/scripts/run_parking_actor_critic.py -ntu 1 -ngsptu 10 --policy beta --exp_name b_ntu_1_ngsptu_10
python cs285/scripts/run_parking.py -rtg -l 3 --policy beta --exp_name b_rtg_sa_l_3
python cs285/scripts/run_parking.py -rtg -l 4 --policy beta --exp_name b_rtg_sa_l_4
```

(Qianhua)
```
python cs285/scripts/run_parking.py -rtg --exp_name n_rtg_sa
python cs285/scripts/run_parking_actor_critic.py -ntu 1 -ngsptu 1 --exp_name n_ntu_1_ngsptu_1
python cs285/scripts/run_parking_actor_critic.py -ntu 10 -ngsptu 1 --exp_name n_ntu_10_ngsptu_1
python cs285/scripts/run_parking_actor_critic.py -ntu 1 -ngsptu 10  --exp_name n_ntu_1_ngsptu_10
```
## adjust network
(Yunduan)
```
python cs285/scripts/run_parking.py -rtg --nn_baseline --policy beta --exp_name b_rtg_sa_nn
python cs285/scripts/run_parking.py -rtg --nn_baseline --policy normal --exp_name n_rtg_sa_nn
```

(Yunduan)
```
```
