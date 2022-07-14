//
// builtins.qc
//

void(float vwidth, float vheight, float notmenu) CSQC_UpdateView =
{
	clearscene();

	setproperty(VF_DRAWENGINESBAR, 1);
	setproperty(VF_DRAWCROSSHAIR, 1);
	setproperty(VF_DRAWWORLD, 1);

	addentities((intermission?0:MASK_VIEWMODEL)|MASK_ENGINE);

	renderscene();
};