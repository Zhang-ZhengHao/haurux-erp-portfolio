from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
PUBLIC_URL = "https://zhang-zhenghao.github.io/haurux-erp-portfolio/"
PROFILE_URL = "https://github.com/zhang-zhenghao"
PERSONAL_GMAIL_PATTERN = re.compile(
    r"\b[A-Z0-9._%+-]+@gmail[.]com\b",
    re.IGNORECASE,
)
LEGACY_ACCOUNT_PATTERN = re.compile(
    r"\b\d{11,}(?:z-droid|zzh-dotcom)\b",
    re.IGNORECASE,
)


def read(relative_path: str) -> str:
    path = ROOT / relative_path
    if not path.is_file():
        raise AssertionError(f"Required file is missing: {relative_path}")
    return path.read_text(encoding="utf-8")


class GitHubPresenceContractTests(unittest.TestCase):
    def test_public_source_manifest_is_exact_and_resolvable(self):
        manifest = read(".github/public-files.txt").splitlines()
        expected = sorted((
            ".github/public-files.txt",
            ".gitignore",
            ".nojekyll",
            "CASE_STUDY.md",
            "CASE_STUDY.zh-CN.md",
            "LICENSE.md",
            "README.md",
            "README.zh-CN.md",
            "assets/HAURUX_ERP_UIUX_Portfolio.pdf",
            "assets/HAURUX_ERP_UIUX_Portfolio_zh-CN.pdf",
            "assets/avatar.png",
            "assets/favicon.png",
            "assets/social-preview.png",
            "assets/social-preview-zh-CN.png",
            "docs/images/accounting.png",
            "docs/images/dashboard.png",
            "docs/images/inventory.png",
            "docs/images/mobile-accounting.png",
            "docs/images/portfolio-cover.png",
            "docs/images/procurement.png",
            "docs/images/role-permissions.png",
            "docs/images/sales.png",
            "docs/images/zh-CN/accounting.png",
            "docs/images/zh-CN/dashboard.png",
            "docs/images/zh-CN/inventory.png",
            "docs/images/zh-CN/mobile-accounting.png",
            "docs/images/zh-CN/portfolio-cover.png",
            "docs/images/zh-CN/procurement.png",
            "docs/images/zh-CN/role-permissions.png",
            "docs/images/zh-CN/sales.png",
            "index.html",
            "portfolio-print.html",
            "portfolio-print.zh-CN.html",
            "tests/test_chinese_portfolio_contract.py",
            "tests/test_github_presence_contract.py",
            "tests/test_portfolio_contract.py",
            "zh/index.html",
        ))
        self.assertEqual(manifest, expected)
        for relative_path in manifest:
            self.assertTrue((ROOT / relative_path).is_file(), relative_path)

    def test_public_source_manifest_excludes_internal_only_files(self):
        manifest = read(".github/public-files.txt").splitlines()
        forbidden_files = {
            "BID_MESSAGE_ID.txt",
            "app.toml",
            "tests/test_managed_product_contract.py",
            "tests/test_private_bid_contract.py",
            "tests/test_profile_contract.py",
        }
        forbidden_prefixes = (
            ".github/workflows/",
            ".webtest/",
            ".worktrees/",
            "docs/superpowers/",
            "github-profile/",
            "scripts/",
        )
        self.assertTrue(forbidden_files.isdisjoint(manifest))
        for relative_path in manifest:
            self.assertFalse(
                relative_path.startswith(forbidden_prefixes),
                f"Internal-only path is public: {relative_path}",
            )

    def test_public_portfolio_tests_do_not_require_platform_files(self):
        public_test = read("tests/test_portfolio_contract.py")
        self.assertNotIn('ROOT / "app.toml"', public_test)

    def test_public_text_source_contains_no_personal_gmail_address(self):
        manifest = read(".github/public-files.txt").splitlines()
        text_suffixes = {".html", ".md", ".py", ".txt"}
        combined = "\n".join(
            read(relative_path)
            for relative_path in manifest
            if Path(relative_path).suffix.lower() in text_suffixes
        )
        self.assertIsNone(PERSONAL_GMAIL_PATTERN.search(combined))

    def test_repository_readme_is_an_english_case_study_landing_page(self):
        readme = read("README.md")
        for phrase in (
            "HAURUX ERP Concept",
            "Zhenghao Zhang",
            "ERP UI/UX Concept Portfolio",
            "Live Demo",
            "Download PDF",
            "Read the Case Study",
            "37-screen",
            "User & Role",
            "Concept / Demo",
            PUBLIC_URL,
            "Simplified Chinese",
            "GitHub Pages publishes the verified public tree from `main /`",
        ):
            self.assertIn(phrase, readme)
        self.assertIsNone(re.search(r"[\u3400-\u9fff]", readme))

    def test_migrated_public_copy_uses_personal_identity_without_private_contact(self):
        public_text_paths = (
            "README.md",
            "README.zh-CN.md",
            "CASE_STUDY.md",
            "CASE_STUDY.zh-CN.md",
            "LICENSE.md",
            "index.html",
            "zh/index.html",
            "portfolio-print.html",
            "portfolio-print.zh-CN.html",
        )
        combined = "\n".join(read(path) for path in public_text_paths)
        self.assertIn("Zhenghao Zhang", combined)
        self.assertIn("HAURUX ERP Concept", combined)
        self.assertIn(PROFILE_URL, combined)
        self.assertIsNone(LEGACY_ACCOUNT_PATTERN.search(combined))
        self.assertIsNone(PERSONAL_GMAIL_PATTERN.search(combined))
        self.assertNotIn("HAURUX TECH STUDIO", combined)
        self.assertNotIn("mailto:", combined)

    def test_detailed_english_case_study_documents_decisions_and_limits(self):
        case_study = read("CASE_STUDY.md")
        for heading in (
            "## Context",
            "## Constraints and Assumptions",
            "## Information Architecture",
            "## Key Workflows",
            "## Design Decisions",
            "## Responsive and Accessible by Design",
            "## Validation",
            "## From Concept to Production",
            "## Integrity Statement",
        ):
            self.assertIn(heading, case_study)
        self.assertIn("synthetic data", case_study)
        self.assertIn("37", case_study)
        self.assertIsNone(re.search(r"[\u3400-\u9fff]", case_study))

    def test_code_and_portfolio_assets_have_separate_rights(self):
        license_text = read("LICENSE.md")
        self.assertIn("MIT License", license_text)
        self.assertIn("Portfolio Assets", license_text)
        self.assertIn("All Rights Reserved", license_text)
        for asset_type in ("portrait", "screenshots", "PDF", "case-study content"):
            self.assertIn(asset_type, license_text)

    def test_real_erp_screenshots_are_present(self):
        expected = (
            "portfolio-cover.png",
            "dashboard.png",
            "role-permissions.png",
            "procurement.png",
            "inventory.png",
            "sales.png",
            "accounting.png",
            "mobile-accounting.png",
        )
        image_dir = ROOT / "docs" / "images"
        for name in expected:
            image = image_dir / name
            self.assertTrue(image.is_file(), name)
            self.assertGreater(image.stat().st_size, 20_000, name)

        social_preview = ROOT / "assets" / "social-preview.png"
        self.assertTrue(social_preview.is_file())
        self.assertGreater(social_preview.stat().st_size, 20_000)

    def test_live_page_has_complete_share_metadata(self):
        html = read("index.html")
        for snippet in (
            f'<link rel="canonical" href="{PUBLIC_URL}"',
            '<meta property="og:type" content="website"',
            '<meta property="og:title"',
            '<meta property="og:description"',
            f'<meta property="og:image" content="{PUBLIC_URL}assets/social-preview.png"',
            '<meta name="twitter:card" content="summary_large_image"',
            f'content="{PUBLIC_URL}assets/social-preview.png"',
            '<link rel="icon" type="image/png" href="assets/favicon.png"',
        ):
            self.assertIn(snippet, html)
        favicon = ROOT / "assets" / "favicon.png"
        self.assertTrue(favicon.is_file())
        self.assertGreater(favicon.stat().st_size, 1_000)

    def test_live_screen_inventory_matches_the_case_study(self):
        html = read("index.html")
        for snippet in (
            "Foundation & navigation <span>5 screens</span>",
            "User & access <span>5 screens</span>",
            "Sales <span>8 screens</span>",
            "PR / PO <span>8 screens</span>",
            "IMS / Inventory <span>6 screens</span>",
            "Accounting <span>5 screens</span>",
        ):
            self.assertIn(snippet, html)

    def test_live_site_uses_a_generic_project_contact_section(self):
        html = read("index.html")
        for phrase in (
            "Start with one clear workflow.",
            "Current product",
            "Roles and rules",
            "First milestone",
            "Discuss your ERP",
        ):
            self.assertIn(phrase, html)
        self.assertNotIn('id="copyBid"', html)
        self.assertNotIn('id="bidText"', html)

    def test_live_site_has_consistent_english_positioning(self):
        html = read("index.html")
        for phrase in (
            '<html lang="en">',
            "Complex ERP,",
            "Explore the case study",
            "Complex operations should not feel complex on screen.",
            "A prototype you can test, not just view.",
            "Every screen earns its place.",
            "Evidence, not claims",
            "A system built to scale.",
        ):
            self.assertIn(phrase, html)

    def test_live_site_keeps_concept_claims_verifiable(self):
        html = read("index.html")
        self.assertIn("Concept / Demo · Synthetic data", html)
        self.assertIn("Interactive web prototype", html)
        self.assertIn("Concept pattern · Exception management", html)
        self.assertNotIn("Figma-ready", html)
        self.assertNotIn("Flood and dam inspection system", html)

    def test_dashboard_date_and_demo_action_are_not_misleading(self):
        html = read("index.html")
        self.assertIn("Sunday, 27 Sep 2026", html)
        self.assertNotIn("Tuesday, 27 Sep", html)
        self.assertIn('id="protoActionStatus"', html)
        self.assertIn("does not submit or export production data", html)
        self.assertIn("protoAction.addEventListener('click'", html)

    def test_internal_github_actions_are_sane_when_available(self):
        manifest = read(".github/public-files.txt").splitlines()
        workflow_paths = (
            ".github/workflows/verify.yml",
            ".github/workflows/deploy-pages.yml",
        )
        for workflow_path in workflow_paths:
            self.assertNotIn(workflow_path, manifest)

        workflow_presence = [(ROOT / path).is_file() for path in workflow_paths]
        self.assertIn(workflow_presence, ([False, False], [True, True]))
        if not any(workflow_presence):
            return

        verify = read(workflow_paths[0])
        deploy = read(workflow_paths[1])
        self.assertIn("python3 -m unittest discover -s tests -v", verify)
        self.assertIn("pull_request:", verify)
        self.assertIn("workflow_run:", deploy)
        self.assertIn("Verify Portfolio", deploy)
        self.assertIn("github.event.workflow_run.conclusion == 'success'", deploy)
        self.assertIn("actions/checkout@v7", verify)
        self.assertIn("actions/setup-python@v7", verify)
        self.assertIn("actions/configure-pages@v6", deploy)
        self.assertIn("actions/upload-pages-artifact@v5", deploy)
        self.assertIn("actions/deploy-pages@v5", deploy)
        self.assertGreaterEqual((verify + deploy).count("persist-credentials: false"), 3)
        self.assertNotIn("cp -R assets", deploy)
        for public_asset in (
            "assets/HAURUX_ERP_UIUX_Portfolio.pdf",
            "assets/avatar.png",
            "assets/favicon.png",
            "assets/social-preview.png",
            "docs/images/dashboard.png",
            "docs/images/role-permissions.png",
        ):
            self.assertIn(public_asset, deploy)

    def test_live_site_uses_only_relevant_erp_proof_images(self):
        html = read("index.html")
        self.assertIn('src="docs/images/dashboard.png"', html)
        self.assertIn('src="docs/images/role-permissions.png"', html)
        self.assertNotIn("lead-automation.png", html)
        self.assertNotIn("research-brief.png", html)

    def test_print_portfolio_is_an_english_reusable_concept(self):
        printable = read("portfolio-print.html")
        self.assertIn('<html lang="en">', printable)
        self.assertIn("Complex ERP", printable)
        self.assertIn("Self-initiated concept study", printable)
        self.assertIn("Portfolio integrity statement", printable)

    def test_new_public_copy_has_no_em_or_en_dashes(self):
        copy_paths = (
            "README.md",
            "README.zh-CN.md",
            "CASE_STUDY.md",
            "CASE_STUDY.zh-CN.md",
            "LICENSE.md",
            "zh/index.html",
            "portfolio-print.html",
            "portfolio-print.zh-CN.html",
        )
        for path in copy_paths:
            content = read(path)
            self.assertNotRegex(content, r"[—–]", path)


if __name__ == "__main__":
    unittest.main()
