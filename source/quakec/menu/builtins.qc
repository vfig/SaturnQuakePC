//
// builtins.qc
//

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
	drawpic(display_pos, "gfx/qload.bmp", display_size, [1, 1, 1], 1);

	// fake loading bar
	//menu_loadingbar_width += 32;
	//menu_loadingbar_width = bound(0, menu_loadingbar_width, display_size[0]);

	//string menu_loadingbar_text = "THE END IS NEVER THE END IS NEVER";
	//float menu_loadingbar_size = display_size[0] / strlen(menu_loadingbar_text);
	//drawfill([display_pos[0], (display_pos[1] + display_size[1]) - menu_loadingbar_size], [menu_loadingbar_width, display_size[1] / menu_loadingbar_size], [1, 1, 1], 1);
};