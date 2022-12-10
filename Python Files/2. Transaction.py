import json
import base64
from algosdk import account, mnemonic, constants
from algosdk.v2client import algod
from algosdk.future import transaction

private_key = mnemonic.to_private_key("damp denial juice observe sentence kitchen erase window will cruise key tired "
                                      "sun bonus abstract lottery congress argue wolf kidney debris teach pipe "
                                      "ability entry")
account_address = "CHBY5G7VF57PHI3LWISDLQCJ3LKO3FAEUWDV75RQI7ZFEZLX2NIJY2WDTM"


algod_client = algod.AlgodClient(
    algod_token="",
    algod_address="https://testnet-algorand.api.purestake.io/ps2",
    headers={"X-API-Key": "ip4tG8gnmjIOcrlb06DI9kfk4LxpK3wa08eoVCb2"}
)

print(f"Account address: {account_address}")
account_info = algod_client.account_info(account_address)
print(f"Account balance: {account_info.get('amount')/1000000} Algos")


# building & signing a transaction
params = algod_client.suggested_params()
params.flat_fee = constants.MIN_TXN_FEE
params.fee = 1000
receiver = "4O6BRAPVLX5ID23AZWV33TICD35TI6JWOHXVLPGO4VRJATO6MZZQRKC7RI"
amount = 1420000
note = "my second Algorand transaction".encode()
unsigned_transaction = transaction.PaymentTxn(account_address, params, receiver, amount, None, note)
signed_transaction = unsigned_transaction.sign(private_key)

# submitting a transaction
transaction_id = algod_client.send_transaction(signed_transaction)
print(f"Signed transaction with transaction ID: {transaction_id}")

# wait for confirmation
try:
    confirmed_transaction = transaction.wait_for_confirmation(algod_client, transaction_id, 4)
except Exception as err:
    print(err)

print("Transaction information: {}".format(json.dumps(confirmed_transaction, indent=4)))
print("Decoded note: {}".format(base64.b64decode(confirmed_transaction["txn"]["txn"]["note"]).decode()))

print(f"transfer amount: {amount/1000000} Algos")
print(f"Fee: {params.fee/1000000} Algos")

account_info = algod_client.account_info(account_address)
print(f"Account balance after transaction: {account_info.get('amount')/1000000} Algos")
