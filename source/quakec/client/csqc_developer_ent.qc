//
// csqc_developer_ent.qc
//

class csqc_developer_ent : CBaseSprite
{
	void() csqc_developer_ent;
	virtual float() predraw;
};

void csqc_developer_ent :: csqc_developer_ent ( void )
{
	if (message == "light") spritepath = "textures/sprites/debug/lightbulb";
	else spritepath = "textures/sprites/debug/question";

	spritescale = 0.25;
	drawmask = MASK_ENGINE;
};

float csqc_developer_ent :: predraw ( void )
{
	if (cvar("developer") < 1)
		return PREDRAW_NEXT;

	//float(vector org, float radius, vector lightcolours, optional float style, optional string cubemapname, optional float pflags) dynamiclight_add = #305;
	//dynamiclight_add(origin, 256, [1, 0, 0]);

	super::predraw();
	return PREDRAW_NEXT;
};