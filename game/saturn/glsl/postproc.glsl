!!ver 130
!!samps screen=0

!!cvardf r_saturnmode_crt

varying vec2 txc;

#include "sys/defs.h"

#ifdef VERTEX_SHADER

	void main ()
	{
		txc = v_texcoord.xy;
		gl_Position = ftetransform();
	}

#endif

#ifdef FRAGMENT_SHADER

	void main ()
	{
		#if r_saturnmode_crt > 0
			// https://www.shadertoy.com/view/WsVSzV

			vec2 screensize = vec2(w_user[0]);

			float warp = 0.75; // simulate curvature of CRT monitor
			float scan = 1.5; // simulate darkness between scanlines

			vec2 uv = gl_FragCoord.xy / screensize.xy;
			vec2 dc = abs(0.5 - uv);
			dc *= dc;

			uv.x -= 0.5; uv.x *= 1.0 + (dc.y * (0.3 * warp)); uv.x += 0.5;
			uv.y -= 0.5; uv.y *= 1.0 + (dc.x * (0.4 * warp)); uv.y += 0.5;

			uv.y = 1.0 - uv.y;

			if (uv.y > 1.0 || uv.x < 0.0 || uv.x > 1.0 || uv.y < 0.0)
			{
				gl_FragColor = vec4(0.0, 0.0, 0.0, 1.0);
			}
			else
			{
				float apply = abs(sin(gl_FragCoord.y) * 0.5 * scan); // determine if we are drawing in a scanline
				gl_FragColor = vec4(mix(texture2D(s_screen, uv).rgb, vec3(0.0), apply), 1.0); // sample the texture
			}
		#else
			vec4 screen = texture2D(s_screen, txc);

			gl_FragColor = screen;
		#endif
	}

#endif