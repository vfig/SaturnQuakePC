gfx/unspecified
{
	program saturn_level
	diffusemap textures/grid.png
	cull disable
}

saturn_water
{
	program saturn_water
}

sky_saturn_01
{
	program saturn_sky
	{
		map textures/sky/sky_saturn_01_base.png
	}
	{
		map textures/sky/sky_saturn_01_clouds.png
	}
	cull disable
}

sky_saturn_02
{
	program saturn_sky
	{
		map textures/sky/sky_saturn_02_base.png
	}
	{
		map textures/sky/sky_saturn_02_clouds.png
	}
	cull disable
}