#!/bin/sh

## declare an array variable
declare -a variables=("Prec" "Solr" "TPQW")

for var in "${variables[@]}"
do
   echo "$var"
   #for yr in {1980..2009}
   for yr in {2071..2100}
   do
      for mon in {01..12}
      do
         #FILE="/pscratch/sd/e/esinha/inputdata/atm/datm7/AWE-GEN/AWEGEN_forcing/elmforc.AWEGEN_ssp585.$var.$yr-$mon.nc"
         #FILE="/pscratch/sd/e/esinha/inputdata/atm/datm7/AWE-GEN/increase_temp_mean/elmforc.AWEGEN_ssp585.$var.$yr-$mon.nc"
         FILE="/pscratch/sd/e/esinha/inputdata/atm/datm7/AWE-GEN/increase_temp_IAV/elmforc.AWEGEN_ssp585.$var.$yr-$mon.nc"
         #FILE="/pscratch/sd/e/esinha/inputdata/atm/datm7/AWE-GEN/increase_temp_precip/elmforc.AWEGEN_ssp585.$var.$yr-$mon.nc"
         #FILE="/pscratch/sd/e/esinha/inputdata/atm/datm7/AWE-GEN/increase_precip_mean/elmforc.AWEGEN_ssp585.$var.$yr-$mon.nc"
         echo $FILE
         ncks --chk_nan $FILE
      done
   done
done
