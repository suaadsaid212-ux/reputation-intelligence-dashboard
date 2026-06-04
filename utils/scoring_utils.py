def calculate_rii(
    exposure,
    vulnerability,
    resilience
):

    rii = (
        exposure +
        vulnerability -
        resilience
    )

    return round(rii, 2)
