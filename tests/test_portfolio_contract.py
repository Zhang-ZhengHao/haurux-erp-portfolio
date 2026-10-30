from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class PortfolioContractTests(unittest.TestCase):
    def test_page_targets_the_bid_brief_and_identity(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn('<span class="brand-mark">HX</span>', html)
        for phrase in (
            "HAURUX ERP Concept",
            "Zhenghao Zhang",
            "User",
            "Sales",
            "PR / PO",
            "IMS",
            "Accounting",
            "Concept / Demo",
            "Discuss your ERP",
        ):
            self.assertIn(phrase, html)


    def test_interactive_proof_hooks_exist(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        for hook in (
            'data-prototype="dashboard"',
            'data-prototype="users"',
            'data-prototype="procurement"',
            'data-prototype="inventory"',
            'data-prototype="sales"',
            'data-prototype="finance"',
            'data-workflow="procure"',
            'data-workflow="fulfil"',
            'data-workflow="reorder"',
        ):
            self.assertIn(hook, html)

    def test_every_erp_module_has_real_screen_content(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        for screen in (
            "Role permission matrix",
            "PR approval queue",
            "Inventory movement ledger",
            "Sales fulfilment board",
            "Accounting reconciliation",
        ):
            self.assertIn(screen, html)
        self.assertNotIn("screen ready", html)
        self.assertNotIn("can be expanded from this view", html)

    def test_screen_inventory_and_downloadable_portfolio_exist(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn('id="screenInventory"', html)
        self.assertIn('href="assets/HAURUX_ERP_UIUX_Portfolio.pdf"', html)
        self.assertIn("37 core web screens", html)
        self.assertTrue((ROOT / "assets" / "HAURUX_ERP_UIUX_Portfolio.pdf").is_file())

    def test_public_contact_is_direct_and_generic(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn('href="https://github.com/Zhang-ZhengHao#work-with-me--%E9%A1%B9%E7%9B%AE%E5%90%88%E4%BD%9C"', html)
        self.assertIn("Project inquiries", html)
        self.assertIn("GitHub inquiries are public and require sign-in.", html)
        self.assertNotIn("mailto:", html)


    def test_avatar_asset_is_present(self):
        avatar = ROOT / "assets" / "avatar.png"
        self.assertTrue(avatar.is_file())
        self.assertGreater(avatar.stat().st_size, 10_000)

    def test_content_is_visible_without_scroll_javascript(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertNotIn(".reveal { opacity: 0;", html)
