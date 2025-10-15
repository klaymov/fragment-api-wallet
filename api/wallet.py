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
    api_key: str, mnemonic: list, address: str, amount: int, payload: str
) -> str:
    client = TonapiClient(api_key=api_key, is_testnet=False)
    wallet, _public_key, _private_key, mnemonic = WalletV5R1.from_mnemonic(client, mnemonic)

    return await wallet.transfer(
        destination=address,
        amount=to_amount(amount, 9, 9),
        body=payload,
    )


async def get_balance(api_key: str, mnemonic: list) -> int:
    client = TonapiClient(api_key=api_key, is_testnet=False)
    wallet, _public_key, _private_key, mnemonic = WalletV5R1.from_mnemonic(client, mnemonic)

    balance = await wallet.balance()
    return to_amount(balance)
