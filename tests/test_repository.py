"""Проверки переносимого пакета и изолированной GitHub-обёртки."""

import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/clear-writing"


class SkillPackageTest(unittest.TestCase):
    def test_language_editions_have_the_same_files(self):
        inventories = [{path.relative_to(SKILL / language) for path in
                        (SKILL / language).rglob("*.md")} for language in ("ru", "en")]
        self.assertEqual(inventories[0], inventories[1])
        self.assertEqual(12, len(inventories[0]))

    def test_frontmatter_and_technical_routing(self):
        entry = (SKILL / "SKILL.md").read_text()
        self.assertTrue(entry.startswith("---\nname: clear-writing\ndescription: "))
        self.assertIn('version: "10"', entry)
        for language in ("ru", "en"):
            self.assertIn(f"({language}/technical.md)", entry)
            self.assertIn("(technical.md)", (SKILL / language / "guide.md").read_text())

    def test_relative_markdown_links_exist(self):
        for source in ROOT.rglob("*.md"):
            if ".git" in source.relative_to(ROOT).parts:
                continue
            for target in re.findall(r"\]\(([^\s)]+)\)", source.read_text()):
                if ":" in target or target.startswith("#"):
                    continue
                with self.subTest(source=source, target=target):
                    self.assertTrue((source.parent / target.split("#")[0]).exists())


class GitHubWrapperTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        (self.root / "bin").mkdir()
        shutil.copy2(ROOT / "bin/gh", self.root / "bin/gh")
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        self.credentials = self.root / ".git/gh"
        self.credentials.mkdir(mode=0o700)
        self.hosts = self.credentials / "hosts.yml"
        self.hosts.write_text("github.com:\n  user: serge-masiutin\n  users:\n"
                              "    serge-masiutin:\n      oauth_token: test-only-token\n")
        self.hosts.chmod(0o600)
        fake_bin = self.root / "fake-bin"
        fake_bin.mkdir()
        fake_cli = fake_bin / "gh"
        fake_cli.write_text("#!/usr/bin/env python3\n"
                            "import json, os, sys\n"
                            "if os.environ.get('TEST_API_FAILURE'):\n"
                            "    sys.exit('simulated API failure')\n"
                            "if sys.argv[1:] == ['api', 'user', '--jq', '.login']:\n"
                            "    print(os.environ['TEST_LOGIN'])\n"
                            "else:\n"
                            "    keys = ['GH_CONFIG_DIR', 'GH_TOKEN', 'GITHUB_TOKEN', "
                            "'GH_ENTERPRISE_TOKEN', 'GITHUB_ENTERPRISE_TOKEN', "
                            "'GH_HOST', 'GH_REPO', 'GH_DEBUG', 'DEBUG']\n"
                            "    print(json.dumps({'argv': sys.argv[1:], "
                            "'env': {k: os.environ.get(k) for k in keys}}))\n")
        fake_cli.chmod(0o700)
        self.environment = dict(os.environ, PATH=f"{fake_bin}:{os.environ['PATH']}",
                                TEST_LOGIN="serge-masiutin", GH_TOKEN="external",
                                GITHUB_TOKEN="external", GH_ENTERPRISE_TOKEN="external",
                                GITHUB_ENTERPRISE_TOKEN="external", GH_DEBUG="api",
                                DEBUG="1", GH_REPO="other/repository", GH_HOST="other.host")

    def run_wrapper(self, *arguments):
        return subprocess.run(["ruby", str(self.root / "bin/gh"), *arguments],
                              env=self.environment, capture_output=True, text=True)

    def test_uses_project_credentials_and_clears_external_environment(self):
        result = self.run_wrapper("pr", "list")
        self.assertEqual(0, result.returncode, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(["pr", "list"], report["argv"])
        self.assertEqual("test-only-token", report["env"]["GH_TOKEN"])
        self.assertEqual(self.credentials.resolve(), Path(report["env"]["GH_CONFIG_DIR"]).resolve())
        self.assertEqual("serge-masiutin/clear-writing", report["env"]["GH_REPO"])
        self.assertEqual("github.com", report["env"]["GH_HOST"])
        for key in ("GITHUB_TOKEN", "GH_ENTERPRISE_TOKEN", "GITHUB_ENTERPRISE_TOKEN",
                    "GH_DEBUG", "DEBUG"):
            self.assertIsNone(report["env"][key])

    def test_wrong_api_identity_blocks_command(self):
        self.environment["TEST_LOGIN"] = "another-user"
        result = self.run_wrapper("pr", "list")
        self.assertNotEqual(0, result.returncode)
        self.assertEqual("", result.stdout)
        self.assertIn("ожидался serge-masiutin", result.stderr)

    def test_api_failure_blocks_command(self):
        self.environment["TEST_API_FAILURE"] = "1"
        result = self.run_wrapper("pr", "list")
        self.assertNotEqual(0, result.returncode)
        self.assertEqual("", result.stdout)
        self.assertIn("Не удалось проверить аккаунт", result.stderr)

    def test_wrong_stored_identity_blocks_command(self):
        self.hosts.write_text(self.hosts.read_text().replace("user: serge-masiutin",
                                                            "user: another-user"))
        result = self.run_wrapper("pr", "list")
        self.assertNotEqual(0, result.returncode)
        self.assertEqual("", result.stdout)
        self.assertIn("Аккаунт проекта должен быть", result.stderr)

    def test_auth_mutations_are_blocked_but_status_is_allowed(self):
        for action in ("login", "logout", "switch", "token", "refresh", "setup-git"):
            with self.subTest(action=action):
                result = self.run_wrapper("auth", action)
                self.assertNotEqual(0, result.returncode)
                self.assertEqual("", result.stdout)
        self.assertEqual(0, self.run_wrapper("auth", "status").returncode)

    def test_permissions_are_required(self):
        for path, unsafe_mode, safe_mode in ((self.hosts, 0o644, 0o600),
                                              (self.credentials, 0o755, 0o700)):
            with self.subTest(path=path):
                path.chmod(unsafe_mode)
                result = self.run_wrapper("pr", "list")
                self.assertNotEqual(0, result.returncode)
                self.assertEqual("", result.stdout)
                path.chmod(safe_mode)

    def test_missing_credentials_fail_without_global_login(self):
        self.hosts.unlink()
        result = self.run_wrapper("pr", "list")
        self.assertNotEqual(0, result.returncode)
        self.assertIn("bin/gh-login", result.stderr)
        self.assertEqual("", result.stdout)


class GitSetupTest(unittest.TestCase):
    def test_setup_changes_only_repository_configuration(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            repository = root / "repository"
            (repository / "bin").mkdir(parents=True)
            shutil.copy2(ROOT / "bin/setup-git", repository / "bin/setup-git")
            subprocess.run(["git", "init", "-q", str(repository)], check=True)
            home = root / "home"
            (home / ".ssh").mkdir(parents=True)
            key = home / ".ssh/id_ed25519_serge_masiutin_gh"
            key.write_text("test-only-placeholder-not-a-key")
            global_config = home / ".gitconfig"
            original = "[user]\n\tname = Unrelated User\n\temail = unrelated@example.invalid\n"
            global_config.write_text(original)
            environment = dict(os.environ, HOME=str(home), GIT_CONFIG_GLOBAL=str(global_config))
            subprocess.run(["bash", str(repository / "bin/setup-git")],
                           env=environment, check=True, capture_output=True)
            self.assertEqual(original, global_config.read_text())
            for setting, expected in (("user.name", "Serge Masiutin"),
                                      ("user.email", "sergeimasiutin@gmail.com"),
                                      ("user.signingkey", str(key)), ("gpg.format", "ssh"),
                                      ("commit.gpgsign", "true")):
                result = subprocess.run(["git", "-C", str(repository), "config", "--local",
                                         "--get", setting], env=environment, check=True,
                                        capture_output=True, text=True)
                self.assertEqual(expected, result.stdout.strip())


if __name__ == "__main__":
    unittest.main()
