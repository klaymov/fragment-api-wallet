from tonutils.client import TonapiClient
from tonutils.utils import to_amount
from tonutils.wallet import (
    # Uncomment the following lines to use different wallet versions:
    # WalletV3R1,
    # WalletV3R2,
    # WalletV4R1,
    # WalletV4R2,
    WalletV5R1,
    # HighloadWalletV2,
    # HighloadWalletV3,
)


async def send_transfer(
    API_KEY: str,
    MNEMONIC: list,
    address: str,
    amount: int,
    payload: str
    ) -> str:
    client = TonapiClient(api_key=API_KEY, is_testnet=False)
    wallet, public_key, private_key, mnemonic = WalletV5R1.from_mnemonic(client, MNEMONIC)
    
    tx_hash = await wallet.transfer(
        destination=address,
        amount=to_amount(amount, 9, 9),
        body=payload,
    )

    return tx_hash


async def get_balance(
    API_KEY: str,
    MNEMONIC: list
    ) -> int:
    client = TonapiClient(api_key=API_KEY, is_testnet=False)
    wallet, public_key, private_key, mnemonic = WalletV5R1.from_mnemonic(client, MNEMONIC)
    
    balance = await wallet.balance()
    return to_amount(balance)