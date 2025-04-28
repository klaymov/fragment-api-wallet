from api import fragment, wallet

# wallet
WALLET_API_KEY = ''
WALLET_MNEMONIC = []

# fragment
COOKIES = ''
HASH = ''


async def get_user(username: str) -> dict | None:
    try:
        user = await fragment.get_user_address(COOKIES, HASH, username)
        nickname = user.get("found").get("name")
        address = user.get("found").get("recipient")
        if not nickname:
            return None
        return {
            "nickname": nickname,
            "address": address
        }
    except Exception as ex:
        print(ex)
        return None


async def pay_stars_order(
    username: str,
    quantity: int
    ) -> str | None:   
    try:
        # init address
        user = await fragment.get_user_address(COOKIES, HASH, username)
        nickname = user.get("found").get("name")
        address = user.get("found").get("recipient")
        if not nickname:
            return None
        
        # init buy
        init = await fragment.init_buy_stars(COOKIES, HASH, address, quantity)
        req_id = init['req_id']
        
        # get pay
        buy = await fragment.get_buy_stars(COOKIES, HASH, req_id)
        address = buy.get('transaction', {}).get('messages', [{}])[0].get('address')
        amount = buy.get('transaction', {}).get('messages', [{}])[0].get('amount')
        payload = buy.get('transaction', {}).get('messages', [{}])[0].get('payload')
        
        payload = await fragment.encoded(payload)
        
        # pay
        tx_hash = await wallet.send_transfer(WALLET_API_KEY, WALLET_MNEMONIC, address, amount, payload)

        if tx_hash:
            return tx_hash
        return None
    except Exception as ex:
        print(ex)
        return None
