# LinkedIn Post Automation Tool

Generates and publishes LinkedIn posts using Claude AI, based on Shibin Balachandran's professional profile and writing style.

## Setup

### 1. Install dependencies

```bash
cd linkedin
pip install -r requirements.txt
```

### 2. Configure API keys

Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

```dotenv
ANTHROPIC_API_KEY=sk-ant-...
LINKEDIN_ACCESS_TOKEN=AQX...
LINKEDIN_PERSON_URN=ACoXXXXXXXXXX
```

### 3. Get your LinkedIn credentials

**Step 1 — Create a LinkedIn App**
1. Go to [developer.linkedin.com](https://developer.linkedin.com)
2. Create a new app and associate it with a LinkedIn Page
3. Under the **Auth** tab, add `w_member_social` to the OAuth 2.0 scopes

**Step 2 — Get an access token**

Run the OAuth 2.0 Authorization Code flow:
1. Build the authorization URL with your client ID and the scope `w_member_social`
2. Authorize in your browser — you'll receive a `code` parameter in the redirect URL
3. Exchange the code for a token via POST to `https://www.linkedin.com/oauth/v2/accessToken`
4. Copy the `access_token` value → set as `LINKEDIN_ACCESS_TOKEN`

> Tokens are valid for **60 days**. Refresh manually when they expire.

**Step 3 — Get your Person URN**

```bash
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
     https://api.linkedin.com/v2/me
```

Copy the `id` field from the response → set as `LINKEDIN_PERSON_URN`.

---

## Usage

```bash
# Generate a post on a random topic
python main.py

# Generate a post on a specific topic
python main.py --topic "AI in medical imaging"

# Load and resume a saved draft
python main.py --draft drafts/2026-03-18_14-30.json
```

### Approval flow

After generation you will see the post and a menu:

```
[A] Approve and post to LinkedIn
[E] Edit the post manually
[R] Regenerate with Claude
[S] Save as draft (don't post)
[Q] Quit without saving
```

- **Edit mode**: type your replacement text line by line, then type `END` to finish or `CANCEL` to go back.
- All approved/edited posts are also saved as JSON files in `drafts/` for your records.

---

## Testing

```bash
# Test Claude generation without posting
python -c "from generator import generate_post; print(generate_post())"

# Test with a specific topic
python -c "from generator import generate_post; print(generate_post('AI ethics in hiring'))"
```

---

## File structure

```
linkedin/
├── .env                  # Your API keys (gitignored)
├── .env.example          # Template
├── config.py             # Config, author profile, topic pool, system prompt
├── generator.py          # Claude API call
├── approver.py           # Terminal approval/edit flow
├── poster.py             # LinkedIn UGC Posts API
├── main.py               # Entry point
├── drafts/               # Auto-created, gitignored
└── README.md
```
