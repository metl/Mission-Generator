# Each entry: (min_total, max_total, payout)
payout_table = {
    (6, 9): 25000,
    (10, 10): 50000,
    (11, 11): 75000,
    (12, 12): 100000,
    (13, 13): 125000,
    (14, 14): 150000,
    (15, 15): 175000,
    (16, 17): 200000,
    (18, 19): 225000,
    (20, 999): 250000,  # 20+
}
def get_payout(total):
    for (low, high), amount in payout_table.items():
        if low <= total <= high:
            return amount
    return 0