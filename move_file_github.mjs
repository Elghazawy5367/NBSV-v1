import { Octokit } from "@octokit/rest";

const TOKEN = process.env.GITHUB_TOKEN;
const OWNER = "Elghazawy5367";
const REPO = "NBSV-v1";
const SRC = "tracker/index.html";
const DST = "docs/index.html";

const octokit = new Octokit({ auth: TOKEN });

console.log(`Connecting to ${OWNER}/${REPO}...`);

// Step 1: Get source file
console.log(`Reading ${SRC}...`);
const { data: srcFile } = await octokit.repos.getContent({
  owner: OWNER, repo: REPO, path: SRC,
});
const content = srcFile.content; // already base64
const srcSha = srcFile.sha;

// Step 2: Create/update destination
console.log(`Creating ${DST}...`);
let existingSha;
try {
  const { data: existing } = await octokit.repos.getContent({
    owner: OWNER, repo: REPO, path: DST,
  });
  existingSha = existing.sha;
} catch (e) {
  if (e.status !== 404) throw e;
}

if (existingSha) {
  await octokit.repos.createOrUpdateFileContents({
    owner: OWNER, repo: REPO, path: DST,
    message: `Move ${SRC} to ${DST}`,
    content,
    sha: existingSha,
  });
  console.log(`  Updated existing ${DST}`);
} else {
  await octokit.repos.createOrUpdateFileContents({
    owner: OWNER, repo: REPO, path: DST,
    message: `Move ${SRC} to ${DST}`,
    content,
  });
  console.log(`  Created ${DST}`);
}

// Step 3: Delete source
console.log(`Deleting ${SRC}...`);
await octokit.repos.deleteFile({
  owner: OWNER, repo: REPO, path: SRC,
  message: `Remove ${SRC} (moved to ${DST})`,
  sha: srcSha,
});
console.log(`  Deleted ${SRC}`);

console.log("\nDone! File successfully moved.");
