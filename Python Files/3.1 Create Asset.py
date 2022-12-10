import json
from algosdk.v2client import algod
from algosdk import account, mnemonic
from algosdk.future.transaction import AssetConfigTxn, AssetTransferTxn, AssetFreezeTxn, wait_for_confirmation
from varFunctions import print_asset_holding, print_created_asset

m = "asset hazard volume easily convince attract picture cash ask goddess dilemma push glue seven favorite cause rather holiday devote idea divert basic jacket abandon nuclear"
account_PK = mnemonic.to_private_key(m)
account_Public = account.address_from_private_key(account_PK)

algod_client = algod.AlgodClient(
    algod_token="",
    algod_address="https://testnet-algorand.api.purestake.io/ps2",
    headers={"X-API-Key": "ip4tG8gnmjIOcrlb06DI9kfk4LxpK3wa08eoVCb2"}
)

# CREATE ASSET
params = algod_client.suggested_params()
txn = AssetConfigTxn(
    sender=account_Public,
    sp=params,
    total=1000,
    default_frozen=False,
    unit_name="ABSTRACT",
    asset_name="abstract",
    manager=account_Public,
    reserve=account_Public,
    freeze=account_Public,
    clawback=account_Public,
    url="https://path/to/my/asset/details",
    decimals=0)

stxn = txn.sign(account_PK)

try:
    txid = algod_client.send_transaction(stxn)
    print("Signed transaction with txID: {}".format(txid))
    # Wait for the transaction to be confirmed
    confirmed_txn = wait_for_confirmation(algod_client, txid, 4)
    print("TXID: ", txid)
    print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))
except Exception as err:
    print(err)

print("Transaction information: {}".format(
    json.dumps(confirmed_txn, indent=4)))

try:
    ptx = algod_client.pending_transaction_info(txid)
    asset_id = ptx["asset-index"]
    print_created_asset(algod_client, account_Public, asset_id)
    print_asset_holding(algod_client, account_Public, asset_id)
except Exception as e:
    print(e)
