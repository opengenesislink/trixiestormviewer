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

// Values originate in OGLWeatherState; smoothly interpolated by the viewer.
// x=rain intensity, y=snow intensity, z=wind strength, w=Zink HQ profile.
uniform vec4 trixie_weather;
uniform float trixie_weather_time;

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

    if (cloud_scale < 0.001 && max(trixie_weather.x, trixie_weather.y) < 0.01)
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

    // Weather-front cloud model using the EEP texture already provided by the
    // region. Multiple noise scales form broad frontal banks, stratocumulus
    // masses and irregular edges. No secondary texture assets are required.
    // It is still a sky dome (2D) rather than a raymarched 3D volume.
    float rain = clamp(trixie_weather.x, 0.0, 1.0);
    float snow = clamp(trixie_weather.y, 0.0, 1.0);
    float wet = max(rain, snow);
    float wind = clamp(trixie_weather.z, 0.0, 1.0);
    float highQuality = clamp(trixie_weather.w, 0.0, 1.0);

    // Fronts drift in a stable direction. Weather v1 supplies wind speed,
    // not direction, so do not imply a physically accurate wind vector.
    vec2 drift = vec2(0.00023, -0.000065) * trixie_weather_time *
                 (1.0 + 2.3 * wind);
    vec2 largeUV = uv1 + drift;
    float largeNoise = cloudNoise(largeUV).x;
    float bankNoise = cloudNoise(largeUV * 0.57 + vec2(0.17, 0.33)).x;
    float middleNoise = cloudNoise(largeUV * 2.21 + vec2(0.31, 0.15)).x;
    float fineNoise = cloudNoise(uv3 + drift * 2.1).x;
    float shadeNoise = cloudNoise(uv2 + drift * 0.58).x;
    float shadeDetail = cloudNoise(uv4 + drift * 1.5).x;

    float details = 0.50 * largeNoise + 0.25 * middleNoise +
                    0.16 * fineNoise + 0.09 * bankNoise;
    if (highQuality > 0.5)
    {
        // Only the optional high-quality Zink profile incurs extra taps.
        float billows = cloudNoise(largeUV * 3.47 + vec2(0.08, 0.27)).x;
        float veils = cloudNoise(largeUV * 0.31 + vec2(0.49, 0.05)).x;
        details = mix(details, 0.69 * details + 0.19 * billows +
                               0.12 * veils, highQuality);
    }

    float originalShape = (largeNoise - 0.5) +
        (fineNoise - 0.5) * cloud_pos_density2.z * 0.73 +
        (middleNoise - 0.5) * 0.20;
    float originalCoverage = clamp((originalShape + cloudDensity) *
        8.0 * max(cloud_pos_density1.z, 0.0), 0.0, 1.0);
    originalCoverage = smoothstep(0.06, 0.96, originalCoverage);

    // Wide rain banks have dark underbellies and open pockets. Snow systems
    // have more continuous, soft-edged strata instead of black thunderheads.
    float frontalBase = 0.58 * bankNoise + 0.42 * largeNoise;
    float frontalCover = smoothstep(0.33 - wet * 0.10,
                                   0.72 - wet * 0.19, frontalBase);
    float detailCover = smoothstep(0.36 - wet * 0.09,
                                  0.66 - wet * 0.10, details);
    float weatherCover = mix(detailCover, frontalCover * 0.73 +
                            detailCover * 0.27, clamp(0.65 * rain +
                            0.30 * snow, 0.0, 1.0));
    float alpha1 = mix(originalCoverage,
        clamp(weatherCover * (0.60 + 0.43 * wet) +
              originalCoverage * 0.23, 0.0, 1.0), wet);
    alpha1 *= altitude_blend_factor;
    alpha1 = clamp(alpha1, 0.0, 0.98);

    // Low-frequency shadow thickness and multi-scale illuminated edges.
    float thickness = clamp((shadeNoise - 0.36) * 1.35 +
                      (shadeDetail - 0.5) * 0.39 +
                      (bankNoise - 0.4) * 0.62, 0.0, 1.0);
    thickness = smoothstep(0.10, 0.93, thickness);
    float rim = smoothstep(0.51, 0.82, middleNoise) *
                (1.0 - thickness) * 0.23;
    float incomingLight = clamp(1.10 - thickness * 0.66 + rim, 0.22, 1.35);

    vec3 color = cloudColorSun * incomingLight +
                 cloudColorAmbient * (0.89 + middleNoise * 0.14);
    // Weather-appropriate natural tones: bluish charcoal for rain and
    // brighter, cooler grey-white for snow. Do not force a global tint onto
    // terrain or the user's custom EEP environment.
    vec3 rainBase = mix(vec3(0.21, 0.24, 0.29),
                        vec3(0.39, 0.43, 0.49), 1.0 - thickness);
    vec3 snowBase = mix(vec3(0.53, 0.58, 0.65),
                        vec3(0.77, 0.80, 0.84), 1.0 - thickness);
    // Keep storm clouds dim at night and in low-sun environments rather
    // than making winter clouds glow independently of EEP illumination.
    float ambientLight = clamp(dot(cloudColorSun + cloudColorAmbient,
        vec3(0.2126, 0.7152, 0.0722)) * 1.6, 0.22, 1.0);
    rainBase *= ambientLight;
    snowBase *= ambientLight;
    color = mix(color, rainBase, clamp(rain * 1.17, 0.0, 0.90));
    color = mix(color, snowBase, clamp(snow * 1.08, 0.0, 0.88));
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

