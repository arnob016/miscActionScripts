
import argparse
import datetime
import requests
from stellar_sdk import Asset,Claimant, ClaimPredicate, Keypair, Network, Server, TransactionBuilder


def get_time():
    return datetime.datetime.now().strftime("%d%m%Y-%I:%M:%S%p")


def load_accounts(path):
    with open(path) as w:
        data = w.read()
    return data.split("\n")


def source_account(source_secret_key):
    source_keypair = Keypair.from_secret(source_secret_key)
    source_public_key = source_keypair.public_key
    source_account_getted = server.load_account(source_public_key)
    return (source_account_getted, source_keypair)


def send_token(transaction, source_keypair):

    transaction.sign(source_keypair)

    response = server.submit_transaction(transaction)
    return response


def newTrcBuil(source_account_getted, memo):
    base_fee = 100
    return TransactionBuilder(
        source_account=source_account_getted,
        network_passphrase=Network.PUBLIC_NETWORK_PASSPHRASE,
        base_fee=base_fee,
    ).add_text_memo(memo)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Stellar: Auto send pay to your defined list')
    parser.add_argument(
        '-ssk', type=str, help='Your source secret key.', required=True)
    parser.add_argument(
        '-rlist', type=str, help='Destination public key, file path.', required=True)
    parser.add_argument('-a', type=str, help='Amount to send', required=True)
    parser.add_argument('-m', type=str, help='Memo massage', required=True)
    asset = [
	    Asset("BULL", "GC7OPUQ7ZUGE6IUP66HVXCNYWIYJ7M522Z5X7KG23BRI7YZN2RCJKWXF"),
	]
    args = parser.parse_args()

    server = Server(horizon_url="https://horizon.stellar.org")
    sa = source_account(args.ssk)
    source_account_getted, source_keypair = sa
    account_list = load_accounts(args.rlist)

    p = newTrcBuil(source_account_getted, args.m)
    list_claimants = []
    count = 0
    for no, acc in enumerate(account_list):
        list_claimants.append(Claimant(
            destination=acc,
            predicate=ClaimPredicate.predicate_not(ClaimPredicate.predicate_before_relative_time(1209600))
        ))
        if (no+1) % 1 == 0:
            p.append_create_claimable_balance_op(asset[0], args.a, list_claimants, source=source_keypair.public_key)
            list_claimants = []
            count += 1
        if count==2:
            transaction = (
                p
                .set_timeout(30)
                .build()
            )
            send_return = send_token(transaction, source_keypair)
            p = newTrcBuil(source_account_getted, args.m)
            trxLink = send_return["_links"]['self']['href']
            print_log = f'{get_time()} {no+1:5d} {"Successful" if send_return["successful"] else "Unsuccessful"} {trxLink} {send_return["source_account"]} '
            print(print_log)
            destitaion_account = requests.get(
                send_return['_links']['operations']['href'][:-21], params={"limit": 200}).json()['_embedded']['records']
            print_log = print_log[:-1]+"\n"
            with open("history.txt", "a+") as w:
                w.write(print_log)
            list_claimants = []
            count = 0
            break
