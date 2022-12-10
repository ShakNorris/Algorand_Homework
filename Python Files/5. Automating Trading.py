import base64
from algosdk import mnemonic, encoding, constants
from algosdk.v2client import algod
from algosdk.future import transaction
from algosdk.future.transaction import LogicSigTransaction, PaymentTxn, AssetTransferTxn, wait_for_confirmation

m = "asset hazard volume easily convince attract picture cash ask goddess dilemma push glue seven favorite cause " \
     "rather holiday devote idea divert basic jacket abandon nuclear"
account = "Y5VVMVHLZFC6HWD3XAVEM4VA3AOSDO6G5LNZEQARAQKVWYBYUKKAKNGLBY"
private_key = mnemonic.to_private_key(m)
receiver = "4O6BRAPVLX5ID23AZWV33TICD35TI6JWOHXVLPGO4VRJATO6MZZQRKC7RI"
buildweb_id = 14035004

algod_client = algod.AlgodClient(
    algod_token="",
    algod_address="https://testnet-algorand.api.purestake.io/ps2",
    headers={"X-API-Key": "ip4tG8gnmjIOcrlb06DI9kfk4LxpK3wa08eoVCb2"}
)

# OPT IN
params = algod_client.suggested_params()
account_info = algod_client.account_info(account)
holding = None
index = 0
for my_account_info in account_info['assets']:
    scrutinized_asset = account_info['assets'][index]
    index = index + 1
    if scrutinized_asset['asset-id'] == buildweb_id:
        holding = True
        break
if not holding:
    # Use the AssetTransferTxn class to transfer assets and opt-in
    transaction = AssetTransferTxn(sender=account, sp=params, receiver=account, amt=0, index=buildweb_id)
    Tr_signature = transaction.sign(private_key)
    # Send the transaction to the network and retrieve the txid.
    try:
        transaction_ID = algod_client.send_transaction(Tr_signature)
        print("Signed transaction with ID: {}".format(transaction_ID))
        # Wait for the transaction to be confirmed
        confirmed_transaction = wait_for_confirmation(algod_client, transaction_ID, 4)
        print("Transaction ID: ", transaction_ID)
        print("Result confirmed in round: {}".format(confirmed_transaction['confirmed-round']))
    except Exception as err:
        print(err)


#Atomic Transaction
params = algod_client.suggested_params()
params.flat_fee = constants.MIN_TXN_FEE
params.fee = 1000
amount = 4200000

txn_1 = transaction.PaymentTxn(account, params, receiver, amount)

asset_params = algod_client.suggested_params()

txn_2 = AssetTransferTxn(receiver, asset_params, account, 1, buildweb_id)

gid = transaction.calculate_group_id([txn_1, txn_2])
txn_1.group = gid
txn_2.group = gid

stxn1 = txn_1.sign(private_key)
with open("step5.lsig", "rb") as f:
    lsig = encoding.future_msgpack_decode(base64.b64encode(f.read()))
stxn2 = LogicSigTransaction(txn_2, lsig)

signed_group = [stxn1, stxn2]

txid = algod_client.send_transactions(signed_group)

# Print the transaction ID of the first transaction of the group
print("Send transaction with txID: {}".format(txid))




