# Vertigo Games – Clan Management API (Task 1)

---

## Purpose

This RESTful API manages player clans. It is built with **FastAPI**, uses an async PostgreSQL connection (Cloud SQL).
The API allows you to:
- Create new clans
- Get details of a single clan by ID
- List all clans (with optional region filter and creation date sorting)
- Delete clans

---

## Database Structure

- **Schema:** `api`
- **Table:** `clans`

| Column      | Type                     | Notes                               |
|-------------|--------------------------|-------------------------------------|
| `id`        | UUID (PK)                | Auto-generated unique clan ID       |
| `name`      | TEXT                     | Required clan name                  |
| `region`    | VARCHAR(4)               | Region code (e.g. “TR”, “US”)       |
| `created_at`| TIMESTAMP WITH TIMEZONE | Auto-generated creation timestamp   |

---

## Endpoints

All endpoints accept and return JSON.

---

* ### POST `/clans`

**Description:** Create a new clan.

**Request Body:**
```json
{
  "name": "Shadow Clan",
  "region": "EU"
}
```
**Response:**
```json
{
  "id": "generated-uuid",
  "message": "Clan created successfully."
}
```

* ### GET `/clans/{clan_id}`

**Description:** Get details for a single clan by its unique ID.

**Example Response:**
```json
{
  "id": "generated-uuid",
  "name": "Shadow Clan",
  "region": "EU",
  "created_at": "2025-06-29T19:48:58.339954+00:00"
}

```

* ### GET `/clans`

**Description:** List all clans. Supports optional region filtering and creation date sorting.

**Query Parameters:**

`region` (string): Filter clans by region (e.g., 'EU') \
`sort_by_date` (boolean): If true, sorts clans by created_at descending order

**Example Response:**
```json
[
  {
    "id": "uuid-1",
    "name": "Shadow Clan",
    "region": "EU",
    "created_at": "2025-06-29T19:48:58.339954+00:00"
  },
  {
    "id": "uuid-2",
    "name": "Sunrise Clan",
    "region": "EU",
    "created_at": "2025-06-28T17:22:11.431123+00:00"
  }
]

```

* ### GET `/clans/{clan_id}`

**Description:** Delete a clan by its unique ID.

**Response:**
```json
{
  "id": "deleted-uuid",
  "message": "Clan deleted successfully."
}
```