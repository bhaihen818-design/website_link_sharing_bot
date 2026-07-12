# Project Conversion Plan: File Sharing Bot to Website Link Sharing Bot

## Goal
Convert the Telegram File Sharing Bot into a Website Link Sharing Bot by removing all file-sharing functionality and implementing a clean, fast, production-ready link generation system backed by MongoDB.

## Phase 2: Plan and document all changes required

This document outlines the planned modifications, removals, and additions to the codebase to achieve the conversion goal. The plan focuses on adhering to the requirements of removing file-sharing, implementing website link sharing, and optimizing performance.

### 1. Files to Remove

The following files and their associated functionalities will be completely removed as they are directly related to the old file-sharing system and are no longer required:

*   `plugins/channel_post.py`: This module handles the ingestion of messages into the database channel and the generation of file-specific share links. Its removal is critical for eliminating file-sharing capabilities.
*   `plugins/link_generator.py`: Contains the `/batch` and `/genlink` commands, which are designed for generating links to shared files. These commands will be replaced with new logic for website link generation.
*   `helper_func.py`: This utility file contains several functions (`get_messages`, `get_message_id`, `encode`, `decode`) that are tightly coupled with the file-sharing mechanism and database channel interaction. It will be removed, and any generic helper functions needed will be re-implemented or moved to a new utility module.

### 2. Files to Modify

The following files will undergo significant modifications to adapt to the new bot functionality:

*   `bot.py`:
    *   **Remove:** Logic related to `FORCESUB_CHANNEL`, `FORCESUB_CHANNEL2`, `FORCESUB_CHANNEL3`, and `CHANNEL_ID` will be removed. The `db_channel` initialization will also be removed.
    *   **Review:** The import of `web_server` from `plugins` will be reviewed; if its sole purpose is for file-sharing related web endpoints, it will be removed.
*   `config.py`:
    *   **Remove:** Environment variables and default values for `CHANNEL_ID`, `FORCESUB_CHANNEL`, `FORCESUB_CHANNEL2`, `FORCESUB_CHANNEL3`, `SHORTLINK_URL`, `SHORTLINK_API`, `VERIFY_EXPIRE`, `IS_VERIFY`, `TUT_VID`, `CUSTOM_CAPTION`, `PROTECT_CONTENT`, and `DISABLE_CHANNEL_BUTTON` will be removed.
    *   **Update:** `START_MSG` and `FORCE_MSG` will be updated to reflect the bot's new purpose as a website link sharer.
*   `database/database.py`:
    *   **Remove:** `default_verify`, `new_user`'s `verify_status` field, `db_verify_status`, and `db_update_verify_status` will be removed.
    *   **Add:** New MongoDB collections will be introduced: `settings` (for storing the base website URL) and `links` (for storing generated tokens, slugs, and URLs). Corresponding asynchronous functions for interacting with these collections (e.g., `get_website_url`, `set_website_url`, `add_link`, `get_link`, `delete_link`) will be implemented using `motor.motor_asyncio`.
    *   **Indexes:** Unique indexes will be created for `token` and `slug` fields in the `links` collection.
*   `plugins/start.py`:
    *   **Remove:** The entire `if 
```python
        elif len(message.text) > 7 and verify_status['is_verified']:
```
block, which handles file link resolution and message copying, will be removed. The ad-token verification logic will also be removed.
    *   **Add:** New logic will be implemented to handle the `/start` command with a `TOKEN`. This will involve querying the `links` collection in MongoDB, constructing the website URL, and sending a message with an inline button to open the website.
    *   **Modify:** The `/users` and `/broadcast` commands will be retained, but their implementation will be reviewed for any dependencies on removed file-sharing components.

### 3. New Files to Create

*   `database/link_db.py`: A new module to encapsulate all MongoDB operations related to the `settings` and `links` collections. This will include functions for setting/getting the base website URL, and for creating, retrieving, and deleting link entries.
*   `plugins/website_settings.py`: This module will contain the new `/setweb` and `/getweb` commands for managing the base website URL.
*   `plugins/new_link_generator.py`: This module will contain the updated `/genlink` command, which will generate a unique token and slug, store it in MongoDB, and return a Telegram start link.

### 4. General Considerations

*   **Performance:** All database interactions will use `motor.motor_asyncio` to ensure asynchronous operations. Unnecessary imports and handlers will be removed to keep the bot lightweight.
*   **Code Quality:** The code will be modular, well-commented, and adhere to best practices. Unused files and imports will be removed.
*   **Compatibility:** The existing project structure, bot startup, configuration system, logging, and admin system will be preserved as much as possible.
*   **Security:** The generated tokens will be random and unique. The website URL will be stored securely in MongoDB and never hardcoded.

This plan provides a clear roadmap for the conversion, ensuring all requirements are met while maintaining code quality and performance. The next phase will involve executing these changes systematically.
