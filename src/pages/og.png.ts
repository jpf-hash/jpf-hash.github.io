import type { APIRoute } from "astro";
import sharp from "sharp";
import config from "@/config";

export const GET: APIRoute = async () => {
  // Create a simple OG image with site title using SVG
  const svg = `
    <svg width="1200" height="630" xmlns="http://www.w3.org/2000/svg">
      <rect width="1200" height="630" fill="#0f172a"/>
      <text x="600" y="280" text-anchor="middle" font-family="system-ui, sans-serif" font-size="72" font-weight="bold" fill="#22d3ee">${config.site.title}</text>
      <text x="600" y="360" text-anchor="middle" font-family="system-ui, sans-serif" font-size="28" fill="#94a3b8">${config.site.description}</text>
      <text x="600" y="500" text-anchor="middle" font-family="system-ui, sans-serif" font-size="24" fill="#64748b">${new URL(config.site.url).hostname}</text>
    </svg>
  `;

  const pngBuffer = await sharp(Buffer.from(svg)).png().toBuffer();

  return new Response(new Uint8Array(pngBuffer), {
    headers: { "Content-Type": "image/png" },
  });
};
