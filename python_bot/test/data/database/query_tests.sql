SELECT nome_impianto,
    latitudine,
    longitudine,
    ROUND(
        2 * 6371 * ASIN(
            SQRT(
                POWER(
                    SIN((45.740115 - abs(latitudine)) * pi() / 180 / 2),
                    2
                ) + COS(45.740115 * pi() / 180) * COS(abs(latitudine) * pi() / 180) * POWER(
                    SIN((9.217506 - longitudine) * pi() / 180 / 2),
                    2
                )
            )
        )
    ,
    2) AS distance
FROM installations
ORDER BY distance
LIMIT 5