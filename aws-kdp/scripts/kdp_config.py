"""Global KDP constants — single place to tweak.

Cover math, page math, and royalty constants used across agents.
"""

from __future__ import annotations

# ────────────────────────────────────────────────────────
# Cover math (KDP paperback, white paper, US marketplace)
# ────────────────────────────────────────────────────────

# spine_width (inches) = page_count × SPINE_PER_PAGE_WHITE
SPINE_PER_PAGE_WHITE = 0.002252
SPINE_PER_PAGE_CREAM = 0.0025

BLEED_IN = 0.125
LIVE_AREA_MARGIN_IN = 0.25   # keep text 0.25" from trim
BARCODE_SIZE_IN = (1.5, 1.5) # W × H on back cover bottom-right
BARCODE_MARGIN_IN = 0.25
MIN_SPINE_FOR_TEXT_IN = 0.125 # KDP: below this, spine cannot carry text


TRIM_SIZES = {
    "8.5x11":  (8.5, 11.0),
    "8.5x8.5": (8.5, 8.5),
    "6x9":     (6.0, 9.0),
    "7x10":    (7.0, 10.0),
    "8x10":    (8.0, 10.0),
}


def spine_width_inches(page_count: int, paper: str = "white") -> float:
    rate = SPINE_PER_PAGE_WHITE if paper == "white" else SPINE_PER_PAGE_CREAM
    return round(page_count * rate + 1e-9, 4)


def full_cover_dims(page_size: str, page_count: int, paper: str = "white") -> dict:
    """Return full cover dimensions (width, height, spine) in inches for KDP upload."""
    if page_size not in TRIM_SIZES:
        raise ValueError(f"unknown page_size {page_size}; supported: {list(TRIM_SIZES)}")
    trim_w, trim_h = TRIM_SIZES[page_size]
    spine = spine_width_inches(page_count, paper)
    full_w = round(trim_w + spine + trim_w + 2 * BLEED_IN, 4)
    full_h = round(trim_h + 2 * BLEED_IN, 4)
    return {
        "trim_size": page_size,
        "trim_width_in": trim_w,
        "trim_height_in": trim_h,
        "spine_width_in": spine,
        "full_width_in": full_w,
        "full_height_in": full_h,
        "bleed_in": BLEED_IN,
        "live_margin_in": LIVE_AREA_MARGIN_IN,
        "spine_can_have_text": spine >= MIN_SPINE_FOR_TEXT_IN,
    }


# ────────────────────────────────────────────────────────
# Royalty math (KDP paperback, 60% royalty rate, US marketplace)
# ────────────────────────────────────────────────────────

PRINTING_FIXED_USD = 0.85
PRINTING_PER_PAGE_BW = 0.012    # black-and-white interior
PRINTING_PER_PAGE_COLOR = 0.07  # color interior (premium)

ROYALTY_RATE_PAPERBACK = 0.60
KENP_RATE_USD = 0.0045           # approximate US KDP Select KENP read rate


def printing_cost_usd(page_count: int, color: bool = False) -> float:
    per_page = PRINTING_PER_PAGE_COLOR if color else PRINTING_PER_PAGE_BW
    return round(PRINTING_FIXED_USD + page_count * per_page, 3)


def royalty_per_sale_usd(list_price: float, page_count: int, color: bool = False) -> float:
    return round((list_price - printing_cost_usd(page_count, color)) * ROYALTY_RATE_PAPERBACK, 3)


def break_even_acos_pct(list_price: float, page_count: int, color: bool = False) -> float:
    royalty = royalty_per_sale_usd(list_price, page_count, color)
    if list_price <= 0:
        return 0.0
    return round(100 * royalty / list_price, 2)


def max_cpc_usd(
    list_price: float,
    page_count: int,
    target_acos_pct: float = 40,
    conversion_rate_pct: float = 8,
    color: bool = False,
) -> float:
    royalty = royalty_per_sale_usd(list_price, page_count, color)
    return round(royalty * (target_acos_pct / 100.0) * (conversion_rate_pct / 100.0), 3)


# ────────────────────────────────────────────────────────
# BSR → Sales/day conversion (US paperback, approximate)
#
# Piecewise estimates compiled from Publisher Rocket, KDSPY, Book Bolt
# community data 2023-2025. Each tier returns (low, mid, high) estimates.
# These are ESTIMATES — real sales vary by category and season. Use the
# MID value for point estimates, the RANGE for confidence intervals.
# ────────────────────────────────────────────────────────

BSR_TIERS = [
    # (min_bsr, max_bsr, low_sales, mid_sales, high_sales)
    (1,        10,        2000,  3500,  5000),
    (11,       100,       300,   900,   2000),
    (101,      1_000,     80,    160,   300),
    (1_001,    5_000,     25,    45,    80),
    (5_001,    10_000,    10,    17,    25),
    (10_001,   25_000,    6,     9,     13),
    (25_001,   50_000,    3,     5,     8),
    (50_001,   100_000,   1.5,   2.5,   4),
    (100_001,  200_000,   0.7,   1.2,   2),
    (200_001,  500_000,   0.2,   0.4,   0.8),
    (500_001,  1_000_000, 0.05,  0.12,  0.25),
    (1_000_001, 99_999_999, 0.01, 0.03, 0.07),
]


def bsr_to_daily_sales(bsr: int) -> dict:
    """Return estimated daily sales range for a given BSR.

    Returns dict with low/mid/high daily sales estimates + tier description.
    """
    if bsr is None or bsr <= 0:
        return {"low": 0, "mid": 0, "high": 0, "tier": "invalid"}
    for lo, hi, l, m, h in BSR_TIERS:
        if lo <= bsr <= hi:
            return {"low": l, "mid": m, "high": h, "tier": f"BSR {lo:,}–{hi:,}"}
    return {"low": 0, "mid": 0, "high": 0, "tier": "out_of_range"}


def estimate_monthly_royalty(
    bsr: int, list_price: float, page_count: int, color: bool = False
) -> dict:
    """End-to-end monthly royalty estimate for a book at a given BSR."""
    sales = bsr_to_daily_sales(bsr)
    royalty = royalty_per_sale_usd(list_price, page_count, color)
    return {
        "bsr": bsr,
        "daily_sales_low": sales["low"],
        "daily_sales_mid": sales["mid"],
        "daily_sales_high": sales["high"],
        "royalty_per_sale_usd": royalty,
        "monthly_low_usd": round(sales["low"] * 30 * royalty, 2),
        "monthly_mid_usd": round(sales["mid"] * 30 * royalty, 2),
        "monthly_high_usd": round(sales["high"] * 30 * royalty, 2),
    }


# ────────────────────────────────────────────────────────
# Niche scoring — Blue Ocean framework
# ────────────────────────────────────────────────────────

def opportunity_score(
    avg_monthly_sales_top10: float, avg_review_count_top10: float
) -> dict:
    """Industry-standard Opportunity Score.

    Opportunity = monthly_sales / reviews.
    High score = lots of sales but few reviews = break-in easy (new market).
    Low score = many reviews = saturated, hard for new books to rank.
    """
    if avg_review_count_top10 <= 0:
        # Division by zero — treat as infinite opportunity (brand new niche)
        opp = 999
        tier = "BLUE_OCEAN"
    else:
        opp = round(avg_monthly_sales_top10 / avg_review_count_top10, 3)
        if opp >= 5:
            tier = "BLUE_OCEAN"
        elif opp >= 2:
            tier = "MODERATE"
        elif opp >= 0.5:
            tier = "COMPETITIVE"
        else:
            tier = "SATURATED"
    return {"opportunity": opp, "tier": tier}


def competition_strength(
    avg_review_count_top10: float,
    avg_age_days_top10: float,
    avg_rating_top10: float = 4.3,
) -> dict:
    """Composite competition score (lower = easier to break in)."""
    # Normalize each signal to 0-10
    review_score = min(10, avg_review_count_top10 / 50)           # 50 reviews ≈ 1 point
    age_score = min(10, avg_age_days_top10 / 180)                 # 1800 days ≈ 10
    rating_score = max(0, (avg_rating_top10 - 3.0) * 5)           # 3.0 → 0, 5.0 → 10
    composite = round((review_score + age_score + rating_score) / 3, 2)
    return {
        "composite_0_to_10": composite,
        "review_score": round(review_score, 2),
        "age_score": round(age_score, 2),
        "rating_score": round(rating_score, 2),
    }


# Hard-elimination rules — applied BEFORE scoring
HARD_ELIMINATION_RULES = {
    "dead_market": {
        "condition": "top3_bsr_all > 300_000",
        "reason": "All top-3 books selling < 1 copy/day — no real demand",
    },
    "over_saturated": {
        "condition": "top10_reviews_all > 500 AND all_4_star_plus",
        "reason": "Big established players — new books can't rank without huge ad budget",
    },
    "race_to_bottom": {
        "condition": "top10_price_all <= 6.99 AND top10_pages_all <= 50",
        "reason": "Generic low-quality books at rock-bottom prices — no margin",
    },
    "single_publisher_lock": {
        "condition": "top10_same_publisher_count >= 6",
        "reason": "One publisher dominates — likely has amz internal promotion",
    },
    "seasonal_missed_window": {
        "condition": "seasonal AND days_to_peak < 75",
        "reason": "KDP review (72h) + SEO warmup (30-60 days) = launch too late",
    },
    "ip_trap": {
        "condition": "niche_contains_trademark",
        "reason": "Character/brand name in keyword — auto-reject pipeline",
    },
}


def apply_hard_elimination(niche_data: dict) -> list[str]:
    """Return list of violated rules. Empty list = niche passes hard filter."""
    violations = []
    top3 = niche_data.get("top3_bsr", [])
    top10_reviews = niche_data.get("top10_reviews", [])
    top10_prices = niche_data.get("top10_prices", [])
    top10_pages = niche_data.get("top10_pages", [])
    top10_publishers = niche_data.get("top10_publishers", [])

    # dead_market: the 3 BEST-RANKED (lowest BSR) books in top-10 all > 300k means
    # NOBODY in the niche actually sells. Compare by BSR value, not by search position,
    # because Amazon ranks search by relevance — the strongest seller is often deeper.
    if top3 and len(top3) >= 3:
        best3 = sorted(top3)[:3]
        if all(b > 300_000 for b in best3):
            violations.append("dead_market")

    if (
        top10_reviews
        and len(top10_reviews) >= 10
        and all(r > 500 for r in top10_reviews[:10])
    ):
        violations.append("over_saturated")

    if (
        top10_prices
        and top10_pages
        and len(top10_prices) >= 10
        and len(top10_pages) >= 10
        and all(p <= 6.99 for p in top10_prices[:10])
        and all(pg <= 50 for pg in top10_pages[:10])
    ):
        violations.append("race_to_bottom")

    if top10_publishers and len(top10_publishers) >= 10:
        from collections import Counter
        # "Independently published" is Amazon's catch-all for indie / KDP self-pub —
        # it is NOT a single publisher, so exclude from the lock check.
        _INDIE_ALIASES = {"independently published", "?", "", "unknown"}
        filtered = [p for p in top10_publishers[:10] if str(p).strip().lower() not in _INDIE_ALIASES]
        if filtered:
            c = Counter(filtered)
            if max(c.values()) >= 6:
                violations.append("single_publisher_lock")

    if niche_data.get("is_seasonal") and niche_data.get("days_to_peak", 999) < 75:
        violations.append("seasonal_missed_window")

    if niche_data.get("has_trademark_risk"):
        violations.append("ip_trap")

    return violations


def niche_score(
    demand_0_10: float,
    competition_strength_0_10: float,
    margin_0_10: float,
    content_scale_0_10: float,
    longevity_0_10: float,
    opportunity_0_10: float,
) -> dict:
    """Weighted niche score including Opportunity factor.

    Weights sum to 1.0. Opportunity is heavily weighted because it is the
    single best predictor of new-book success.
    """
    # Competition is INVERTED in the score — high competition = low points
    competition_ease = 10 - competition_strength_0_10

    weights = {
        "demand":       0.20,
        "opportunity":  0.25,   # NEW — heaviest weight
        "competition":  0.15,
        "margin":       0.15,
        "content":      0.10,
        "longevity":    0.15,
    }
    overall = (
        weights["demand"] * demand_0_10
        + weights["opportunity"] * opportunity_0_10
        + weights["competition"] * competition_ease
        + weights["margin"] * margin_0_10
        + weights["content"] * content_scale_0_10
        + weights["longevity"] * longevity_0_10
    )
    overall = round(overall, 2)

    if overall >= 7.5:
        rating = "HOT"
    elif overall >= 6.0:
        rating = "WARM"
    elif overall >= 4.5:
        rating = "COLD"
    else:
        rating = "SKIP"

    return {"overall": overall, "rating": rating, "weights": weights}


# ────────────────────────────────────────────────────────
# KDP content limits
# ────────────────────────────────────────────────────────

LIMITS = {
    "title_plus_subtitle_chars": 200,
    "subtitle_chars": 150,
    "description_chars": 4000,
    "keyword_chars": 50,
    "keywords_count": 7,
    "category_count_initial": 2,
    "category_count_extra_request": 10,
    "min_line_weight_pt": 0.75,
    "min_dpi": 300,
    "max_pdf_mb": 650,
}


# ────────────────────────────────────────────────────────
# Seasonal ramp calendar (start N days before peak)
# ────────────────────────────────────────────────────────

SEASONS = [
    {"event": "valentines", "peak": "02-14", "ramp_days": 85},
    {"event": "mothers_day", "peak": "05-11", "ramp_days": 70},
    {"event": "fathers_day", "peak": "06-15", "ramp_days": 70},
    {"event": "back_to_school", "peak": "08-20", "ramp_days": 80},
    {"event": "halloween", "peak": "10-31", "ramp_days": 90},
    {"event": "christmas", "peak": "12-25", "ramp_days": 130},
    {"event": "new_year", "peak": "01-01", "ramp_days": 80},
]


if __name__ == "__main__":
    import json

    sample = {
        "cover_52_8.5x11": full_cover_dims("8.5x11", 52),
        "cover_100_8.5x8.5": full_cover_dims("8.5x8.5", 100),
        "royalty_8.99_52p": royalty_per_sale_usd(8.99, 52),
        "break_even_acos_8.99_52p": break_even_acos_pct(8.99, 52),
        "max_cpc_8.99_52p_40acos_8cvr": max_cpc_usd(8.99, 52, 40, 8),
        "bsr_28k_daily_sales": bsr_to_daily_sales(28_000),
        "bsr_28k_monthly_royalty_8.99_52p": estimate_monthly_royalty(28_000, 8.99, 52),
        "opportunity_300sales_180reviews": opportunity_score(300, 180),
        "opportunity_450sales_40reviews": opportunity_score(450, 40),
        "niche_score_sample_hot": niche_score(8, 4, 8, 9, 9, 7),
        "niche_score_sample_saturated": niche_score(9, 8, 6, 7, 8, 1),
    }
    print(json.dumps(sample, indent=2))
