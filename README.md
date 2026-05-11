# Battery-life-prediction-and-degradation-trends
Its a project focusing on generating the minimum life of a battery when device (especially UAV'S)needs to change their battery so the machine can work smoothly and also it reduces the risk of physical or technical harm on machine as we can avoid these situations by upgrading the battery before it completely dies or stop working in the mid working 


Steps I have used to plot curves,predict RULand                       
GUI showing cycle degradation trends- 

Step1- I used google collab to generate the plots and 
outputs for the RUL Prediction and degradation 
trends where python codes gave me the SOH(state 
of health) plots vs cycle number and RUL (remaining 
useful life)vs cycle number- 
1)upload the file and loaded the dataset of B0005 
Battery . 
2)extracted cycle data 
3)filter only discharge cycle 
 
4)inspected cycle structure correctly 
5)print discharge cycle 
6)extract discharge cycles with correct indexing 
7)check the first discharge cycle 
8)extact capacity wuth a field name in file as ‘capacity’. 
9)convert capacities to SOH. 
10)plotting SOH vs cycle number. 
11)calculate RUL for each cycle. 
12)plotting RUL vs cycle number. 

Step2- using ML random forester method (which is an ensembling methiod) I did the 
prediction of RUL. 

Step3- using interactive widgets(ipywidgets which is a 
python library) I developed GUI showing cycle 
degradation trend in which both SOH and RUL 
curves update interactively on one graph
