# Episode 101294736 Replay Fetch

Status: FAILED TO RETRIEVE RAW REPLAY

No X1.11 strategy files were modified.

## Requested Episode

- Episode ID: `101294736`
- Primary API requested: `kaggle_environments.get_episode_replay(101294736)`
- Direct endpoint requested: `https://www.kaggle.com/requests/EpisodeService/GetEpisodeReplay`
- Fallback endpoint probed: `https://www.kaggle.com/requests/EpisodeService/ListEpisodes`

## Local Sandbox Attempt

Initial non-escalated network access failed before reaching Kaggle:

- Exception: `ConnectionError`
- Exact network error: `HTTPSConnectionPool(host='www.kaggle.com', port=443): Max retries exceeded with url: /requests/EpisodeService/GetEpisodeReplay (Caused by NewConnectionError("HTTPSConnection(host='www.kaggle.com', port=443): Failed to establish a new connection: [WinError 10013] An attempt was made to access a socket in a way forbidden by its access permissions"))`

Metadata saved:

- `episode_101294736_fetch_meta.json`

## Official Function Attempt

Command path:

- `kaggle_environments.get_episode_replay(101294736)`

Result:

- HTTP body received by the library was empty.
- The library called `response.json()` and raised:
  - `requests.exceptions.JSONDecodeError: Expecting value: line 1 column 1 (char 0)`

Metadata saved:

- `episode_101294736_get_episode_replay_meta.json`

## Direct Endpoint Attempts

All direct unauthenticated `POST` attempts reached Kaggle but returned:

- HTTP status: `400`
- Reason: `Bad Request`
- Body length: `0`
- JSON parse error: `JSONDecodeError('Expecting value: line 1 column 1 (char 0)')`

Payload variants tried:

- JSON: `{"EpisodeId": 101294736}`
- JSON: `{"episodeId": 101294736}`
- JSON: `{"id": 101294736}`
- Form: `EpisodeId=101294736`

Raw bodies saved:

- `episode_101294736_raw_response.json` length `0`
- `episode_101294736_raw_EpisodeId_json.txt` length `0`
- `episode_101294736_raw_episodeId_json.txt` length `0`
- `episode_101294736_raw_id_json.txt` length `0`
- `episode_101294736_raw_EpisodeId_form.txt` length `0`

Metadata saved:

- `episode_101294736_endpoint_variants_meta.json`
- `episode_101294736_service_probe_meta.json`

## Session/XSRF Attempt

A GET to `https://www.kaggle.com/` succeeded and produced anonymous cookies including:

- `ka_sessionid`
- `CSRF-TOKEN`
- `XSRF-TOKEN`
- `CLIENT-TOKEN`

The subsequent POST to `GetEpisodeReplay` with `X-XSRF-TOKEN`, `Referer`, browser-like `User-Agent`, `Accept: application/json`, and `Content-Type: application/json` returned:

- HTTP status: `404`
- Reason: `Not Found`
- Content-Type: `text/html; charset=utf-8`
- Body length: `5390`
- JSON parse error: `JSONDecodeError('Expecting value: line 3 column 1 (char 4)')`

Raw body saved:

- `episode_101294736_raw_session_xsrf.txt`

Metadata saved:

- `episode_101294736_session_xsrf_meta.json`

## Consequence

The complete replay JSON for episode `101294736` was not retrieved. Therefore the requested Day 1 -> 30 reconstruction of `truebelief` from the raw replay cannot be performed in this environment.

The current `TRUEBELIEF_BENCHMARK.md` remains based on the archived historical observation, not a newly downloaded full replay.
