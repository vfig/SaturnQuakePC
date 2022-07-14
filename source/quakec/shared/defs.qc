//
// shared.qc
//

//
// SHARED DEFINITIONS - ALL MODULES
//

//
// ASPECT RATIO VALUES
//

vector aspect_fullscreen = [4, 3];
vector aspect_widescreen = [16, 9];
vector aspect_widescreen_alt = [16, 10];
vector aspect_ultrawide = [21, 9];

//
// USEFUL FUNCTIONS
//

// cvar_toggle
void(string cvar_s, vector values) cvar_toggle =
{
	if (cvar(cvar_s) == values[0])
		cvar_set(cvar_s, ftos(values[1]));
	else
		cvar_set(cvar_s, ftos(values[0]));
};

// CalculateDisplayPos
vector(vector screensize, vector aspect) CalculateDisplayPos =
{
	float ratio1 = aspect_x / aspect_y;
	float ratio2 = aspect_y / aspect_x;
	vector dpos;

	if (screensize_y < screensize_x && (screensize_y * ratio1) < screensize_x) // window is widescreen-shaped
		dpos = [(screensize_x / 2) - ((screensize_y * ratio1) / 2), 0];
	else if ((screensize_x / screensize_y) == ratio1) // perfectly 16:9 window
		dpos = [0, 0];
	else // window is phone-shaped (?)
		dpos = [0, (screensize_y / 2) - ((screensize_x * ratio2) / 2)];
	
	return dpos;
};

// CalculateDisplaySize
vector(vector screensize, vector aspect) CalculateDisplaySize =
{
	float ratio1 = aspect_x / aspect_y;
	float ratio2 = aspect_y / aspect_x;
	vector dsize;

	if (screensize_y < screensize_x && (screensize_y * ratio1) < screensize_x) // window is widescreen-shaped
		dsize = [screensize_y * ratio1, screensize_y];
	else if ((screensize_x / screensize_y) == ratio1) // perfectly 16:9 window
		dsize = [screensize_x, screensize_y];
	else // window is phone-shaped (?)
		dsize = [screensize_x, screensize_x * ratio2];

	return dsize;
};

//
// MATH
//

// zeroconvert
// shorthand for turning -1 to 0 for keyvalues for which 0 is a valid non-default selection
// from Copper

float(float in) zeroconvert =
{
	if (in == -1) return 0;
	return in;
};

float(float in, float def) zeroconvertdefault =
{
	if (in == -1) return 0;
	if (in == 0) return def;
	return in;
};

// BoundsAngleSize
// for measuring how large an entity is along an arbitrary vector
// from Copper

float(vector v, vector s) BoundsAngleSize =
{
	v_x = fabs(v_x);
	v_y = fabs(v_y);
	v_z = fabs(v_z);
	
	// size is always + + + but this is in case I switch the parameters somewhere
	s_x = fabs(s_x);
	s_y = fabs(s_y);
	s_z = fabs(s_z);
	
	return v * s;
};

// clamp
// Limits the given value to the given range.
// from Copper

float(float value, float minValue, float maxValue) clamp =
{
	if (value > maxValue)
		return maxValue;
	else if (value < minValue)
		return minValue;

	return value;
};

#if defined(MENU)
	string loading_bg;
	vector display_pos;
	vector display_size;
#endif