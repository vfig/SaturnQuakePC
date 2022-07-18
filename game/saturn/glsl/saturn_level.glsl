!!ver 100-450
!!samps diffuse

#include "sys/defs.h"

varying vec2 tc;
varying vec4 vc;
varying vec4 wp;

#define PI 3.14159265358979323846

#ifdef VERTEX_SHADER

void main ()

	{
		tc = v_texcoord;
		vc = v_colour;
		gl_Position = ftetransform();
		wp = gl_Position;
	}

#endif

#ifdef FRAGMENT_SHADER

	void main ()
	{
		vec4 vclr = vc;		
		vec4 col = texture2D(s_diffuse, tc);
		col.rgb -= vec3(1.0) - vclr.rgb;
		gl_FragColor = col;
	}

#endif