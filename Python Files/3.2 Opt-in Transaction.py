from algosdk.v2client import algod
from algosdk import account, mnemonic
from algosdk.future.transaction import AssetConfigTxn, AssetTransferTxn, AssetFreezeTxn, wait_for_confirmation
from varFunctions import print_asset_holding

m = "damp denial juice observe sentence kitchen erase window will cruise key tired sun bonus abstract lottery congress argue wolf kidney debris teach pipe ability entry"
private_key = mnemonic.to_private_key(m)
account_Public = account.address_from_private_key(private_key)

algod_client = algod.AlgodClient(
    algod_token="",
    algod_address="https://testnet-algorand.api.purestake.io/ps2",
    headers={"X-API-Key": "ip4tG8gnmjIOcrlb06DI9kfk4LxpK3wa08eoVCb2"}
)

asset_id = 123838398

# OPT-IN
# Check if asset_id is in account 3's asset holdings prior
# to opt-in
params = algod_client.suggested_params()
account_info = algod_client.account_info(account_Public)
holding = None
idx = 0
for my_account_info in account_info['assets']:
    scrutinized_asset = account_info['assets'][idx]
    idx = idx + 1
    if scrutinized_asset['asset-id'] == asset_id:
        holding = True
        break
if not holding:
    # Use the AssetTransferTxn class to transfer assets and opt-in
    txn = AssetTransferTxn(
        sender=account_Public,
        sp=params,
        receiver=account_Public,
        amt=0,
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
    # Now check the asset holding for that account.
    # This should now show a holding with a balance of 0.
    print_asset_holding(algod_client,account_Public, asset_id)
