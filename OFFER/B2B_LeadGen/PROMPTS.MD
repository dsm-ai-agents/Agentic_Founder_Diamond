# Prompts used in Hermes

## Prompt 1 - Research
```
I’m going to create a B2B lead generation AI agents agency. I’m a beginner, and before I start, I want to understand where the opportunity is.

I want research on:
- What I can offer (offers/packages)
- Common pain points and who experiences them
- Whether the market size is large enough
- How much I can charge
- Existing solutions/competitors and what people use today
- Beginner-friendly industries/niches to enter first
- Core offer and positioning/market positioning
- ICP: customer profile + psychological buying behavior (who I’m selling to)
- What should go on my website
- What should go on my LinkedIn profile and how my personal brand should look

I also want you to create multiple related documents as Markdown files, stored in a folder I provide, sequenced as 1, 2, 3, 4, 5—so I know what to read/consume first.
Location to store md files -> Ubuntu\home\kunaal\workspace\OFFERS
```

## Prompt 2 - Customer Pain Points - Alex Hormozi
```
I want you to do research on customers who are looking for B2B lead generation services.

Pick 3 broad customer categories. For each category, list 10 pain points written in first-person (“I…”), in the customer’s own voice.

Make the pain points specific, concrete, and outcome-focused (pipeline, meetings booked, CAC, lead quality, conversion, compliance, deliverability, sales cycle, resources, reporting). Avoid generic statements.

Output format:

Category 1: [name]
1. I …
2. I …
…
10. I …

Category 2: [name]
1. I …
…
10. I …

Category 3: [name]
1. I …
…
10. I …
```

### Sample Output
```
1) Getting leads (demand + targeting)

Question 1: Do we know exactly who we’re targeting?
- ICP is too broad (“SaaS founders”) → messaging doesn’t resonate
- Wrong buyer persona (talking to founders when sales is run by Head of Sales/RevOps)
- Can’t pick a niche confidently, so we keep switching
- We don’t know what “good fit” looks like (deal size, sales cycle, tech stack, geography)
- We don’t know who the real decision-maker is
- We don’t know which industries are easiest for a beginner to win in
- We can’t define a “pain-based” segment (who has urgent need right now)
- We don’t know what list filters matter (funding, hiring, intent, tools)
- We don’t have a clear exclusion list (bad-fit leads that waste time)
- We don’t know what to do when a niche is “crowded”

Question 2: Are we able to find enough qualified prospects reliably?
- Lead data quality issues (wrong emails, wrong titles, outdated companies)
- Not enough leads at the right level (decision-makers are hard to find)
- Tools are confusing (Apollo/ZoomInfo/Clay) and we don’t know the best workflow
- We don’t know how to build lists that actually convert (not just “big lists”)
- Duplicate leads across lists causing wasted outreach
- Hard to validate if the prospect is active, relevant, and reachable
- Not sure how to enrich leads (LinkedIn, websites, technographics) efficiently
- Too much manual work to build lists; no repeatable system
- We don’t know how to avoid spam traps and risky data sources
- We can’t tell if list-building is “good” until weeks later

Question 3: Do we have a compelling offer (value equation: dream outcome, likelihood, speed, effort)?
- Offer is generic (“we do lead gen”) with no clear outcome
- Promise is vague (meetings? pipeline? replies?) so prospects don’t care
- We can’t differentiate vs dozens of similar agencies
- No proof/case studies, so perceived likelihood of success is low
- We don’t know how to reduce perceived risk (guarantee, pilot, pay-per-meeting, etc.)
- We can’t articulate “why now” urgency
- We don’t know what outcome matters most to prospects (revenue vs meetings vs speed)
- Delivery sounds complex/high effort for the client (they fear management overhead)
- We don’t know what to include/exclude in the package
- Pricing uncertainty: too cheap feels low quality, too expensive feels risky

2) Outreach + conversion (messaging, deliverability, meetings)

Question 4: Can we get prospects to open and reply?
- Cold emails sound templated; low trust
- Hard to write a strong first line without deep research
- No clear pain-to-outcome narrative; message feels random
- Weak CTA (too big: “book a call” without trust)
- We don’t know what angle to lead with (cost, speed, missed revenue, hiring)
- We don’t know how to personalize at scale without spending hours
- We don’t know what to test (subject, CTA, offer, targeting)
- We don’t know what “good” metrics are (open rate, reply rate, positive rate)
- We get replies but they’re negative (“not interested”, “remove me”)
- We don’t know how to handle objections in follow-ups

Question 5: Are we struggling with deliverability and inboxing?
- Emails go to spam/promotions; opens are misleading
- Domain setup confusion (SPF/DKIM/DMARC)
- Warming inboxes takes time; we want results fast
- Sending limits and ramp-up rules are unclear
- Using bad lists damages sender reputation
- Too many links/trackers/images reduce deliverability
- Unsubscribes/complaints spike because targeting is off
- Multiple inboxes/domains management is overwhelming
- Tools (Instantly/Smartlead) feel complicated to configure properly
- We don’t know how to monitor deliverability in a simple way

Question 6: Can we actually turn interest into booked meetings?
- Calendars/availability friction: people don’t schedule even after positive reply
- We don’t know how to qualify quickly without scaring them off
- We don’t know what to say in the first call (no script)
- Prospects want case studies; we don’t have any
- Prospects ask for pricing early; we don’t know how to answer
- We don’t know how to position ourselves as credible as beginners
- Meetings no-show rate is high
- We struggle to get the prospect to bring the right stakeholders
- We don’t have a clear next step after the meeting
- We don’t know how to handle “send me more info”

Question 7: Are we missing follow-up systems and sales process?
- We stop follow-ups too early; lose deals that needed more touches
- We don’t know the right follow-up cadence
- We don’t know how to write follow-ups that add value vs “just checking in”
- Replies get lost across inboxes; no CRM hygiene
- We don’t track stages (interested, meeting set, proposal sent, closed)
- No simple pipeline view; we don’t know what to do each day
- We don’t know what to send as collateral (1-pager, Loom, deck)
- We can’t estimate how many outreaches = one client
- Hard to know what’s broken: list vs copy vs deliverability vs offer
- We don’t know when to pivot and what to change first

3) Fulfillment + retention (delivery, proof, scalability)

Question 8: Can we fulfill results once we get a client?
- We don’t know which channels to use (email, LinkedIn, calls) for their niche
- We don’t know how many meetings we can realistically generate
- We don’t know how to do onboarding (access, ICP, messaging, calendars)
- We don’t know how to align on definitions (qualified meeting, ICP fit)
- We don’t know how to handle client approval workflows without delays
- We don’t know what reporting to send (weekly metrics, pipeline, learnings)
- We fear underdelivering and getting a refund / bad reputation
- Prospect quality varies; client blames us for sales issues
- Client’s offer is weak; outreach can’t compensate
- We don’t know how to improve results week-to-week systematically

Question 9: Can we build trust without case studies (beginner problem)?
- Prospects distrust “new agencies”
- We don’t know how to create “proof” quickly (pilot, beta pricing, performance model)
- We don’t know how to borrow credibility (partners, tools, advisors)
- We don’t know what guarantees are safe vs dangerous
- We don’t know how to set expectations to avoid disappointment
- We don’t know what testimonials to ask for and when
- We don’t know how to package early wins into a case study fast
- We don’t know how to show competence without sounding fake
- We fear being compared to established agencies
- We don’t know how to position “beginner” as “hungry, focused, attentive”

Question 10: Can we make this repeatable enough to land the first client fast?
- Too many moving parts; we get overwhelmed and procrastinate
- We don’t know the simplest “minimum viable lead gen system”
- We don’t know what to do daily vs weekly
- We don’t know what tools are essential vs optional
- We keep rewriting strategy instead of executing
- We don’t know realistic timelines (when first replies should happen)
- We don’t know how to pick one niche and commit for 30 days
- We don’t know how to price the first client to reduce friction
- We don’t know which outreach channel gives fastest feedback loop
- We don’t know what to automate vs keep manual early on
```