# Расчет для накладной клиента с НДС
def calc_nds(price, value, nds, psb=None):
    no_nds_price = round(float(price) - (float(price) * float(nds)) / (100 + float(nds)), 2)
    sum_all = round(int(value) * float(price), 2)
    sum_no_nds = round(float(sum_all) - (float(sum_all) * float(nds)) / (100 + float(nds)), 2)
    sum_nds = sum_all - sum_no_nds

    if psb:
        mest_all = int(value) / int(psb)
    else:
        mest_all = 0

    return no_nds_price, sum_no_nds, sum_nds, sum_all, mest_all


# Расчет для накладной клиента без НДС
def calc_no_nds(price, value, nds, psb=None):
    no_nds_price = round(float(price), 2)
    sum_no_nds = no_nds_price * int(value)
    sum_all = round(sum_no_nds * (1 + nds / 100), 2)
    sum_nds = sum_all - sum_no_nds

    if psb:
        mest_all = int(value) / int(psb)
    else:
        mest_all = 0

    return no_nds_price, sum_no_nds, sum_nds, sum_all, mest_all
