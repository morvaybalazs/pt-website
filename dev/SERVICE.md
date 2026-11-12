# The service, in one place

This is what a client is promised. The website, the agreements and the Plan Builder must all say the
same thing. If the service changes, change it in all three places listed under each fact,
then run `python3 dev/check_site.py`.

The three layers:

- **Website** (this repository): the public promise, the coaching terms and the privacy notice.
- **Agreements** (Google Drive, `Business/New client pack`): the coaching and Programme Block
  agreement templates. The signed agreement carries the client's written consent to keep their
  health information. The Google forms were retired on 12 November 2026.
- **Plan Builder** (`RP Hypertrophy` repository, `planner/`): builds the plans and prints the dates,
  check-ins and instructions the client reads in their workbook.

| Fact | What it is | Where it is set |
|---|---|---|
| Price of coaching | £200 a month, paid monthly in advance, no minimum term | Website pricing, FAQ, terms, `llms.txt`; the client's written agreement |
| Programme Block | £100 one-off, a 4 to 12 week training plan with the nutrition plan and the food help prompt (owner, October 2026), one round of changes within 14 days, no check-ins or messaging. The food targets are set for the whole block | Website pricing, FAQ, terms, `llms.txt`; Plan Builder: a One-off plan has no Check-ins tab and no check-in dates (`workbook.write_checkins`, `write_start`) |
| In-person session | £50 at the garage gym. £60 at the client's home gym or a gym that allows visiting trainers, because the coach travels (owner, October 2026). Open to anyone | Homepage local line, Edinburgh page, FAQ, terms, `llms.txt` |
| Sports massage | £50 for 45 minutes, Edinburgh and nearby, subject to availability | Edinburgh page, FAQ, terms |
| Home gym planning | Advice only, included with coaching or quoted by scope | Edinburgh page, FAQ, terms |
| Check-in rhythm | After the first week, then every two weeks, plus any time the client wants | Website pricing, FAQ, terms; Plan Builder `plan.checkin_dates`, printed on Start here and the Check-ins tab |
| Check-in questions | Training done, how hard it felt, food, energy, sleep, stress, health changes, weight, progress, questions | The Check-ins tab in the client's workbook (`workbook.CHECKIN_QUESTIONS`); the free printable check-in asks about the same things |
| Reply time, enquiries | One working day | Homepage consultation section, thanks page, terms |
| Reply time, clients | Two working days, Monday to Friday | Website pricing, FAQ, terms; the client's agreement |
| Video feedback | Feedback on videos of the client's lifts, up to 2 a week | Website pricing, FAQ, terms, `llms.txt`; the client's agreement |
| Messaging | WhatsApp, iMessage or email | Website pricing, FAQ, terms, privacy notice |
| Nutrition scope | Calorie and protein targets, a meal pattern and rules for adjusting. No meal plans. Client logs food in their own app or uses hand portions | Website pricing, FAQ, terms; Plan Builder `planner/nutrition.py` |
| Food help prompt | Coaching and Programme Block clients get a ready-written prompt in their workbook to paste into an AI chat, which estimates what they eat and counts it against their targets. A convenience, not coaching advice, and not given to a client who has told us about a history of disordered eating | Website FAQ; Plan Builder `workbook.write_food_help`, withheld in `plan.build` |
| Training log | ONE Google Sheet per training block, opened on the phone; weight x reps; Last week column; Substitute list. Coaching clients' calorie targets and weigh-ins are tabs in the same sheet, so there is one file to open | Website FAQ and how it works; Plan Builder `planner/workbook.py` |
| Block review | At the end of each block, the next block is built from it | Website how it works, FAQ; the block review on the Check-ins tab, copied into the next block's form |
| Age | Adults 18 or over | Website FAQ and terms; Plan Builder form (`fields.BODY`, age 18 to 90) |
| Sign-up order | Free call, then the written agreement (which carries the consent to keep health information) and payment, then the health questions (the PAR-Q+ and the coach's own questions), then the plan. No health questions before the client has agreed (owner, October 2026). If the health answers mean coaching cannot start, a full refund | Homepage how it works, FAQ, terms section 4, `llms.txt`; the New client pack's start page; Plan Builder `fields.stop_reasons` builds no plan without written consent |
| Who gets no food targets on a Programme Block | A client who takes an appetite-lowering medicine or has disclosed a history of disordered eating: nobody checks in on that plan. Training only for them; food targets come with coaching (owner, October 2026) | FAQ, terms, `llms.txt`; Plan Builder `plan.build` gives a One-off plan no food targets for them |
| Refund | Full refund within the first 14 days of coaching. Programme Block: refundable until delivered, and a full refund within 14 days of getting it if the client is not happy (owner, October 2026) | Website pricing, FAQ, terms, `llms.txt` |
| Copies to attach | The New client pack in Drive holds PDF copies of the coaching terms and the privacy notice, for a client who should get them as attachments. The pages here are the master; each copy carries its page's "Last updated" date in its name | `dev/make_pack_copies.py` makes them; `dev/check_site.py` fails when a copy is older than its page |
| GLP-1 clients | Welcome. Higher protein target, a check that they are eating enough, prescriber stays in charge of the medicine | Homepage note under the prices, FAQ, GLP-1 guide; Plan Builder raises protein to 2.2 g/kg (`nutrition.APPETITE_MEDICINE_PROTEIN`); fat-loss calories never go under 1,200 kcal (women) or 1,500 kcal (men) (`nutrition.CALORIE_FLOOR`); the coach checks food at every check-in |

## Claims that must not come back

These were on the site and are wrong or unsupported. `dev/check_site.py` fails if they reappear.

- "No contracts" (there is a service agreement; say "no minimum term")
- "Most Popular" on a price card (no sales evidence for it)
- "25-39% of the weight lost is muscle" (the studies measured lean mass, not muscle)
- "Updated weekly" programming, "weekly or fortnightly check-ins"
- "Meal planning support" (no meal plans are provided)
- "MyFitnessPal connected to your workout data" (no such integration)
- "Quick daytime replies", "reply within a few hours", opening hours of 06:00 to 21:00 seven days
- "No sales pitch" for a call where a paid service is discussed
- "Core specialism" in GLP-1 support
- The invented testimonials from Sarah, Mike and Emma
- "No check-ins, messaging or nutrition plan" for the Programme Block (it includes the nutrition plan since October 2026)

## Testimonials

There are none on the site at the moment. The three that were there (Sarah, Mike and Emma) were
invented, which the Digital Markets, Competition and Consumers Act 2024 makes illegal, so they came
off in S32 and `dev/check_site.py` fails if those names come back.

A quote goes on the site only when all of these are true:

- They are the client's own words about their own experience. Never write a quote for someone,
  and never put a real client's name on words they did not say.
- The client gave written permission for that exact wording, with the date. Keep it where you can
  find it again.
- The quote's `<figure class="quote">` carries `data-permission="YYYY-MM-DD"`, the date of that
  permission, and `data-pilot="yes"` if the coaching was a free pilot, in which case the page says
  so. `dev/check_site.py` enforces both.
