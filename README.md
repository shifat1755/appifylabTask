# Basic Social Media Application

## Overview

A full-stack social media feed application built with FastAPI (backend) and React with TypeScript (frontend). The application provides core social media functionalities including user authentication, post creation with images, commenting, liking, and notifications.

## Technology Overview

The application follows a **clean architecture** pattern with clear separation of concerns:

- **Backend**: FastAPI with async SQLAlchemy, PostgreSQL database, Redis for caching and notifications
- **Frontend**: React 19 with TypeScript, Vite build tool, React Router for navigation
- **Database**: PostgreSQL with async SQLAlchemy ORM and Alembic for migrations
- **Caching/Storage**: Redis for refresh token storage(so that we can blacklist them) and notification management

## Core Functionalities

### 1. Authentication & Authorization

**Functionality:**

- User registration with email, password, first name, last name
- JWT-based authentication with access tokens and refresh tokens
- Refresh tokens stored in Redis with session management
- HttpOnly cookies for secure token storage
- Protected routes on frontend that require authentication
- Logout functionality that revokes refresh tokens

**Decisions:**

- **JWT Tokens**: Used for stateless authentication with short-lived access tokens and longer-lived refresh tokens
- **Redis for Refresh Tokens**: Chose Redis over database storage for better performance and scalability. Refresh tokens are stored with session IDs to support multiple device sessions
- **HttpOnly Cookies**: Refresh tokens stored in HttpOnly cookies to prevent XSS attacks
- **Session-based Refresh Tokens**: Each login creates a unique session ID, allowing users to manage multiple active sessions and revoking them when user logged out or request a new access token.

### 2. Post Management

**Functionality:**

- Create posts with text content and optional image uploads
- Image files stored in organized directory structure (`uploads/posts/user_{user_id}/`)
- Post visibility settings: `public` (default) or `private`
- View posts with pagination support (skip/limit)
- Filter posts by author, visibility
- Sort posts by: newest, oldest, most_liked, most_commented
- Access control: private posts only visible to the author
- Update and delete own posts
- Automatic increment/decrement of likes_count and comments_count

**Decisions:**

- **Denormalized Counts**: `likes_count` and `comments_count` stored directly on Post model for faster queries without joins
- **Optional Authentication**: Post listing endpoint accepts optional authentication to show private posts to authors

### 3. Comment System

**Functionality:**

- Create comments on posts
- Nested comment replies (parent-child relationship)
- View comments with pagination
- Filter to show only top-level comments or include replies
- Sort comments by: newest, oldest, most_liked
- Update and delete own comments
- Automatic increment of post's `comments_count` when comment is created
- Cascade deletion: deleting a post deletes all its comments

**Decisions:**

- **Top-level Filtering**: Default behavior shows only top-level comments to reduce initial load, with option to fetch replies
- **Denormalized Counts**: Comment `likes_count` stored on Comment model for performance

### 4. Like System

**Functionality:**

- Toggle likes on posts and comments (like/unlike)
- View list of users who liked a post or comment
- Automatic increment/decrement of like counts
- Unique constraint prevents duplicate likes from same user
- Supports both post and comment likes through polymorphic `target_type` field

**Decisions:**

- **Polymorphic Likes**: Single `Like` model handles both post and comment likes using `target_type` enum and `target_id`
- **Toggle Behavior**: Single endpoint toggles like state (creates if not exists, deletes if exists)
- **Composite Index**: Index on `(target_type, target_id)` for efficient lookups
- **Unique Constraint**: Prevents same user from liking same content multiple times

### 6. Notification Service

**Functionality:**

- Real-time notifications stored in Redis
- Notification types:
  - `post_liked`: When someone likes your post
  - `post_commented`: When someone comments on your post
  - `comment_liked`: When someone likes your comment
- Fetch notifications for current user
- Notifications automatically deleted after being fetched (fire-and-forget model)
- 7-day expiration on notification lists

**Decisions:**

- **Redis Storage**: Notifications stored in Redis (DB 2) for fast access and automatic expiration
- **Fire-and-Forget Model**: Notifications are consumed once when fetched, reducing storage overhead

### 7. Frontend Features

**Functionality:**

- Login and registration pages
- Protected feed route requiring authentication
- Feed page displaying posts with:
  - Post creation form with image upload
  - Visibility selector (public/private)
  - Like/unlike functionality
  - Notification dropdown with updates
  - Logout functionality

## Technical Stack

### Backend

- **Framework**: FastAPI 0.117.1
- **Database**: PostgreSQL with asyncpg driver
- **ORM**: SQLAlchemy 2.0 (async)
- **Migrations**: Alembic
- **Authentication**: PyJWT 2.10.1
- **Password Hashing**: bcrypt 5.0, passlib 1.7.4
- **Caching/Storage**: Redis 6.4.0 (async)
- **Validation**: Pydantic 2.11.9

### Frontend

- **Framework**: React 19.2.0
- **Language**: TypeScript 5.9.3
- **Build Tool**: Vite 7.2.4
- **Routing**: React Router DOM 7.9.6
- **HTTP Client**: Axios 1.13.2

## Database Schema

### Users Table

- User authentication and profile information
- Relationships: posts, comments, likes

### Posts Table

- Content, image_url, visibility (public/private)
- Denormalized: likes_count, comments_count
- Relationships: author, comments

### Comments Table

- Self-referential for nested replies (parent_comment_id)
- Denormalized: likes_count
- Relationships: post, author, parent_comment, replies

### Likes Table

- Polymorphic: target_type (post/comment) + target_id
- Unique constraint: (user_id, target_id, target_type)
- Composite index for efficient lookups

## API Endpoints

### Authentication (`/api/auth`)

- `POST /signup` - User registration
- `POST /login` - User login (returns access token, sets refresh token cookie)
- `POST /logout` - Logout (revokes refresh token)
- `POST /refresh` - Refresh access token using refresh token cookie

### Posts (`/api/posts`)

- `POST /posts` - Create post (with optional image)
- `GET /posts` - List posts (with pagination, filtering, sorting)
- `GET /posts/{post_id}` - Get single post
- `PUT /posts/{post_id}` - Update post
- `DELETE /posts/{post_id}` - Delete post

### Comments (`/api/posts/{post_id}/comments`)

- `POST /posts/{post_id}/comments` - Create comment
- `GET /posts/{post_id}/comments` - List comments (with pagination, filtering)
- `PUT /comments/{comment_id}` - Update comment
- `DELETE /comments/{comment_id}` - Delete comment

### Likes (`/api/likes`)

- `POST /posts/{post_id}/likes` - Toggle post like
- `GET /posts/{post_id}/likes` - Get post likes list
- `POST /comments/{comment_id}/likes` - Toggle comment like
- `GET /comments/{comment_id}/likes` - Get comment likes list

### Notifications (`/api/notifications`)

- `GET /notifications` - Get and consume user notifications

## Security Features

1. **Password Hashing**: bcrypt with salt rounds
2. **JWT Tokens**: Signed tokens with expiration
3. **HttpOnly Cookies**: Refresh tokens in secure, HttpOnly cookies
4. **CORS**: Configured for specific frontend origin
5. **Access Control**: Private posts only accessible to authors
6. **Input Validation**: Pydantic schemas validate all inputs
7. **SQL Injection Protection**: SQLAlchemy ORM with parameterized queries

## Key Design Decisions

1. **Async Architecture**: Entire backend uses async/await for better concurrency and performance
2. **Clean Architecture**: Separation into domain, application (usecases), infrastructure (repos, models), and presentation (routes, schemas) layers
3. **Repository Pattern**: Data access abstracted through repository classes
4. **Use Case Pattern**: Business logic encapsulated in use case classes
5. **Denormalized Counts**: Like and comment counts stored on parent models to avoid expensive joins
6. **Redis for Notifications**: Fast, ephemeral storage suitable for real-time notifications
7. **Optional Authentication**: Some endpoints accept optional auth to support both authenticated and anonymous access patterns

## Future Enhancements

Potential areas for extension:

- User profiles and friend relationships
- Post sharing functionality
- Rich text editing for posts/comments
- Image optimization and CDN integration
- Notification persistence for historical viewing
- Rate limiting and API throttling
- Proper image storage(s3,GCS)
