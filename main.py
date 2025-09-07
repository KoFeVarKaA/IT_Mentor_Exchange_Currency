from src.dao.dao_bd import DaoBD
from view.imitation_view import TestView


# DaoBD.delete_all_tables()
# DaoBD.create_tables()
responses = TestView.do_all_test()
for i in range(len(responses)):
    status_code = responses[i].status_code
    if responses[i].status_code != 200:
        print("ERROR: Плохой кодер, переделывай")
        break
    print(status_code)