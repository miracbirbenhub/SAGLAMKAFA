import app
# option
##frodo_fix58
INPUT_IGNORE = 0
INV_WITH_SPLIT = 0
indexver = 0
IN_GAME_SHOP_ENABLE = 1
CONSOLE_ENABLE = 0
UmutBalikTaskbar = 0
Vectors = ''
YangDrop = 1
switchbot = 0
BOSS_TRACKING = 0
bosstracking = 0
LOAD_CURTAIN = 0
premium = 0
premiumgoster = 1


if app.ENABLE_SEND_TARGET_INFO:
	MONSTER_INFO_DATA = {}

if app.ENABLE_REFINE_RENEWAL:
	IS_AUTO_REFINE = False
	AUTO_REFINE_TYPE = 0
	AUTO_REFINE_DATA = {
		"ITEM" : [-1, -1],
		"NPC" : [0, -1, -1, 0]
	}
	
if app.ENABLE_MAINTENANCE_SYSTEM:
	MAINTENANCEADMIN_OPEN = 0

if app.ENABLE_CUBE_RENEWAL:
	CUBE_RENEWAL_IS_OPENED = 0
	cube_count_items = {}
	
if app.ENABLE_AUTO_SHOUT:
	auto_shout_status = 0
	auto_shout_text = ""

IS_BONUS_CHANGER = FALSE

BK_STYLE = 1
RUH_TASI_STYLE = 1

INPUT = 0
CLIENT_YOL = "lib/"
CONFIG_YOL = "locale/tr/ui/config/"

if app.ENABLE_ITEM_DELETE_SYSTEM:
	silme = 0
	ITEM_DELETE_LIST = {}
CHAL_DATA = []

if app.ENABLE_ITEM_OFFER:
	EXCHANGE_YANG_DATA = []
	EXCHANGE_YANG_DATA2 = []
	ITEM_OFFER_DATA = []
	ITEM_OFFER_DATA2 = []

missions_bp = {}
info_missions_bp = {}
rewards_bp = {}
final_rewards = []
size_battle_pass = 0
status_battle_pass = 0

auto_pick_item = 1
auto_pick_yang = 1
AffectShowHide = 1
depolar = 1

ITEM_DATA = {}
ITEM_SEARCH_DATA = []
NEW_INGAME_SHOP=0

ENABLE_MULTI_RANKING=1
py_Flag = {}
def GetFlag(flagname):
	global py_Flag
	return py_Flag.get(flagname, None)
def SetFlag(flagname,value):
	global py_Flag
	py_Flag[flagname] = value

PVPMODE_ENABLE = 1
PVPMODE_TEST_ENABLE = 0
PVPMODE_ACCELKEY_ENABLE = 1
PVPMODE_ACCELKEY_DELAY = 0.5
PVPMODE_PROTECTED_LEVEL = 30

FOG_LEVEL0 = 4800.0
FOG_LEVEL1 = 9600.0
FOG_LEVEL2 = 12800.0
FOG_LEVEL = FOG_LEVEL0
FOG_LEVEL_LIST=[FOG_LEVEL0, FOG_LEVEL1, FOG_LEVEL2]		

CAMERA_MAX_DISTANCE_SHORT = 2500.0
CAMERA_MAX_DISTANCE_LONG = 3500.0
CAMERA_MAX_DISTANCE_LIST=[CAMERA_MAX_DISTANCE_SHORT, CAMERA_MAX_DISTANCE_LONG]
CAMERA_MAX_DISTANCE = CAMERA_MAX_DISTANCE_SHORT

CHRNAME_COLOR_INDEX = 0

ENVIRONMENT_NIGHT="d:/ymir work/environment/moonlight04.msenv"

DAILY_REWARD_COLLECT1 = 0
DAILY_REWARD_COLLECT2 = 0
DAILY_REWARD_COLLECT3 = 0
DAILY_REWARD_COLLECT4 = 0
DAILY_REWARD_COLLECT5 = 0
DAILY_REWARD_COLLECT6 = 0
DAILY_REWARD_COLLECT7 = 0

daily_reward_left_time = 0

daily_reward = {
				
					0	:	[0,0],
					1	:	[70026,1],
					2	:	[70026,1],
					3	:	[70026,1],
					4	:	[70026,1],
					5	:	[70026,1],
					6	:	[70026,1],
					7	:	[70026,1]
				}

biyologinfo = {
						# 0	: ["biyolog", "Gün", "Başlangıç Saati", Başlangıç Dakika, Bitiş Saati, "Bitiş Dakika","İtem","Tür","Drop","Seviye"],
						0	: ["Görev Yok", "Yok", "Yok", "Yok"],
						30006	: ["Ork Dişi", "Hareket Hızı +%10", "Yok", "Yok"],
						30047	: ["Lanet Kitabı", "Saldırı Hızı +%5", "Yok", "Yok"],
						30015	: ["Şeytan Hatırası", "Savunma +60", "Yok", "Yok"],
						30050	: ["Buz Topu", "Saldırı Değeri +50", "Yok", "Yok"],
						30165	: ["Zelkova Dalı", "Hareket Hızı +%11", "Hasar Azaltma +%10", "Yok"],
						30166	: ["Tugyis Tabelası", "Saldırı Hızı +%6", "Saldırı Değeri +%10", "Yok"],
						30167	: ["Krm. Hayalet Ağaç Dalı", "Karakter Savunması +%10", "Yok", "Yok"],
						30168	: ["Liderin Notları", "Yarı İnsanlara Karşı Güç +%8", "Yok", "Yok"],
						30251	: ["Kemgöz Mücevheri", "Max HP +1000", "Savunma +120", "Saldırı Değeri +50"],
						30252	: ["Bilgelik Mücevheri", "Max HP +1100", "Savunma +140", "Saldırı Değeri +60"]
					}

# constant
HIGH_PRICE = 500000
MIDDLE_PRICE = 50000
ERROR_METIN_STONE = 28960
SUB2_LOADING_ENABLE = 1
EXPANDED_COMBO_ENABLE = 1
CONVERT_EMPIRE_LANGUAGE_ENABLE = 1
USE_ITEM_WEAPON_TABLE_ATTACK_BONUS = 0
ADD_DEF_BONUS_ENABLE = 1
LOGIN_COUNT_LIMIT_ENABLE = 0
DEPOZIT_QUESTINDEX = 0
ANTIEXP_QUESTINDEX = 0
TELEPORTER_QUESTINDEX = 0
MENU_BG = 0

USE_SKILL_EFFECT_UPGRADE_ENABLE = 1

VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD = 1
GUILD_MONEY_PER_GSP = 100
GUILD_WAR_TYPE_SELECT_ENABLE = 1
TWO_HANDED_WEAPON_ATT_SPEED_DECREASE_VALUE = 0

HAIR_COLOR_ENABLE = 1
ARMOR_SPECULAR_ENABLE = 1
WEAPON_SPECULAR_ENABLE = 1
SEQUENCE_PACKET_ENABLE = 1
KEEP_ACCOUNT_CONNETION_ENABLE = 1
MINIMAP_POSITIONINFO_ENABLE = 0
CONVERT_EMPIRE_LANGUAGE_ENABLE = 0
USE_ITEM_WEAPON_TABLE_ATTACK_BONUS = 0
ADD_DEF_BONUS_ENABLE = 0
LOGIN_COUNT_LIMIT_ENABLE = 0
PVPMODE_PROTECTED_LEVEL = 30
TWO_HANDED_WEAPON_ATT_SPEED_DECREASE_VALUE = 10

isItemQuestionDialog = 0

def GET_ITEM_QUESTION_DIALOG_STATUS():
	global isItemQuestionDialog
	return isItemQuestionDialog

def SET_ITEM_QUESTION_DIALOG_STATUS(flag):
	global isItemQuestionDialog
	isItemQuestionDialog = flag

import app
import net

########################

def SET_DEFAULT_FOG_LEVEL():
	global FOG_LEVEL
	app.SetMinFog(FOG_LEVEL)

def SET_FOG_LEVEL_INDEX(index):
	global FOG_LEVEL
	global FOG_LEVEL_LIST
	try:
		FOG_LEVEL=FOG_LEVEL_LIST[index]
	except IndexError:
		FOG_LEVEL=FOG_LEVEL_LIST[0]
	app.SetMinFog(FOG_LEVEL)

def GET_FOG_LEVEL_INDEX():
	global FOG_LEVEL
	global FOG_LEVEL_LIST
	return FOG_LEVEL_LIST.index(FOG_LEVEL)

########################

def SET_DEFAULT_CAMERA_MAX_DISTANCE():
	global CAMERA_MAX_DISTANCE
	app.SetCameraMaxDistance(CAMERA_MAX_DISTANCE)

def SET_CAMERA_MAX_DISTANCE_INDEX(index):
	global CAMERA_MAX_DISTANCE
	global CAMERA_MAX_DISTANCE_LIST
	try:
		CAMERA_MAX_DISTANCE=CAMERA_MAX_DISTANCE_LIST[index]
	except:
		CAMERA_MAX_DISTANCE=CAMERA_MAX_DISTANCE_LIST[0]

	app.SetCameraMaxDistance(CAMERA_MAX_DISTANCE)

def GET_CAMERA_MAX_DISTANCE_INDEX():
	global CAMERA_MAX_DISTANCE
	global CAMERA_MAX_DISTANCE_LIST
	return CAMERA_MAX_DISTANCE_LIST.index(CAMERA_MAX_DISTANCE)

########################

import chrmgr
import player
import app

def SET_DEFAULT_CHRNAME_COLOR():
	global CHRNAME_COLOR_INDEX
	chrmgr.SetEmpireNameMode(CHRNAME_COLOR_INDEX)

def SET_CHRNAME_COLOR_INDEX(index):
	global CHRNAME_COLOR_INDEX
	CHRNAME_COLOR_INDEX=index
	chrmgr.SetEmpireNameMode(index)

def GET_CHRNAME_COLOR_INDEX():
	global CHRNAME_COLOR_INDEX
	return CHRNAME_COLOR_INDEX

def SET_VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD(index):
	global VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD
	VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD = index

def GET_VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD():
	global VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD
	return VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD

def SET_DEFAULT_CONVERT_EMPIRE_LANGUAGE_ENABLE():
	global CONVERT_EMPIRE_LANGUAGE_ENABLE
	net.SetEmpireLanguageMode(CONVERT_EMPIRE_LANGUAGE_ENABLE)

def SET_DEFAULT_USE_ITEM_WEAPON_TABLE_ATTACK_BONUS():
	global USE_ITEM_WEAPON_TABLE_ATTACK_BONUS
	player.SetWeaponAttackBonusFlag(USE_ITEM_WEAPON_TABLE_ATTACK_BONUS)

def SET_DEFAULT_USE_SKILL_EFFECT_ENABLE():
	global USE_SKILL_EFFECT_UPGRADE_ENABLE
	app.SetSkillEffectUpgradeEnable(USE_SKILL_EFFECT_UPGRADE_ENABLE)

def SET_TWO_HANDED_WEAPON_ATT_SPEED_DECREASE_VALUE():
	global TWO_HANDED_WEAPON_ATT_SPEED_DECREASE_VALUE
	app.SetTwoHandedWeaponAttSpeedDecreaseValue(TWO_HANDED_WEAPON_ATT_SPEED_DECREASE_VALUE)

########################
import item

ACCESSORY_MATERIAL_LIST = [50623, 50624, 50625, 50626, 50627, 50628, 50629, 50630, 50631, 50632, 50633, 50634, 50635, 50636, 50637, 50638]
#ACCESSORY_MATERIAL_LIST = [50623, 50623, 50624, 50624, 50625, 50625, 50626, 50627, 50628, 50629, 50630, 50631, 50632, 50633, 
#			    50623, 50623, 50624, 50624, ]
JewelAccessoryInfos = [
		# jewel		wrist	neck	ear
		[ 50634,	14420,	16220,	17220 ],	
		[ 50635,	14500,	16500,	17500 ],	
		[ 50636,	14520,	16520,	17520 ],	
		[ 50637,	14540,	16540,	17540 ],	
		[ 50638,	14560,	16560,	17560 ],	
	]
def GET_ACCESSORY_MATERIAL_VNUM(vnum, subType):
	ret = vnum
	item_base = (vnum / 10) * 10
	for info in JewelAccessoryInfos:
		if item.ARMOR_WRIST == subType:	
			if info[1] == item_base:
				return info[0]
		elif item.ARMOR_NECK == subType:	
			if info[2] == item_base:
				return info[0]
		elif item.ARMOR_EAR == subType:	
			if info[3] == item_base:
				return info[0]
 
	if vnum >= 16210 and vnum <= 16219:
		return 50625

	if item.ARMOR_WRIST == subType:	
		WRIST_ITEM_VNUM_BASE = 14000
		ret -= WRIST_ITEM_VNUM_BASE
	elif item.ARMOR_NECK == subType:
		NECK_ITEM_VNUM_BASE = 16000
		ret -= NECK_ITEM_VNUM_BASE
	elif item.ARMOR_EAR == subType:
		EAR_ITEM_VNUM_BASE = 17000
		ret -= EAR_ITEM_VNUM_BASE

	type = ret/20

	if type<0 or type>=len(ACCESSORY_MATERIAL_LIST):
		type = (ret-170) / 20
		if type<0 or type>=len(ACCESSORY_MATERIAL_LIST):
			return 0

	return ACCESSORY_MATERIAL_LIST[type]

##################################################################
## »õ·Î Ãß°¡µÈ 'º§Æ®' ¾ÆÀÌÅÛ Å¸ÀÔ°ú, º§Æ®ÀÇ ¼ÒÄÏ¿¡ ²ÈÀ» ¾ÆÀÌÅÛ °ü·Ã.. 
## º§Æ®ÀÇ ¼ÒÄÏ½Ã½ºÅÛÀº ¾Ç¼¼¼­¸®¿Í µ¿ÀÏÇÏ±â ¶§¹®¿¡, À§ ¾Ç¼¼¼­¸® °ü·Ã ÇÏµåÄÚµùÃ³·³ ÀÌ·±½ÄÀ¸·Î ÇÒ ¼ö¹Û¿¡ ¾ø´Ù..

def GET_BELT_MATERIAL_VNUM(vnum, subType = 0):
	# ÇöÀç´Â ¸ğµç º§Æ®¿¡´Â ÇÏ³ªÀÇ ¾ÆÀÌÅÛ(#18900)¸¸ »ğÀÔ °¡´É
	return 18900

##################################################################
## ÀÚµ¿¹°¾à (HP: #72723 ~ #72726, SP: #72727 ~ #72730)

# ÇØ´ç vnumÀÌ ÀÚµ¿¹°¾àÀÎ°¡?
def IS_AUTO_POTION(itemVnum):
	return IS_AUTO_POTION_HP(itemVnum) or IS_AUTO_POTION_SP(itemVnum)
	
# ÇØ´ç vnumÀÌ HP ÀÚµ¿¹°¾àÀÎ°¡?
def IS_AUTO_POTION_HP(itemVnum):
	if 72723 <= itemVnum and 72726 >= itemVnum:
		return 1
	elif itemVnum >= 76021 and itemVnum <= 76022:		## »õ·Î µé¾î°£ ¼±¹°¿ë È­·æÀÇ Ãàº¹
		return 1
	elif itemVnum == 79012:
		return 1
		
	return 0
	
# ÇØ´ç vnumÀÌ SP ÀÚµ¿¹°¾àÀÎ°¡?
def IS_AUTO_POTION_SP(itemVnum):
	if 72727 <= itemVnum and 72730 >= itemVnum:
		return 1
	elif itemVnum >= 76004 and itemVnum <= 76005:		## »õ·Î µé¾î°£ ¼±¹°¿ë ¼ö·æÀÇ Ãàº¹
		return 1
	elif itemVnum == 79013:
		return 1
				
	return 0

def IS_UNLIMITED_ITEM(itemVnum):
	if itemVnum >= 71510 and itemVnum <= 71519:		## »õ·Î µé¾î°£ ¼±¹°¿ë ¼ö·æÀÇ Ãàº¹
		return 1
	elif itemVnum >= 71523 and itemVnum <= 71530:
		return 1
				
	return 0