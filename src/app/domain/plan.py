FREE = "free"
PREMIUM = "premium"

PLAN_LIMITS = {
    FREE: {
        "quotes_per_day": 5
    },
    PREMIUM: {
        "quotes_per_day": float("inf")
    }
}
