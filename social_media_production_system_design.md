# Social Media Platform --- Production-Grade System Design

## 1. Project Overview

This project is a production-oriented social media platform designed to
be scalable, secure, testable, and maintainable.

The goal is to start with a well-structured Django application and
evolve it toward a distributed architecture only when scale or product
requirements justify it.

### Core principles

-   Production-grade architecture from the beginning
-   Modular Django backend
-   Django ORM for database access
-   Django Ninja for API development
-   Pydantic schemas for request/response validation
-   PostgreSQL as the primary database
-   Redis for caching and temporary data
-   Celery for background processing
-   Docker for reproducible environments
-   Automated testing and CI/CD
-   Strong authentication and authorization
-   Observability through logs, metrics, health checks, and error
    tracking
-   API versioning
-   Incremental scaling instead of premature microservices

------------------------------------------------------------------------

# 2. Technology Stack

  ----------------------------------------------------------------------------
  Layer                   Technology              Purpose
  ----------------------- ----------------------- ----------------------------
  Frontend                Next.js / React         Web application

  Backend                 Django                  Core backend framework

  API                     Django Ninja            REST-style API layer

  Validation              Pydantic                Request/response schemas

  ORM                     Django ORM              Database access

  Database                PostgreSQL              Primary relational database

  Cache                   Redis                   Caching, rate limiting,
                                                  temporary data

  Background jobs         Celery                  Asynchronous/background
                                                  processing

  Message broker          Redis initially         Celery broker

  Object storage          AWS S3 / MinIO          Images, videos, media

  Search                  OpenSearch              User/post/hashtag search

  Realtime                WebSockets              Notifications and messaging

  Reverse proxy           Nginx                   Routing, TLS termination,
                                                  static/media handling

  CDN                     CloudFront or           Media/content delivery
                          equivalent              

  Containers              Docker                  Consistent environments

  CI/CD                   GitHub Actions          Automated checks and
                                                  deployment

  Testing                 Pytest + pytest-django  Automated tests

  Linting                 Ruff                    Code quality

  Type checking           MyPy                    Static type checking

  Error tracking          Sentry                  Production error monitoring

  Metrics                 Prometheus              Application/infrastructure
                                                  metrics

  Dashboards              Grafana                 Metrics visualization

  Dependency management   uv                      Python environment and
                                                  dependencies

  Version control         Git + GitHub            Source control and
                                                  collaboration
  ----------------------------------------------------------------------------

------------------------------------------------------------------------

# 3. High-Level Architecture

``` text
                         ┌──────────────────────┐
                         │   Next.js Frontend   │
                         │      Web Client      │
                         └──────────┬───────────┘
                                    │
                                  HTTPS
                                    │
                         ┌──────────▼───────────┐
                         │    Nginx / Gateway   │
                         └──────────┬───────────┘
                                    │
                         ┌──────────▼───────────┐
                         │  Django + Ninja API  │
                         │       Backend        │
                         └──────────┬───────────┘
                                    │
              ┌─────────────────────┼─────────────────────┐
              │                     │                     │
       ┌──────▼──────┐       ┌──────▼──────┐      ┌─────▼──────┐
       │ PostgreSQL  │       │    Redis    │      │  S3/MinIO  │
       │  Database   │       │ Cache/Queue │      │   Media     │
       └─────────────┘       └──────┬──────┘      └─────────────┘
                                    │
                             ┌──────▼──────┐
                             │   Celery    │
                             │   Workers   │
                             └──────┬──────┘
                                    │
                    ┌───────────────┼────────────────┐
                    │               │                │
              Notifications    Media Tasks      Feed Tasks
```

Later, as traffic grows:

``` text
                         CDN
                          │
                   Load Balancer
                          │
                     API Gateway
                          │
          ┌───────────────┼────────────────┐
          │               │                │
     User Service    Post Service     Feed Service
          │               │                │
          └───────────────┼────────────────┘
                          │
                    Kafka Cluster
                          │
             ┌────────────┼────────────┐
             │            │            │
           Redis       Database     Workers
                          │
                     Object Storage
```

Microservices should only be introduced when there is a clear reason to
separate a component.

------------------------------------------------------------------------

# 4. Core Product Features

## 4.1 User

-   Registration
-   Login/logout
-   Email verification
-   Password reset
-   User profile
-   Username
-   Bio
-   Profile picture
-   Account settings
-   Account deactivation
-   Followers/following

## 4.2 Posts

-   Create post
-   Edit post
-   Delete post
-   Text content
-   Images
-   Videos
-   Visibility settings
-   Post timestamps
-   Hashtags
-   Mentions

## 4.3 Engagement

-   Like/unlike
-   Comments
-   Replies
-   Share/repost
-   Bookmark/save

## 4.4 Feed

-   Following feed
-   Personalized feed
-   Pagination
-   Feed caching
-   Ranking
-   Trending content

## 4.5 Notifications

-   New follower
-   Post like
-   Comment
-   Reply
-   Mention
-   Repost
-   Real-time notification delivery

## 4.6 Search

-   Search users
-   Search posts
-   Search hashtags
-   Search suggestions
-   Trending hashtags

## 4.7 Messaging

-   Conversations
-   Direct messages
-   Read/unread state
-   Real-time messaging
-   Online/offline state

## 4.8 Future Features

-   Stories
-   Reels/short videos
-   Communities/groups
-   Live streaming
-   AI recommendations
-   AI moderation
-   Content reporting
-   Creator analytics

------------------------------------------------------------------------

# 5. Why Django + Django Ninja + Pydantic?

The backend will use:

``` text
Django
   │
   ├── Django ORM
   │
   ├── Authentication
   │
   ├── Admin
   │
   └── Application framework
          │
          ▼
     Django Ninja
          │
          ▼
       Pydantic
```

Django ORM handles database operations.

Django Ninja handles API routing and integrates naturally with Pydantic
schemas.

Pydantic handles API input/output validation.

Example:

``` python
from ninja import NinjaAPI, Schema

api = NinjaAPI()


class PostCreateSchema(Schema):
    content: str


@api.post("/posts")
def create_post(request, data: PostCreateSchema):
    post = Post.objects.create(
        user=request.user,
        content=data.content,
    )

    return {
        "id": post.id,
        "content": post.content,
    }
```

------------------------------------------------------------------------

# 6. Production-Grade Project Structure

``` text
social-media/
│
├── apps/
│   │
│   ├── users/
│   │   ├── migrations/
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── api.py
│   │   ├── services.py
│   │   ├── selectors.py
│   │   ├── permissions.py
│   │   ├── admin.py
│   │   └── tests/
│   │
│   ├── posts/
│   │   ├── migrations/
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── api.py
│   │   ├── services.py
│   │   └── tests/
│   │
│   ├── comments/
│   ├── likes/
│   ├── follows/
│   ├── feed/
│   ├── notifications/
│   ├── messaging/
│   ├── search/
│   └── media/
│
├── config/
│   ├── settings/
│   │   ├── base.py
│   │   ├── development.py
│   │   ├── production.py
│   │   └── testing.py
│   │
│   ├── api.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── common/
│   ├── authentication/
│   ├── exceptions/
│   ├── pagination/
│   ├── middleware/
│   └── utils/
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── api/
│
├── docker/
│   ├── django/
│   ├── nginx/
│   └── postgres/
│
├── scripts/
│
├── .env.example
├── .gitignore
├── .pre-commit-config.yaml
├── Dockerfile
├── docker-compose.yml
├── manage.py
├── pyproject.toml
├── uv.lock
└── README.md
```

------------------------------------------------------------------------

# 7. Python and uv Setup

## 7.1 Create the project

``` bash
mkdir social-media
cd social-media
uv init
```

Remove the generated `main.py` because Django will be the application
entry point.

On Linux/macOS:

``` bash
rm main.py
```

On Windows PowerShell:

``` powershell
Remove-Item main.py
```

## 7.2 Create the virtual environment

``` bash
uv venv
```

Windows PowerShell:

``` powershell
.venv\Scripts\Activate.ps1
```

Windows CMD:

``` cmd
.venv\Scripts\activate
```

## 7.3 Install runtime dependencies

``` bash
uv add django django-ninja psycopg[binary] pydantic-settings django-environ
```

Additional production dependencies can be added as the corresponding
features are implemented.

## 7.4 Install development dependencies

``` bash
uv add --dev pytest pytest-django ruff mypy pre-commit
```

## 7.5 Create Django project

``` bash
uv run django-admin startproject config .
```

------------------------------------------------------------------------

# 8. Initial Django Apps

Do not create every application before it is needed.

Start with the foundational applications:

``` bash
uv run python manage.py startapp users
uv run python manage.py startapp posts
```

Later add:

``` text
comments
likes
follows
feed
notifications
messaging
search
media
```

------------------------------------------------------------------------

# 9. Settings Architecture

Instead of keeping everything in one `settings.py`:

``` text
config/settings/
├── base.py
├── development.py
├── production.py
└── testing.py
```

## Base settings

Shared configuration:

-   Installed apps
-   Middleware
-   Templates
-   Authentication
-   Database configuration structure
-   Static files
-   API configuration

## Development settings

-   Local PostgreSQL
-   Local Redis
-   Debugging enabled where appropriate
-   Development logging

## Production settings

-   `DEBUG=False`
-   Secure cookies
-   HTTPS settings
-   Security headers
-   Production database
-   Production Redis
-   S3/object storage
-   Structured logging
-   Monitoring
-   Allowed hosts

## Testing settings

-   Test database
-   Fast test configuration
-   Test-specific services

------------------------------------------------------------------------

# 10. Environment Variables

Create:

``` text
.env
.env.example
```

Example `.env.example`:

``` env
DJANGO_SETTINGS_MODULE=config.settings.development

SECRET_KEY=

DEBUG=False

DATABASE_URL=
REDIS_URL=

AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_STORAGE_BUCKET_NAME=
AWS_REGION=

SENTRY_DSN=
```

Never commit real secrets.

`.gitignore` should include:

``` gitignore
.env
.venv/
__pycache__/
*.pyc
.pytest_cache/
.mypy_cache/
.ruff_cache/
```

The `.env.example` file can be committed because it contains
placeholders rather than secrets.

------------------------------------------------------------------------

# 11. PostgreSQL

PostgreSQL is the primary database.

Architecture:

``` text
Django
   │
   ▼
Django ORM
   │
   ▼
PostgreSQL
```

Important database practices:

-   Foreign keys
-   Unique constraints
-   Check constraints
-   Composite indexes
-   Partial indexes where justified
-   Transactions
-   Efficient pagination
-   Query optimization
-   Connection management
-   Database migrations
-   Backups

Do not use SQLite as the production database.

------------------------------------------------------------------------

# 12. Custom User Model

A custom user model should be created before the first production
migration.

Example direction:

``` python
class User(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)
    profile_image = models.URLField(blank=True)
```

Then configure:

``` python
AUTH_USER_MODEL = "users.User"
```

The exact user model will be designed before creating the initial
migration.

------------------------------------------------------------------------

# 13. API Structure

All APIs should be versioned.

Base:

``` text
/api/v1/
```

Example endpoints:

``` text
POST   /api/v1/auth/register
POST   /api/v1/auth/login
POST   /api/v1/auth/refresh

GET    /api/v1/users/{username}
PATCH  /api/v1/users/me

POST   /api/v1/posts
GET    /api/v1/posts/{id}
PATCH  /api/v1/posts/{id}
DELETE /api/v1/posts/{id}

POST   /api/v1/posts/{id}/like
DELETE /api/v1/posts/{id}/like

POST   /api/v1/posts/{id}/comments
GET    /api/v1/posts/{id}/comments

POST   /api/v1/users/{id}/follow
DELETE /api/v1/users/{id}/follow

GET    /api/v1/feed
GET    /api/v1/notifications
```

Breaking API changes can later be introduced as:

``` text
/api/v2/
```

------------------------------------------------------------------------

# 14. API Schema Design

Each major API should have explicit Pydantic request and response
schemas.

Example:

``` python
from datetime import datetime
from ninja import Schema


class PostCreateSchema(Schema):
    content: str


class PostResponseSchema(Schema):
    id: int
    content: str
    username: str
    created_at: datetime
```

This prevents loosely defined API contracts.

------------------------------------------------------------------------

# 15. Authentication Architecture

Authentication should be designed properly from the beginning.

``` text
Register
   │
   ▼
Email Verification
   │
   ▼
Login
   │
   ├── Access Token
   │
   └── Refresh Token
```

Future authentication capabilities:

-   Email/password authentication
-   Email verification
-   Password reset
-   Refresh-token rotation
-   Logout
-   Session management
-   Google OAuth
-   GitHub OAuth
-   Account deactivation

Authentication and authorization are separate concepts.

``` text
Authentication
"What user are you?"

Authorization
"What is this user allowed to do?"
```

------------------------------------------------------------------------

# 16. Redis

Redis will not be the source of truth for core application data.

It will be used for:

-   Caching
-   Feed caching
-   Rate limiting
-   Temporary data
-   Session-related data where appropriate
-   Celery broker initially

Example feed flow:

``` text
GET /api/v1/feed
        │
        ▼
      Redis
        │
    ┌───┴────┐
    │        │
   Hit      Miss
    │        │
    ▼        ▼
 Return   PostgreSQL
             │
             ▼
           Redis
```

------------------------------------------------------------------------

# 17. Celery and Background Jobs

Long-running or asynchronous operations should not block API requests.

Example:

``` text
User uploads image
       │
       ▼
     API
       │
       ▼
    S3/MinIO
       │
       ▼
   Celery Task
       │
       ├── Resize image
       ├── Generate thumbnail
       └── Optimize media
```

Other possible Celery jobs:

-   Notifications
-   Email sending
-   Media processing
-   Feed generation
-   Cleanup jobs
-   Analytics aggregation
-   Scheduled tasks

------------------------------------------------------------------------

# 18. Media Architecture

Images and videos should not be stored directly inside PostgreSQL.

Recommended architecture:

``` text
Client
  │
  ▼
Django API
  │
  ▼
Generate presigned upload URL
  │
  ▼
S3 / MinIO
  │
  ▼
CDN
  │
  ▼
Users
```

The database stores metadata such as:

``` text
media_url
media_type
file_size
created_at
```

For videos:

``` text
Upload
   │
   ▼
S3
   │
   ▼
Celery
   │
   ▼
FFmpeg processing
   │
   ├── 360p
   ├── 720p
   └── 1080p
   │
   ▼
CDN
```

------------------------------------------------------------------------

# 19. Feed Architecture

## Initial approach

Start with fan-out on read.

``` text
User requests feed
        │
        ▼
Find followed users
        │
        ▼
Find their recent posts
        │
        ▼
Sort/rank
        │
        ▼
Return paginated results
```

This is easier to build and sufficient for an initial product.

## Scaled approach

For high traffic, use fan-out on write.

``` text
User creates post
       │
       ▼
Message Queue
       │
       ▼
Feed Worker
       │
       ▼
Followers' feeds
       │
       ▼
Redis
```

This allows feed reads to become much faster, but introduces additional
complexity.

------------------------------------------------------------------------

# 20. Notifications

Example:

``` text
User A likes User B's post
             │
             ▼
        Like Service
             │
             ▼
          Queue
             │
             ▼
     Notification Worker
             │
             ▼
      Notification DB
             │
             ▼
         WebSocket
             │
             ▼
          User B
```

Example notification:

``` text
User A liked your post.
```

------------------------------------------------------------------------

# 21. Search

Initially, PostgreSQL can support simple search.

As the product grows, introduce OpenSearch.

Architecture:

``` text
Post Created
    │
    ▼
PostgreSQL
    │
    ▼
Message Queue
    │
    ▼
Search Worker
    │
    ▼
OpenSearch
```

Search categories:

-   Users
-   Posts
-   Hashtags
-   Trending content

------------------------------------------------------------------------

# 22. Real-Time Features

WebSockets can be used for:

-   Notifications
-   Direct messages
-   Message read status
-   Presence/online state
-   Other real-time events

For example:

``` text
Django
   │
   ▼
WebSocket
   │
   ▼
Client
```

For horizontally scaled deployments, Redis or another shared
infrastructure can be used to coordinate real-time events.

------------------------------------------------------------------------

# 23. Database Model Planning

Core entities:

``` text
User
 │
 ├── Posts
 ├── Followers
 ├── Following
 ├── Likes
 ├── Comments
 ├── Bookmarks
 ├── Notifications
 └── Messages
```

Core tables:

``` text
users
posts
follows
likes
comments
bookmarks
notifications
hashtags
post_hashtags
conversations
messages
media
```

Important indexes will be added based on actual query patterns.

Examples:

``` text
posts.user_id
posts.created_at
follows.follower_id
follows.following_id
likes.post_id
comments.post_id
notifications.user_id
hashtags.name
```

Indexes should be added intentionally rather than everywhere.

------------------------------------------------------------------------

# 24. Security

Security is a first-class requirement.

## Authentication

-   Password hashing
-   Secure tokens
-   Token expiration
-   Refresh-token rotation
-   Email verification

## API security

-   Authentication
-   Authorization
-   Rate limiting
-   Input validation
-   Request size limits
-   Proper error handling

## Database security

-   Parameterized ORM queries
-   Least-privilege database credentials
-   Encrypted connections in production
-   Secure backups

## Media security

-   File type validation
-   File size limits
-   Safe file names
-   Malware/content scanning where appropriate
-   Private media authorization

## Web security

-   HTTPS
-   Secure cookies
-   CSRF protection where applicable
-   XSS protection
-   Security headers
-   CORS configuration
-   Trusted host configuration

------------------------------------------------------------------------

# 25. Testing Strategy

Use Pytest and pytest-django.

Testing structure:

``` text
tests/
├── unit/
├── integration/
└── api/
```

Test categories:

### Unit tests

-   Service functions
-   Utility functions
-   Business rules

### Integration tests

-   Database operations
-   Redis interactions
-   Celery workflows
-   External service integration

### API tests

-   Authentication
-   Authorization
-   Request validation
-   Response schemas
-   HTTP status codes
-   Pagination

Example areas:

``` text
User tests
Post tests
Follow tests
Like tests
Comment tests
Permission tests
Authentication tests
Feed tests
Notification tests
```

------------------------------------------------------------------------

# 26. Code Quality

Use:

``` text
Ruff
MyPy
Pre-commit
Pytest
```

Development flow:

``` text
Developer
    │
    ▼
Pre-commit
    │
    ├── Ruff
    └── MyPy
    │
    ▼
Pytest
    │
    ▼
Pull Request
```

Code should be formatted, linted, typed where practical, and tested
before merging.

------------------------------------------------------------------------

# 27. Docker

Docker should provide reproducible development and production
environments.

Initial development services:

``` text
┌────────────────────┐
│      Django        │
├────────────────────┤
│    PostgreSQL      │
├────────────────────┤
│       Redis        │
├────────────────────┤
│      Celery        │
└────────────────────┘
```

Eventually:

``` text
Django
PostgreSQL
Redis
Celery Worker
Celery Beat
Nginx
```

A developer should eventually be able to start the local infrastructure
with:

``` bash
docker compose up
```

------------------------------------------------------------------------

# 28. Git and GitHub

Initialize Git immediately:

``` bash
git init
```

Initial commit example:

``` text
chore: initialize production-grade Django project
```

Suggested branches:

``` text
main
develop

feature/authentication
feature/posts
feature/follows
feature/feed
feature/notifications
```

Even as a solo developer, pull requests can be used to simulate a
professional workflow.

------------------------------------------------------------------------

# 29. CI/CD

GitHub Actions should eventually perform:

``` text
Push / Pull Request
        │
        ▼
Install dependencies with uv
        │
        ▼
Ruff
        │
        ▼
MyPy
        │
        ▼
Pytest
        │
        ▼
Docker build
        │
        ▼
Deploy
```

The exact deployment provider can be selected later.

------------------------------------------------------------------------

# 30. Observability

Production systems need visibility into failures and performance.

Architecture:

``` text
Application
    │
    ├── Structured Logs
    │
    ├── Metrics
    │
    ├── Error Tracking
    │
    └── Health Checks
```

Recommended tools:

``` text
Sentry       → Error tracking
Prometheus   → Metrics
Grafana      → Dashboards
```

Health endpoints:

``` text
/health
/health/db
/health/redis
```

These should provide enough information for deployment/load balancer
health checks without exposing sensitive information.

------------------------------------------------------------------------

# 31. Scalability Strategy

## Phase 1 --- Modular monolith

``` text
Next.js
   │
   ▼
Django + Ninja
   │
   ├── Users
   ├── Posts
   ├── Social
   ├── Feed
   └── Notifications
   │
   ▼
PostgreSQL
   │
   ├── Redis
   └── Celery
```

## Phase 2 --- Growing application

Introduce:

``` text
Redis
Celery
S3
CDN
OpenSearch
WebSockets
```

## Phase 3 --- High scale

Potentially introduce:

``` text
Kafka
Dedicated Feed Service
Dedicated Notification Service
Read replicas
Database partitioning
Service extraction
```

## Phase 4 --- Large-scale architecture

Only where justified:

``` text
API Gateway
Load Balancers
Multiple application instances
Independent services
Kafka cluster
Redis cluster
Database replicas
Object storage
CDN
Advanced observability
```

Do not introduce a technology simply because it is popular. Every
component should solve a demonstrated problem.

------------------------------------------------------------------------

# 32. Development Roadmap

## Phase 0 --- Foundation

``` text
[ ] Create project with uv
[ ] Create virtual environment
[ ] Install Django
[ ] Install Django Ninja
[ ] Install Pydantic-related configuration tools
[ ] Configure PostgreSQL
[ ] Configure Docker
[ ] Configure environment variables
[ ] Create custom User model
[ ] Configure migrations
[ ] Configure Pytest
[ ] Configure Ruff
[ ] Configure MyPy
[ ] Configure pre-commit
[ ] Configure Git
[ ] Configure GitHub repository
[ ] Configure GitHub Actions
[ ] Add basic logging
[ ] Add health endpoint
```

## Phase 1 --- Authentication

``` text
[ ] Registration
[ ] Login
[ ] Logout
[ ] Access token
[ ] Refresh token
[ ] Email verification
[ ] Password reset
[ ] Authentication middleware
[ ] Permissions
```

## Phase 2 --- Profiles and Social Graph

``` text
[ ] User profile
[ ] Profile picture
[ ] Bio
[ ] Follow
[ ] Unfollow
[ ] Followers
[ ] Following
[ ] Block user
```

## Phase 3 --- Posts

``` text
[ ] Create post
[ ] Get post
[ ] Update post
[ ] Delete post
[ ] Pagination
[ ] Images
[ ] Video
[ ] Hashtags
[ ] Mentions
```

## Phase 4 --- Engagement

``` text
[ ] Like
[ ] Unlike
[ ] Comments
[ ] Replies
[ ] Bookmark
[ ] Share/repost
```

## Phase 5 --- Feed

``` text
[ ] Following feed
[ ] Cursor pagination
[ ] Redis caching
[ ] Feed ranking
[ ] Feed optimization
[ ] Fan-out strategy
```

## Phase 6 --- Notifications

``` text
[ ] Notification model
[ ] Like notification
[ ] Comment notification
[ ] Follow notification
[ ] Mention notification
[ ] WebSocket delivery
[ ] Mark as read
```

## Phase 7 --- Search

``` text
[ ] User search
[ ] Post search
[ ] Hashtag search
[ ] OpenSearch
[ ] Search indexing
```

## Phase 8 --- Messaging

``` text
[ ] Conversations
[ ] Messages
[ ] WebSockets
[ ] Read status
[ ] Online/offline state
```

## Phase 9 --- Production Deployment

``` text
[ ] Production Docker image
[ ] Nginx
[ ] HTTPS
[ ] S3
[ ] CDN
[ ] PostgreSQL production instance
[ ] Redis production instance
[ ] Celery workers
[ ] CI/CD
[ ] Monitoring
[ ] Sentry
[ ] Backups
[ ] Security hardening
```

## Phase 10 --- Scale

``` text
[ ] Kafka
[ ] Feed workers
[ ] Database read replicas
[ ] Query optimization
[ ] Database partitioning where justified
[ ] Service extraction where justified
[ ] Advanced caching
[ ] Load testing
```

------------------------------------------------------------------------

# 33. Initial Repository Structure

At the very beginning, keep the repository manageable:

``` text
social-media/
│
├── apps/
│   └── users/
│
├── config/
│   └── settings/
│
├── common/
│
├── tests/
│
├── docker/
│
├── scripts/
│
├── .env.example
├── .gitignore
├── .pre-commit-config.yaml
├── Dockerfile
├── docker-compose.yml
├── manage.py
├── pyproject.toml
├── uv.lock
└── README.md
```

As features are implemented, add:

``` text
posts/
comments/
likes/
follows/
feed/
notifications/
messaging/
search/
media/
```

------------------------------------------------------------------------

# 34. Initial Commands

A clean initial setup can follow this sequence:

``` bash
mkdir social-media
cd social-media

uv init
uv venv
```

Activate the virtual environment.

Then:

``` bash
uv add django django-ninja psycopg[binary] pydantic-settings django-environ
```

Development tools:

``` bash
uv add --dev pytest pytest-django ruff mypy pre-commit
```

Create Django:

``` bash
uv run django-admin startproject config .
```

Create initial apps:

``` bash
uv run python manage.py startapp users
uv run python manage.py startapp posts
```

Then configure the custom User model before creating the initial
production database migration.

Run development checks:

``` bash
uv run python manage.py check
```

Create migrations:

``` bash
uv run python manage.py makemigrations
```

Apply migrations:

``` bash
uv run python manage.py migrate
```

Run the server:

``` bash
uv run python manage.py runserver
```

------------------------------------------------------------------------

# 35. API Documentation

Django Ninja provides interactive API documentation.

The development API should be available at:

``` text
http://127.0.0.1:8000/api/v1/docs
```

This gives us a convenient interface for testing and understanding API
contracts.

Production API documentation should be configured intentionally and
protected or disabled if the product's security policy requires it.

------------------------------------------------------------------------

# 36. Engineering Principles

The project should follow these principles:

### Keep business logic out of API handlers

Instead of putting everything in `api.py`:

``` text
API
 ↓
Service
 ↓
ORM
```

Example:

``` text
api.py
   ↓
services.py
   ↓
models.py
```

### Separate reads and writes where useful

For complex queries:

``` text
selectors.py
```

can contain optimized read/query logic.

### Keep APIs thin

The API layer should primarily handle:

-   Authentication
-   Validation
-   Calling business logic
-   Serialization
-   HTTP responses

### Optimize only when necessary

Do not introduce complex infrastructure without a real requirement.

------------------------------------------------------------------------

# 37. Important Architectural Decision

The project will start as a **modular monolith**, not a collection of
microservices.

That means:

``` text
One Django deployment
        │
        ├── Users module
        ├── Posts module
        ├── Social module
        ├── Feed module
        ├── Notification module
        └── Messaging module
```

This provides:

-   Faster development
-   Easier debugging
-   Simpler deployment
-   Shared Django ORM
-   Easier transactions
-   Lower infrastructure complexity

When a component needs independent scaling or deployment, it can be
extracted later.

------------------------------------------------------------------------

# 38. Final Target Architecture

The long-term architecture can evolve toward:

``` text
                         ┌─────────────────┐
                         │   Next.js App   │
                         └────────┬────────┘
                                  │
                                 CDN
                                  │
                         ┌────────▼────────┐
                         │ Load Balancer   │
                         └────────┬────────┘
                                  │
                         ┌────────▼────────┐
                         │  API Gateway    │
                         └────────┬────────┘
                                  │
              ┌───────────────────┼───────────────────┐
              │                   │                   │
       ┌──────▼──────┐    ┌──────▼──────┐    ┌──────▼──────┐
       │ User/Graph  │    │    Posts    │    │    Feed     │
       │   Module    │    │   Module    │    │   Module    │
       └──────┬──────┘    └──────┬──────┘    └──────┬──────┘
              │                   │                   │
              └───────────────────┼───────────────────┘
                                  │
                             Message Bus
                               Kafka
                                  │
              ┌───────────────────┼───────────────────┐
              │                   │                   │
            Redis             PostgreSQL          Workers
              │                   │                   │
              │                   │              Celery
              │                   │
              └──────────┬────────┘
                         │
                    Object Storage
                         │
                        S3
                         │
                        CDN
```

The architecture should evolve based on measurable requirements such as
traffic, latency, database load, queue depth, storage requirements, and
operational complexity.

------------------------------------------------------------------------

# 39. First Milestone

The first milestone is **not** building posts, likes, or feeds.

It is establishing a reliable production foundation:

``` text
uv
 ↓
Django
 ↓
Django Ninja
 ↓
Pydantic
 ↓
PostgreSQL
 ↓
Custom User
 ↓
Docker
 ↓
Pytest
 ↓
Ruff
 ↓
MyPy
 ↓
Pre-commit
 ↓
GitHub Actions
 ↓
Health checks
 ↓
Logging
```

Once this foundation is stable, authentication should be the first major
product feature.

------------------------------------------------------------------------

# 40. Recommended Build Order

``` text
FOUNDATION
    ↓
CUSTOM USER
    ↓
AUTHENTICATION
    ↓
PROFILE
    ↓
FOLLOW SYSTEM
    ↓
POSTS
    ↓
LIKES + COMMENTS
    ↓
BOOKMARKS + SHARES
    ↓
FEED
    ↓
REDIS
    ↓
CELERY
    ↓
NOTIFICATIONS
    ↓
WEBSOCKETS
    ↓
MEDIA / S3
    ↓
SEARCH / OPENSEARCH
    ↓
MESSAGING
    ↓
CI/CD
    ↓
MONITORING
    ↓
LOAD TESTING
    ↓
SCALING
```

This order lets us build a real product while continuously improving the
architecture instead of spending weeks building infrastructure before
having usable functionality.
