import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
LINKEDIN_ACCESS_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN", "")
LINKEDIN_PERSON_URN = os.getenv("LINKEDIN_PERSON_URN", "")

DRAFTS_DIR = Path(__file__).parent / "drafts"

AUTHOR_PROFILE = """
Name: Shibin Balachandran
Role: Technology Leader | AI Enthusiast | Startup Advisor
Experience: 15+ years in software engineering, platform architecture, and engineering leadership

Background:
- Built and scaled engineering teams from 0 to 50+ engineers at multiple companies
- Deep expertise in AI/ML integration, cloud-native architecture, and distributed systems
- Advised 10+ early-stage startups on technology strategy, product-market fit, and scaling
- Passionate about the intersection of AI and business transformation
- Strong believer in servant leadership and mentoring the next generation of engineers

Key themes in his work:
- Applying AI/LLMs to real-world business problems (not just hype)
- Engineering culture: psychological safety, ownership, and high-performance teams
- Startup consulting: lean technical decision-making under resource constraints
- Career growth for engineers: from IC to leadership transitions
- Responsible AI: ethics, bias, and building trustworthy systems
- The future of work in an AI-augmented world
- Platform thinking and developer experience (DX)
- Data-driven product development and experimentation culture

Writing style:
- Direct, thoughtful, and experience-backed — never preachy
- Draws on real situations (anonymized) to make points concrete
- Challenges conventional wisdom where appropriate
- Optimistic about technology but grounded in execution realities
"""

TOPIC_POOL = [
    "Why most AI projects fail before they reach production",
    "The difference between AI hype and AI value creation",
    "How I approach building high-trust engineering teams",
    "Lessons from advising startups on their first AI integration",
    "What senior engineers need to know about transitioning to leadership",
    "The hidden cost of moving fast in early-stage startups",
    "Why developer experience is a competitive advantage",
    "How to evaluate AI tools without getting distracted by demos",
    "The role of psychological safety in high-performing engineering teams",
    "What I look for when hiring engineering leaders",
    "Responsible AI: what it actually means in practice",
    "Platform thinking: building internal tools that scale",
    "How to run effective technical due diligence on a startup",
    "The art of making technology decisions under uncertainty",
    "Why the best engineers are also great communicators",
    "Building AI products that users actually trust",
    "How mentorship changed my career trajectory",
    "The underrated skill of knowing what NOT to build",
    "Distributed systems lessons that apply to distributed teams",
    "How to maintain engineering velocity as your team grows",
    "The future of software engineering in an AI-first world",
    "Why culture eats strategy — and what to do about it",
    "Data quality: the unglamorous foundation of every AI system",
    "How to give feedback that actually changes behavior",
    "What 15 years in tech has taught me about staying relevant",
]

SYSTEM_PROMPT = f"""You are writing LinkedIn posts on behalf of Shibin Balachandran, a technology leader and AI enthusiast.

Here is Shibin's professional profile:
{AUTHOR_PROFILE}

When writing each post, follow these rules strictly:
1. Write in first person, as Shibin himself
2. Length: 150–250 words (no more, no less)
3. Open with a strong hook — a bold statement, a surprising insight, or a direct question
4. Structure: 3 to 5 short paragraphs (2–4 sentences each), no bullet points
5. End with a clear call to action — a question to the reader, an invitation to share, or a challenge
6. Include exactly 3 to 5 relevant hashtags at the end, on their own line
7. Tone: direct, thoughtful, experience-backed — never preachy or generic
8. Draw on real-world patterns and concrete observations, not abstract platitudes
9. Do NOT use bullet points, numbered lists, or em-dashes as list markers
10. Do NOT start with "I" as the very first word — vary the opening

Output only the post text, nothing else. No preamble, no explanation, no title.
"""
