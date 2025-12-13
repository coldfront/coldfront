import { defineConfig, loadEnv } from "vite";
import eslint from 'vite-plugin-eslint';
import path from "path";

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), "");
  const appPort = env.APP_PORT ? Number(env.APP_PORT) : 5173;
  return {
    server: {
      port: appPort,
      origin: "http://localhost:" + appPort,
    },
    root: path.resolve(__dirname, "src"),
    resolve: {
      alias: {
        "~bootstrap": path.resolve(__dirname, "node_modules/bootstrap"),
        "~fontawesome": path.resolve(
          __dirname,
          "node_modules/@fortawesome/fontawesome-free",
        ),
      },
    },
    plugins: [eslint()],
    base: "/static", // This should match django settings.STATIC_URL
    build: {
      // Where Vite will save its output files.
      // This should be added to django settings.STATICFILES_DIRS
      outDir: path.resolve(__dirname, "bundles"),
      emptyOutDir: true,
      assetsDir: "",
      manifest: "manifest.json",
      rollupOptions: {
        input: {
          coldfront: path.resolve(__dirname, "src/coldfront.ts"),
          "coldfront-center-summary": path.resolve(
            __dirname,
            "src/centerSummary.ts",
          ),
          "coldfront-allocation-summary": path.resolve(
            __dirname,
            "src/allocationSummary.ts",
          ),
        },
        output: {
          entryFileNames: `[name].js`,
          chunkFileNames: `[name].js`,
          assetFileNames: `[name].[ext]`,
        },
      },
    },
  };
});
