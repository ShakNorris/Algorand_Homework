from algosdk import constants
from algosdk.future import transaction
from algosdk.v2client import algod
from algosdk import mnemonic
from algosdk.future.transaction import AssetTransferTxn, wait_for_confirmation


mA = "asset hazard volume easily convince attract picture cash ask goddess dilemma push glue seven favorite cause " \
     "rather holiday devote idea divert basic jacket abandon nuclear "
mB = "damp denial juice observe sentence kitchen erase window will cruise key tired sun bonus abstract lottery " \
     "congress argue wolf kidney debris teach pipe ability entry "
private_keyA = mnemonic.to_private_key(mA)
private_keyB = mnemonic.to_private_key(mB)
account_A = "Y5VVMVHLZFC6HWD3XAVEM4VA3AOSDO6G5LNZEQARAQKVWYBYUKKAKNGLBY"
account_B = "CHBY5G7VF57PHI3LWISDLQCJ3LKO3FAEUWDV75RQI7ZFEZLX2NIJY2WDTM"


asset_id = 123838398

algod_client = algod.AlgodClient(
    algod_token="",
    algod_address="https://testnet-algorand.api.purestake.io/ps2",
    headers={"X-API-Key": "ip4tG8gnmjIOcrlb06DI9kfk4LxpK3wa08eoVCb2"}
)

# building a transaction from B to A
params_A = algod_client.suggested_params()
params_A.flat_fee = constants.MIN_TXN_FEE
params_A.fee = 1000
amount = 1200000

txn_1 = transaction.PaymentTxn(account_B, params_A, account_A, amount)

params_B = algod_client.suggested_params()
txn_2 = AssetTransferTxn(account_A, params_B, account_B, 1, asset_id)

gid = transaction.calculate_group_id([txn_1, txn_2])
txn_1.group = gid
txn_2.group = gid

stxn_1 = txn_1.sign(private_keyB)
stxn_2 = txn_2.sign(private_keyA)

signed_group = [stxn_1, stxn_2]

tx_id = algod_client.send_transactions(signed_group)

# wait for confirmation
confirmed_txn = wait_for_confirmation(algod_client, tx_id, 4)
print("txID: {}".format(tx_id), " confirmed in round: {}".format(
    confirmed_txn.get("confirmed-round", 0)))
