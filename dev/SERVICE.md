# The service, in one place

This is what a client is promised. The website, the agreements and the Plan Builder must all say the
same thing. If the service changes, change it in all three places listed under each fact,
then run `python3 dev/check_site.py`.

The three layers:

- **Website** (this repository): the public promise, the coaching terms and the privacy notice.
- **Agreements and forms** (`Balazs Morvay Coaching/Business/New client pack`, on the coach's Mac):
  the coaching and Programme Block agreement templates, whose signed copy carries the client's
  written consent to keep their health information, and the massage health form and session
  record. The Google forms were retired on 12 November 2026.
- **Plan Builder** (the `Balazs Morvay Coaching` project, `planner/`): builds the plans and prints the dates,
  check-ins and instructions the client reads in their workbook.

| Fact | What it is | Where it is set |
|---|---|---|
| Business name | B. Morvay Coaching & Sports Massage (owner, 25 November 2026), the same as the Google Business Profile, so search engines see one business. Short forms: "B. Morvay" in some page titles, and "B. Morvay Coaching" only as the JSON-LD `alternateName`. Never "Balazs Morvay Coaching" or "Balazs Morvay Online Personal Training" (the old listing name) | Every page's header tagline, footer, titles, `og:site_name` and JSON-LD; terms, privacy notice, `llms.txt`, `dev/make_pack_copies.py`; the agreement templates and blank massage forms in the New client pack; the Google Business Profile |
| Where he's based | East Calder, just west of Edinburgh (owner, 25 November 2026). The garage gym (personal training only) is in East Calder. Massage happens only at the client's home, and home visits cover Edinburgh and West Lothian (owner, 25 November 2026). The street address appears only as the postal address in the terms (the law asks a trader to give one); the Google Business Profile hides it and lists service areas instead | Homepage About and booking, Edinburgh page, FAQ, online coaching page, terms, privacy notice, JSON-LD `address` (town only), `llms.txt` |
| Price of coaching | £200 a month, paid monthly in advance, no minimum term | Website pricing, FAQ, terms, `llms.txt`; the client's written agreement |
| Programme Block | £100 one-off, a 4 to 12 week training plan with the nutrition plan and the food help prompt (owner, October 2026), one round of changes within 14 days, no check-ins or messaging. The food targets are set for the whole block | Website pricing, FAQ, terms, `llms.txt`; Plan Builder: a One-off plan has no Check-ins tab and no check-in dates (`workbook.write_checkins`, `write_start`) |
| In-person session | £50 at the garage gym. £60 at the client's home gym, because the coach travels (owner, October 2026). No sessions at commercial gyms for now, so no renting space (owner, November 2026). Open to anyone | Homepage local line, Edinburgh page, FAQ, terms, `llms.txt` |
| Positioning | Since November 2026 the homepage leads with sports massage from a personal trainer in Edinburgh ("Sports massage from a personal trainer"): the first 60-minute massage visit first, with online coaching as the next step after a session. Balazs is a "sports massage therapist and personal trainer". Not a "strength coach" (owner, November 2026: not his title, and it could put off massage clients). Never "sports therapist": in the UK it suggests a sports therapy degree. "Sports therapy" as a service name carries the same risk, so it is not used (owner to confirm, November 2026) | Homepage, Edinburgh page, FAQ, terms, `llms.txt`; `dev/check_site.py` bans "sports therapist" |
| Qualifications | Name them, never "sports massage qualified". HNC Soft Tissue Therapy (SQA, July 2017, SCQF 7; units include Clinical Sports Massage and Sports Massage for Events and Special Populations). BSc (Hons) Physical Activity and Health, 2:1, Edinburgh Napier University (2020). CIMSPA Approved Entry Qualification, Personal Trainer Practitioner (2021): say "CIMSPA-recognised personal trainer", never "CIMSPA member" or "registered" (membership lapsed in 2022). He left HND Sports Therapy after year 1, so still never "sports therapist". "10+ years in the industry" is unconfirmed (owner to confirm, November 2026). Evidence: the Gmail label "Qualifications" | Homepage (hero, About, JSON-LD), online coaching, FAQ, Edinburgh page, `llms.txt`; `dev/check_site.py` |
| Sports massage | At the client's home only, anywhere in Edinburgh and West Lothian, travel included, with no travel surcharge (owner, 25 November 2026): 60 minutes £70, 45 minutes £60. Every first visit is the 60 minutes: a talk and movement check (about 10 minutes), about 40 minutes of massage, two or three exercises practised in the session (about 10 minutes), a one-page branded exercise plan sent to the client's phone the same evening by WhatsApp or email (the fill-in PDF `New client pack/Massage/3. Exercise plan (blank).pdf`: goal, today's marker, 2 or 3 exercises with weeks 1 and 2, weeks 3 and 4, how often and one cue; owner, 25 November 2026), and a check-in message a few days later. Return visits: a quick catch-up, more of the time on massage, exercises reviewed and the plan updated the same day; the 45 minutes is for return visits. No 30-minute option. Retired the same day: the 75-minute Massage and Plan (£85, £95 at home), the £65 60-minute massage, the £10 extra for home visits and massage at the garage gym | Homepage (hero, first visit, prices, questions, JSON-LD), FAQ, terms, Edinburgh page, online coaching local line, `llms.txt` |
| Request form | One form, the same on the homepage (Netlify form `booking`) and the online coaching page (`consultation`): what would you like (sports massage, personal training, online coaching, not sure yet); then, only when they apply, where to train (training only) and the area or postcode (any visit to the client's home); then when suits you, name, email, phone and anything else (owner, 25 November 2026: simple and clean, from the UI/UX books). `check_site` fails if the two forms' choices differ | `index.html`, `online-coaching.html`, `site.js`, privacy notice |
| Where the Programme Block is offered | After a massage visit and on the free coaching call, and in the homepage "after your session" section. No price card on the online coaching page since 25 November 2026, only one line, so it doesn't pull people away from monthly coaching | Homepage, online coaching page, FAQ, `llms.txt` |
| Massage booking order | Booking request on the homepage, with no health details. Reply within one working day with times. A booking confirmation by email or text (session, price, time, place, a link to the terms). At the start of the first visit, the client fills in the massage health form (a PDF, on the coach's phone or laptop), which carries their consent, their declaration and their signature. Paid per session, as agreed when booking; 24 hours' notice to move or cancel | Homepage book section, FAQ, terms sections 1, 2, 4 and 6, privacy notice; the blank form in `Business/New client pack/Massage` (owner, November 2026: blank forms, no Google Forms, no software) |
| Massage scope | No diagnosis. Refer to a physiotherapist or GP when something needs one. Contraindications are screened on the health form | Homepage session note and FAQ, FAQ page, terms section 4 |
| Massage records | The signed health form, a signed "no changes" line on its second page at each return visit (a new form after any change and once a year), and a short session record per visit, all as PDFs in `Clients/<Name>/` on the coach's encrypted Mac. A form filled on the phone is moved to the Mac the same day and deleted from the phone. Kept for 7 years after the last session, then deleted (check this matches the insurer's requirement) | Privacy notice; `Business/New client pack/Massage` |
| Home gym planning | Advice only, included with coaching or quoted by scope | Edinburgh page, FAQ, terms |
| Check-in rhythm | After the first week, then every two weeks, plus any time the client wants | Website pricing, FAQ, terms; Plan Builder `plan.checkin_dates`, printed on Start here and the Check-ins tab |
| Check-in questions | Training done, how hard it felt, food, energy, sleep, stress, health changes, weight, progress, questions | The Check-ins tab in the client's workbook (`workbook.CHECKIN_QUESTIONS`); the free printable check-in asks about the same things |
| Reply time, enquiries | One working day, for booking requests and coaching enquiries | Homepage booking section, online coaching consultation section, thanks page, terms |
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
- The 75-minute Massage and Plan, the £10 extra for massage home visits, and massage at the garage gym (retired 25 November 2026)
- "No sales pitch" for a call where a paid service is discussed
- "Core specialism" in GLP-1 support
- The invented testimonials from Sarah, Mike and Emma
- "No check-ins, messaging or nutrition plan" for the Programme Block (it includes the nutrition plan since October 2026)
- "Sports therapist" as a description of Balazs (he is a sports massage therapist; the title suggests a sports therapy degree)
- Massage that "flushes out toxins" or "lactic acid", or that treats, fixes or cures injuries

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
