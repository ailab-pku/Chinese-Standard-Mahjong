#include <Python.h>
#include <string>
#include <unordered_map>
#include "../ChineseOfficialMahjongHelper/Classes/mahjong-algorithm/fan_calculator.h"

using namespace std;

static unordered_map<string, mahjong::tile_t> str2tile;

static void MahjongInit() {
	for(int i = 1; i <= 9; ++i) {
		str2tile["W" + to_string(i)] = mahjong::make_tile(TILE_SUIT_CHARACTERS, i);
		str2tile["B" + to_string(i)] = mahjong::make_tile(TILE_SUIT_DOTS, i);
		str2tile["T" + to_string(i)] = mahjong::make_tile(TILE_SUIT_BAMBOO, i);
	}
	for(int i = 1; i <= 4; ++i)
		str2tile["F" + to_string(i)] = mahjong::make_tile(TILE_SUIT_HONORS, i);
	for(int i = 1; i <= 3; ++i)
		str2tile["J" + to_string(i)] = mahjong::make_tile(TILE_SUIT_HONORS, i + 4);
}

static const char *doc = "Calculate Mahjong Fans.\n"
"Parameters:\n"
"\tpack - A tuple of fixed packs, each of which is a tuple of form (\"CHI\"/\"PENG\"/\"GANG\", tile, offer:0..3);\n"
"\thand - A tuple of standing tiles;\n"
"\twinTile - Winning Tile;\n"
"\tflowerCount - Number of flower tiles;\n"
"\tisSelfDrawn - bool indicate self drawn;\n"
"\tis4thTileDrawn - bool indicate 4th tile;\n"
"\tisAboutKong - bool indicate about kong;\n"
"\tisWallLast - bool indicate wall last;\n"
"\tseatWind - seat wind of 0..3 indicate east/south/west/north;\n"
"\tprevalentWind - prevalent wind of 0..3 indicate east/south/west/north.\n"
"Returns:\n"
"\tA tuple of fans, each of which is a tuple of form (fan_count, fan_name).\n"
"Raises:"
"\tTypeError - If any invalid input is encountered.\n";

static PyObject *MahjongFanCalculator(PyObject *self, PyObject *args, PyObject *kwargs) {
	try {
		// Parse arguments
		static char *kwlist[] = {"pack", "hand", "winTile", "flowerCount"
			, "isSelfDrawn", "is4thTile", "isAboutKong", "isWallLast"
			, "seatWind", "prevalentWind", nullptr};
		PyObject *packs = nullptr, *hands = nullptr;
		const char *winTile = nullptr;
		int flowerCount, isSelfDrawn, is4thTile, isAboutKong, isWallLast, seatWind, prevalentWind;
		if(!PyArg_ParseTupleAndKeywords(args, kwargs, "OOsippppii", kwlist
			, &packs, &hands, &winTile, &flowerCount
			, &isSelfDrawn, &is4thTile, &isAboutKong, &isWallLast, &seatWind, &prevalentWind))
			return nullptr;
		// Prepare params
		mahjong::calculate_param_t calculate_param = {};
		// Parse pack tuple
		if(!PyTuple_Check(packs)) throw "Param `pack` must be a tuple!";
		int packSize = PyTuple_Size(packs);
		calculate_param.hand_tiles.pack_count = packSize;
		for(int i = 0; i < packSize; ++i) {
			// Parse pack info
			PyObject *pack = PyTuple_GET_ITEM(packs, i);
			if(!PyTuple_Check(pack)) throw "Param `pack` must be a tuple of tuples!";
			const char *type = nullptr, *tile = nullptr;
			int offer, packCode;
			if(!PyArg_ParseTuple(pack, "ssi", &type, &tile, &offer)) return nullptr;
			if(str2tile.find(tile) == str2tile.end()) throw "ERROE_WRONG_TILE_CODE";
			if(offer < 0 || offer >= 4) throw "ERROE_WRONG_OFFER_CODE";
			if(!strcmp(type, "PENG")) packCode = PACK_TYPE_PUNG;
			else if(!strcmp(type, "GANG")) packCode = PACK_TYPE_KONG;
			else if(!strcmp(type, "CHI")) packCode = PACK_TYPE_CHOW;
			else throw "ERROE_WRONG_PACK_CODE";
			calculate_param.hand_tiles.fixed_packs[i] = mahjong::make_pack(offer, packCode, str2tile[tile]);
		}
		// Parse hand tuple
		if(!PyTuple_Check(hands)) throw "Param `hand` must be a tuple!";
		int handSize = PyTuple_Size(hands);
		calculate_param.hand_tiles.tile_count = handSize;
		for(int i = 0; i < handSize; ++i) {
			// Parse hand tile
			PyObject *hand = PyTuple_GET_ITEM(hands, i);
			if(!PyUnicode_Check(hand)) throw "Param `hand` must be a tuple of strs!";
			const char *tile = PyUnicode_AsUTF8(hand);
			if(str2tile.find(tile) == str2tile.end()) throw "ERROE_WRONG_TILE_CODE";
			calculate_param.hand_tiles.standing_tiles[i] = str2tile[tile];
		}
		// Other params
		if(str2tile.find(winTile) == str2tile.end()) throw "ERROE_WRONG_TILE_CODE";
		calculate_param.win_tile = str2tile[winTile];
		calculate_param.flower_count = flowerCount;
		calculate_param.win_flag = 
			isSelfDrawn * WIN_FLAG_SELF_DRAWN +
			is4thTile * WIN_FLAG_4TH_TILE +
			isAboutKong * WIN_FLAG_ABOUT_KONG +
			isWallLast * WIN_FLAG_WALL_LAST;
		calculate_param.seat_wind = (mahjong::wind_t)seatWind;
		calculate_param.prevalent_wind = (mahjong::wind_t)prevalentWind;
		// Prepare results
		mahjong::fan_table_t fan_table = {};
		int re = mahjong::calculate_fan(&calculate_param, &fan_table);
		switch(re) {
			case -1: throw "ERROR_WRONG_TILES_COUNT";
			case -2: throw "ERROR_TILE_COUNT_GREATER_THAN_4";
			case -3: throw "ERROR_NOT_WIN";
		}
		int l = 0;
		for(int i = 0; i < mahjong::FAN_TABLE_SIZE; i++)
			if(fan_table[i]) ++l;
		PyObject *ans = PyTuple_New(l);
		l = 0;
		for(int i = 0; i < mahjong::FAN_TABLE_SIZE; i++)
			if(fan_table[i]) {
				PyObject *item = Py_BuildValue("(is)", mahjong::fan_value_table[i] * fan_table[i], mahjong::fan_name[i]);
				PyTuple_SetItem(ans, l++, item);
			}
		return ans;
	} catch (const char *msg) {
		PyErr_SetString(PyExc_TypeError, msg);
		return nullptr;
	}
}

static PyMethodDef methods[] = {
	{"MahjongFanCalculator", (PyCFunction)(void(*)(void))MahjongFanCalculator, METH_VARARGS | METH_KEYWORDS, doc},
	{NULL, NULL, 0, NULL},
};

static PyModuleDef module = {
    PyModuleDef_HEAD_INIT,
    "MahjongGB",
    "Library to calculate fans in Chinese Standard Mahjong.",
    -1,
    methods,
};
PyMODINIT_FUNC
PyInit_MahjongGB(void) {
    MahjongInit();
    return PyModule_Create(&module);
}