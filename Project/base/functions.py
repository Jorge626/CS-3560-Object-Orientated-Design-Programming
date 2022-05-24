from django.db import connection


def setTierID(PK):
    cursor = connection.cursor()
    cursor.execute("""
    UPDATE
        base_bill
    SET
        tierID_id =CASE
                      WHEN (currentReading BETWEEN 0 AND 300) THEN 1
                      WHEN (currentReading BETWEEN 300 AND 750) THEN 2
                      ELSE 3
                      END
    WHERE
        accountID_id = %s AND billID = (SELECT MAX(billID) FROM base_bill) """, [PK, ])
    print(cursor.fetchone())


def setLateFee(PK):
    cursor = connection.cursor()
    cursor.execute("""
    SELECT paidInFull 
    FROM    (SELECT billID, paidInFull
            FROM base_bill 
            WHERE
                    accountID_id = %s
            ORDER BY billID
            DESC
            LIMIT 2)
    ORDER BY billID
    ASC
    LIMIT 1
    """, [PK, ])

    paidInFullCheck = (str(cursor.fetchone()[0]))

    if (paidInFullCheck == "False"):
        cursor.execute("""
        SELECT readingDate 
        FROM    (SELECT billID, readingDate
                FROM base_bill 
                WHERE
                        accountID_id = %s
                ORDER BY billID
                DESC
                LIMIT 2)
        ORDER BY billID
        ASC
        LIMIT 1""", [PK, ])

        pastReadingDate = (str(cursor.fetchone()[0]))

# --------------------------------------------------------------------------------------------------------
        cursor = connection.cursor()
        cursor.execute("""
        UPDATE
            base_bill
        SET
            latefee = CASE
                      WHEN (julianday("now") - julianday(%s) - 1) < 30 THEN 0
                      WHEN (julianday("now") - julianday(%s) - 1) between 30 AND 45 THEN 25
                      WHEN (julianday("now") - julianday(%s) - 1) between 45 AND 60 THEN 50
                      ELSE 75
                      END
        WHERE
            accountID_id = %s AND billID = (SELECT MAX(billID) FROM base_bill) """, [pastReadingDate, pastReadingDate, pastReadingDate, PK, ])

    else:
        cursor.execute("""
        UPDATE
            base_bill
        SET
            latefee = CASE
                      WHEN (julianday("now") - julianday(readingDate) - 1) < 30 THEN 0
                      WHEN (julianday("now") - julianday(readingDate) - 1) between 30 AND 45 THEN 25
                      WHEN (julianday("now") - julianday(readingDate) - 1) between 45 AND 60 THEN 50
                      ELSE 75
                      END
        WHERE
            accountID_id = %s AND billID = (SELECT MAX(billID) FROM base_bill) """, [PK, ])


def setAmountDue(PK):

    lastpaymentdue = 0

    cursor = connection.cursor()
    cursor.execute("""
    SELECT paidInFull 
    FROM    (SELECT billID, paidInFull
            FROM base_bill 
            WHERE
                    accountID_id = %s
            ORDER BY billID
            DESC
            LIMIT 2)
    ORDER BY billID
    ASC
    LIMIT 1
    """, [PK, ])

    paidInFullCheck = (str(cursor.fetchone()[0]))

    if (paidInFullCheck == "False"):
        cursor.execute("""
        SELECT amountDue 
        FROM    (SELECT billID, AmountDue
                FROM base_bill 
                WHERE
                        accountID_id = %s
                ORDER BY billID
                DESC
                LIMIT 2)
        ORDER BY billID
        ASC
        LIMIT 1
        """, [PK, ])

        lastpaymentdue = cursor.fetchone()[0]

    cursor.execute("""
    UPDATE
        base_bill
    SET
        amountDue = round((((SELECT price 
                        FROM base_rate
                        WHERE tierID = (SELECT tierID_id   
                        FROM base_bill 
                        WHERE accountID_id = %s AND billID = 
                        (SELECT MAX(billID) FROM base_bill))) * currentReading) + %s + lateFee),2)
    WHERE
            accountID_id = %s AND billID = (SELECT MAX(billID) FROM base_bill) """, [PK, lastpaymentdue, PK, ])


def updateBills(PK):

    setTierID(PK)
    setLateFee(PK)
    setAmountDue(PK)
