import base64
import aiohttp
from aiohttp import ClientResponse


async def encoded(encoded_string: str) -> str:
    """Decode."""
    missing_padding = len(encoded_string) % 4
    if missing_padding != 0:
        encoded_string += "=" * (4 - missing_padding)

    try:
        decoded_bytes = base64.b64decode(encoded_string)
        decoded_string = decoded_bytes.decode("utf-8", errors="ignore")

        for i, char in enumerate(decoded_string):
            if char.isdigit():
                cleaned_string = decoded_string[i:]
                break
        else:
            cleaned_string = decoded_string
    except Exception:  # noqa: BLE001
        return encoded_string
    else:
        return cleaned_string


async def post(cookies: str, _hash: str, data: dict) -> ClientResponse:
    params = {"hash": _hash}

    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7,ru-RU;q=0.6,ru;q=0.5",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "origin": "https://fragment.com",
        "priority": "u=1, i",
        "referer": "https://fragment.com/stars/buy?recipient=test&quantity=50",
        "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "cookie": cookies,
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",  # noqa: E501
        "x-requested-with": "XMLHttpRequest",
    }
    async with (
        aiohttp.ClientSession() as session,
        session.post(
            "https://fragment.com/api", params=params, headers=headers, data=data
        ) as response,
    ):
        return response


async def get_user_address(cookies: str, _hash: str, username: str) -> dict:
    data = {
        "query": username,
        "quantity": "",
        "method": "searchStarsRecipient",
    }
    response: ClientResponse = await post(cookies, _hash, data)
    return await response.json()


async def init_buy_stars(cookies: str, _hash: str, recipient: str, quantity: int) -> dict:
    data = {
        "recipient": recipient,
        "quantity": quantity,
        "method": "initBuyStarsRequest",
    }
    response: ClientResponse = await post(cookies, _hash, data)
    return await response.json()


async def get_buy_stars(cookies: str, _hash: str, req_id: str) -> dict:
    data = {
        "transaction": "1",
        "id": req_id,
        "show_sender": "0",
        "method": "getBuyStarsLink",
    }
    response: ClientResponse = await post(cookies, _hash, data)
    return await response.json()
