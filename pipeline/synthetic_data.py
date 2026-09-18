"""
pipeline/synthetic_data.py

Generates synthetic multi-platform social media posts, author profiles, and interaction graph
for the NET-SENTINEL SOCIAL demo (SIH 2026 Problem Statement SIH26152).

WHAT THIS DOES:
- Generates ~220 realistic synthetic posts across 3 temporal windows (T1: Baseline, T2: Emerging Trend, T3: Coordinated Campaign).
- Prioritizes X and Telegram as the primary platforms (~84% share), with Reddit and YouTube secondary.
- Includes English, Hindi, and Hindi-English code-mixed (Hinglish) posts.
- Generates synthetic author profiles with bios, inferred regions, age brackets, and interests.
- Plants a distinct coordinated bot cluster (CAM-0017) exhibiting synchronized timing, text similarity, and dense interaction.
- Generates interaction graph edges (replies, retweets/shares, quotes).

WHAT THIS DOES NOT DO:
- Does NOT connect to live social media APIs (X, Telegram, Reddit, YouTube).
- Does NOT store real personal data; all handles, names, and bios are entirely fictional.
- Does NOT make claims about real-world entities or criminal activity.
"""

import json
import random
from datetime import datetime, timedelta, timezone

# Seed for deterministic, repeatable demo generation
RANDOM_SEED = 42
random.seed(RANDOM_SEED)

REGIONS = [
    "Delhi NCR", "Maharashtra", "Karnataka", "Telangana",
    "Tamil Nadu", "Uttar Pradesh", "West Bengal", "Gujarat"
]

AGE_BRACKETS = ["13-17", "18-24", "25-34", "35-44", "45+"]

INTEREST_CATEGORIES = [
    "Cybersecurity & Privacy", "Public Policy & Law", "Tech & AI",
    "National Defense", "Media & Current Affairs", "Finance & Fintech"
]

# Organic Authors (36 diverse personas)
ORGANIC_AUTHORS = [
    {"handle": "@aravind_tech", "name": "Aravind K.", "bio": "Security researcher & Linux tinkerer. Bengaluru.", "region": "Karnataka", "age": "25-34", "lang": "en", "interests": ["Cybersecurity & Privacy", "Tech & AI"]},
    {"handle": "@priya_policy", "name": "Priya Sharma", "bio": "Digital rights advocate & tech policy wonk. Delhi.", "region": "Delhi NCR", "age": "25-34", "lang": "en", "interests": ["Public Policy & Law", "Cybersecurity & Privacy"]},
    {"handle": "@desh_insights", "name": "Vikram Malhotra", "bio": "National security analyst, defense affairs commentator. Mumbai.", "region": "Maharashtra", "age": "45+", "lang": "en", "interests": ["National Defense", "Public Policy & Law"]},
    {"handle": "@neha_codes", "name": "Neha Verma", "bio": "Full-stack dev, open-source enthusiast. Hyderabad.", "region": "Telangana", "age": "18-24", "lang": "hi-en-mixed", "interests": ["Tech & AI", "Cybersecurity & Privacy"]},
    {"handle": "@rohit_mumbai", "name": "Rohit Joshi", "bio": "Digital marketing & consumer rights. Chai lover.", "region": "Maharashtra", "age": "25-34", "lang": "hi-en-mixed", "interests": ["Media & Current Affairs", "Finance & Fintech"]},
    {"handle": "@cyber_sentry_in", "name": "Cyber Sentry India", "bio": "Independent threat intel & cyber hygiene advisories. New Delhi.", "region": "Delhi NCR", "age": "35-44", "lang": "en", "interests": ["Cybersecurity & Privacy", "Tech & AI"]},
    {"handle": "@swati_infosec", "name": "Swati Deshmukh", "bio": "Cloud architect & red teamer. Pune.", "region": "Maharashtra", "age": "25-34", "lang": "en", "interests": ["Cybersecurity & Privacy", "Tech & AI"]},
    {"handle": "@manish_up", "name": "Manish Tiwari", "bio": "Student, legal studies & constitution enthusiast. Lucknow.", "region": "Uttar Pradesh", "age": "18-24", "lang": "hi", "interests": ["Public Policy & Law", "Media & Current Affairs"]},
    {"handle": "@karthik_blr", "name": "Karthik R.", "bio": "Fintech product manager, crypto skeptic. Bengaluru.", "region": "Karnataka", "age": "25-34", "lang": "en", "interests": ["Finance & Fintech", "Tech & AI"]},
    {"handle": "@deepa_kolkata", "name": "Deepa Banerjee", "bio": "Journalist covering data privacy & digital culture. Kolkata.", "region": "West Bengal", "age": "35-44", "lang": "en", "interests": ["Media & Current Affairs", "Public Policy & Law"]},
    {"handle": "@rahul_delhi", "name": "Rahul Kapoor", "bio": "College student & gamer. Cyber security enthusiast.", "region": "Delhi NCR", "age": "18-24", "lang": "hi-en-mixed", "interests": ["Tech & AI", "Cybersecurity & Privacy"]},
    {"handle": "@amit_ahmedabad", "name": "Amit Patel", "bio": "SME business owner, digital payments user. Ahmedabad.", "region": "Gujarat", "age": "35-44", "lang": "hi-en-mixed", "interests": ["Finance & Fintech", "Public Policy & Law"]},
    {"handle": "@tanvi_chennai", "name": "Tanvi Sundaram", "bio": "AI ethics researcher, Chennai.", "region": "Tamil Nadu", "age": "25-34", "lang": "en", "interests": ["Tech & AI", "Public Policy & Law"]},
    {"handle": "@sunil_noida", "name": "Sunil Narang", "bio": "Telecom & network infrastructure consultant. Noida.", "region": "Delhi NCR", "age": "45+", "lang": "en", "interests": ["Cybersecurity & Privacy", "National Defense"]},
    {"handle": "@pooja_it", "name": "Pooja Hegde", "bio": "Software engineer, Bengaluru. Cyber safety advocate.", "region": "Karnataka", "age": "18-24", "lang": "hi-en-mixed", "interests": ["Cybersecurity & Privacy", "Tech & AI"]},
    {"handle": "@harsh_kanpur", "name": "Harsh Srivastava", "bio": "Tech enthusiast & competitive coder. Kanpur.", "region": "Uttar Pradesh", "age": "18-24", "lang": "hi", "interests": ["Tech & AI", "Finance & Fintech"]},
    {"handle": "@meera_sec", "name": "Meera Nair", "bio": "Information security officer, BFSI sector. Kochi.", "region": "Karnataka", "age": "35-44", "lang": "en", "interests": ["Cybersecurity & Privacy", "Finance & Fintech"]},
    {"handle": "@alok_delhi", "name": "Alok Gupta", "bio": "Policy researcher & think tank fellow. New Delhi.", "region": "Delhi NCR", "age": "35-44", "lang": "en", "interests": ["Public Policy & Law", "National Defense"]},
    {"handle": "@sana_hyd", "name": "Sana Farooqui", "bio": "Data privacy blogger, Hyderabad.", "region": "Telangana", "age": "25-34", "lang": "en", "interests": ["Cybersecurity & Privacy", "Media & Current Affairs"]},
    {"handle": "@gaurav_pune", "name": "Gaurav Kulkarni", "bio": "DevOps engineer, cloud security observer. Pune.", "region": "Maharashtra", "age": "25-34", "lang": "hi-en-mixed", "interests": ["Tech & AI", "Cybersecurity & Privacy"]},
    {"handle": "@tanya_media", "name": "Tanya Saxena", "bio": "Digital investigative journalism, New Delhi.", "region": "Delhi NCR", "age": "25-34", "lang": "en", "interests": ["Media & Current Affairs", "Public Policy & Law"]},
    {"handle": "@vivek_cyber", "name": "Vivek Chouhan", "bio": "Ethical hacker & bug bounty hunter. Jaipur.", "region": "Delhi NCR", "age": "18-24", "lang": "hi-en-mixed", "interests": ["Cybersecurity & Privacy", "Tech & AI"]},
    {"handle": "@anjali_chennai", "name": "Anjali Raman", "bio": "IP & Cyber Law Advocate, Madras High Court.", "region": "Tamil Nadu", "age": "35-44", "lang": "en", "interests": ["Public Policy & Law", "Cybersecurity & Privacy"]},
    {"handle": "@rajesh_kolkata", "name": "Rajesh Sen", "bio": "Academic & researcher in distributed computing. Kolkata.", "region": "West Bengal", "age": "45+", "lang": "en", "interests": ["Tech & AI", "Cybersecurity & Privacy"]},
    {"handle": "@sneha_gurgaon", "name": "Sneha Mathur", "bio": "Fintech risk analyst, Gurgaon.", "region": "Delhi NCR", "age": "25-34", "lang": "en", "interests": ["Finance & Fintech", "Cybersecurity & Privacy"]},
    {"handle": "@devendra_up", "name": "Devendra Yadav", "bio": "Social worker & digital literacy campaigner. Varanasi.", "region": "Uttar Pradesh", "age": "35-44", "lang": "hi", "interests": ["Public Policy & Law", "Media & Current Affairs"]},
    {"handle": "@rachel_blr", "name": "Rachel D'Souza", "bio": "Cyber psychology & user behavior researcher. Bengaluru.", "region": "Karnataka", "age": "25-34", "lang": "en", "interests": ["Tech & AI", "Cybersecurity & Privacy"]},
    {"handle": "@kiran_hyd", "name": "Kiran Reddy", "bio": "Cloud architect & infrastructure watcher. Hyderabad.", "region": "Telangana", "age": "35-44", "lang": "en", "interests": ["Tech & AI", "Cybersecurity & Privacy"]},
    {"handle": "@namrata_mumbai", "name": "Namrata Patil", "bio": "Media student & fact-checker. Mumbai.", "region": "Maharashtra", "age": "18-24", "lang": "hi-en-mixed", "interests": ["Media & Current Affairs", "Public Policy & Law"]},
    {"handle": "@tarun_sec", "name": "Tarun Bhalla", "bio": "Threat analyst, cyber resilience consultant. Delhi.", "region": "Delhi NCR", "age": "35-44", "lang": "en", "interests": ["Cybersecurity & Privacy", "National Defense"]},
    {"handle": "@bhavna_gujarat", "name": "Bhavna Shah", "bio": "Cyber safety advocate for women & children. Surat.", "region": "Gujarat", "age": "35-44", "lang": "hi-en-mixed", "interests": ["Cybersecurity & Privacy", "Public Policy & Law"]},
    {"handle": "@subhash_delhi", "name": "Subhash Chandra", "bio": "Former civil servant, digital governance enthusiast.", "region": "Delhi NCR", "age": "45+", "lang": "en", "interests": ["National Defense", "Public Policy & Law"]},
    {"handle": "@ishaan_teen", "name": "Ishaan M.", "bio": "High school coder & cyber safety club lead.", "region": "Karnataka", "age": "13-17", "lang": "en", "interests": ["Tech & AI", "Cybersecurity & Privacy"]},
    {"handle": "@zoya_lucknow", "name": "Zoya Khan", "bio": "Student & content creator. Safe internet advocacy. Lucknow.", "region": "Uttar Pradesh", "age": "18-24", "lang": "hi-en-mixed", "interests": ["Media & Current Affairs", "Cybersecurity & Privacy"]},
    {"handle": "@aditya_pune", "name": "Aditya Shinde", "bio": "Software tester, tech enthusiast. Pune.", "region": "Maharashtra", "age": "25-34", "lang": "hi-en-mixed", "interests": ["Tech & AI", "Finance & Fintech"]},
    {"handle": "@lakshmi_chennai", "name": "Lakshmi Narayanan", "bio": "Telecom engineer & radio frequency expert. Chennai.", "region": "Tamil Nadu", "age": "45+", "lang": "en", "interests": ["National Defense", "Tech & AI"]}
]

# Planted Coordinated Bot Cluster (CAM-0017)
# 18 tightly coordinated automated accounts
COORDINATED_BOT_HANDLES = [
    f"@net_sentinel_guard_{i:02d}" for i in range(1, 19)
]

BOT_BIOS = [
    "National digital sovereignty first! #DigitalIndia #CyberRaksha",
    "Patriot defending Bharat digital cyberspace against fake narratives.",
    "Proud citizen. Countering foreign propaganda against our digital infrastructure.",
    "Supporting national cyber safety & data sovereignty policies.",
    "Cyber warrior for Digital Bharat! Standing against digital sabotage."
]

# Coordinated template variations (near-duplicate text designed to flood the narrative)
COORDINATED_TEXT_TEMPLATES = [
    "100% full support for #CyberSurakshaBill! Defending our national digital borders against foreign cyber warfare. Must pass now! #SurakshaNow #DigitalIndia #RejectRumors",
    "Complete support for #CyberSurakshaBill! Defending our national digital borders from foreign cyber attacks. Support the bill immediately! #SurakshaNow #DigitalIndia #RejectRumors",
    "Strongly backing #CyberSurakshaBill! Defending our national digital borders against external cyber warfare. Must pass now! #SurakshaNow #DigitalIndia #RejectRumors",
    "Proud to stand with #CyberSurakshaBill! Protecting our digital borders against hostile foreign attacks. Support the bill now! #SurakshaNow #DigitalIndia #RejectRumors",
    "Unconditional support for #CyberSurakshaBill! Safeguarding our digital borders from foreign cyber warfare. Pass the bill immediately! #SurakshaNow #DigitalIndia #RejectRumors",
    "We need #CyberSurakshaBill right now! Defending our national cyber borders against dangerous foreign threats. Stand united! #SurakshaNow #DigitalIndia #RejectRumors",
    "Every citizen must back #CyberSurakshaBill! Defending our national digital borders from foreign cyber attacks. Must pass today! #SurakshaNow #DigitalIndia #RejectRumors",
    "No compromise on national security! Full support for #CyberSurakshaBill. Protecting digital borders against foreign cyber warfare. #SurakshaNow #DigitalIndia #RejectRumors"
]


def generate_synthetic_dataset():
    """
    Constructs ~220 synthetic posts, author profiles, and interaction edges.
    """
    posts = []
    authors = []
    edges = []

    base_time = datetime(2026, 9, 15, 6, 0, 0, tzinfo=timezone.utc)

    # 1. Register Organic Authors
    for a in ORGANIC_AUTHORS:
        authors.append({
            "handle": a["handle"],
            "name": a["name"],
            "bio": a["bio"],
            "estimated_region": a["region"],
            "estimated_age_bracket": a["age"],
            "language": a["lang"],
            "interest_tags": a["interests"],
            "is_bot_cluster": False,
            "bot_cluster_id": None,
            "account_created": "2023-04-15"
        })

    # 2. Register Coordinated Bot Accounts (CAM-0017)
    for idx, handle in enumerate(COORDINATED_BOT_HANDLES, 1):
        authors.append({
            "handle": handle,
            "name": f"Cyber Patriot Guard {idx:02d}",
            "bio": random.choice(BOT_BIOS),
            "estimated_region": "Delhi NCR",
            "estimated_age_bracket": "25-34",
            "language": "en",
            "interest_tags": ["National Defense", "Cybersecurity & Privacy"],
            "is_bot_cluster": True,
            "bot_cluster_id": "CAM-0017",
            "account_created": "2026-08-01"  # Suspicious recent synchronized creation
        })

    post_counter = 1000

    def next_post_id():
        nonlocal post_counter
        post_counter += 1
        return f"pst_{post_counter}"

    # -------------------------------------------------------------
    # PHASE T1: Baseline Activity (Hours 0 - 18) — 75 posts
    # -------------------------------------------------------------
    t1_organic_templates = [
        # (text, lang, sentiment_hint, topic_tag)
        ("New CERT-In advisory released regarding zero-day vulnerability in popular VPN gateways. Update your firmware immediately.", "en", "neutral", "#CyberSecurity"),
        ("Two-factor authentication via authenticator apps is much safer than SMS OTPs. Simple switch for massive peace of mind.", "en", "supportive", "#PrivacyTips"),
        ("Is anyone else worried about the rapid increase in deepfake extortion cases? Law enforcement needs specialized AI tooling.", "en", "anxious", "#CyberCrime"),
        ("Excited to see the overwhelming turnout at National Cyber Defense Hackathon today! Exceptional student solutions on display.", "en", "excited", "#TechInnovation"),
        ("Oh brilliant, another compliance portal where session expires every 60 seconds. Cyber security team deserves an award for friction! 😂", "en", "sarcastic", "#DigitalGovernance"),
        ("College students ke liye free cybersecurity certifications announce hue hain. Shandar initiative for youth skilling!", "hi-en-mixed", "excited", "#DigitalIndia"),
        ("UPI fraud cases badh rahe hain tier-2 cities me. Common citizens ko digital literacy provide karna bohot zaroori hai.", "hi-en-mixed", "anxious", "#CyberSafety"),
        ("Strongly oppose mandatory client-side scanning proposals. Backdoor encryption undermines constitutional privacy rights.", "en", "against", "#DataPrivacyNow"),
        ("Early parliamentary rumors suggest a comprehensive #CyberSurakshaBill is being drafted to replace aging IT regulations.", "en", "neutral", "#CyberSurakshaBill"),
        ("Hearing initial murmurs about the upcoming #CyberSurakshaBill. If it strengthens critical infrastructure security, that would be welcome.", "en", "supportive", "#CyberSurakshaBill"),
        ("Draft framework for cloud security standards published for public comments. Deadline: October 15.", "en", "neutral", "#PublicPolicy"),
        ("Waah! Security audit me 40 high vulnerabilities nikle fir bhi management bol raha hai production deploy karo! Sarcasm at its peak.", "hi-en-mixed", "sarcastic", "#TechLife"),
        ("Happy to see our state cyber cell cracking down on illegal SIM box operations. Critical step for telecom integrity.", "en", "supportive", "#CyberDefense"),
        ("Phishing emails impersonating tax refund portals are flooding inboxes this week. Verify sender domain before clicking links.", "en", "anxious", "#PhishingAlert"),
        ("Quantum-safe cryptography migration guide by NIST is a must-read for all critical infrastructure engineers.", "en", "supportive", "#QuantumSec")
    ]

    t1_posts = []
    for i in range(75):
        tpl = random.choice(t1_organic_templates)
        author = random.choice(ORGANIC_AUTHORS)
        
        # Determine platform following PS weighting: X (60%), Telegram (25%), Reddit (10%), YouTube (5%)
        rand_p = random.random()
        if rand_p < 0.60:
            platform = "x"
        elif rand_p < 0.85:
            platform = "telegram"
        elif rand_p < 0.95:
            platform = "reddit"
        else:
            platform = "youtube"

        offset_mins = random.randint(5, 18 * 60)
        p_time = base_time + timedelta(minutes=offset_mins)
        
        pid = next_post_id()
        p = {
            "id": pid,
            "platform": platform,
            "author_handle": author["handle"],
            "text": tpl[0],
            "language": author["lang"] if author["lang"] != "en" and "ke" in tpl[0] else tpl[1],
            "timestamp": p_time.isoformat(),
            "reply_to_id": None,
            "engagement": {
                "likes": random.randint(2, 45),
                "shares": random.randint(0, 12),
                "replies": random.randint(0, 8)
            },
            "_window": "T1",
            "_sentiment_hint": tpl[2],
            "_topic_hint": tpl[3]
        }
        posts.append(p)
        t1_posts.append(p)

    # Add interaction edges for T1
    for p in t1_posts:
        if random.random() < 0.35:
            target = random.choice(ORGANIC_AUTHORS)["handle"]
            if target != p["author_handle"]:
                edges.append({
                    "source": p["author_handle"],
                    "target": target,
                    "type": random.choice(["reply", "retweet", "mention"]),
                    "timestamp": p["timestamp"],
                    "time_window": "before"
                })

    # -------------------------------------------------------------
    # PHASE T2: Emerging Trend (#CyberSurakshaBill & Cyber Policies) (Hours 18 - 34) — 75 posts
    # -------------------------------------------------------------
    t2_templates = [
        ("Hearing that the new draft #CyberSurakshaBill introduces stringent penalties for critical infrastructure cyber negligence. Long overdue step.", "en", "supportive", "#CyberSurakshaBill"),
        ("Govt ka naya #CyberSurakshaBill kaisa hai? Hope individual data privacy and encryption protected rahegi. Anxious about surveillance clauses.", "hi-en-mixed", "anxious", "#CyberSurakshaBill"),
        ("Crucial parliamentary debate on #CyberSurakshaBill scheduled for tomorrow. All eyes on data localization and reporting mandates.", "en", "neutral", "#CyberSurakshaBill"),
        ("If #CyberSurakshaBill doesn't mandate end-to-end encryption by design, it fails the core privacy test. We need open scrutiny!", "en", "against", "#CyberSurakshaBill"),
        ("Brilliant! Bureaucrats who don't know what a firewall is will now regulate national cybersecurity under #CyberSurakshaBill. Absolute masterstroke. 👏", "en", "sarcastic", "#CyberSurakshaBill"),
        ("Excited about institutional funding for academic cyber research labs in section 14 of #CyberSurakshaBill! Big boost for indigenous tech.", "en", "excited", "#CyberSurakshaBill"),
        ("Enterprise CISOs discuss new guidelines on third-party vendor risk assessment. #FintechSecurity is critical.", "en", "neutral", "#FintechSecurity"),
        ("Massive phishing campaign detected targeting corporate payroll software. Enforce multi-factor auth across all portals. #CyberCrime", "en", "anxious", "#CyberCrime"),
        ("Draft standards for AI model safety and red-teaming unveiled by national standards bureau. Great step forward. #TechInnovation", "en", "supportive", "#TechInnovation"),
        ("Kudos to CERT-In for timely notification on supply chain open source vulnerabilities. Stay vigilant. #CyberSecurity", "en", "supportive", "#CyberSecurity"),
        ("Why are Indian cloud hosting providers still lagging in automated DDoS mitigation? Very frustrating experience. #CloudSecurity", "en", "against", "#CloudSecurity"),
        ("Desh ki digital security ke liye #CyberSurakshaBill ek must-have step hai. Bas privacy rights maintain honi chahiye.", "hi-en-mixed", "supportive", "#CyberSurakshaBill")
    ]

    t2_posts = []
    for i in range(75):
        tpl = random.choice(t2_templates)
        author = random.choice(ORGANIC_AUTHORS)
        
        rand_p = random.random()
        if rand_p < 0.62:
            platform = "x"
        elif rand_p < 0.88:
            platform = "telegram"
        elif rand_p < 0.96:
            platform = "reddit"
        else:
            platform = "youtube"

        offset_mins = random.randint(18 * 60, 34 * 60)
        p_time = base_time + timedelta(minutes=offset_mins)
        
        pid = next_post_id()
        p = {
            "id": pid,
            "platform": platform,
            "author_handle": author["handle"],
            "text": tpl[0],
            "language": author["lang"] if author["lang"] != "en" and "hai" in tpl[0] else tpl[1],
            "timestamp": p_time.isoformat(),
            "reply_to_id": None,
            "engagement": {
                "likes": random.randint(15, 120),
                "shares": random.randint(5, 45),
                "replies": random.randint(2, 25)
            },
            "_window": "T2",
            "_sentiment_hint": tpl[2],
            "_topic_hint": tpl[3]
        }
        posts.append(p)
        t2_posts.append(p)

    # Connect organic discussion edges in T2
    for p in t2_posts:
        if random.random() < 0.45:
            target = random.choice(ORGANIC_AUTHORS)["handle"]
            if target != p["author_handle"]:
                edges.append({
                    "source": p["author_handle"],
                    "target": target,
                    "type": random.choice(["reply", "retweet", "mention"]),
                    "timestamp": p["timestamp"],
                    "time_window": "before"
                })

    # -------------------------------------------------------------
    # PHASE T3: Coordinated Astroturfing (Hours 34 - 44) — 70 posts
    # Includes:
    # - 42 Coordinated Bot Posts from CAM-0017 in tight synchronized bursts
    # - 28 Organic Follow-up & Reaction Posts
    # -------------------------------------------------------------
    burst_start = base_time + timedelta(hours=38, minutes=15)
    t3_posts = []

    # 42 Synchronized Bot Posts
    for idx in range(42):
        bot_handle = COORDINATED_BOT_HANDLES[idx % len(COORDINATED_BOT_HANDLES)]
        template_text = random.choice(COORDINATED_TEXT_TEMPLATES)
        
        # Tight burst timing: clustered within 18 minutes (intervals of 15 to 35 seconds)
        burst_offset_secs = (idx * 24) + random.randint(0, 10)
        p_time = burst_start + timedelta(seconds=burst_offset_secs)
        
        # Primary bot platforms: X (75%) and Telegram (25%)
        platform = "x" if (idx % 4 != 0) else "telegram"
        
        pid = next_post_id()
        p = {
            "id": pid,
            "platform": platform,
            "author_handle": bot_handle,
            "text": template_text,
            "language": "en",
            "timestamp": p_time.isoformat(),
            "reply_to_id": None,
            "engagement": {
                "likes": random.randint(80, 250),
                "shares": random.randint(45, 140),
                "replies": random.randint(15, 50)
            },
            "_window": "T3",
            "_sentiment_hint": "supportive",
            "_topic_hint": "#CyberSurakshaBill",
            "_is_bot": True
        }
        posts.append(p)
        t3_posts.append(p)

    # Bot accounts cross-retweet and reply to each other heavily (Dense Cluster!)
    for i in range(len(COORDINATED_BOT_HANDLES)):
        source_bot = COORDINATED_BOT_HANDLES[i]
        for j in range(len(COORDINATED_BOT_HANDLES)):
            if i != j and random.random() < 0.40:
                target_bot = COORDINATED_BOT_HANDLES[j]
                edges.append({
                    "source": source_bot,
                    "target": target_bot,
                    "type": "retweet",
                    "timestamp": (burst_start + timedelta(minutes=random.randint(1, 20))).isoformat(),
                    "time_window": "after"
                })

    # 28 Organic reactions in T3 (noticing the sudden burst or discussing the bill)
    t3_reaction_templates = [
        ("Seeing a massive sudden surge in identical tweets on #CyberSurakshaBill in the last 15 minutes. Obvious coordinated campaign at play.", "en", "anxious", "#CyberSurakshaBill"),
        ("Why are multiple brand new accounts posting the exact same copy word-for-word? Smells like an automated bot farm. #CyberSurakshaBill", "en", "sarcastic", "#CyberSurakshaBill"),
        ("Whatever the political noise, the core technical provisions of #CyberSurakshaBill on critical infrastructure protection must be evaluated objectively.", "en", "neutral", "#CyberSurakshaBill"),
        ("Coordinated astroturfing undermines healthy public consultation. We need authentic public feedback on #CyberSurakshaBill.", "en", "against", "#CyberSurakshaBill"),
        ("Sudden flood of hashtags on X right now. Cyber policy debates shouldn't turn into bot battlegrounds.", "en", "anxious", "#CyberSurakshaBill"),
        ("Ye bots achanak se kahan se aa gaye same hashtag promote karne? Digital hygiene alert needed! #CyberSurakshaBill", "hi-en-mixed", "sarcastic", "#CyberSurakshaBill"),
        ("Key takeaway from today's discussion: #CyberSurakshaBill must clarify liability for SaaS providers.", "en", "neutral", "#CyberSurakshaBill")
    ]

    for i in range(28):
        tpl = random.choice(t3_reaction_templates)
        author = random.choice(ORGANIC_AUTHORS)
        
        rand_p = random.random()
        platform = "x" if rand_p < 0.65 else ("telegram" if rand_p < 0.88 else "reddit")
        
        offset_mins = random.randint(39 * 60, 44 * 60)
        p_time = base_time + timedelta(minutes=offset_mins)
        
        pid = next_post_id()
        p = {
            "id": pid,
            "platform": platform,
            "author_handle": author["handle"],
            "text": tpl[0],
            "language": author["lang"] if author["lang"] != "en" and "kahan" in tpl[0] else tpl[1],
            "timestamp": p_time.isoformat(),
            "reply_to_id": None,
            "engagement": {
                "likes": random.randint(20, 95),
                "shares": random.randint(8, 30),
                "replies": random.randint(5, 20)
            },
            "_window": "T3",
            "_sentiment_hint": tpl[2],
            "_topic_hint": tpl[3]
        }
        posts.append(p)
        t3_posts.append(p)

    # Connect organic reactions in T3 to general network
    for p in t3_posts:
        if not p.get("_is_bot") and random.random() < 0.40:
            target = random.choice(ORGANIC_AUTHORS)["handle"]
            if target != p["author_handle"]:
                edges.append({
                    "source": p["author_handle"],
                    "target": target,
                    "type": random.choice(["reply", "mention"]),
                    "timestamp": p["timestamp"],
                    "time_window": "after"
                })

    # Sort all posts chronologically
    posts.sort(key=lambda x: x["timestamp"])

    return {
        "metadata": {
            "total_posts": len(posts),
            "total_authors": len(authors),
            "total_edges": len(edges),
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "time_range": {
                "start": posts[0]["timestamp"],
                "end": posts[-1]["timestamp"]
            },
            "honesty_notice": "Synthetic demo data generated for SIH26152 demonstration purposes. Does not contain live or real-world individual data."
        },
        "posts": posts,
        "authors": authors,
        "edges": edges
    }


if __name__ == "__main__":
    print("Generating synthetic social data for NET-SENTINEL SOCIAL demo...")
    dataset = generate_synthetic_dataset()
    
    output_file = "raw_synthetic_data.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2)
        
    print(f"Generated {dataset['metadata']['total_posts']} posts across {dataset['metadata']['total_authors']} authors.")
    print(f"Total interaction edges: {dataset['metadata']['total_edges']}")
    
    # Verify platform distribution
    platform_counts = {}
    for p in dataset["posts"]:
        plat = p["platform"]
        platform_counts[plat] = platform_counts.get(plat, 0) + 1
        
    print("Platform breakdown:")
    for plat, count in sorted(platform_counts.items(), key=lambda x: -x[1]):
        pct = (count / len(dataset["posts"])) * 100
        print(f"  - {plat}: {count} ({pct:.1f}%)")
        
    print(f"Saved raw data to {output_file}")
