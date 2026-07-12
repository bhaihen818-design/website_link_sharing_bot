import time
from database.database import database

settings_col = database['settings']
links_col = database['links']

# Create indexes
async def create_indexes():
    await links_col.create_index("token", unique=True)
    await links_col.create_index("slug", unique=True)

# Website Settings
async def set_website_url(url: str):
    await settings_col.update_one(
        {"_id": "website_url"},
        {"$set": {"url": url}},
        upsert=True
    )

async def get_website_url():
    data = await settings_col.find_one({"_id": "website_url"})
    return data['url'] if data else None

# Link Management
async def add_link(token: str, slug: str, url: str, user_id: int):
    await links_col.insert_one({
        "token": token,
        "slug": slug,
        "url": url,
        "created_by": user_id,
        "created_at": time.time()
    })

async def get_link_by_token(token: str):
    return await links_col.find_one({"token": token})

async def get_link_by_slug(slug: str):
    return await links_col.find_one({"slug": slug})
