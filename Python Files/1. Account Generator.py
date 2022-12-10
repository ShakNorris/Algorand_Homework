import algosdk

# Generate a fresh private key and associated account address
private_key, account_address = algosdk.account.generate_account()

# Convert the private key into a mnemonic which is easier to use
mnemonic = algosdk.mnemonic.from_private_key(private_key)

print("Private key mnemonic: " + mnemonic)
print("Account address: " + account_address)


# Private key mnemonic: asset hazard volume easily convince attract picture cash ask goddess dilemma push glue seven favorite cause rather holiday devote idea divert basic jacket abandon nuclear
# Account address: Y5VVMVHLZFC6HWD3XAVEM4VA3AOSDO6G5LNZEQARAQKVWYBYUKKAKNGLBY
#
# Private key mnemonic: damp denial juice observe sentence kitchen erase window will cruise key tired sun bonus abstract lottery congress argue wolf kidney debris teach pipe ability entry
# Account address: CHBY5G7VF57PHI3LWISDLQCJ3LKO3FAEUWDV75RQI7ZFEZLX2NIJY2WDTM
