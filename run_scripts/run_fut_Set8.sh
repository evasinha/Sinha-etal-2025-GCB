# --- Configuration flags ----
# Modify the paths below to reflect correct directories
# Set paths
readonly BASE_DIR="/global/homes/e/${USER}/wrk/E3SM_projects"
readonly CODE_DIR="${BASE_DIR}/E3SM"
readonly INPUT_DATA_DIR="/global/cfs/cdirs/e3sm/${USER}/inputdata"
#readonly OUTPUT_DIR="/global/cfs/cdirs/e3sm/${USER}/e3sm_scratch/pm-cpu"
readonly OUTPUT_DIR="/global/cfs/cdirs/e3smdata/${USER}/"

# Simulation
readonly COMPSET="20TR_DATM%GSWP3v1_ELM%CN-CROP_SICE_SOCN_SROF_SGLC_SWAV"
readonly COMPSET_alias="I20TRGSWELMCNCROP"
readonly RESOLUTION="ELM_USRDAT"
readonly MYDATE=$(date '+%Y%m%d')
readonly MYDATE_REST=20240324
readonly CASE_NAME="${MYDATE}_${RESOLUTION}_${COMPSET_alias}_Set8"

readonly CASE_ROOT="${OUTPUT_DIR}/${CASE_NAME}"
readonly CASE_SCRIPTS_DIR="${CASE_ROOT}/case_scripts"
readonly CASE_RUN_DIR="${CASE_ROOT}/run"

# Machine and project
readonly MACHINE=pm-cpu
readonly PROJECT="e3sm"

# Run options
readonly MODEL_START_TYPE="hybrid"  # 'continue', 'branch', 'hybrid'
readonly START_DATE="2070-01-01"

readonly RUN_REFCASE="${MYDATE_REST}_${RESOLUTION}_${COMPSET_alias}_hist1"
readonly RUN_REFDIR="${OUTPUT_DIR}/${RUN_REFCASE}/run"
readonly RUN_REFDATE="1980-01-01"

# Delete old case and run directory
rm -rf ${CASE_ROOT}

echo $'\n----- Starting create_newcase -----\n'

${CODE_DIR}/cime/scripts/create_newcase \
        --case ${CASE_NAME} \
        --output-root ${CASE_ROOT} \
        --script-root ${CASE_SCRIPTS_DIR} \
        --compset ${COMPSET} \
        --res ${RESOLUTION} \
        --output-root ${OUTPUT_DIR} \
        --machine ${MACHINE} \
        --compiler intel \
        --project ${PROJECT}

# =======================
# Custom user_nl settings
# =======================
cd ${CASE_SCRIPTS_DIR}

export fsurdat=${INPUT_DATA_DIR}/lnd/clm2/surfdata_map/surfdata_US_Midwest_0.25x0.25_50pfts_simyr1980_c240315.nc
export finidat=${RUN_REFDIR}/${RUN_REFCASE}.elm.r.${RUN_REFDATE}-00000.nc
export flanduse=${INPUT_DATA_DIR}/lnd/clm2/surfdata_map/landuse.timeseries_US_Midwest_0.25x0.25_hist_50pfts_simyr2070-2099_c240315.nc

export domainpath=${INPUT_DATA_DIR}/lnd/clm2/surfdata_map/
export domainfile=domain.lnd.US_Midwest_0.25x0.25_c240315.nc

cat >> user_nl_elm << EOF
&elm_inparm
 hist_mfilt = 365, 365
 hist_nhtfrq = -24, -24
 hist_dov2xy = .true., .false.
 hist_fincl2 = 'GPP', 'ER', 'NEE', 'NPP', 'EFLX_LH_TOT', 'FSH', 'DMYIELD', 'TOTCOLC', 'TOTSOMC', 'PLANTDAY', 'HARVESTDAY', 'GRAINFILLDAY','TLAI', 'LEAFC', 'SMINN_TO_PLANT', 'BTRAN', 'FPG', 'TOTPFTN', 'SOILWATER_10CM', 'FROOTC'
 fsurdat='$fsurdat'
 finidat = '$finidat'
 flanduse_timeseries = '$flanduse'
 do_transient_crops = .true.
 check_finidat_fsurdat_consistency = .false.
 check_finidat_year_consistency = .false.
 check_dynpft_consistency = .false.
 suplphos = 'ALL'
 do_budgets = .false.
 nyears_ad_carbon_only = 25
 spinup_mortality_factor = 10
EOF

cat >> user_nl_datm << EOF
 mapalgo = "nn", "nn", "nn", "nn", "nn", "nn"
EOF

# ----- Case setup -----
./xmlchange RUNDIR=${CASE_RUN_DIR}
./xmlchange ELM_USRDAT_NAME=US_Midwest_TEST
./xmlchange ATM_DOMAIN_PATH=${domainpath}
./xmlchange LND_DOMAIN_PATH=${domainpath}
./xmlchange ATM_DOMAIN_FILE=${domainfile}
./xmlchange LND_DOMAIN_FILE=${domainfile}
./xmlchange RUN_STARTDATE=${START_DATE}
./xmlchange RUN_TYPE=${MODEL_START_TYPE}
./xmlchange RUN_REFDIR=${RUN_REFDIR}
./xmlchange RUN_REFCASE=${RUN_REFCASE}
./xmlchange RUN_REFDATE=${RUN_REFDATE}
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=30
./xmlchange REST_N=5
./xmlchange DATM_CLMNCEP_YR_ALIGN='2070'
./xmlchange DATM_CLMNCEP_YR_START='2070'
./xmlchange DATM_CLMNCEP_YR_END='2099'
./xmlchange JOB_WALLCLOCK_TIME=10:00:00
./xmlchange MAX_MPITASKS_PER_NODE=128
./xmlchange MAX_TASKS_PER_NODE=128
./xmlchange NTASKS=1024

./case.setup

# Modify datm streams
cp ${CASE_SCRIPTS_DIR}/CaseDocs/datm.streams.txt.CLMGSWP3v1.Precip ${CASE_SCRIPTS_DIR}/user_datm.streams.txt.CLMGSWP3v1.Precip
cp ${CASE_SCRIPTS_DIR}/CaseDocs/datm.streams.txt.CLMGSWP3v1.Solar ${CASE_SCRIPTS_DIR}/user_datm.streams.txt.CLMGSWP3v1.Solar
cp ${CASE_SCRIPTS_DIR}/CaseDocs/datm.streams.txt.CLMGSWP3v1.TPQW ${CASE_SCRIPTS_DIR}/user_datm.streams.txt.CLMGSWP3v1.TPQW
chmod +rw ${CASE_SCRIPTS_DIR}/user_datm.streams.txt.CLMGSWP3v1.Precip
chmod +rw ${CASE_SCRIPTS_DIR}/user_datm.streams.txt.CLMGSWP3v1.Solar
chmod +rw ${CASE_SCRIPTS_DIR}/user_datm.streams.txt.CLMGSWP3v1.TPQW

# Modify content of datm streams
cat ${CASE_SCRIPTS_DIR}/user_datm.streams.txt.CLMGSWP3v1.Precip|sed s/clmforc.GSWP3.c2011.0.5x0.5.Prec/elmforc.AWEGEN_ssp585.Prec/g > tmpfile && mv tmpfile ${CASE_SCRIPTS_DIR}/user_datm.streams.txt.CLMGSWP3v1.Precip
cat ${CASE_SCRIPTS_DIR}/user_datm.streams.txt.CLMGSWP3v1.Solar|sed s/clmforc.GSWP3.c2011.0.5x0.5.Solr/elmforc.AWEGEN_ssp585.Solr/g > tmpfile && mv tmpfile ${CASE_SCRIPTS_DIR}/user_datm.streams.txt.CLMGSWP3v1.Solar
cat ${CASE_SCRIPTS_DIR}/user_datm.streams.txt.CLMGSWP3v1.TPQW|sed s/clmforc.GSWP3.c2011.0.5x0.5.TPQWL/elmforc.AWEGEN_ssp585.TPQW/g > tmpfile && mv tmpfile ${CASE_SCRIPTS_DIR}/user_datm.streams.txt.CLMGSWP3v1.TPQW

cat ${CASE_SCRIPTS_DIR}/user_datm.streams.txt.CLMGSWP3v1.Precip|sed s/domain.lnd.360x720_gswp3.0v1.c170606.nc/domain.lnd.domain.lnd.US_Midwest_noocean_230616.nc/g > tmpfile && mv tmpfile ${CASE_SCRIPTS_DIR}/user_datm.streams.txt.CLMGSWP3v1.Precip
cat ${CASE_SCRIPTS_DIR}/user_datm.streams.txt.CLMGSWP3v1.Solar|sed s/domain.lnd.360x720_gswp3.0v1.c170606.nc/domain.lnd.domain.lnd.US_Midwest_noocean_230616.nc/g > tmpfile && mv tmpfile ${CASE_SCRIPTS_DIR}/user_datm.streams.txt.CLMGSWP3v1.Solar
cat ${CASE_SCRIPTS_DIR}/user_datm.streams.txt.CLMGSWP3v1.TPQW|sed s/domain.lnd.360x720_gswp3.0v1.c170606.nc/domain.lnd.domain.lnd.US_Midwest_noocean_230616.nc/g > tmpfile && mv tmpfile ${CASE_SCRIPTS_DIR}/user_datm.streams.txt.CLMGSWP3v1.TPQW

cat ${CASE_SCRIPTS_DIR}/user_datm.streams.txt.CLMGSWP3v1.Precip|sed 's|global/cfs/cdirs/e3sm/inputdata/atm/datm7/atm_forcing.datm7.GSWP3.0.5d.v1.c170516/Precip|global/cfs/cdirs/e3sm/esinha/inputdata/atm/datm7/AWE-GEN/increase_temp_precip_std|' > tmpfile && mv tmpfile ${CASE_SCRIPTS_DIR}/user_datm.streams.txt.CLMGSWP3v1.Precip
cat ${CASE_SCRIPTS_DIR}/user_datm.streams.txt.CLMGSWP3v1.Solar|sed 's|global/cfs/cdirs/e3sm/inputdata/atm/datm7/atm_forcing.datm7.GSWP3.0.5d.v1.c170516/Solar|global/cfs/cdirs/e3sm/esinha/inputdata/atm/datm7/AWE-GEN/increase_temp_precip_std|' > tmpfile && mv tmpfile ${CASE_SCRIPTS_DIR}/user_datm.streams.txt.CLMGSWP3v1.Solar
cat ${CASE_SCRIPTS_DIR}/user_datm.streams.txt.CLMGSWP3v1.TPQW|sed 's|global/cfs/cdirs/e3sm/inputdata/atm/datm7/atm_forcing.datm7.GSWP3.0.5d.v1.c170516/TPHWL|global/cfs/cdirs/e3sm/esinha/inputdata/atm/datm7/AWE-GEN/increase_temp_precip_std|' > tmpfile && mv tmpfile ${CASE_SCRIPTS_DIR}/user_datm.streams.txt.CLMGSWP3v1.TPQW

cat ${CASE_SCRIPTS_DIR}/user_datm.streams.txt.CLMGSWP3v1.Precip|sed 's|global/cfs/cdirs/e3sm/inputdata/atm/datm7/atm_forcing.datm7.GSWP3.0.5d.v1.c170516|global/cfs/cdirs/e3sm/esinha/inputdata/lnd/clm2/surfdata_map|' > tmpfile && mv tmpfile ${CASE_SCRIPTS_DIR}/user_datm.streams.txt.CLMGSWP3v1.Precip
cat ${CASE_SCRIPTS_DIR}/user_datm.streams.txt.CLMGSWP3v1.Solar|sed 's|global/cfs/cdirs/e3sm/inputdata/atm/datm7/atm_forcing.datm7.GSWP3.0.5d.v1.c170516|global/cfs/cdirs/e3sm/esinha/inputdata/lnd/clm2/surfdata_map|' > tmpfile && mv tmpfile ${CASE_SCRIPTS_DIR}/user_datm.streams.txt.CLMGSWP3v1.Solar
cat ${CASE_SCRIPTS_DIR}/user_datm.streams.txt.CLMGSWP3v1.TPQW|sed 's|global/cfs/cdirs/e3sm/inputdata/atm/datm7/atm_forcing.datm7.GSWP3.0.5d.v1.c170516|global/cfs/cdirs/e3sm/esinha/inputdata/lnd/clm2/surfdata_map|' > tmpfile && mv tmpfile ${CASE_SCRIPTS_DIR}/user_datm.streams.txt.CLMGSWP3v1.TPQW

sed -i '/FLDS/d' ${CASE_SCRIPTS_DIR}/user_datm.streams.txt.CLMGSWP3v1.TPQW

# ----- Case build -----
./case.build

# ----- Run model -----
./case.submit
