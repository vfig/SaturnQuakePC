//
// builtins.qc
//

float lbar_width;
vector lbar_size; // 124 x 12
vector lbar_pos;
vector lbar_color = [1, 0, 0];

void(vector screensize) CalculateMenuDisplay =
{
	display_pos = CalculateDisplayPos(screensize, aspect_fullscreen);
	display_size = CalculateDisplaySize(screensize, aspect_fullscreen);
};

void(vector screensize, float opaque) m_drawloading =
{
	CalculateMenuDisplay(screensize);

	// bg
	drawfill([0, 0], [screensize[0], screensize[1]], [0, 0, 0], 1);
	drawpic(display_pos, loading_bg, display_size, [1, 1, 1], 1);

	// fake loading bar
	lbar_size = [display_size[0] * 0.3875, display_size[1] * 0.05];
	lbar_pos = [display_pos[0] + display_size[0] * 0.30625, display_pos[1] + display_size[1] * 0.85];

	lbar_width += 8;
	lbar_width = bound(0, lbar_width, lbar_size[0]);

	drawfill(lbar_pos, [lbar_width, lbar_size[1]], lbar_color, 1);
};

void(string cmdtext) GameCommand =
{
	switch (cmdtext)
	{
		case "reset_loadingbar" :
			lbar_width = 0;
			break;
		default:
			break;
	}
};