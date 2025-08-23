# Agri AI Django Backend

This backend replaces the three Supabase Edge Functions used in your Vite+React+Capacitor app:

- `POST /api/v1/ai-diagnosis`
- `POST /api/v1/farming-advice`
- `POST /api/v1/market-analysis`

## Quickstart

```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

Test with curl (replace API key as needed):

```bash
curl -X POST http://localhost:8000/api/v1/ai-diagnosis \
  -H "Authorization: Bearer dev-key-123" -H "Content-Type: application/json" \
  -d '{{"cropType":"maize","symptoms":"yellow leaves, brown spots"}}'
```

Open API docs: http://localhost:8000/api/docs/

## Hook up the Frontend

Replace the Supabase URLs in your `Documentation.tsx` examples (and anywhere else) with your Django URL:

```ts
const API_BASE = import.meta.env.VITE_API_BASE ?? "http://localhost:8000/api/v1";

fetch(`${API_BASE}/ai-diagnosis`, {{ method: "POST", headers: {{
  "Authorization": "Bearer YOUR_API_KEY",
  "Content-Type": "application/json"
}}, body: JSON.stringify({{ cropType, symptoms }}) }})
```

## Production Notes

- Set `DEBUG=false` and a strong `DJANGO_SECRET_KEY`.
- Configure Postgres by setting `DB_ENGINE=django.db.backends.postgresql` and DB_* env vars.
- Set `CORS_ALLOW_ALL=false` and `CORS_ALLOWED_ORIGINS` to your web/app origins.
- Rotate and store API keys securely (consider a DB-backed API key model).

## Extending with Real AI

The placeholder heuristics live in `ai/services.py`. Swap these with calls to your LLM or model.
For example, using OpenAI:

```py
import os
from openai import OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def diagnose(crop_type, symptoms):
    prompt = f"Diagnose {crop_type} issue given symptoms: {symptoms} ..."
    # call client.chat.completions.create(...)
    ...
```


## JWT Auth (SimpleJWT)

Auth endpoints (under `/api/v1/auth/`):
- `POST /token` → obtain access & refresh
- `POST /token/refresh` → rotate refresh, returns new access/refresh
- `POST /token/verify` → verify a token
- `POST /token/blacklist` → revoke a refresh token (requires `refresh` in body)
- `POST /register` → create a user with a role (FARMER/AGRONOMIST/TRADER/ADMIN)
- `GET /me` → current user info


## Email verification & password reset
- `POST /api/v1/auth/request-email-verification` → send verify email
- `POST /api/v1/auth/verify-email` `{ uid, token }` → activate user
- `POST /api/v1/auth/password-reset` `{ email }`
- `POST /api/v1/auth/password-reset-confirm` `{ uid, token, new_password }`

By default, emails print to console. Configure SMTP via `.env`.

## Seed users
```bash
python manage.py seed_users
# Users: admin/Admin123!, agro/Agro123!, trader/Trader123!, farmer/Farmer123!
```

## Local ML model
Diagnosis now uses a tiny scikit-learn Naive Bayes model (no external APIs). See `ai/services.py`.

## Rate limiting & audit logs
- Rate limit: 20/min on sync endpoints, 10/min on job creation
- Audit logs stored in `api_requestlog` table (request+response truncated)

## Celery jobs
Start Redis and a worker:
```bash
docker compose up -d redis
celery -A core worker -l info
```
Async endpoints:
- `POST /api/v1/jobs/ai-diagnosis` → `{ task_id }`
- `GET /api/v1/jobs/<task_id>` → `{ state, result|info }`
```)


## Extras implemented: Magic link, Channels, Transformer integration, Per-role rate limits, Admin audit API, Frontend helpers

### Magic link
- `POST /api/v1/auth/magic-link-request` `{ email }`
- `POST /api/v1/auth/magic-link-verify` `{ token }` -> returns tokens on success
- Templates in `templates/emails/*`

### WebSocket task progress
- WebSocket path: `ws://<host>/ws/tasks/<task_id>/`
- Consumer polls Celery AsyncResult and streams updates.

### Transformer model
- `ai/transformer_model.py` will load a HF model (e.g. `distilbert-base-uncased-finetuned-sst-2-english`) if available.
- Fallback to sklearn pipeline if transformer unavailable.

### Per-role rate limits
- Implemented a simple cache-based decorator `api/role_ratelimit.py` and ADMIN audit API at `/api/v1/admin/audit-logs`.

### Frontend helpers
- `src/services/auth.ts` for JWT + magic link flows
- `src/hooks/useTask.tsx` WebSocket task progress hook

1. Introduction
This Software Requirements Specification (SRS) outlines the comprehensive requirements for
the Mlimi App, a mobile application designed to serve smallholder farmers in Malawi. The
document details the system's purpose, scope, functional and non-functional requirements, architectural overview, and project plan, providing a foundational blueprint for its development. The Mlimi App aims to address critical information gaps and empower farmers through digital
tools, ultimately contributing to enhanced agricultural productivity and economic resilienceinthe region. 1.1. Project Overview
The Mlimi App is conceptualized as a mobile application to support smallholder farmers inMalawi, functioning as a digital assistant for various farming activities.1 Its primary purposeistocentralize crucial agricultural information and services, which are currently fragmented anddifficult for farmers to access.1 The application's core functionalities include an advertisingplatform for agricultural products, real-time market price updates, weather forecasting withalerts, pest detection capabilities via an external API, and the dissemination of expert farming advicethrough newsletters and community forums.1
The primary beneficiaries of the Mlimi App are smallholder farmers and agricultural advisors
within Malawi.1 These individuals constitute the core system end-users, with the applicationtailored to their specific needs and operational contexts. The agricultural landscape in Malawi
heavily relies on smallholder farming, making timely and accurate information access a
significant factor in improving livelihoods and food security. The app is envisioned to playapivotal role in modernizing farming practices and fostering a more informed agricultural
community. 1.2. Problem Statement and Justification
Smallholder farmers in Malawi face a significant challenge due to the critical lack of centralizedand timely access to essential farming information.1 This includes vital data such as current
market prices for their produce, up-to-date weather forecasts, and reliable support for pest anddisease management.1 The current operational environment sees farmers relying on disparate,
pg. 5
often unreliable sources like radio broadcasts, word-of-mouth, and time-consuming physical
market visits to gather information.1 This fragmented approach leads to reduced farmproductivity, increased financial insecurity, and a diminished capacity to adapt effectivelytounpredictable climate patterns and market fluctuations.1 The absence of a comprehensive digital
system that simultaneously addresses these critical needs leaves farmers vulnerable to sub- optimal decision-making and missed opportunities. The Mlimi App is proposed as a direct solution to these pervasive challenges, offering a unifieddigital platform for essential agricultural data and support.1 By centralizing information anddelivering it directly to farmers' mobile devices, the application aims to significantly improvefarm productivity, increase farmers' incomes, and enhance their resilience to both climate andmarket challenges.1 The socio-economic benefits are substantial, as empowering farmers withtimely and accurate information can lead to better crop management, optimized selling strategies, and proactive responses to environmental threats, thereby contributing directly to the livelihoodsof Malawian farmers and the broader agricultural economy. The reliance on radio and word-of-mouth points to a deeper challenge: the digital divide andaccessibility issues prevalent among smallholder farmers in Malawi.1 While the Mlimi Appis amobile application and targets users with "basic smartphone usage ability"
1
, the underlyingconcern extends beyond mere device ownership. It encompasses data costs, the availabilityandreliability of network infrastructure, particularly in rural areas, and digital literacy levels that gobeyond fundamental smartphone operation. This necessitates that the app's design is
exceptionally intuitive, highly data-efficient, and incorporates robust offline capabilities. Suchdesign considerations are paramount to effectively bridge the existing digital divide and ensureequitable access to the app's benefits. Furthermore, the project's stated exclusion of "Full nationwide deployment without external
funding" for the initial scope
1 highlights a critical long-term consideration for the Mlimi App'sviability. While this constraint applies to the initial development phase, it underscores the needfor a strategic approach to sustainability and scalability. The app's ultimate success in achievingits objectives of improving productivity, income, and resilience is contingent upon its widespreadadoption. This implies that, even at the SRS stage, the project must implicitly acknowledge thenecessity of a clear strategy for securing future funding, forging partnerships with relevant non- governmental organizations, government bodies, or telecommunication providers, and
developing a phased rollout plan. Such a strategy would address the financial and logistical
hurdles inherent in scaling a digital solution within a developing country context, ensuringtheproject's continued impact beyond its initial deployment. 1.3. Project Scope
pg. 6
The Mlimi App's development project encompasses a defined set of functionalities and
limitations to ensure focused and achievable outcomes. The inclusions represent the core featuresthat will be developed and delivered as part of this project.1 These include an advertisingplatform that allows users to post their agricultural products with photos, descriptions, andprices, facilitating direct farmer-to-buyer connections.1 The system will also provide real-time market
price updates, aggregating data from various markets to display the best offers available tofarmers.1 Weather forecast integration is a key inclusion, delivering daily forecasts and pushnotifications for critical weather alerts.1 A pest detection feature, utilizing an external API, will
enable farmers to upload crop images for diagnosis and receive advice.1 The app will alsodeliverperiodic farming newsletters containing tips and market trends, and incorporate a communityforum for farmers to interact, post questions, and share advice.1 Crucially, the applicationwill
feature a multilingual mobile interface, supporting English and Chichewa at a minimum, andallow offline access to critical information such as saved weather data, market prices, andpest
information.1
Conversely, the project explicitly defines exclusions to manage expectations and prevent scopecreep. These include the physical setup of marketplaces, integration with government regulatorysystems, and full nationwide deployment without securing external funding.1 These exclusionsdelineate the boundaries of the initial development effort, focusing resources on the core digital
assistant functionalities. The project aims to transform current operations, where smallholder farmers predominantlyrelyon traditional, often inefficient methods like radio, word-of-mouth, and scattered market visitsfor information.1 There is currently no centralized digital system that simultaneously serves all
critical needs of these farmers.1 Post-deployment, the Mlimi App is envisioned to revolutionizethis landscape, enabling farmers to access comprehensive agricultural support directly ontheir
mobile devices, thereby fostering a more informed and empowered agricultural community.1
The inclusion of "Offline access to critical information"
1
is a fundamental requirement for thetarget user base in Malawi, where internet connectivity can be unreliable or costly. This featureis not merely an add-on; it dictates a core architectural decision. It necessitates a robust local
database, such as SQLite, which is mentioned as a potential storage solution.1 Furthermore, it
requires the implementation of efficient data synchronization mechanisms to ensure that cacheddata is updated promptly whenever an internet connection becomes available. The designmust
also clearly communicate to users the freshness of the data, indicating when information was last
updated. This capability is vital for ensuring the app remains useful even in areas with limitedor
no connectivity, directly supporting its accessibility mandate. The requirement for a "Multilingual mobile interface (English and Chichewa at minimum)"
1
represents more than just a translation effort; it is a strategic decision that profoundly impacts the
pg. 7
app's potential for adoption and usability among smallholder farmers. Many in the target
demographic may not be proficient in English, making local language support essential for
effective communication and comprehension. This strategic choice directly enhances the app'sreach and its effectiveness in addressing the core problem of information access. It also impliesaneed for meticulous translation and cultural adaptation, not only of text but potentially of visual
elements and examples used in advice or newsletters, to ensure relevance and clarity. This alsolays the groundwork for future scalability to other regional languages within Malawi, shouldtheproject expand. 1.4. System Personnel
The success of the Mlimi App project is contingent on the clear definition and collaborationof
various personnel roles. The system end-users are primarily smallholder farmers, who will
interact with the app's core functionalities, and agricultural advisors, who may utilize features
like the community forum to provide expert guidance.1
The project team responsible for the app's development and management consists of a Developer, who will handle the technical implementation and coding; a Project Manager, tasked withoverseeing project execution, timelines, and resource allocation; and a UI/UX Designer, crucial
for ensuring a user-friendly and intuitive interface.1 The overall ownership of the project rests
with Mphatso Soko and the broader Project Stakeholder Team, who are responsible for definingthe project vision, allocating necessary resources, and making key strategic decisions.1
The identification of "smallholder farmers" with "basic smartphone usage ability"
1 as the
primary end-users profoundly shapes the user interface and user experience (UI/UX) design. Theinclusion of a dedicated "UI/UX Designer" on the project team 1
is therefore not just a standardpractice but a critical necessity. This implies that the design process must prioritize extremesimplicity, heavy reliance on visual cues, intuitive icon-based navigation, and a minimal useof
text, especially considering the multilingual requirement. While "short tutorials and onboardingguides"
1 are planned, the fundamental design must inherently minimize the need for extensivetraining, allowing users to quickly grasp and utilize the app's features with minimal friction. Thisdirect causal link between the user demographic and the design philosophy is paramount for
achieving high user adoption and satisfaction. 1.5. System Overview and Architecture
pg. 8
The Mlimi App is designed with a modular architecture to ensure flexibility, scalability, andeaseof maintenance.1 The high-level architecture comprises several key components workinginconcert. The
Mobile Front-end will be developed using Ionic, a cross-platform framework that allows for asingle codebase to be deployed across multiple mobile operating systems, with Android APKbeing the initial deliverable.1 This choice facilitates rapid development and broad accessibilityfor the target user base. The
Django REST API Backend will serve as the robust and scalable server-side framework, handling business logic, data processing, and communication with the front-end via RESTful
API calls.1
The system relies heavily on Integration with external APIs to provide specialized
functionalities without requiring the development of these complex systems fromscratch. Specifically, the OpenWeatherMap API will be utilized for fetching real-time weather data, and the PlantVillage Nuru API will power the AI-driven pest detection feature.1 These
integrations are crucial for extending the app's capabilities and delivering value-added servicestofarmers. For
Database Storage, the project considers either SQLite or Firebase.1 SQLite is well-suitedfor
local, offline data storage on the mobile device, supporting the app's offline access requirement. Firebase, a cloud-based platform, offers capabilities for real-time data synchronization, cloudstorage, and user authentication, which could be leveraged for backend data persistence or
specific features requiring real-time updates. The final choice or combination of these databasesolutions will be critical in balancing offline capability with backend data management. The system's structural relationships are further clarified through diagrams. A Use Case
Diagram (Figure 1) illustrates the interactions between various actors, such as farmers, agricultural advisors, and external APIs, and the system's core functionalities.1 This diagramprovides a high-level view of how users will interact with the system to achieve their goals.
Figure 1
Context Diagram (Figure 2) depicts the Mlimi App as a central system and its interactions withexternal entities, including human users (farmers) and external systems like OpenWeatherMapand PlantVillage Nuru.1 This diagram clearly delineates the system's boundaries and its
interfaces with the outside world.
pg. 9
Figure 2
The architectural components—Ionic, Django, OpenWeatherMap, PlantVillage Nuru, andthechosen database—form an intricately interconnected system.1 The mobile front-end built withIonic is entirely dependent on the Django backend API for data retrieval and submission. Inturn, the Django backend relies on the external APIs, OpenWeatherMap and PlantVillage Nuru, toprovide core functionalities like weather forecasting and pest detection. The selection andimplementation of the database solution directly influence both the front-end's ability to support
offline data access and the backend's capacity for persistent data storage. This intricate webof
dependencies necessitates careful design considerations for data flow, robust error handlingmechanisms across all layers, and a comprehensive security strategy to protect data in transit andat rest. The app's core value proposition, which includes real-time market prices, weather alerts, andpest
detection, is heavily reliant on the reliability and data quality of external APIs.1 If these third- party services experience downtime or provide inaccurate data, the utility and credibility of theMlimi App could be severely compromised. This reliance underscores the importance of
implementing robust error handling within the app, such as displaying informative messages tousers when an external service is unavailable. Furthermore, fallback mechanisms, such as
displaying the last known good data with a timestamp, could mitigate the impact of API failures. It is also crucial to thoroughly understand the terms of service, rate limits, and service level
agreements of these external APIs to ensure sustainable and compliant integration. 2. Functional Requirements
pg. 10
This section details the specific functions the Mlimi App must perform to meet the needs of itsusers. Each requirement is described comprehensively, outlining what the systemis designedtodo. 2.1. User Management and Authentication
The system shall allow users to register and log in securely. Farmers and agricultural advisors
will be able to create unique accounts, log in using their credentials (e.g., phone number or email
and password), and manage their profiles. This includes essential functionalities such as
password reset options. This capability is fundamental for enabling personalized experiences, ensuring data security (as outlined in Requirement 14), and facilitating core features like
advertising products (Requirement 1), participating in community forums (Requirement 6), andreceiving targeted newsletters (Requirement 5).1
Given the target audience of smallholder farmers in Malawi, many of whommay have limitedliteracy or consistent access to email, traditional email/password registration methods couldpresent a significant barrier to adoption. Consequently, exploring alternative authenticationmethods, such as phone number-based registration with One-Time Passwords (OTPs) deliveredvia SMS, could significantly enhance accessibility and user-friendliness. This choice carries
implications for backend security protocols and necessitates potential integration with SMSgateway services. The SRS acknowledges the importance of considering such nuances tooptimize usability for the specific user base. Furthermore, user registration and profile management inherently involve the collection of
personal data. In light of the non-functional requirement to "secure user data"
1
, this extends
beyond mere technical security measures to encompass broader data privacy considerations andexplicit user consent. The project must ensure the implementation of a clear privacy policythat
transparently outlines what data is collected, how it is used, and how it is protected. Mechanismsfor users to understand and consent to data collection, particularly for sensitive informationlikelocation data (for weather and market prices) or crop photos (for pest detection), are crucial for
building trust and ensuring ethical data handling practices. 2.2. Product Advertising and Listing
The system shall allow farmers to advertise agricultural products.1 Users will be able to post
detailed listings for their agricultural produce, including the product name and type (e.g., Maize,
pg. 11
Tomatoes, Livestock). Each listing will support a comprehensive description of the product, specifying quantity, quality, and harvest date. The platform will enable the upload of multiplephotos of the product to provide visual context for potential buyers. Farmers will also be abletospecify an asking price, either per unit or total, and provide contact information, such as a phonenumber, or utilize an in-app messaging feature for buyer communication. The location of theproduct or farm will also be a key piece of information in the listing. An acceptance criterionfor
this feature is that a farmer can successfully post a product listing with all required fields, andthis listing becomes searchable and viewable by other users within the application. 2.3. Market Price Aggregation and Display
The system shall display current market prices.1 The application will aggregate real-time or near
real-time market prices for various agricultural commodities from different local markets acrossMalawi. This data will be presented in a clear and easily digestible format, highlighting "best
offers" such as the highest buying prices or lowest selling prices. Users will have the abilitytofilter this information by product type, specific market location, and date to refine their search. An acceptance criterion for this feature is that users can view a comprehensive list of current
market prices for selected agricultural products, apply filters by market, and clearly identifyhighlighted best offers. The requirement to "aggregate prices from different markets"
1 presents a significant data
sourcing and verification challenge. The reliability and freshness of this market price data areparamount to its utility for farmers. This implies the necessity of a robust data ingestion strategy. This could involve manual input from designated market agents, automated data scrapingfrompublicly available sources, or integration with existing agricultural data platforms if suchinfrastructure exists in Malawi. Furthermore, the system will need to incorporate validationmechanisms to ensure data accuracy and potentially include a feedback loop for users to report
any discrepancies, thereby maintaining the integrity and trustworthiness of the market
information. Providing "real-time market price updates"
1 directly addresses the issue of "financial insecurity"highlighted in the problem statement. This feature carries profound economic implications, as it
empowers farmers with critical information parity. By having access to current market prices, farmers are less susceptible to exploitation by middlemen and can negotiate more effectivelyfor
their produce, potentially leading to increased bargaining power and higher incomes. This
improved access to market intelligence could also contribute to greater efficiency within
Malawi's agricultural markets, potentially reducing post-harvest losses that often occur due toalack of market access or timely information.
pg. 12
2.4. Weather Forecasting and Alerts
The system shall provide real-time weather updates.1 The Mlimi App will fetch and displaydailyweather forecasts, including key parameters such as temperature, precipitation levels, andwindspeed, specifically tailored to the user's registered location. In addition to daily forecasts, thesystem will deliver push notifications for critical weather alerts, such as warnings for heavyrainfall, impending droughts, or strong winds, which could significantly impact farming
activities.1 An acceptance criterion for this feature is that users consistently receive daily weatherforecasts relevant to their registered location, and critical weather alerts are delivered promptlyvia push notifications. The provision of weather forecasts "relevant to the user's location"
1 necessitates accurate
geolocation capabilities, leveraging technologies such as GPS or network-based locationservices. This raises important considerations regarding user privacy, requiring explicit consent fromusersto access their location data. The application must transparently communicate howlocationdatais utilized and the measures taken to protect this sensitive information, building user trust. Timely weather alerts
1 are a crucial component for enhancing "resilience to climate... challenges".1 This functionality enables farmers to make informed and proactive decisions
regarding their agricultural practices, such as optimizing planting schedules, planning irrigation, determining optimal harvesting times, and implementing preventative measures against climaterelated risks. This transforms the weather reporting feature from a simple informational tool intoa strategic asset for proactive agricultural planning and climate change adaptation, directlycontributing to improved crop yields and reduced climate-induced losses. 2.5. Pest Detection and Advice
The system shall detect pests via an API.1 Farmers will be able to upload images of their crops, such as leaves or stems, to the application. The system will then utilize the PlantVillage NuruAPI to analyze these images and provide a diagnosis of potential pests or diseases affectingtheplants.1 Alongside the diagnosis, the app will offer recommended treatment or management
advice relevant to the identified issue. An acceptance criterion for this feature is that a user cansuccessfully upload a crop image, and the system delivers a pest diagnosis and relevant advicewithin the specified non-functional requirement of less than 30 seconds.1
The accuracy of "pest diagnosis"
1
is heavily dependent on the quality of the uploaded images.
pg. 13
Smallholder farmers, who may have "basic smartphone usage ability"
1
, might not be familiar
with the optimal techniques for capturing diagnostic photos (e.g., appropriate lighting, focus, angle, or specific plant parts to photograph). This implies a critical need for clear, in-app
guidance and visual examples on how to take effective images. Without such guidance, poor
image quality could lead to inaccurate diagnoses, which would severely erode user trust anddiminish the utility of this feature. Providing "recommended treatment or management advice" based on an external API
1 carriessignificant implications, particularly concerning the accuracy and appropriateness of the advice. There is a potential risk that an incorrect diagnosis or unsuitable advice for the local context or
specific crop variety could lead to crop loss or the misuse of agricultural inputs like pesticides. This underscores the need for clear disclaimers within the application regarding the nature of theAI-powered advice. Furthermore, implementing a feedback mechanism for users to report
incorrect diagnoses or ineffective advice would be beneficial. Consideration might also be givento incorporating human oversight or validation for critical advice, especially concerning pesticideuse, to ensure responsible and safe agricultural practices. This aspect touches upon the ethical
deployment of AI in agriculture and potential liabilities arising from its recommendations. 2.6. Farming Newsletters and Content Delivery
The system shall deliver newsletters.1 Periodic newsletters, containing valuable farming tips, best
practices, current market trends, and seasonal agricultural advice, will be delivered directlywithin the application. Users should have the ability to browse an archive of past newsletters andsave particularly important ones for offline access, ensuring continuous learning and referenceeven without an active internet connection. An acceptance criterion for this feature is that usersconsistently receive periodic newsletters, and they can easily access and reviewan archive of all
previous editions within the app. The provision of "periodic newsletters containing farming tips and market trends"
1 necessitatesarobust content management system (CMS) and a dedicated process for content creation andcuration. The credibility and relevance of this content are paramount for user engagement andtrust. This raises the question of content sourcing: Will the expert advice come fromthe
agricultural advisors identified as system end-users
1
, from local research institutions, or fromofficial government bodies like the Malawi Ministry of Agriculture (which is referenced intheproject documentation)?
1 Ensuring that the content is locally relevant, accurate, and actionableiscrucial for the success of this feature. Newsletters serve as a powerful medium for knowledge dissemination. By providing "expert
farming advice"
1
, the Mlimi App directly contributes to capacity building among smallholder
pg. 14
farmers. This educational component can lead to the adoption of improved farming practices, theintegration of new agricultural techniques, and ultimately, higher crop yields. This directlysupports the project's overarching goal of "increasing productivity".1 The feature transcends
simple information delivery, evolving into a tool for continuous agricultural education andempowerment. 2.7. Community Forum Interaction
The system shall allow community interaction.1 Users will be able to post questions, share advice, discuss common farming challenges, and interact with other smallholder farmers and agricultural
advisors within a dedicated forum section of the application. The forum functionality will
include features such as topic creation, the ability to reply to posts, and mechanisms for showingappreciation (e.g., likes or upvotes). Consideration will also be given to supporting image andvideo sharing within posts to enhance communication. An acceptance criterion for this featureisthat users can successfully create new forum posts, reply to existing discussions, and viewthefull threads of conversations. A community forum 1 requires robust moderation to maintain its value and prevent the spreadof
misinformation, spam, or inappropriate content. This implies the necessity of implementingeffective moderation tools, which could be manual (requiring human moderators) or potentiallyassisted by artificial intelligence. Clear community guidelines must be established and enforcedto ensure a constructive and supportive environment. Without effective moderation, the forumcould quickly become unusable or even detrimental, undermining its intended purpose as a
source of "expert farming advice"
1 and reliable peer support. The community forum's ability to facilitate "farmers' interaction"
1 extends beyond simple
information exchange. It fosters peer-to-peer learning, enabling farmers to share practical
experiences, discuss localized solutions, and collectively address common challenges. This
interaction also contributes to the building of social capital within the farming community, creating a supportive network. Such a network allows farmers to learn fromeach other's
successes and failures, adapt best practices to their specific local contexts, and collectivelyenhance their resilience and problem-solving capabilities in the face of agricultural uncertainties. 2.8. Multilingual Support
The system shall support multilingual interfaces.1 The application's entire user interface,
pg. 15
including all menus, buttons, labels, and static content, will be available in at least two languages:
English and Chichewa. Users will have the ability to easily switch between the supportedlanguages at any point within the application. An acceptance criterion for this feature is that all
user interface elements are correctly translated and displayed accurately in both English andChichewa, and the language switching functionality operates seamlessly without errors or delays. 2.9. Offline Access Capabilities
The system shall allow offline access to critical data.1 Key information, such as previouslysavedweather forecasts, cached market prices, and results from prior pest diagnoses along withtheir
associated advice, will remain accessible to users even when their device lacks an active internet
connection. The application will clearly indicate the timestamp of when the data was last updated, providing transparency regarding data freshness. An acceptance criterion for this feature is that
users can access saved weather information, market prices, and pest diagnosis data whentheir
device is offline, and the application clearly displays the last update time for this cached data. Functional Requirements Traceability Matrix
The following table provides a detailed traceability matrix for the functional requirements, linking them to their origins, priorities, verification methods, and related use cases. This matrixserves as a critical tool for ensuring that all specified functionalities are addressed throughout thedevelopment lifecycle and are adequately tested. Req. ID Require
ment
Descrip
tion
Source Priority Status Verifica
tion
Method
RelatedUse
Cases
FR-001 User
Registra
tion &
Login
Users
can
create
account
s, log
in, and
Implicit
from 1
(Req 1, 5, 6, 14)
Must- Have
Propose
d
User
Accepta
nce
Testing, Security
Register
Account, LogIn, Manage
pg. 16
manage
profiles
securely
. Testing ProfileFR-002 The
system
shall
allow
farmers
to
advertis
e
product
s
Users
can post
their
agricult
ural
product
s with
photos, descript
ions, and
prices.
1 (Req
1)
Must- Have
Propose
d
User
Accepta
nce
Testing, SystemTesting
Post
Product
Listing, ViewProduct
ListingFR-003 The
system
shall
display
current
market
prices
Aggreg
ates
prices
from
differen
t
markets
and
shows
the best
offers.
1 (Req
2)
Must- Have
Propose
d
SystemTesting, Data
Validati
on
ViewMarket
Prices, Filter
Market
Prices
FR-004 The
system
shall
provide
realtime
weather
updates
Weathe
r
forecast
s are
fetched
and
displaye
d daily
1 (Req
3)
Must- Have
Propose
d
SystemTesting, Push
Notifica
tion
Testing
Get
Weather
Forecas
t,ReceiveWeather Alert
pg. 17
with
alerts. FR-005 The
system
shall
detect
pests
via an
API
Farmers
can
upload
images
of crops
and get
pest
diagnos
is.
1 (Req
4)
Must- Have
Propose
d
SystemTesting, API
Testing
UploadCropImage, Get Pest
Diagnos
is
FR-006 The
system
shall
deliver
newslett
ers
Periodic
newslett
ers
containi
ng
farming
tips and
market
trends
will be
sent.
1 (Req
5)
Should- Have
Propose
d
User
Accepta
nce
Testing, Content
ReviewReadNewslet
ter, BrowseNewslet
ter
ArchiveFR-007 The
system
shall
allow
commu
nity
interacti
on
Users
can post
questio
ns and
share
advice
in
forums.
1 (Req
6)
Should- Have
Propose
d
User
Accepta
nce
Testing, SystemTesting
Post
ForumQuestion, Replyto
ForumPost
FR-008 The
system
shall
Availab
le in
English
1 (Req
7)
Must- Have
Propose
d
Localiz
ation
Testing, SwitchLanguage
pg. 18
support
multilin
gual
interfac
es
and
Chiche
wa at
minimu
m. User
Accepta
nce
Testing
FR-009 The
system
shall
allow
offline
access
to
critical
data
Users
can
access
saved
weather
, price, and pest
info
when
offline.
1 (Req
8)
Must- Have
Propose
d
Offline
Testing, Data
Synchro
nization
Testing
Access
OfflineData
3. External Interface Requirements
This section details how the Mlimi App will interact with various external systems, hardwarecomponents, software applications, and communication protocols. Defining these interfaces iscrucial for ensuring seamless integration and proper system functionality. 3.1. User Interfaces
The user interface (UI) of the Mlimi App will be a mobile application, meticulously designedtocater to its target audience. A paramount consideration is intuitive design, emphasizing
simplicity, clear navigation, and abundant visual cues. This design philosophy is critical giventhat the target users possess "basic smartphone usage ability".1 The interface must facilitate easeof use without requiring extensive technical proficiency. Multilingual support is another key aspect, with all UI elements, including menus, buttons, labels, and static content, dynamically switching between English and Chichewa.1 This ensuresaccessibility and comprehension across the diverse linguistic landscape of Malawi.
pg. 19
Accessibility considerations will extend to users with varying levels of literacy or potential
visual impairments, incorporating features like large fonts, high contrast themes, and clear
iconography. The UI must also exhibit responsiveness, adapting seamlessly to various Androiddevice screen sizes and resolutions to provide a consistent experience across different devices. Furthermore, robust feedback mechanisms will be integrated, providing clear visual andhapticresponses to user actions, such as successful uploads or error messages. Finally, comprehensiveonboarding and tutorials will be provided directly within the app to guide newusers throughits functionalities.1
Given the target audience and the critical multilingual support 1
, it is insufficient to merelytranslate the user interface. The UI/UX design must undergo rigorous testing with actual
smallholder farmers in Malawi. This localized testing is essential to ensure cultural
appropriateness, ease of understanding, and overall usability within the specific context of theend-users. This implies that the "pilot tests with farmers"
1 are not only vital for validatingtheapp's overall functionality but are particularly critical for validating and refining the UI/UXdesign based on real-world farmer feedback. The non-functional requirement for the "homepage to load within 5 seconds on slownetworks"1
has direct implications for UI responsiveness. This constraint mandates that the UI designprioritizes the rapid display of critical information, even if other elements load progressively. This may involve the use of skeleton screens, lazy loading techniques, and highly efficient dataserialization to ensure a perceived responsive experience despite challenging network conditions. Additionally, the UI should clearly indicate loading states to manage user expectations andprevent frustration during data retrieval. 3.2. Hardware Interfaces
The Mlimi App will leverage specific hardware capabilities of mobile devices to deliver its
functionalities. The device's camera is a mandatory requirement for the pest detection feature, enabling farmers to upload images of their crops for analysis.1
GPS and location services are essential for providing accurate weather forecasts relevant totheuser's geographical position.1 While the app supports offline access, consistent
internet connectivity (via cellular data or Wi-Fi) is necessary for real-time updates, initial datasynchronization, and all API interactions.1 The application will also require
sufficient local storage on the device for installation and for caching critical data to support
offline access. Finally, minimum processor and RAM specifications will be defined to ensure
pg. 20
smooth application performance and responsiveness. 3.3. Software Interfaces
The Mlimi App will integrate with several external software systems to extend its capabilities. These integrations are critical for delivering specialized functionalities without developingthemin-house. The OpenWeatherMap API is a primary integration point.1 Its purpose is to fetch real-timeweather data, including temperature, precipitation, humidity, and wind speed, along withmulti- day forecasts. The integration will be performed via RESTful API calls originating fromtheDjango backend. Authentication will rely on API keys, which must be managed with strict
confidentiality to ensure security.1 Robust error handling mechanisms will be implementedtogracefully manage scenarios such as API downtime or exceeding rate limits. The PlantVillage Nuru API is another crucial integration, dedicated to pest detection throughimage analysis.1 This interface will handle the upload of crop images and return diagnosis results, including the type of pest or disease, a confidence score, and recommended advice. Similar toOpenWeatherMap, integration will be via RESTful API calls from the Django backend, withAPI key confidentiality being paramount.1 A key performance requirement for this integrationisthat pest diagnosis must be completed in less than 30 seconds.1
In the future, the system may consider integrations with SMS gateways for delivering OTPs
during authentication or critical alerts, or with payment systems if monetization features for
product advertising are introduced. Integration with other existing agricultural databases couldalso enhance the app's data richness. External Interface Specifications
The following table provides detailed specifications for the primary external software interfaces, outlining their purpose, technical characteristics, and key considerations for integration. Interfac
e Name
Descrip
tion
Type Protoco
l
Data
Exchan
ge
Authent
ication
Method
Reliabil
ity/SLADependencies
pg. 21
OpenW
eatherM
ap API
Provide
s realtime
and
forecast
weather
data
globally
.
REST
API
HTTPS, JSON
Input:
Latitude
,Longitu
de, API
Key;
Output:
Temper
ature, Humidit
y, Precipit
ation, Wind
Speed, Forecas
t
(daily/h
ourly)
API
Key
Typicall
y high, but
subject
to
external
provide
r's
uptime.
Internet
Connect
ivityPlantVil
lage
Nuru
API
AI- powere
d
service
for
diagnos
ing
plant
diseases
from
images.
REST
API
HTTPS, JSON
Input:
Crop
Image
(JPEG/
PNG), API
Key;
Output:
Disease
/Pest
Diagnos
is, Confide
nce
Score, Recom
mended
Advice
API
Key
Subject
to
external
provide
r's
uptime
and
processi
ng
capacity
.
Internet
Connect
ivity, CameraAccess
pg. 22
3.4. Communications Interfaces
The Mlimi App will employ various communication interfaces to interact with users and external
services. Push notifications will be a primary method for delivering critical information, suchasweather alerts
1
, and potentially for other updates like market price changes or newnewsletter
releases. All communication with the backend and external APIs will utilize
HTTPS (Hypertext Transfer Protocol Secure) to ensure data encryption and secure transmission. JSON (JavaScript Object Notation) will be the standard data transfer format for all API
communications, facilitating lightweight and efficient data exchange. The project's stated development cost of "MWK 100,000 for Internet/Data bundles"
1 andthetarget user base of smallholder farmers in Malawi highlight that data costs are a significant
concern for end-users. This implies that all communication interfaces—fromAPI calls andpushnotifications to content delivery—must be rigorously optimized for data efficiency. This includesemploying compressed data formats, minimizing redundant requests, and providing users withoptions to control their data usage (e.g., adjustable image quality settings for uploads, configurable frequency of updates). Such data optimization is crucial for ensuring the app's
affordability and continued accessibility, directly impacting its widespread adoption amongitstarget users. 4. Non-Functional Requirements
This section defines the quality attributes and constraints that the Mlimi App must satisfybeyondits core functionalities. These requirements are crucial for the system's overall success, user
satisfaction, and long-term viability. 4.1. Performance Requirements
The Mlimi App must demonstrate robust performance to ensure a positive user experience, particularly given the potential for slow network conditions in Malawi. Response times arecritical: the system shall load the homepage within 5 seconds, even on slow networks.1
Furthermore, the system shall perform pest diagnosis, which involves image upload and API
pg. 23
processing, in less than 30 seconds.1 Other critical operations, such as searching for agricultural
products or loading market prices, should also adhere to stringent response time targets, ideallyunder 3 seconds, to maintain user engagement. In terms of throughput, the system shall be designed to handle a specified number of concurrent
users and API requests without experiencing degradation in performance. For instance, it shouldcomfortably support at least 100 concurrent users and process 500 requests per minute duringpeak usage. Scalability is a fundamental architectural consideration; the chosen architecture(Django REST API backend, Firebase/SQLite) shall be capable of scaling to support a growinguser base and increasing data volumes without necessitating significant re-architecture. Finally, resource utilization on the mobile device is paramount, meaning the application shall be
optimized to minimize battery consumption and data usage, which are critical factors for userswith limited resources. The non-functional requirement for the "homepage to load within 5 seconds on slownetworks"1
directly acknowledges the challenging network conditions prevalent in Malawi. This necessitatesthat performance testing explicitly simulates low bandwidth and high latency environments toaccurately assess the app's responsiveness. Meeting this target requires a combination of server- side optimizations, such as efficient database queries and caching mechanisms, and client-sideoptimizations, including progressive loading of content and aggressive image compression. For users with "basic smartphone usage ability"
1 and potentially limited data bundles, a slowor
unresponsive application can quickly lead to frustration and abandonment. The performancenonfunctional requirements
1 are not merely technical metrics; they are direct determinants of user
satisfaction, adoption rates, and, ultimately, the app's capacity to achieve its goals of increasingagricultural productivity and farmer income. A poorly performing application, regardless of itsfeatures, will undermine its value proposition and hinder its ability to deliver meaningful impact. 4.2. Reliability Requirements
The Mlimi App must exhibit high reliability to ensure continuous availability of critical
information for farmers. The system shall ensure 90% uptime reliability.1 This commitment
ensures that the application and its services are generally accessible when needed. Error handling must be robust; the system shall gracefully manage various error conditions, such as network loss, failures in external API responses, or invalid user input. In such scenarios, the app should provide informative messages to the user without crashing or losing data. Dataintegrity is paramount, with mechanisms in place to ensure the consistency and accuracyof all
stored data, including user profiles, product listings, and market prices. Finally, in the event of a
pg. 24
system failure, the system shall have defined recovery procedures to restore data and resumeoperations within a specified timeframe, adhering to established Recovery Time Objectives
(RTO) and Recovery Point Objectives (RPO). While a 90% uptime target 1 may seem acceptable, for services as critical as real-time market
prices and weather alerts, even 10% downtime (approximately 73 hours per month) couldsignificantly impact farmers' operational decisions and erode their trust in the application. Thissuggests that 90% should be considered a baseline minimum, with continuous efforts to exceedthis target, particularly for core functionalities that directly influence farmers' livelihoods. Achieving higher reliability necessitates robust monitoring systems, automated alerting for
anomalies, and efficient automated recovery mechanisms to minimize downtime periods. For smallholder farmers who depend on the Mlimi App for critical information to manage their
livelihoods, consistent availability and accurate data are absolutely paramount. Frequent
downtime or inaccuracies in the data will rapidly diminish user trust, leading to lowadoptionrates and eventual abandonment of the application. The reliability non-functional requirement 1
is, therefore, a direct determinant of the app's long-term success and its ability to fulfill its
promise of "enabling better adaptation to market and environmental changes".1 Areliable systembuilds confidence and fosters sustained engagement.