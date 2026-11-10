/**
 * @file class1\deferred\cloudsF.glsl
 *
 * $LicenseInfo:firstyear=2005&license=viewerlgpl$
 * Second Life Viewer Source Code
 * Copyright (C) 2005, Linden Research, Inc.
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation;
 * version 2.1 of the License only.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with this library; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
 *
 * Linden Research, Inc., 945 Battery Street, San Francisco, CA  94111  USA
 * $/LicenseInfo$
 */
/*[EXTRA_CODE_HERE]*/

out vec4 frag_data[4];

/////////////////////////////////////////////////////////////////////////
// The fragment shader for the sky
/////////////////////////////////////////////////////////////////////////

in vec3 vary_CloudColorSun;
in vec3 vary_CloudColorAmbient;
in float vary_CloudDensity;

uniform sampler2D cloud_noise_texture;
uniform sampler2D cloud_noise_texture_next;
uniform float blend_factor;
uniform vec3 cloud_pos_density1;
uniform vec3 cloud_pos_density2;
uniform float cloud_scale;
uniform float cloud_variance;

in vec2 vary_texcoord0;
in vec2 vary_texcoord1;
in vec2 vary_texcoord2;
in vec2 vary_texcoord3;
in float altitude_blend_factor;

vec4 cloudNoise(vec2 uv)
{
   vec4 a = texture(cloud_noise_texture, uv);
   vec4 b = texture(cloud_noise_texture_next, uv);
   vec4 cloud_noise_sample = mix(a, b, blend_factor);
   return cloud_noise_sample;
}

void main()
{
    // Set variables
    vec2 uv1 = vary_texcoord0.xy;
    vec2 uv2 = vary_texcoord1.xy;

    vec3 cloudColorSun = vary_CloudColorSun;
    vec3 cloudColorAmbient = vary_CloudColorAmbient;
    float cloudDensity = vary_CloudDensity;
    vec2 uv3 = vary_texcoord2.xy;
    vec2 uv4 = vary_texcoord3.xy;

    if (cloud_scale < 0.001)
    {
        discard;
    }

    vec2 disturbance  = vec2(cloudNoise(uv1 / 8.0f).x, cloudNoise((uv3 + uv1) / 16.0f).x) * cloud_variance * (1.0f - cloud_scale * 0.25f);
    vec2 disturbance2 = vec2(cloudNoise((uv1 + uv3) / 4.0f).x, cloudNoise((uv4 + uv2) / 8.0f).x) * cloud_variance * (1.0f - cloud_scale * 0.25f);

    // Offset texture coords
    uv1 += cloud_pos_density1.xy + (disturbance * 0.2);    //large texture, visible density
    uv2 += cloud_pos_density1.xy;   //large texture, self shadow
    uv3 += cloud_pos_density2.xy;   //small texture, visible density
    uv4 += cloud_pos_density2.xy;   //small texture, self shadow

    float density_variance = min(1.0, (disturbance.x* 2.0 + disturbance.y* 2.0 + disturbance2.x + disturbance2.y) * 4.0);

    cloudDensity *= 1.0 - (density_variance * density_variance);

    // TrixieStorm: layered cloud silhouettes with soft edges and lighting.
    // EEP cloud texture, coverage, scale and user-custom cloud textures are
    // preserved. This is enhanced 2-D shading, not volumetric raymarching.
    float large_noise = cloudNoise(uv1).x;
    float middle_noise = cloudNoise(uv1 * 2.35 + vec2(0.137, 0.319)).x;
    float fine_noise = cloudNoise(uv3).x;

    // Low-frequency masses give cloud silhouettes; mid- and high-frequency
    // noise introduce billowy edges without replacing custom EEP imagery.
    float cloud_shape = (large_noise - 0.5)
        + (middle_noise - 0.5) * 0.24
        + (fine_noise - 0.5) * cloud_pos_density2.z * 0.73;

    float coverage = clamp((cloud_shape + cloudDensity) *
                           9.0 * max(cloud_pos_density1.z, 0.0), 0.0, 1.0);
    float alpha1 = coverage * coverage * (3.0 - 2.0 * coverage);
    alpha1 *= altitude_blend_factor;
    alpha1 = clamp(alpha1, 0.0, 1.0);

    // Offset samples mimic light filtering through uneven cloud thickness:
    // lit puff tops are brighter while broad interiors have soft shadows.
    float shadow_large = cloudNoise(uv2).x;
    float shadow_fine = cloudNoise(uv4).x;
    float thickness = clamp(((shadow_large - 0.5) +
                             (shadow_fine - 0.5) * 0.28 + cloudDensity)
                            * 2.8 * max(cloud_pos_density1.z, 0.0), 0.0, 1.0);
    thickness = thickness * thickness * (3.0 - 2.0 * thickness);
    float puff_highlight = clamp((middle_noise - 0.42) * 0.24, 0.0, 0.14);
    float sun_visibility = 1.12 - thickness * 0.64 + puff_highlight;

    vec3 color = cloudColorSun * sun_visibility
               + cloudColorAmbient * (0.90 + middle_noise * 0.12);
    color.rgb = clamp(color.rgb, vec3(0.0), vec3(1.0));
    color.rgb *= 2.0;

    /// Gamma correct for WL (soft clip effect).

    frag_data[1] = vec4(0.0,0.0,0.0,0.0);
    frag_data[2] = vec4(0,0,0,GBUFFER_FLAG_SKIP_ATMOS);

#if defined(HAS_EMISSIVE)
    frag_data[0] = vec4(0);
    frag_data[3] = vec4(color.rgb, alpha1);
#else
    frag_data[0] = vec4(color.rgb, alpha1);
#endif
}

