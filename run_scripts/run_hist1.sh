# --- Configuration flags ----
# Modify the paths below to reflect correct directories
# Set paths
readonly BASE_DIR="/global/homes/e/${USER}/wrk/E3SM_projects"
readonly CODE_DIR="${BASE_DIR}/E3SM"
readonly INPUT_DATA_DIR="/global/cfs/cdirs/e3sm/${USER}/inputdata"
#readonly OUTPUT_DIR="/pscratch/sd/e/${USER}/e3sm_scratch/pm-cpu"
readonly OUTPUT_DIR="/global/cfs/cdirs/e3smdata/${USER}/"

# Simulation
readonly COMPSET="20TR_DATM%GSWP3v1_ELM%CN-CROP_SICE_SOCN_SROF_SGLC_SWAV"
readonly COMPSET_alias="I20TRGSWELMCNCROP"
readonly COMPSET_REST="I1850GSWELMCNCROP"
readonly RESOLUTION="ELM_USRDAT"
readonly MYDATE=$(date '+%Y%m%d')
readonly MYDATE_REST=20240318
readonly CASE_NAME="${MYDATE}_${RESOLUTION}_${COMPSET_alias}_hist1"

readonly CASE_ROOT="${OUTPUT_DIR}/${CASE_NAME}"
readonly CASE_SCRIPTS_DIR="${CASE_ROOT}/case_scripts"
readonly CASE_RUN_DIR="${CASE_ROOT}/run"

# Machine and project
readonly MACHINE=pm-cpu
readonly PROJECT="e3sm"

# Run options
readonly MODEL_START_TYPE="hybrid"  # 'initial', 'continue', 'branch', 'hybrid'
readonly START_DATE="1850-01-01"

readonly RUN_REFCASE="${MYDATE_REST}_${RESOLUTION}_${COMPSET_REST}_fnsp"
readonly RUN_REFDIR="${OUTPUT_DIR}/${RUN_REFCASE}/run"
readonly RUN_REFDATE="0601-01-01"

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

export fsurdat=${INPUT_DATA_DIR}/lnd/clm2/surfdata_map/surfdata_US_Midwest_0.25x0.25_50pfts_simyr1850_c240315.nc
export finidat=${RUN_REFDIR}/${RUN_REFCASE}.elm.r.${RUN_REFDATE}-00000.nc
export flanduse=${INPUT_DATA_DIR}/lnd/clm2/surfdata_map/landuse.timeseries_US_Midwest_0.25x0.25_hist_50pfts_simyr1850-2015_c240315.nc

export domainpath=${INPUT_DATA_DIR}/lnd/clm2/surfdata_map/
export domainfile=domain.lnd.US_Midwest_0.25x0.25_c240315.nc

cat >> user_nl_elm << EOF
&elm_inparm
 hist_mfilt = 365, 365
 hist_nhtfrq = -24, -24
 hist_dov2xy = .true., .false.
 hist_fincl2 = 'GPP', 'ER', 'NEE', 'NPP', 'NBP', 'TOTSOMC', 'DMYIELD', 'PLANTDAY', 'HARVESTDAY'
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
./xmlchange STOP_N=70
./xmlchange REST_N=10
./xmlchange JOB_WALLCLOCK_TIME=12:00:00
./xmlchange MAX_MPITASKS_PER_NODE=128
./xmlchange MAX_TASKS_PER_NODE=128
./xmlchange NTASKS=1024

# run case.setup
./case.setup

# run case.build
./case.build

# Run case.submit
./case.submit
