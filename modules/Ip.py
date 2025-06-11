from telethon import events
import aiohttp
import logging

logging.basicConfig(
    format="%(message)s",
    datefmt="%H:%M:%S %d-%m-%Y",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def register(client):
    @client.on(events.NewMessage(pattern=r"-ip\s+([\d\.]+)"))
    async def ip_lookup(event):
        if not await is_owner(event):
            return
        ip_address = event.pattern_match.group(1).strip()
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"http://ip-api.com/json/{ip_address}?fields=66846719") as response:
                    if response.status != 200:
                        await event.message.edit(f"Error: Unable to fetch data for IP {ip_address}", parse_mode='markdown')
                        return
                    data = await response.json()
                    if data.get("status") == "fail":
                        await event.message.edit(f"Error: Invalid IP address {ip_address}", parse_mode='markdown')
                        return
                    info = (
                        f"IP Lookup for {ip_address}\n\n"
                        f"Country: {data.get('country', 'N/A')}\n"
                        f"Region: {data.get('regionName', 'N/A')}\n"
                        f"City: {data.get('city', 'N/A')}\n"
                        f"ZIP: {data.get('zip', 'N/A')}\n"
                        f"Latitude: {data.get('lat', 'N/A')}\n"
                        f"Longitude: {data.get('lon', 'N/A')}\n"
                        f"Timezone: {data.get('timezone', 'N/A')}\n"
                        f"ISP: {data.get('isp', 'N/A')}\n"
                        f"Organization: {data.get('org', 'N/A')}\n"
                        f"AS: {data.get('as', 'N/A')}\n"
                        f"Mobile: {data.get('mobile', 'N/A')}\n"
                        f"Proxy: {data.get('proxy', 'N/A')}\n"
                        f"Hosting: {data.get('hosting', 'N/A')}"
                    )
                    await event.message.edit(info, parse_mode='markdown')
            logger.info(f"IP lookup for {ip_address} by {event.sender_id}")
        except Exception as e:
            await event.message.edit(f"Error: {e}", parse_mode='markdown')
            logger.error(f"Error in IP lookup for {ip_address}: {e}")

async def is_owner(event):
    sender = await event.get_sender()
    return sender.id == 1540613583
