import sentry_sdk
sentry_sdk.init(
    "https://95b3e680d8184766b415f8b11088c037@o560368.ingest.sentry.io/5695874",

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0
)


division_by_zero = 1 / 0