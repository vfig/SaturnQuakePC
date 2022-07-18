!!ver 100-450
!!samps diffuse

#include "sys/defs.h"

varying vec2 tc;
varying vec4 vc;

#define PERIOD 4

#ifdef VERTEX_SHADER

void main ()

	{
		tc = v_texcoord;
		vc = v_colour;
		gl_Position = ftetransform();
	}

#endif

#ifdef FRAGMENT_SHADER

	uint lcg(uint p) {
		return p * 1664525u + 1013904223u;
	}

	uvec4 pcg4d(uvec4 v)
	{
		v = v * 1664525u + 1013904223u;
		v.x += v.y*v.w; v.y += v.z*v.x; v.z += v.x*v.y; v.w += v.y*v.z;
		v.x += v.y*v.w; v.y += v.z*v.x; v.z += v.x*v.y; v.w += v.y*v.z;
		v = v ^ (v>>16u);

		return v;
	}

	vec3 fade(vec3 t)
	{
		return t * t * t * (t * (t * 6.0 - 15.0) + 10.0);
	}

	float grad(uint hash, float x, float y, float z)
	{
		uint h = hash & 15u;
		float u = h < 8u ? x : y;
		float v = h < 4u ? y : (h == 12u || h == 14u ? x : z);
		return ((h & 1u) == 0u ? u : -u) + ((h & 2u) == 0u ? v : -v);
	}

	uint hash(uvec3 p)
	{
		uvec4 hash4 = pcg4d(uvec4(p, p.x^p.y^p.z));
		return hash4.x;
	}

	float noise3d_gpu(vec3 p, uint period)
	{
		vec3 pFloor;
		vec3 pF = modf(p * float(period), pFloor);
		uvec3 pI = uvec3(pFloor) % period;
		vec3 uvw = fade(pF);
	 
		uint h000 = hash((pI + uvec3(0u, 0u, 0u)) % period);
		uint h001 = hash((pI + uvec3(0u, 0u, 1u)) % period);
		uint h010 = hash((pI + uvec3(0u, 1u, 0u)) % period);
		uint h011 = hash((pI + uvec3(0u, 1u, 1u)) % period);
		uint h100 = hash((pI + uvec3(1u, 0u, 0u)) % period);
		uint h101 = hash((pI + uvec3(1u, 0u, 1u)) % period);
		uint h110 = hash((pI + uvec3(1u, 1u, 0u)) % period);
		uint h111 = hash((pI + uvec3(1u, 1u, 1u)) % period);
		
		return mix(mix(mix(grad(h000, pF.x, pF.y	, pF.z	), grad(h100, pF.x-1.0, pF.y	, pF.z	), uvw.x),
					   mix(grad(h010, pF.x, pF.y-1.0, pF.z	), grad(h110, pF.x-1.0, pF.y-1.0, pF.z	), uvw.x), uvw.y),
				   mix(mix(grad(h001, pF.x, pF.y	, pF.z-1.0), grad(h101, pF.x-1.0, pF.y	, pF.z-1.0), uvw.x),
					   mix(grad(h011, pF.x, pF.y-1.0, pF.z-1.0), grad(h111, pF.x-1.0, pF.y-1.0, pF.z-1.0), uvw.x), uvw.y), uvw.z);
	}

	void main ()
	{
		float noise = noise3d_gpu(vec3(tc, e_time * 0.25), uint(PERIOD));
		vec3 blue = vec3(9.4, 9.4, 15.7);
		noise = noise * 0.5 + 0.5;
		vec4 vclr = vc;	
		vec4 col = texture2D(s_diffuse, tc);
		//col.rgb -= vec3(noise * 0.1, noise * 0.1, noise * 0.1);
		col.rgb -= vec3(1.0) - vclr.rgb;
		gl_FragColor = col;
	}

#endif