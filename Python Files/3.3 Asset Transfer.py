import json
from algosdk.v2client import algod
from algosdk import account, mnemonic
from algosdk.future.transaction import AssetConfigTxn, AssetTransferTxn, AssetFreezeTxn, wait_for_confirmation
from varFunctions import print_asset_holding

private_key = mnemonic.to_private_key("asset hazard volume easily convince attract picture cash ask goddess dilemma "
                                      "push glue seven favorite cause rather holiday devote idea divert basic jacket "
                                      "abandon nuclear")

sender = "Y5VVMVHLZFC6HWD3XAVEM4VA3AOSDO6G5LNZEQARAQKVWYBYUKKAKNGLBY"
receiver = "CHBY5G7VF57PHI3LWISDLQCJ3LKO3FAEUWDV75RQI7ZFEZLX2NIJY2WDTM"
asset_id = 123838398

algod_client = algod.AlgodClient(
    algod_token="",
    algod_address="https://testnet-algorand.api.purestake.io/ps2",
    headers={"X-API-Key": "ip4tG8gnmjIOcrlb06DI9kfk4LxpK3wa08eoVCb2"}
)

params = algod_client.suggested_params()

txn = AssetTransferTxn(
    sender=sender,
    sp=params,
    receiver=receiver,
    amt=1,
    index=asset_id)
stxn = txn.sign(private_key)
# Send the transaction to the network and retrieve the txid.
try:
    txid = algod_client.send_transaction(stxn)
    print("Signed transaction with txID: {}".format(txid))
    # Wait for the transaction to be confirmed
    confirmed_txn = wait_for_confirmation(algod_client, txid, 4)
    print("TXID: ", txid)
    print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))
except Exception as err:
    print(err)
# The balance should now be 10.
print_asset_holding(algod_client, receiver, asset_id)
