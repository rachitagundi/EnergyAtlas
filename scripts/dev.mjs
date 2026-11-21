// Convenience runner after installing the Python and frontend dependencies.
import { spawn } from "node:child_process";
import { existsSync } from "node:fs";
import { fileURLToPath } from "node:url";
import path from "node:path";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const python = process.env.ENERGYATLAS_PYTHON || path.join(root, ".venv-fullstack", process.platform === "win32" ? "Scripts/python.exe" : "bin/python");
if (!existsSync(python)) {
  console.error("Create .venv-fullstack and install backend dependencies first. See START_HERE_WINDOWS.md.");
  process.exit(1);
}
const vite = path.join(root, "frontend/node_modules/vite/bin/vite.js");
if (!existsSync(vite)) {
  console.error("Run npm ci in frontend first.");
  process.exit(1);
}
const api = spawn(python, ["-m", "uvicorn", "app.main:app", "--app-dir", "backend", "--host", "127.0.0.1", "--port", "8010"], { cwd: root, stdio: "inherit" });
const web = spawn(process.execPath, [vite, "--host", "127.0.0.1", "--port", process.env.PORT || "5173", ...process.argv.slice(2)], { cwd: path.join(root, "frontend"), stdio: "inherit" });
let closing = false;
function close(code = 0) {
  if (closing) return;
  closing = true;
  api.kill();
  web.kill();
  process.exitCode = code;
}
for (const child of [api, web]) {
  child.on("error", err => { console.error(err.message); close(1); });
  child.on("exit", code => close(code || 0));
}
process.on("SIGINT", () => close());
process.on("SIGTERM", () => close());
