#define MAT_EXM
#define ACTION_DIRECT
//#define SELECT_INDIRECT
#define STAT_INDIRECT
#define METER_INDIRECT


#define MAT_COUNT 65536
#define ACTION_COUNT 32768
#define SELECT_COUNT 32768
#define STAT_COUNT 16384
#define METER_COUNT 500 







// Unsupported configs
#ifdef SELECT_INDIRECT
#ifdef ACTION_INDIRECT
Unsupported
#endif
#endif

#if !defined(MAT_EXM) && !defined(MAT_TCAM)
Unsupported
#endif

#if defined(METER_DIRECT) || defined(METER_INDIRECT)
#if defined(SELECT_INDIRECT) || defined(SFUL_DIRECT) || defined(SFUL_INDIRECT)
Unsupported
#endif
#endif

#if defined(SELECT_INDIRECT)
#if defined(METER_DIRECT) || defined(METER_INDIRECT) || defined(SFUL_DIRECT) || defined(SFUL_INDIRECT)
Unsupported
#endif
#endif

#if defined(SFUL_DIRECT) || defined(SFUL_INDIRECT)
#if defined(SELECT_INDIRECT) || defined(METER_DIRECT) || defined(METER_INDIRECT)
Unsupported
#endif
#endif

