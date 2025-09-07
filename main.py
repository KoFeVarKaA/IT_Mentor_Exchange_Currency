from src.dao.dao_currencies import DaoCurrencies
from src.dao.dao_rates import DaoRates

DaoRates.create_table()
DaoCurrencies.create_table()
print("succses")