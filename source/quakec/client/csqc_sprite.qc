//
// CBaseSprite.qc
//

class CBaseSprite
{
	string spritepath;
	vector spritesize;
	float spritescale;

	void() CBaseSprite;
	virtual float() predraw;
};

void CBaseSprite :: CBaseSprite ( void )
{
	if (!spritepath) spritepath = "textures/sprites/debug/lightbulb";
	if (!spritescale) spritescale = 0.5;
	if (!spritesize) spritesize = drawgetimagesize(spritepath) * spritescale;
	drawmask = MASK_ENGINE;
};

float CBaseSprite :: predraw ( void )
{
	makevectors(view_angles);

	R_BeginPolygon(spritepath, DRAWFLAG_TWOSIDED, FALSE);
	R_PolygonVertex(origin + v_right * spritesize[0] - v_up * spritesize[1], [1, 1], [1, 1, 1], 1);
	R_PolygonVertex(origin - v_right * spritesize[0] - v_up * spritesize[1], [0, 1], [1, 1, 1], 1);
	R_PolygonVertex(origin - v_right * spritesize[0] + v_up * spritesize[1], [0, 0], [1, 1, 1], 1);
	R_PolygonVertex(origin + v_right * spritesize[0] + v_up * spritesize[1], [1, 0], [1, 1, 1], 1);
	R_EndPolygon();

	addentity(this);
	return PREDRAW_NEXT;
};