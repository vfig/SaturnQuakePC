//
// builtins.qc
//

float iscale;
vector isize;
vector dpos;
vector dsize;
string cprint_msg;
float cprint_timer;

// loading bar
float lbar_width;
vector lbar_size; // 124 x 12
vector lbar_pos;
vector lbar_color = [1, 0, 0];

string loading_bg = "gfx/loading_screens/qload.png";

// weapon viewsprite
string weapon_viewsprite;
vector weapon_viewsprite_pos;
vector weapon_viewsprite_size;

// status bar
string hud_sbar = "gfx/sbar";
string hud_ibar = "gfx/ibar";
string hud_scorebar = "gfx/scorebar";

string hud_ranking = "gfx/ranking.lmp";
string hud_complete = "gfx/complete.lmp";
string hud_intermission = "gfx/inter.lmp";
string hud_finale = "gfx/finale.lmp";

vector hud_sbar_pos = [0, 216];
vector hud_ibar_pos = [0, 192];
vector hud_sbar_size = [320, 24];
vector hud_ibar_size = [320, 24];

vector hud_ranking_size = [168, 24];
vector hud_complete_size = [192, 24];
vector hud_intermission_size = [160, 144];
vector hud_finale_size = [288, 24];

// adapted from V_CalcBob in the engine
float() CalcViewBob =
{
	float bob;
	float cycle;

	float mod = cvar("cl_bobcycle");
	float up = cvar("cl_bobup");
	float bobval = cvar("cl_bob");
	float pi = 3.1415926535;
	vector vel = pmove_vel / 1.5;
	
	if (mod <= 0)
		return 0.0f;
	
	cycle = time - (int)(time / mod) * mod;
	cycle /= mod;

    if (cycle < up)
        cycle = pi * cycle / up;
    else
        cycle = pi + pi * (cycle - up) / (1.0 - up);

    bob = sqrt(vel[0] * vel[0] + vel[1] * vel[1]) * bobval;
	bob = bob * 0.4 + bob * 0.7 * sin(cycle);

	if (bob > 16)
		bob = 16;
	else if (bob < 0)
		bob = 0;

	return bob;
};

void() DrawIntermission =
{
	setproperty(VF_DRAWCROSSHAIR, 0);
	if (intermission == 1)
	{
		drawpic([0, 0], hud_intermission, hud_intermission_size, [1, 1, 1], 1);
		drawpic([0, 0], hud_complete, hud_complete_size, [1, 1, 1], 1);
	}
	else if (intermission == 2)
	{
		drawpic([0, 0], hud_finale, hud_finale_size, [1, 1, 1], 1);
	}
};

void(float vwidth, float vheight, float notmenu) CSQC_UpdateView =
{
	clearscene();

	iscale = 1;
	
	float activeweaponframe = getstatf(STAT_WEAPONFRAME);
	float activeweapon = getstatf(STAT_ACTIVEWEAPON);

	if (cvar("r_saturnmode") != 0)
	{
		//cvar_set("cl_sbar", "1");
		//cvar_set("r_viewmodel_quake", "0");

		drawfontscale = [iscale, iscale, iscale];

		isize = [320 * iscale, 240 * iscale];

		drawfill([0, 0], [vwidth, vheight], [0, 0, 0], 1);
		setviewprop(VF_RT_DESTCOLOUR, "screenrt", -IMGFMT_R8G8B8A8, isize);
		setproperty(VF_VIEWPORT, [0, 0], isize);
	}

	if (cvar("r_saturnmode") != 0)
	{
		setproperty(VF_DRAWENGINESBAR, 0);
		setproperty(VF_DRAWWORLD, 1);
		addentities(MASK_ENGINE);
	}
	else
	{
		if (cvar("r_drawhud") > 0)
		{
			setproperty(VF_DRAWENGINESBAR, 1);
			if (cvar("crosshair") > 0)
				setproperty(VF_DRAWCROSSHAIR, 1);
			else
				setproperty(VF_DRAWCROSSHAIR, 0);
		}
		else
		{
			setproperty(VF_DRAWENGINESBAR, 0);
			setproperty(VF_DRAWCROSSHAIR, 0);
		}

		setproperty(VF_DRAWWORLD, 1);

		if (cvar("r_drawviewmodel") > 0)
			addentities((intermission?0:MASK_VIEWMODEL)|MASK_ENGINE);
		else
			addentities(MASK_ENGINE);			
	}

	renderscene();

	if (cvar("r_saturnmode") != 0)
	{
		if (cprint_timer > time)
			drawtextfield([0, isize[1] / 4], isize, 2, cprint_msg);

		weapon_viewsprite_size = [320, 240];
		weapon_viewsprite_pos = [0, CalcViewBob() - 48];

		if (activeweapon == IT_AXE)
		{
			if (activeweaponframe == 0) weapon_viewsprite = "gfx/weapons/axe_idle01.png";
			if (activeweaponframe == 1) weapon_viewsprite = "gfx/weapons/axe_swing01a.png";
			if (activeweaponframe == 2) weapon_viewsprite = "gfx/weapons/axe_swing01b.png";
			if (activeweaponframe == 3) weapon_viewsprite = "gfx/weapons/axe_swing01c.png";
			if (activeweaponframe == 4) weapon_viewsprite = "gfx/weapons/axe_swing01d.png";
			if (activeweaponframe == 5) weapon_viewsprite = "gfx/weapons/axe_swing02a.png";
			if (activeweaponframe == 6) weapon_viewsprite = "gfx/weapons/axe_swing02b.png";
			if (activeweaponframe == 7) weapon_viewsprite = "gfx/weapons/axe_swing02c.png";
			if (activeweaponframe == 8) weapon_viewsprite = "gfx/weapons/axe_idle01.png";
		}
		else if (activeweapon == IT_SHOTGUN)
		{
			if (activeweaponframe == 0) weapon_viewsprite = "gfx/weapons/shotgun_idle01.png";
			if (activeweaponframe == 1) weapon_viewsprite = "gfx/weapons/shotgun_shoot01a.png";
			if (activeweaponframe == 3) weapon_viewsprite = "gfx/weapons/shotgun_shoot01b.png";
			if (activeweaponframe == 5) weapon_viewsprite = "gfx/weapons/shotgun_shoot01c.png";
			if (activeweaponframe == 7) weapon_viewsprite = "gfx/weapons/shotgun_shoot01d.png";
		}
		else if (activeweapon == IT_SUPER_SHOTGUN)
		{
			if (activeweaponframe == 0) weapon_viewsprite = "gfx/weapons/ssg_idle01.png";
			if (activeweaponframe == 1) weapon_viewsprite = "gfx/weapons/ssg_shoot01a.png";
			if (activeweaponframe == 3) weapon_viewsprite = "gfx/weapons/ssg_shoot01b.png";
			if (activeweaponframe == 4) weapon_viewsprite = "gfx/weapons/ssg_idle01.png";
		}
		else if (activeweapon == IT_NAILGUN)
		{
			if (activeweaponframe == 0) weapon_viewsprite = "gfx/weapons/ng_idle01.png";
			if (activeweaponframe == 1) weapon_viewsprite = "gfx/weapons/ng_shoot01_right.png";
			if (activeweaponframe == 2) weapon_viewsprite = "gfx/weapons/ng_shoot01_left.png";
			if (activeweaponframe == 3) weapon_viewsprite = "gfx/weapons/ng_shoot01_right.png";
			if (activeweaponframe == 4) weapon_viewsprite = "gfx/weapons/ng_shoot01_left.png";
			if (activeweaponframe == 5) weapon_viewsprite = "gfx/weapons/ng_shoot01_right.png";
			if (activeweaponframe == 6) weapon_viewsprite = "gfx/weapons/ng_shoot01_left.png";
			if (activeweaponframe == 7) weapon_viewsprite = "gfx/weapons/ng_shoot01_right.png";
			if (activeweaponframe == 8) weapon_viewsprite = "gfx/weapons/ng_shoot01_left.png";
		}
		else if (activeweapon == IT_SUPER_NAILGUN)
		{
			if (activeweaponframe == 0) weapon_viewsprite = "gfx/weapons/sng_idle01.png";
			if (activeweaponframe == 1) weapon_viewsprite = "gfx/weapons/sng_shoot01_left.png";
			if (activeweaponframe == 2) weapon_viewsprite = "gfx/weapons/sng_shoot01_up.png";
			if (activeweaponframe == 3) weapon_viewsprite = "gfx/weapons/sng_shoot01_right.png";
			if (activeweaponframe == 4) weapon_viewsprite = "gfx/weapons/sng_spin01.png";
			if (activeweaponframe == 5) weapon_viewsprite = "gfx/weapons/sng_shoot01_left.png";
			if (activeweaponframe == 6) weapon_viewsprite = "gfx/weapons/sng_shoot01_up.png";
			if (activeweaponframe == 7) weapon_viewsprite = "gfx/weapons/sng_shoot01_right.png";
			if (activeweaponframe == 8) weapon_viewsprite = "gfx/weapons/sng_spin01.png";
		}
		else if (activeweapon == IT_GRENADE_LAUNCHER)
		{
			weapon_viewsprite = "";
		}
		else if (activeweapon == IT_ROCKET_LAUNCHER)
		{
			weapon_viewsprite = "";
		}
		else if (activeweapon == IT_LIGHTNING)
		{
			if (activeweaponframe == 0) weapon_viewsprite = "gfx/weapons/lightning_idle01.png";
			if (activeweaponframe == 1) weapon_viewsprite = "gfx/weapons/lightning_shoot01a.png";
			if (activeweaponframe == 2) weapon_viewsprite = "gfx/weapons/lightning_shoot01b.png";
			if (activeweaponframe == 3) weapon_viewsprite = "gfx/weapons/lightning_shoot01c.png";
			if (activeweaponframe == 4) weapon_viewsprite = "gfx/weapons/lightning_shoot01d.png";
		}
		else if (activeweapon == IT_EXTRA_WEAPON)
		{
			weapon_viewsprite = "";
		}

		if (intermission == 0)
		{
			drawpic(weapon_viewsprite_pos, weapon_viewsprite, weapon_viewsprite_size, [1, 1, 1], 1);

			drawpic(hud_sbar_pos, hud_sbar, hud_sbar_size, [1, 1, 1], 1);
			drawpic(hud_ibar_pos, hud_ibar, hud_ibar_size, [1, 1, 1], 1);
			
			setproperty(VF_DRAWCROSSHAIR, 1);
		}
		else
		{
			DrawIntermission();
		}

		setviewprop(VF_RT_DESTCOLOUR, (string)__NULL__);
		shaderforname("screenrtshader", "{\nprogram postproc\n{\nmap $rt:screenrt\nrgbgen vertex\n}\n}\n");
		// version with no postproc
		//shaderforname("screenrtshader", "{\n{\nmap $rt:screenrt\nrgbgen vertex\n}\n}\n");

		dpos = CalculateDisplayPos([vwidth, vheight], aspect_fullscreen);
		dsize = CalculateDisplaySize([vwidth, vheight], aspect_fullscreen);

		vector screensize = [dsize[0] * cvar("scr_conscale"), dsize[1] * cvar("scr_conscale")];
		vector screenpos = dpos;
		vector userdata[2] = {screensize, screenpos};
		int userdata_size = sizeof(userdata);
		vector *userdata_pointer = &userdata;

		setproperty(VF_USERDATA, userdata_pointer, userdata_size);

		drawpic(dpos, "screenrtshader", dsize, [1, 1, 1], 1);
	}
};

void(float vwidth, float vheight, float notmenu) CSQC_UpdateViewLoading =
{
	dpos = CalculateDisplayPos([vwidth, vheight], aspect_fullscreen);
	dsize = CalculateDisplaySize([vwidth, vheight], aspect_fullscreen);

	// bg
	drawfill([0, 0], [vwidth, vheight], [0, 0, 0], 1);
	drawpic(dpos, loading_bg, dsize, [1, 1, 1], 1);

	// fake loading bar
	lbar_size = [dsize[0] * 0.3875, dsize[1] * 0.05];
	lbar_pos = [dpos[0] + dsize[0] * 0.30625, dpos[1] + dsize[1] * 0.85];

	lbar_width += 8;
	lbar_width = bound(0, lbar_width, lbar_size[0]);

	drawfill(lbar_pos, [lbar_width, lbar_size[1]], lbar_color, 1);
};

void(float apilevel, string enginename, float engineversion) CSQC_Init =
{
	//print("world.model: ", world.model, "\n");
	//precache_model("maps/title.iqm");
	//setmodel(world, "maps/title.iqm");
	lbar_width = 0;
};

float(string msg) CSQC_Parse_CenterPrint =
{
	if (cvar("r_saturnmode") != 0)
	{
		cprint_msg = msg;
		cprint_timer = time + 5;
		return TRUE;
	}
	else
		return FALSE;
};

void(string printmsg, float printlvl) CSQC_Parse_Print =
{
	if (cvar("r_saturnmode") != 0)
	{
		cprint_msg = printmsg;
		cprint_timer = time + 5;
	}
};

float() ParseMapEntity =
{
	local string field, value;
	local entity newent = spawn();
	local void() spawnfunc = __NULL__;
	
	while (1)
	{
		field = getentitytoken();

		if not (field)
			break;

		if (field == "}")
		{
			if (!newent.classname)
				break;

			if (spawnfunc)
			{
				self = newent;
				spawnfunc();
				return TRUE;
			}

			remove(newent);
			return TRUE;
		}

		value = getentitytoken();

		if not (value)
			break;

		if (field == "classname")
		{
			if (value != "worldspawn")
				spawnfunc = spawnfunc_csqc_developer_ent;
	
			newent.classname = value;
		}
		else if (field == "model")
			newent.model = value;
		else if (field == "message")
			newent.message = value;
		else if (field == "angles")
			newent.angles = stov(value);
		else if (field == "origin")
			setorigin(newent, stov(value));
		else if (field == "frame")
			newent.frame = stof(value);
	}

	remove(newent);

	return FALSE;
};

void() CSQC_WorldLoaded =
{
	string token;

	while (1)
	{
		token = getentitytoken();

		if (token == "")
			break;

		if (token != "{")
		{
			print("^1bad entity data token!\n");
			return;
		}
		
		if (!ParseMapEntity())
		{
			print("^1could not parse entity data in mapfile\n");
			return;
		}
	}
};