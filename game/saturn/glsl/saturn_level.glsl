!!ver 100-450
!!samps diffuse

#include "sys/defs.h"

varying vec2 tc;
varying vec4 vc;

#ifdef VERTEX_SHADER
void main ()
{
    tc = v_texcoord;
    vc = v_colour;
    gl_Position = ftetransform();
}
#endif
#ifdef FRAGMENT_SHADER
void main ()
{
    vec4 col = texture2D(s_diffuse, tc);
	col.rgb -= vec3(1.0) - vc.rgb;
    gl_FragColor = col;
}
#endif