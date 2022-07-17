!!samps base=0, cloud=1

#ifdef VERTEX_SHADER

	varying vec3 pos;

	void main ()
	{
		pos = v_position.xyz;
		gl_Position = ftetransform();
	}

#endif

#ifdef FRAGMENT_SHADER

	uniform float e_time;
	uniform vec3 e_eyepos;
	varying vec3 pos;

	void main ()
	{
		vec2 tccoord;
		vec3 dir = pos - e_eyepos;

		dir.z *= 3.0;
		dir.xy /= 0.2*length(dir);
		tccoord = (dir.xy);
		vec3 sky = vec3(texture2D(s_base, tccoord));
		dir.x = dir.x + e_time*0.9;
		tccoord = (dir.xy);
		vec4 clouds = texture2D(s_cloud, tccoord);
		sky = (sky.rgb*(1.0-clouds.a)) + (clouds.a*clouds.rgb);

		gl_FragColor = vec4(sky, 1.0);
	}
#endif