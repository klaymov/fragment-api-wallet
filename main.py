from api import fragment, wallet

# wallet
WALLET_API_KEY = "" #try https://tonapi.io/
WALLET_MNEMONIC = []

# fragment
COOKIES = ""
HASH = ""


async def get_user(username: str) -> dict | None:
    try:
        user = await fragment.get_user_address(cookies=COOKIES, _hash=HASH, username=username)
        nickname = user.get("found").get("name")
        address = user.get("found").get("recipient")
        if nickname and address:
            return {"nickname": nickname, "address": address}
    except Exception as e:  # noqa: BLE001
        print(e)  # noqa: T201
        return None
    else:
        return None


async def pay_stars_order(username: str, quantity: int) -> str | None:
    try:
        # init address
        user = await fragment.get_user_address(cookies=COOKIES, _hash=HASH, username=username)
        nickname = user.get("found").get("name")
        address = user.get("found").get("recipient")
        if not nickname:
            return None

        # init buy
        init = await fragment.init_buy_stars(
            cookies=COOKIES, _hash=HASH, recipient=address, quantity=quantity
        )
        req_id = init["req_id"]

        # get pay
        buy = await fragment.get_buy_stars(cookies=COOKIES, _hash=HASH, req_id=req_id)
        address = buy.get("transaction", {}).get("messages", [{}])[0].get("address")
        amount = buy.get("transaction", {}).get("messages", [{}])[0].get("amount")
        payload = buy.get("transaction", {}).get("messages", [{}])[0].get("payload")

        payload = await fragment.encoded(encoded_string=payload)

        # pay
        tx_hash = await wallet.send_transfer(
            api_key=WALLET_API_KEY,
            mnemonic=WALLET_MNEMONIC,
            address=address,
            amount=amount,
            payload=payload,
        )

        if tx_hash:
            return tx_hash
    except Exception as e:  # noqa: BLE001
        print(e)  # noqa: T201
        return None
    else:
        return None
