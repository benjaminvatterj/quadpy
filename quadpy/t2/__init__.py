from ..tn import get_vol, transform
from ._albrecht_collatz import albrecht_collatz
from ._berntsen_espelid import (
    berntsen_espelid_1,
    berntsen_espelid_2,
    berntsen_espelid_3,
    berntsen_espelid_4,
    dcutri,
)
from ._centroid import centroid
from ._cools_haegemans import cools_haegemans_1  # cools_haegemans_2
from ._cubtri import cubtri
from ._dunavant import (
    dunavant_01,
    dunavant_02,
    dunavant_03,
    dunavant_04,
    dunavant_05,
    dunavant_06,
    dunavant_07,
    dunavant_08,
    dunavant_09,
    dunavant_10,
    dunavant_11,
    dunavant_12,
    dunavant_13,
    dunavant_14,
    dunavant_15,
    dunavant_16,
    dunavant_17,
    dunavant_18,
    dunavant_19,
    dunavant_20,
)
from ._franke import franke_09, franke_10
from ._gatermann import gatermann
from ._griener_schmid import griener_schmid_1, griener_schmid_2
from ._hammer_marlowe_stroud import (
    hammer_marlowe_stroud_1,
    hammer_marlowe_stroud_2,
    hammer_marlowe_stroud_3,
    hammer_marlowe_stroud_4,
    hammer_marlowe_stroud_5,
)
from ._hammer_stroud import hammer_stroud_2, hammer_stroud_3
from ._hillion import (
    hillion_01,
    hillion_02,
    hillion_03,
    hillion_04,
    hillion_05,
    hillion_06,
    hillion_07,
    hillion_08,
    hillion_09,
    hillion_10,
)
from ._laursen_gellert import (
    laursen_gellert_01,
    laursen_gellert_02a,
    laursen_gellert_02b,
    laursen_gellert_03,
    laursen_gellert_04,
    laursen_gellert_05,
    laursen_gellert_06,
    laursen_gellert_07,
    laursen_gellert_08,
    laursen_gellert_09,
    laursen_gellert_10,
    laursen_gellert_11,
    laursen_gellert_12,
    laursen_gellert_13,
    laursen_gellert_14,
    laursen_gellert_15a,
    laursen_gellert_15b,
)
from ._lether import lether
from ._liu_vinokur import (
    liu_vinokur_01,
    liu_vinokur_02,
    liu_vinokur_03,
    liu_vinokur_04,
    liu_vinokur_05,
    liu_vinokur_06,
    liu_vinokur_07,
    liu_vinokur_08,
    liu_vinokur_09,
    liu_vinokur_10,
    liu_vinokur_11,
    liu_vinokur_12,
    liu_vinokur_13,
)
from ._lyness_jespersen import (
    lyness_jespersen_01,
    lyness_jespersen_02,
    lyness_jespersen_03,
    lyness_jespersen_04,
    lyness_jespersen_05,
    lyness_jespersen_06,
    lyness_jespersen_07,
    lyness_jespersen_08,
    lyness_jespersen_09,
    lyness_jespersen_10,
    lyness_jespersen_11,
    lyness_jespersen_12,
    lyness_jespersen_13,
    lyness_jespersen_14,
    lyness_jespersen_15,
    lyness_jespersen_16,
    lyness_jespersen_17,
    lyness_jespersen_18,
    lyness_jespersen_19,
    lyness_jespersen_20,
    lyness_jespersen_21,
)
from ._papanicolopulos import (
    papanicolopulos_rot_08,  #
    papanicolopulos_rot_09,
    papanicolopulos_rot_10,
    papanicolopulos_rot_11,
    papanicolopulos_rot_12,
    papanicolopulos_rot_13,
    papanicolopulos_rot_14,
    papanicolopulos_rot_15,
    papanicolopulos_rot_16,
    papanicolopulos_rot_17,
    papanicolopulos_sym_0,
    papanicolopulos_sym_1,
    papanicolopulos_sym_2,
    papanicolopulos_sym_3,
    papanicolopulos_sym_4,
    papanicolopulos_sym_5,
    papanicolopulos_sym_6,
    papanicolopulos_sym_7,
    papanicolopulos_sym_8,
)
from ._seven_point import seven_point
from ._strang_fix_cowper import (
    strang_fix_cowper_01,
    strang_fix_cowper_02,
    strang_fix_cowper_03,
    strang_fix_cowper_04,
    strang_fix_cowper_05,
    strang_fix_cowper_06,
    strang_fix_cowper_07,
    strang_fix_cowper_08,
    strang_fix_cowper_09,
    strang_fix_cowper_10,
)
from ._stroud import stroud_t2_3_1, stroud_t2_5_1, stroud_t2_7_1
from ._taylor_wingate_bos import (
    taylor_wingate_bos_1,
    taylor_wingate_bos_2,
    taylor_wingate_bos_4,
    taylor_wingate_bos_5,
    taylor_wingate_bos_8,
)
from ._tools import integrate_adaptive
from ._triex import triex_19, triex_28
from ._vertex import vertex
from ._vioreanu_rokhlin import (
    vioreanu_rokhlin_00,
    vioreanu_rokhlin_01,
    vioreanu_rokhlin_02,
    vioreanu_rokhlin_03,
    vioreanu_rokhlin_04,
    vioreanu_rokhlin_05,
    vioreanu_rokhlin_06,
    vioreanu_rokhlin_07,
    vioreanu_rokhlin_08,
    vioreanu_rokhlin_09,
    vioreanu_rokhlin_10,
    vioreanu_rokhlin_11,
    vioreanu_rokhlin_12,
    vioreanu_rokhlin_13,
    vioreanu_rokhlin_14,
    vioreanu_rokhlin_15,
    vioreanu_rokhlin_16,
    vioreanu_rokhlin_17,
    vioreanu_rokhlin_18,
    vioreanu_rokhlin_19,
)
from ._walkington import walkington_p5
from ._wandzura_xiao import (
    wandzura_xiao_1,
    wandzura_xiao_2,
    wandzura_xiao_3,
    wandzura_xiao_4,
    wandzura_xiao_5,
    wandzura_xiao_6,
)
from ._williams_shunn_jameson import (
    williams_shunn_jameson_1,
    williams_shunn_jameson_2,
    williams_shunn_jameson_3,
    williams_shunn_jameson_4,
    williams_shunn_jameson_5,
    williams_shunn_jameson_6,
    williams_shunn_jameson_7,
    williams_shunn_jameson_8,
)
from ._witherden_vincent import witherden_vincent_01  # witherden_vincent_03,
from ._witherden_vincent import (
    witherden_vincent_02,
    witherden_vincent_04,
    witherden_vincent_05,
    witherden_vincent_06,
    witherden_vincent_07,
    witherden_vincent_08,
    witherden_vincent_09,
    witherden_vincent_10,
    witherden_vincent_11,
    witherden_vincent_12,
    witherden_vincent_13,
    witherden_vincent_14,
    witherden_vincent_15,
    witherden_vincent_16,
    witherden_vincent_17,
    witherden_vincent_18,
    witherden_vincent_19,
    witherden_vincent_20,
)
from ._xiao_gimbutas import (
    xiao_gimbutas_01,
    xiao_gimbutas_02,
    xiao_gimbutas_03,
    xiao_gimbutas_04,
    xiao_gimbutas_05,
    xiao_gimbutas_06,
    xiao_gimbutas_07,
    xiao_gimbutas_08,
    xiao_gimbutas_09,
    xiao_gimbutas_10,
    xiao_gimbutas_11,
    xiao_gimbutas_12,
    xiao_gimbutas_13,
    xiao_gimbutas_14,
    xiao_gimbutas_15,
    xiao_gimbutas_16,
    xiao_gimbutas_17,
    xiao_gimbutas_18,
    xiao_gimbutas_19,
    xiao_gimbutas_20,
    xiao_gimbutas_21,
    xiao_gimbutas_22,
    xiao_gimbutas_23,
    xiao_gimbutas_24,
    xiao_gimbutas_25,
    xiao_gimbutas_26,
    xiao_gimbutas_27,
    xiao_gimbutas_28,
    xiao_gimbutas_29,
    xiao_gimbutas_30,
    xiao_gimbutas_31,
    xiao_gimbutas_32,
    xiao_gimbutas_33,
    xiao_gimbutas_34,
    xiao_gimbutas_35,
    xiao_gimbutas_36,
    xiao_gimbutas_37,
    xiao_gimbutas_38,
    xiao_gimbutas_39,
    xiao_gimbutas_40,
    xiao_gimbutas_41,
    xiao_gimbutas_42,
    xiao_gimbutas_43,
    xiao_gimbutas_44,
    xiao_gimbutas_45,
    xiao_gimbutas_46,
    xiao_gimbutas_47,
    xiao_gimbutas_48,
    xiao_gimbutas_49,
    xiao_gimbutas_50,
)
from ._zhang_cui_liu import zhang_cui_liu_1, zhang_cui_liu_2, zhang_cui_liu_3

__all__ = [
    "albrecht_collatz",
    "centroid",
    "cools_haegemans_1",
    # "cools_haegemans_2",
    "cubtri",
    "berntsen_espelid_1",
    "berntsen_espelid_2",
    "berntsen_espelid_3",
    "berntsen_espelid_4",
    "dcutri",
    "dunavant_01",
    "dunavant_02",
    "dunavant_03",
    "dunavant_04",
    "dunavant_05",
    "dunavant_06",
    "dunavant_07",
    "dunavant_08",
    "dunavant_09",
    "dunavant_10",
    "dunavant_11",
    "dunavant_12",
    "dunavant_13",
    "dunavant_14",
    "dunavant_15",
    "dunavant_16",
    "dunavant_17",
    "dunavant_18",
    "dunavant_19",
    "dunavant_20",
    "franke_09",
    "franke_10",
    "gatermann",
    "griener_schmid_1",
    "griener_schmid_2",
    "hammer_marlowe_stroud_1",
    "hammer_marlowe_stroud_2",
    "hammer_marlowe_stroud_3",
    "hammer_marlowe_stroud_4",
    "hammer_marlowe_stroud_5",
    "hammer_stroud_2",
    "hammer_stroud_3",
    "hillion_01",
    "hillion_02",
    "hillion_03",
    "hillion_04",
    "hillion_05",
    "hillion_06",
    "hillion_07",
    "hillion_08",
    "hillion_09",
    "hillion_10",
    "laursen_gellert_01",
    "laursen_gellert_02a",
    "laursen_gellert_02b",
    "laursen_gellert_03",
    "laursen_gellert_04",
    "laursen_gellert_05",
    "laursen_gellert_06",
    "laursen_gellert_07",
    "laursen_gellert_08",
    "laursen_gellert_09",
    "laursen_gellert_10",
    "laursen_gellert_11",
    "laursen_gellert_12",
    "laursen_gellert_13",
    "laursen_gellert_14",
    "laursen_gellert_15a",
    "laursen_gellert_15b",
    "lether",
    "liu_vinokur_01",
    "liu_vinokur_02",
    "liu_vinokur_03",
    "liu_vinokur_04",
    "liu_vinokur_05",
    "liu_vinokur_06",
    "liu_vinokur_07",
    "liu_vinokur_08",
    "liu_vinokur_09",
    "liu_vinokur_10",
    "liu_vinokur_11",
    "liu_vinokur_12",
    "liu_vinokur_13",
    "lyness_jespersen_01",
    "lyness_jespersen_02",
    "lyness_jespersen_03",
    "lyness_jespersen_04",
    "lyness_jespersen_05",
    "lyness_jespersen_06",
    "lyness_jespersen_07",
    "lyness_jespersen_08",
    "lyness_jespersen_09",
    "lyness_jespersen_10",
    "lyness_jespersen_11",
    "lyness_jespersen_12",
    "lyness_jespersen_13",
    "lyness_jespersen_14",
    "lyness_jespersen_15",
    "lyness_jespersen_16",
    "lyness_jespersen_17",
    "lyness_jespersen_18",
    "lyness_jespersen_19",
    "lyness_jespersen_20",
    "lyness_jespersen_21",
    "newton_cotes_closed",
    "newton_cotes_open",
    "papanicolopulos_sym_0",
    "papanicolopulos_sym_1",
    "papanicolopulos_sym_2",
    "papanicolopulos_sym_3",
    "papanicolopulos_sym_4",
    "papanicolopulos_sym_5",
    "papanicolopulos_sym_6",
    "papanicolopulos_sym_7",
    "papanicolopulos_sym_8",
    "papanicolopulos_rot_08",
    "papanicolopulos_rot_09",
    "papanicolopulos_rot_10",
    "papanicolopulos_rot_11",
    "papanicolopulos_rot_12",
    "papanicolopulos_rot_13",
    "papanicolopulos_rot_14",
    "papanicolopulos_rot_15",
    "papanicolopulos_rot_16",
    "papanicolopulos_rot_17",
    "seven_point",
    "sunder_cookson_01",
    "sunder_cookson_02",
    "sunder_cookson_03",
    "sunder_cookson_04",
    "sunder_cookson_05",
    "strang_fix_cowper_01",
    "strang_fix_cowper_02",
    "strang_fix_cowper_03",
    "strang_fix_cowper_04",
    "strang_fix_cowper_05",
    "strang_fix_cowper_06",
    "strang_fix_cowper_07",
    "strang_fix_cowper_08",
    "strang_fix_cowper_09",
    "strang_fix_cowper_10",
    "stroud_t2_3_1",
    "stroud_t2_5_1",
    "stroud_t2_7_1",
    "taylor_wingate_bos_1",
    "taylor_wingate_bos_2",
    "taylor_wingate_bos_4",
    "taylor_wingate_bos_5",
    "taylor_wingate_bos_8",
    "triex_19",
    "triex_28",
    "vertex",
    "vioreanu_rokhlin_00",
    "vioreanu_rokhlin_01",
    "vioreanu_rokhlin_02",
    "vioreanu_rokhlin_03",
    "vioreanu_rokhlin_04",
    "vioreanu_rokhlin_05",
    "vioreanu_rokhlin_06",
    "vioreanu_rokhlin_07",
    "vioreanu_rokhlin_08",
    "vioreanu_rokhlin_09",
    "vioreanu_rokhlin_10",
    "vioreanu_rokhlin_11",
    "vioreanu_rokhlin_12",
    "vioreanu_rokhlin_13",
    "vioreanu_rokhlin_14",
    "vioreanu_rokhlin_15",
    "vioreanu_rokhlin_16",
    "vioreanu_rokhlin_17",
    "vioreanu_rokhlin_18",
    "vioreanu_rokhlin_19",
    "walkington_p5",
    "wandzura_xiao_1",
    "wandzura_xiao_2",
    "wandzura_xiao_3",
    "wandzura_xiao_4",
    "wandzura_xiao_5",
    "wandzura_xiao_6",
    "williams_shunn_jameson_1",
    "williams_shunn_jameson_2",
    "williams_shunn_jameson_3",
    "williams_shunn_jameson_4",
    "williams_shunn_jameson_5",
    "williams_shunn_jameson_6",
    "williams_shunn_jameson_7",
    "williams_shunn_jameson_8",
    "witherden_vincent_01",
    "witherden_vincent_02",
    # "witherden_vincent_03",,
    "witherden_vincent_04",
    "witherden_vincent_05",
    "witherden_vincent_06",
    "witherden_vincent_07",
    "witherden_vincent_08",
    "witherden_vincent_09",
    "witherden_vincent_10",
    "witherden_vincent_11",
    "witherden_vincent_12",
    "witherden_vincent_13",
    "witherden_vincent_14",
    "witherden_vincent_15",
    "witherden_vincent_16",
    "witherden_vincent_17",
    "witherden_vincent_18",
    "witherden_vincent_19",
    "witherden_vincent_20",
    "xiao_gimbutas_01",
    "xiao_gimbutas_02",
    "xiao_gimbutas_03",
    "xiao_gimbutas_04",
    "xiao_gimbutas_05",
    "xiao_gimbutas_06",
    "xiao_gimbutas_07",
    "xiao_gimbutas_08",
    "xiao_gimbutas_09",
    "xiao_gimbutas_10",
    "xiao_gimbutas_11",
    "xiao_gimbutas_12",
    "xiao_gimbutas_13",
    "xiao_gimbutas_14",
    "xiao_gimbutas_15",
    "xiao_gimbutas_16",
    "xiao_gimbutas_17",
    "xiao_gimbutas_18",
    "xiao_gimbutas_19",
    "xiao_gimbutas_20",
    "xiao_gimbutas_21",
    "xiao_gimbutas_22",
    "xiao_gimbutas_23",
    "xiao_gimbutas_24",
    "xiao_gimbutas_25",
    "xiao_gimbutas_26",
    "xiao_gimbutas_27",
    "xiao_gimbutas_28",
    "xiao_gimbutas_29",
    "xiao_gimbutas_30",
    "xiao_gimbutas_31",
    "xiao_gimbutas_32",
    "xiao_gimbutas_33",
    "xiao_gimbutas_34",
    "xiao_gimbutas_35",
    "xiao_gimbutas_36",
    "xiao_gimbutas_37",
    "xiao_gimbutas_38",
    "xiao_gimbutas_39",
    "xiao_gimbutas_40",
    "xiao_gimbutas_41",
    "xiao_gimbutas_42",
    "xiao_gimbutas_43",
    "xiao_gimbutas_44",
    "xiao_gimbutas_45",
    "xiao_gimbutas_46",
    "xiao_gimbutas_47",
    "xiao_gimbutas_48",
    "xiao_gimbutas_49",
    "xiao_gimbutas_50",
    "zhang_cui_liu_1",
    "zhang_cui_liu_2",
    "zhang_cui_liu_3",
    #
    "integrate_adaptive",
    "transform",
    "get_vol",
]
