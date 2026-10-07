from pathlib import Path
import re
import struct
import unittest


ROOT = Path(__file__).resolve().parents[1]
PUBLIC_URL = "https://zhang-zhenghao.github.io/haurux-erp-portfolio/"
CHINESE_URL = f"{PUBLIC_URL}zh/"
PROTOTYPE_KEYS = ("dashboard", "users", "procurement", "inventory", "sales", "finance")
WORKFLOW_KEYS = ("procure", "fulfil", "reorder")


def read(relative_path: str) -> str:
    path = ROOT / relative_path
    if not path.is_file():
        raise AssertionError(f"Required file is missing: {relative_path}")
    return path.read_text(encoding="utf-8")


class ChinesePortfolioContractTests(unittest.TestCase):
    def test_english_page_exposes_the_chinese_edition_without_redirecting(self):
        html = read("index.html")
        for snippet in (
            f'<link rel="alternate" hreflang="en" href="{PUBLIC_URL}"',
            f'<link rel="alternate" hreflang="zh-CN" href="{CHINESE_URL}"',
            f'<link rel="alternate" hreflang="x-default" href="{PUBLIC_URL}"',
            '<meta property="og:locale" content="en_US"',
            '<meta property="og:locale:alternate" content="zh_CN"',
            'class="language-switch"',
            'data-language-link="zh-CN"',
            'href="zh/"',
            '>EN<',
            '>中文<',
            'haurux.locale-handoff.v1',
        ):
            self.assertIn(snippet, html)
        self.assertNotIn("navigator.language", html)
        self.assertNotIn("window.location.replace", html)

    def test_chinese_page_has_localized_metadata_navigation_and_assets(self):
        html = read("zh/index.html")
        for snippet in (
            '<html lang="zh-CN">',
            f'<link rel="canonical" href="{CHINESE_URL}"',
            f'<link rel="alternate" hreflang="en" href="{PUBLIC_URL}"',
            f'<link rel="alternate" hreflang="zh-CN" href="{CHINESE_URL}"',
            f'<link rel="alternate" hreflang="x-default" href="{PUBLIC_URL}"',
            '<meta property="og:locale" content="zh_CN"',
            '<meta property="og:locale:alternate" content="en_US"',
            f'<meta property="og:url" content="{CHINESE_URL}"',
            f'{PUBLIC_URL}assets/social-preview-zh-CN.png',
            '<meta name="twitter:card" content="summary_large_image"',
            'class="language-switch"',
            'data-language-link="en"',
            'href="../"',
            '>EN<',
            '>中文<',
            'aria-current="page">中文',
            '../assets/favicon.png',
            '../assets/HAURUX_ERP_UIUX_Portfolio_zh-CN.pdf',
            '../docs/images/zh-CN/dashboard.png',
            'system-ui',
            'PingFang SC',
            'Microsoft YaHei',
            'Noto Sans CJK SC',
            'WenQuanYi Zen Hei',
        ):
            self.assertIn(snippet, html)
        self.assertRegex(html, r'<meta property="og:title" content="[^"]*[\u3400-\u9fff]')
        self.assertRegex(html, r'<meta name="twitter:title" content="[^"]*[\u3400-\u9fff]')
        self.assertNotRegex(html, r'(?:href|src)="/(?!/)')
        self.assertNotIn("navigator.language", html)
        self.assertNotIn("window.location.replace", html)

    def test_chinese_page_preserves_the_complete_demo_contract(self):
        html = read("zh/index.html")
        for section_id in ("top", "brief", "prototype", "workflow", "proof", "system", "delivery", "bid"):
            self.assertIn(f'id="{section_id}"', html)
        for key in PROTOTYPE_KEYS:
            self.assertIn(f'data-prototype="{key}"', html)
            self.assertIn(f'data-nav="{key}"', html)
        for key in WORKFLOW_KEYS:
            self.assertIn(f'data-workflow="{key}"', html)
        for phrase in (
            "运营看板",
            "用户与角色",
            "采购",
            "库存",
            "销售订单",
            "财务核算",
            "37 个界面",
            "概念演示（Concept / Demo）",
            "合成演示数据（Synthetic data）",
            "Zhenghao Zhang",
            "可通过 X 或你发现此作品集的招聘平台联系我。",
            'id="protoActionStatus"',
            'aria-live="polite"',
        ):
            self.assertIn(phrase, html)
        self.assertGreater(len(re.findall(r"[\u3400-\u9fff]", html)), 1_000)

    def test_chinese_repository_documents_cover_scope_evidence_and_limits(self):
        readme = read("README.zh-CN.md")
        case_study = read("CASE_STUDY.zh-CN.md")
        for phrase in (
            CHINESE_URL,
            f"{PUBLIC_URL}assets/HAURUX_ERP_UIUX_Portfolio_zh-CN.pdf",
            "37 个界面",
            "概念演示（Concept / Demo）",
            "合成演示数据（Synthetic data）",
            "LICENSE.md",
            "docs/images/zh-CN/",
        ):
            self.assertIn(phrase, readme + case_study)
        for heading in (
            "## 项目背景",
            "## 约束与假设",
            "## 信息架构",
            "## 核心工作流",
            "## 设计决策",
            "## 响应式与无障碍设计",
            "## 验证",
            "## 从概念到正式产品",
            "## 诚信声明",
        ):
            self.assertIn(heading, case_study)
        self.assertIn("CASE_STUDY.zh-CN.md", readme)
        self.assertIn("README.md", readme)
        self.assertIn("CASE_STUDY.md", case_study)
        self.assertGreater(len(re.findall(r"[\u3400-\u9fff]", readme + case_study)), 2_500)

    def test_english_repository_documents_expose_the_chinese_edition(self):
        readme = read("README.md")
        case_study = read("CASE_STUDY.md")
        self.assertIn("README.zh-CN.md", readme)
        self.assertIn("CASE_STUDY.zh-CN.md", case_study)
        for content in (readme, case_study):
            self.assertIn(CHINESE_URL, content)
            self.assertIn("assets/HAURUX_ERP_UIUX_Portfolio_zh-CN.pdf", content)

    def test_chinese_print_source_has_nine_localized_pages(self):
        printable = read("portfolio-print.zh-CN.html")
        self.assertIn('<html lang="zh-CN">', printable)
        self.assertEqual(printable.count('<section class="page'), 9)
        for phrase in (
            "WenQuanYi Zen Hei",
            "复杂 ERP",
            "清晰易用。",
            "37 个界面",
            "用户与角色",
            "采购",
            "销售履约",
            "设计系统",
            "交付",
            "概念演示（Concept / Demo）",
            "合成演示数据（Synthetic data）",
            "09 / 09",
        ):
            self.assertIn(phrase, printable)
        self.assertGreater(len(re.findall(r"[\u3400-\u9fff]", printable)), 2_000)

    def test_chinese_print_badges_do_not_wrap(self):
        printable = read("portfolio-print.zh-CN.html")
        self.assertRegex(
            printable,
            r"\.badge\s*\{[^}]*white-space:\s*nowrap",
            "Chinese PDF status badges must stay on one line",
        )

    def test_public_gitignore_contains_only_generic_patterns(self):
        patterns = read(".gitignore").splitlines()
        self.assertEqual(patterns, ["__pycache__/", "*.py[cod]", ".DS_Store"])

    def test_public_readme_describes_branch_publishing_without_actions_badges(self):
        readme = read("README.md")
        self.assertIn("GitHub Pages publishes the verified public tree from `main /`", readme)
        self.assertNotIn("actions/workflows/", readme)
        self.assertNotIn("GitHub Pages automation", readme)

    def test_both_pages_declare_the_transient_language_state_protocol(self):
        for relative_path in ("index.html", "zh/index.html"):
            html = read(relative_path)
            for snippet in (
                "const LANGUAGE_STATE_KEY = 'haurux.locale-handoff.v1'",
                "const LANGUAGE_STATE_VERSION = 1",
                "const LANGUAGE_STATE_TTL_MS = 5 * 60 * 1000",
                "['dashboard', 'users', 'procurement', 'inventory', 'sales', 'finance']",
                "['procure', 'fulfil', 'reorder']",
                "sessionStorage.setItem(LANGUAGE_STATE_KEY",
                "sessionStorage.getItem(LANGUAGE_STATE_KEY)",
                "sessionStorage.removeItem(LANGUAGE_STATE_KEY)",
                "requestAnimationFrame(() => requestAnimationFrame",
            ):
                self.assertIn(snippet, html, relative_path)

    def test_chinese_evidence_images_have_the_expected_dimensions(self):
        expected = {
            "docs/images/zh-CN/portfolio-cover.png": (1440, 900),
            "docs/images/zh-CN/dashboard.png": (1240, 724),
            "docs/images/zh-CN/role-permissions.png": (1240, 804),
            "docs/images/zh-CN/procurement.png": (1240, 781),
            "docs/images/zh-CN/inventory.png": (1240, 816),
            "docs/images/zh-CN/sales.png": (1240, 756),
            "docs/images/zh-CN/accounting.png": (1240, 741),
            "docs/images/zh-CN/mobile-accounting.png": (358, 1003),
            "assets/social-preview-zh-CN.png": (1280, 640),
        }
        for relative_path, dimensions in expected.items():
            path = ROOT / relative_path
            self.assertTrue(path.is_file(), relative_path)
            self.assertGreater(path.stat().st_size, 20_000, relative_path)
            header = path.read_bytes()[:24]
            self.assertEqual(header[:8], b"\x89PNG\r\n\x1a\n", relative_path)
            self.assertEqual(struct.unpack(">II", header[16:24]), dimensions, relative_path)

    def test_chinese_pdf_is_a_substantial_public_asset(self):
        pdf = ROOT / "assets" / "HAURUX_ERP_UIUX_Portfolio_zh-CN.pdf"
        self.assertTrue(pdf.is_file())
        self.assertGreater(pdf.stat().st_size, 500_000)
        self.assertEqual(pdf.read_bytes()[:5], b"%PDF-")
        html = read("portfolio-print.zh-CN.html")
        self.assertIn("HAURUX_ERP_UIUX_Portfolio_zh-CN.pdf", read("zh/index.html"))
        self.assertEqual(html.count('<section class="page'), 9)


if __name__ == "__main__":
    unittest.main()
