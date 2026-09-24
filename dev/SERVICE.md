# The service, in one place

This is what a client is promised. The website, the Google forms and the programme builder must all
say the same thing. If the service changes, change it in all three places listed under each fact,
then run `python3 dev/check_site.py`.

The three layers:

- **Website** (this repository): the public promise, the coaching terms and the privacy notice.
- **Google layer** (Apps Script project "Program Builder Forms"): the intake, check-in and block
  review forms. The intake links to the website's terms and privacy notice through the script
  properties `TERMS_URL` and `PRIVACY_NOTICE_URL`, so there is only ever one copy of each document.
- **Programme builder** (`RP Hypertrophy` repository): builds the plans and prints the dates and
  instructions the client reads in their workbook.

| Fact | What it is | Where it is set |
|---|---|---|
| Price of coaching | £200 a month, paid monthly in advance, no minimum term | Website pricing, FAQ, terms, `llms.txt`; the client's written agreement |
| Programme Block | £100 one-off, a 4 to 12 week plan, one round of changes within 14 days, no check-ins or nutrition plan | Website pricing, FAQ, terms; builder sets `spec["checkins"] = False` |
| In-person session | £60, at the client's home gym, the garage gym, or a gym that allows visiting trainers. Open to anyone | Edinburgh page, FAQ, terms |
| Sports massage | £50 for 45 minutes, Edinburgh and nearby, subject to availability | Edinburgh page, FAQ, terms |
| Home gym planning | Advice only, included with coaching or quoted by scope | Edinburgh page, FAQ, terms |
| Check-in rhythm | After the first week, then every two weeks, plus any time the client wants | Website pricing, FAQ, terms; builder `checkin_dates` prints the dates in the Read Me; Google Check-in form |
| Check-in questions | Training done, how hard it felt, food, energy, sleep, stress, health changes, weight, progress, questions | Google Check-in form (`weekly_checkin.fields`); the free printable check-in mirrors it |
| Reply time, enquiries | One working day | Homepage consultation section, thanks page, terms |
| Reply time, clients | Two working days, Monday to Friday | Website pricing, FAQ, terms; the client's agreement |
| Video feedback | Feedback on videos of the client's lifts, up to 2 a week | Website pricing, FAQ, terms, `llms.txt`; the client's agreement |
| Messaging | WhatsApp, iMessage or email | Website pricing, FAQ, terms, privacy notice |
| Nutrition scope | Calorie and protein targets, a meal pattern and rules for adjusting. No meal plans. Client logs food in their own app or uses hand portions | Website pricing, FAQ, terms; builder `nutrition_lib` |
| Food help prompt | Coaching clients get a ready-written prompt in their workbook to paste into an AI chat, which estimates what they eat and counts it against their targets. A convenience, not coaching advice, and not given to a client who has told us about a history of disordered eating | Website FAQ; builder `FOOD_HELP_SHEET`, withheld by `health_filters` |
| Training log | ONE Google Sheet per training block, opened on the phone; weight x reps; Last week column; Substitute list. Coaching clients' calorie targets and weigh-ins are tabs in the same sheet, so there is one file to open | Website FAQ and how it works; builder week tabs, `render_program` |
| Block review | At the end of each block, the next block is built from it | Website how it works, FAQ; Google End-of-Block Review form |
| Age | Adults 18 or over | Website FAQ and terms; Google intake (`core/age` validation and `validate_submission`) |
| Refund | Full refund within the first 14 days of coaching; Programme Block refundable until delivered | Website pricing, FAQ, terms |
| GLP-1 clients | Welcome. Higher protein target, a check that they are eating enough, prescriber stays in charge of the medicine | Homepage band, FAQ, GLP-1 guide; builder raises the protein floor and adds an under-eating check for appetite medication |

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
