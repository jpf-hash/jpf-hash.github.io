import { cpSync, existsSync, mkdirSync, rmSync } from "node:fs";

const source = "dist/pagefind";
const target = "public/pagefind";

if (!existsSync(source)) {
  throw new Error(`Pagefind output not found: ${source}`);
}

mkdirSync("public", { recursive: true });

if (existsSync(target)) {
  rmSync(target, { recursive: true, force: true });
}

cpSync(source, target, { recursive: true });
