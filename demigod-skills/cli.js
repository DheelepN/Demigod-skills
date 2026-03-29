#!/usr/bin/env node

const fs = require("fs");
const path = require("path");
const os = require("os");

// ─── Constants ────────────────────────────────────────────────────────────────

const PACKAGE_NAME = "@demig0d2/skills";
const VERSION = "1.1.5";

const SKILLS = {
  "book-creator": {
    description: "Complete pipeline — all 6 skills in one, no other installs needed",
    aliases: ["creator", "complete", "all-in-one"],
  },
  "book-writer": {
    description: "Full end-to-end book authoring pipeline with KDP output",
    aliases: ["book", "bookwriter"],
  },
  humanizer: {
    description: "Strip AI patterns + rewrite toward Vivid's style DNA",
    aliases: ["humanize"],
  },
  overhaul: {
    description: "Upgrade any skill file — Automated or Personalized mode",
    aliases: ["upgrade", "skill-upgrader"],
  },
  "concept-expander": {
    description: "Expand a rough book seed into a full concept document",
    aliases: ["concept", "expand"],
  },
  "chapter-auditor": {
    description: "Score chapters across 7 dimensions before humanizing",
    aliases: ["auditor", "audit"],
  },
  "continuity-tracker": {
    description: "Track facts, metaphors, and insights across chapters",
    aliases: ["continuity", "tracker"],
  },
  "research-aggregator": {
    description: "Build a research bank of quotes and thinkers per chapter",
    aliases: ["research", "aggregator"],
  },
};

const ALL_SKILLS = Object.keys(SKILLS);

// ─── Install paths ────────────────────────────────────────────────────────────

function getInstallDir() {
  const platform = os.platform();

  // Claude.ai skills path (user-level, works across all projects)
  // Windows: %USERPROFILE%\.claude\skills
  // macOS/Linux: ~/.claude/skills
  const home = os.homedir();
  return path.join(home, ".claude", "skills");
}

function getSkillSourcePath(skillName) {
  return path.join(__dirname, "skills", skillName, "SKILL.md");
}

function getSkillDestPath(skillName) {
  return path.join(getInstallDir(), skillName, "SKILL.md");
}

// ─── Helpers ─────────────────────────────────────────────────────────────────

function resolveSkillName(input) {
  // Direct match
  if (SKILLS[input]) return input;

  // Alias match
  for (const [name, meta] of Object.entries(SKILLS)) {
    if (meta.aliases.includes(input)) return name;
  }

  return null;
}

function ensureDir(dirPath) {
  if (!fs.existsSync(dirPath)) {
    fs.mkdirSync(dirPath, { recursive: true });
  }
}

function printBanner() {
  console.log(`
  ██████╗ ███████╗███╗   ███╗██╗ ██████╗  ██████╗ ██████╗ 
  ██╔══██╗██╔════╝████╗ ████║██║██╔════╝ ██╔═══██╗██╔══██╗
  ██║  ██║█████╗  ██╔████╔██║██║██║  ███╗██║   ██║██║  ██║
  ██║  ██║██╔══╝  ██║╚██╔╝██║██║██║   ██║██║   ██║██║  ██║
  ██████╔╝███████╗██║ ╚═╝ ██║██║╚██████╔╝╚██████╔╝██████╔╝
  ╚═════╝ ╚══════╝╚═╝     ╚═╝╚═╝ ╚═════╝  ╚═════╝ ╚═════╝ 
                                                    SKILLS
  `);
}

function printHelp() {
  printBanner();
  console.log(`  ${PACKAGE_NAME} v${VERSION}`);
  console.log(`  Claude skill suite by Vivid (Dheelep N)\n`);
  console.log(`  USAGE`);
  console.log(`    npx @demig0d2/skills <command> [skill]\n`);
  console.log(`  COMMANDS`);
  console.log(`    install <skill>   Install a skill to ~/.claude/skills/`);
  console.log(`    install all       Install all skills at once`);
  console.log(`    remove <skill>    Remove an installed skill`);
  console.log(`    remove all        Remove all demigod skills`);
  console.log(`    list              List all available skills`);
  console.log(`    status            Show which skills are installed`);
  console.log(`    info <skill>      Show details about a skill`);
  console.log(`    version           Show package version\n`);
  console.log(`  EXAMPLES`);
  console.log(`    npx @demig0d2/skills install book-writer`);
  console.log(`    npx @demig0d2/skills install all`);
  console.log(`    npx @demig0d2/skills status`);
  console.log(`    npx @demig0d2/skills remove humanizer\n`);
  console.log(`  SKILLS`);
  for (const [name, meta] of Object.entries(SKILLS)) {
    console.log(`    ${name.padEnd(22)} ${meta.description}`);
  }
  console.log();
}

function printList() {
  console.log(`\n  Available skills in @demig0d2/skills:\n`);
  for (const [name, meta] of Object.entries(SKILLS)) {
    const installed = fs.existsSync(getSkillDestPath(name));
    const status = installed ? "✓ installed" : "  available";
    console.log(`  ${status}  ${name.padEnd(22)} ${meta.description}`);
  }
  console.log();
}

function printStatus() {
  console.log(`\n  Skill status (install dir: ${getInstallDir()})\n`);
  for (const [name] of Object.entries(SKILLS)) {
    const installed = fs.existsSync(getSkillDestPath(name));
    const icon = installed ? "✓" : "✗";
    const label = installed ? "installed" : "not installed";
    console.log(`  ${icon}  ${name.padEnd(22)} ${label}`);
  }
  console.log();
}

function printInfo(skillName) {
  const resolved = resolveSkillName(skillName);
  if (!resolved) {
    console.error(`\n  ✗ Unknown skill: "${skillName}"`);
    console.error(`  Run: npx @demig0d2/skills list\n`);
    process.exit(1);
  }

  const meta = SKILLS[resolved];
  const installed = fs.existsSync(getSkillDestPath(resolved));
  const srcPath = getSkillSourcePath(resolved);
  const content = fs.readFileSync(srcPath, "utf8");
  const lines = content.split("\n").length;

  console.log(`\n  Skill: ${resolved}`);
  console.log(`  Description: ${meta.description}`);
  console.log(`  Aliases: ${meta.aliases.join(", ")}`);
  console.log(`  Size: ${lines} lines`);
  console.log(`  Installed: ${installed ? "Yes → " + getSkillDestPath(resolved) : "No"}`);
  console.log(`  Install: npx @demig0d2/skills install ${resolved}\n`);
}

// ─── Install ──────────────────────────────────────────────────────────────────

function installSkill(skillName) {
  const resolved = resolveSkillName(skillName);
  if (!resolved) {
    console.error(`  ✗ Unknown skill: "${skillName}"`);
    console.error(`  Available: ${ALL_SKILLS.join(", ")}\n`);
    process.exit(1);
  }

  const src = getSkillSourcePath(resolved);
  const dest = getSkillDestPath(resolved);
  const destDir = path.dirname(dest);

  if (!fs.existsSync(src)) {
    console.error(`  ✗ Source file missing: ${src}`);
    process.exit(1);
  }

  const alreadyInstalled = fs.existsSync(dest);

  ensureDir(destDir);
  fs.copyFileSync(src, dest);

  if (alreadyInstalled) {
    console.log(`  ↑ Updated: ${resolved}`);
  } else {
    console.log(`  ✓ Installed: ${resolved}`);
  }
  console.log(`    → ${dest}`);
}

function installAll() {
  console.log(`\n  Installing all @demig0d2/skills...\n`);
  for (const skillName of ALL_SKILLS) {
    installSkill(skillName);
  }
  console.log(`\n  All skills installed. Restart Claude to activate.\n`);
}

// ─── Remove ───────────────────────────────────────────────────────────────────

function removeSkill(skillName) {
  const resolved = resolveSkillName(skillName);
  if (!resolved) {
    console.error(`  ✗ Unknown skill: "${skillName}"`);
    process.exit(1);
  }

  const dest = getSkillDestPath(resolved);
  const destDir = path.dirname(dest);

  if (!fs.existsSync(dest)) {
    console.log(`  ○ Not installed: ${resolved} (nothing to remove)`);
    return;
  }

  fs.rmSync(destDir, { recursive: true, force: true });
  console.log(`  ✓ Removed: ${resolved}`);
}

function removeAll() {
  console.log(`\n  Removing all @demig0d2/skills...\n`);
  for (const skillName of ALL_SKILLS) {
    removeSkill(skillName);
  }
  console.log(`\n  All skills removed.\n`);
}

// ─── Main ─────────────────────────────────────────────────────────────────────

function main() {
  const args = process.argv.slice(2);
  const command = args[0];
  const target = args[1];

  if (!command || command === "help" || command === "--help" || command === "-h") {
    printHelp();
    return;
  }

  if (command === "version" || command === "--version" || command === "-v") {
    console.log(`${PACKAGE_NAME} v${VERSION}`);
    return;
  }

  if (command === "list" || command === "ls") {
    printList();
    return;
  }

  if (command === "status") {
    printStatus();
    return;
  }

  if (command === "info") {
    if (!target) {
      console.error(`\n  ✗ Specify a skill: npx @demig0d2/skills info <skill>\n`);
      process.exit(1);
    }
    printInfo(target);
    return;
  }

  if (command === "install") {
    if (!target) {
      console.error(`\n  ✗ Specify a skill or "all"\n`);
      console.error(`  Examples:`);
      console.error(`    npx @demig0d2/skills install book-writer`);
      console.error(`    npx @demig0d2/skills install all\n`);
      process.exit(1);
    }

    if (target === "all") {
      installAll();
    } else {
      console.log();
      installSkill(target);
      console.log(`\n  Restart Claude to activate the skill.\n`);
    }
    return;
  }

  if (command === "remove" || command === "uninstall") {
    if (!target) {
      console.error(`\n  ✗ Specify a skill or "all"\n`);
      process.exit(1);
    }

    if (target === "all") {
      removeAll();
    } else {
      console.log();
      removeSkill(target);
      console.log();
    }
    return;
  }

  // Unknown command
  console.error(`\n  ✗ Unknown command: "${command}"`);
  console.error(`  Run: npx @demig0d2/skills help\n`);
  process.exit(1);
}

main();
