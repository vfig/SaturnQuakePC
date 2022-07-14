//
// builtins.qc
//

float iscale;
vector isize;
vector dpos;
vector dsize;
string cprint_msg;
float cprint_timer;

void(float vwidth, float vheight, float notmenu) CSQC_UpdateView =
{
	clearscene();

	iscale = 1;

	if (cvar("r_saturnmode") != 0)
	{
		cvar_set("cl_sbar", "1");
		cvar_set("r_viewmodel_quake", "0");

		drawfontscale = [iscale, iscale, iscale];

		isize = [320 * iscale, 240 * iscale];

		drawfill([0, 0], [vwidth, vheight], [0, 0, 0], 1);
		setviewprop(VF_RT_DESTCOLOUR, "screenrt", -IMGFMT_R8G8B8A8, isize);
		setproperty(VF_VIEWPORT, [0, 0], isize);
	}

	setproperty(VF_DRAWENGINESBAR, 1);
	setproperty(VF_DRAWCROSSHAIR, 1);
	setproperty(VF_DRAWWORLD, 1);

	addentities((intermission?0:MASK_VIEWMODEL)|MASK_ENGINE);

	renderscene();

	if (cvar("r_saturnmode") != 0)
	{
		if (cprint_timer > time)
			drawtextfield([0, isize[1] / 4], isize, 2, cprint_msg);

		setviewprop(VF_RT_DESTCOLOUR, (string)__NULL__);
		// disable postproc for now
		//shaderforname("screenrtshader", "{\nprogram postproc\n{\nmap $rt:screenrt\nrgbgen vertex\n}\n}\n");
		shaderforname("screenrtshader", "{\n{\nmap $rt:screenrt\nrgbgen vertex\n}\n}\n");

		dpos = CalculateDisplayPos([vwidth, vheight], aspect_fullscreen);
		dsize = CalculateDisplaySize([vwidth, vheight], aspect_fullscreen);

		drawpic(dpos, "screenrtshader", dsize, [1, 1, 1], 1);
	}
};

float(string msg) CSQC_Parse_CenterPrint =
{
	if (cvar("r_saturnmode") != 0)
	{
		cprint_msg = msg;
		cprint_timer = time + 3;
		return TRUE;
	}
	else
		return FALSE;
};