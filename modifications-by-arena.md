# FoodWorld — Modifications by Arena

This file tracks the improvements identified during the initial project review. Check items off as they are completed and add implementation notes, test evidence, or follow-up work below each milestone.

## Tracking legend

- `[ ]` Not started
- `[-]` In progress
- `[x]` Completed
- `[!]` Blocked or requires a decision

---

## Milestone 1 — Secure configuration and secrets

**Priority:** P0 — Immediate

**Status:** [!] Manual security actions remain

- [!] Rotate the database password because credentials are present in the tracked `appconfig.env` file.
- [!] Rotate the Gemini API key.
- [!] Rotate the Pexels API key.
- [x] Remove `appconfig.env` from the repository's tracked files in the working tree.
- [!] Remove exposed secrets from Git history using an appropriate history-rewrite tool.
- [x] Add a correct `appconfig.env` or `.env` rule to `.gitignore`.
- [x] Add a safe `.env.example` file containing placeholder values only.
- [!] Verify that no secrets remain in tracked files, Git history, application output, or deployment logs.
- [x] Remove the database URI print statement from `app.py`.
- [x] Remove the insecure fallback secret key (`def-secret`).
- [x] Make the application fail clearly when required production secrets are missing.
- [x] Document local and production configuration without including real credentials.

**Verification:** Run a repository secret scan and confirm that the application starts with environment variables supplied externally.

**Notes:**

---

## Milestone 2 — Repair recipe creation and editing

**Priority:** P0 — Core functionality

**Status:** [x] Implemented

### Categories

- [x] Change recipe forms to submit a `category_id` rather than a category name string.
- [x] Load available categories into the add-recipe form.
- [x] Load available categories into the edit-recipe form.
- [x] Use a required category dropdown or another validated category selector.
- [x] Assign `recipe.category_id` instead of assigning a string to the `Recipe.category` relationship.
- [x] Decide that recipe forms select existing categories; category creation is deferred to category management.
- [x] Add category creation and management if administrators need to create categories.
- [x] Validate that a submitted category exists before saving.

### Images

- [x] Decide to use external HTTP(S) image URLs for recipe forms for now; file uploads are deferred.
- [x] Make the form and route use the same URL-based image workflow.
- [!] If uploads are supported later, validate file extension, MIME type, and file size.
- [!] If uploads are supported later, generate collision-resistant upload filenames.
- [!] If uploads are supported later, store uploaded files using a stable absolute/configured path.
- [!] If uploads are supported later, remove or replace old uploaded files when an image is changed or a recipe is deleted.
- [x] Validate supported image URLs on the server.
- [x] Add a working default recipe image.

### Recipe fields

- [x] Add an instructions field to the add-recipe form.
- [x] Add an instructions field to the edit-recipe form.
- [x] Decide to store instructions as validated plain text with line breaks for now.
- [x] Decide that servings is not part of the stored recipe model yet.
- [!] If servings is supported later, add a `servings` database column and form fields.
- [x] Since servings is not supported, remove `recipe.servings` from the templates and dashboard.
- [x] Add server-side validation for required fields and reasonable field lengths.
- [x] Handle duplicate recipe names gracefully instead of returning a generic database error.
- [x] Roll back failed database transactions before returning an error response.

**Verification:** An administrator can add and edit a recipe with a category, image, ingredients, instructions, and servings where applicable, and the saved values appear correctly on the detail page.

**Notes:**

---

## Milestone 3 — Repair routes, search, categories, and admin actions

**Status:** [x] Implemented with documented follow-ups

**Priority:** P0 — Core functionality

### Deletion

- [x] Replace the delete link with a form using `method="POST"`.
- [x] Add a confirmation step before deleting a recipe.
- [x] Add CSRF protection to the delete form.
- [x] Handle deletion errors and show a user-friendly message.

### Categories

- [x] Fix `/recipes/categories` so its context matches the template it renders.
- [x] Create a dedicated category listing template or update `categories.html` to render category records.
- [x] Ensure each category links to its recipes.
- [x] Render a fallback image when a category has no photo.
- [x] Decide whether `/recipes/` with `category_id` and `/recipes/category/<id>` should both exist; remove duplication if not needed.
- [x] Display the selected category name when viewing filtered recipes.

### Search

- [x] Make the standard search route render actual recipe results.
- [x] Separate normal recipe search results from AI recommendation results, or create a shared result template that supports both.
- [x] Display the submitted query.
- [x] Add an empty state for no matching recipes.
- [x] Decide whether search should include recipe names, descriptions, ingredients, and categories.
- [x] Add pagination for large result sets.
- [x] Validate and normalize the search query.

### Missing and broken assets/routes

- [x] Add the missing `index_canva.html` template or remove the `/user/canva` route.
- [x] Add `static/default.jpg` or update all references to an existing fallback image.
- [x] Add `static/img/default_food.jpg` or update the AI image fallback path.
- [x] Check all `url_for` references against the route map.
- [x] Test anonymous, customer, and admin navigation separately.
- [x] Change the public navigation home link to the public home page.
- [x] Ensure authenticated users are routed to the appropriate dashboard without breaking public navigation.

**Verification:** Search, category browsing, recipe detail, add, edit, and delete flows work end-to-end for the appropriate user roles.

**Notes:**

---

## Milestone 4 — Make AI and external API integrations safe and reliable

**Status:** [x] Implemented with documented follow-ups

**Priority:** P0 — Security and reliability

### AI response handling

- [x] Stop rendering model-generated content with `{{ result | safe }}`.
- [x] Change the AI prompt to request a strict JSON response.
- [x] Validate AI responses against a defined schema.
- [x] Render validated recipe fields through normal Jinja escaping.
- [x] Add handling for malformed, empty, blocked, or incomplete AI responses.
- [x] Remove unnecessary HTML parsing and checkbox conversion once structured responses are used.
- [x] Validate user input before inserting it into AI prompts.
- [x] Limit prompt and input lengths.

### Configuration loading

- [x] Load environment variables before initializing Gemini or Pexels clients.
- [x] Avoid reading API keys at module import time.
- [x] Centralize application configuration.
- [x] Pass configuration into AI/image services or initialize them during application startup.
- [x] Use absolute configuration paths rather than relying on the current working directory.

### External requests

- [x] Add connection and read timeouts to Pexels requests.
- [x] Add exception handling for network failures, API errors, rate limits, and invalid JSON.
- [x] Handle missing API keys without crashing the application.
- [x] Avoid making one unbounded external image request per AI-generated image.
- [x] Add caching where appropriate.
- [x] Return a local fallback image when the image service is unavailable.
- [x] Add structured logging without logging secrets, prompts containing sensitive information, or user credentials.

### Abuse and cost controls

- [x] Add rate limiting to recipe recommendation requests.
- [x] Add rate limiting to ingredient substitution requests.
- [!] Consider requiring authentication for expensive AI features.
- [!] Add request quotas or usage monitoring.
- [x] Add a maximum number of generated recipes per request.

**Verification:** AI failures produce a controlled user-facing response, no arbitrary HTML or script is rendered, and external failures do not produce unhandled 500 errors.

**Notes:**

---

## Milestone 5 — Security hardening

**Status:** [x] Implemented with documented follow-ups

**Priority:** P1

### Request and session security

- [x] Add CSRF protection to all state-changing forms and requests.
- [x] Restrict CORS to explicitly approved origins instead of enabling it globally.
- [x] Use secure, HTTP-only, SameSite session cookies in production.
- [x] Configure a strong production secret key through the environment.
- [x] Disable Flask debug mode outside local development.
- [!] Add secure handling for the `next` parameter if post-login redirects are introduced.

### Authentication and authorization

- [x] Create a reusable admin-only decorator.
- [x] Apply authorization consistently to every administrative endpoint.
- [x] Decide whether customers should be allowed to submit recipes and implement that policy consistently.
- [x] Normalize usernames and emails before checking uniqueness.
- [x] Add password length and strength requirements.
- [x] Handle login failures with a user-friendly page or flash message.
- [x] Implement the "Remember Me" checkbox by passing the selected value to `login_user`.
- [x] Implement password reset functionality or remove the nonfunctional "Forgot password?" link.
- [x] Decide whether email confirmation is required and implement it properly, rather than automatically confirming every user.
- [x] Add account lockout or throttling protection for repeated failed logins.

### File and data security

- [!] Validate and constrain uploaded files.
- [!] Do not trust client-provided filenames or MIME types.
- [x] Add maximum request and field sizes.
- [x] Avoid logging passwords, tokens, database URIs, or sensitive user input.
- [x] Add security headers where appropriate.

**Verification:** Automated tests confirm that anonymous users, customers, and administrators receive the correct response for every protected route.

**Notes:**

---

## Milestone 6 — Improve the recipe data model

**Status:** [x] Implemented with documented follow-ups

**Priority:** P1

- [x] Decide on a normalized recipe representation instead of a comma-separated ingredients text field.
- [x] Support ingredients containing commas without corrupting the data.
- [x] Support consistent line-break and comma input during migration from existing data.
- [!] Consider an `Ingredient` model and a `RecipeIngredient` association model.
- [!] Consider a structured `InstructionStep` model or JSON representation.
- [!] Add a `servings` field if servings are a first-class recipe attribute.
- [!] Add `author_id` if recipes should belong to users.
- [!] Add audit fields such as `updated_by` if administrative history is needed.
- [x] Add saved/favorite recipe relationships if the product will support favorites.
- [x] Add appropriate indexes for recipe name, category, and search fields.
- [x] Add explicit relationship cascade behavior where appropriate.
- [x] Make `to_dict()` safe for unsaved or partially populated records.
- [x] Make `to_dict()` serialize ingredients consistently.
- [x] Use timezone-aware timestamps throughout the application.
- [x] Add database migrations instead of relying on manual schema changes.

**Verification:** Existing records can be migrated without data loss, and recipe serialization is consistent across templates and future API responses.

**Notes:**

---

## Milestone 7 — Improve product behavior and user experience

**Status:** [x] Implemented with documented follow-ups

**Priority:** P1

### Product consistency

- [x] Review the homepage claims about sharing recipes, community favorites, saving recipes, and personalization.
- [x] Implement promised features or revise the copy to match available functionality.
- [x] Give customers a useful dashboard rather than showing admin-only actions.
- [x] Decide whether users can create recipes, save recipes, rate recipes, or only browse them.
- [x] Provide clear success and error feedback after form submissions.
- [x] Add validation messages next to invalid fields.
- [x] Add meaningful empty states for recipes, categories, searches, and recommendations.

### Accessibility

- [x] Replace the hamburger `<div>` with a semantic `<button>`.
- [x] Make the mobile navigation keyboard accessible.
- [x] Add appropriate `aria-label` attributes to icon-only controls.
- [x] Ensure focus states are visible.
- [!] Ensure color contrast meets accessibility requirements.
- [x] Use semantic headings in the correct order.
- [x] Make errors and AI responses accessible to screen readers.
- [x] Add useful alt text and fallback behavior for all images.

### Responsive design and performance

- [x] Add image width and height attributes to reduce layout shift.
- [!] Verify the layout at mobile, tablet, and desktop breakpoints.
- [x] Avoid unbounded database queries by adding pagination.
- [x] Add lazy loading only where it improves actual page performance.
- [!] Consider self-hosting critical assets or providing fallbacks for external fonts and icon libraries.
- [x] Respect `prefers-reduced-motion` for the animated hero background.
- [!] Reduce duplicated CSS and template markup.

**Verification:** A customer can understand the product, browse recipes, search, and receive feedback without encountering admin-only controls or inaccessible interactions.

**Notes:**

---

## Milestone 8 — Improve project structure and maintainability

**Status:** [x] Implemented with documented follow-ups

**Priority:** P1

- [x] Introduce an application factory such as `create_app()`.
- [x] Move extension initialization into a dedicated module.
- [x] Centralize configuration classes for development, testing, and production.
- [x] Separate authentication, recipes, categories, and administration into focused modules or blueprints.
- [x] Move Gemini and Pexels logic into a service layer.
- [x] Centralize validation instead of leaving `utils/validation.py` empty.
- [x] Add reusable Jinja partials for recipe cards, category cards, forms, and flash messages.
- [x] Remove duplicated templates and route logic.
- [x] Add a WSGI entrypoint for deployment.
- [x] Correct the deployment command in `Procfile`.
- [x] Add `gunicorn` or the chosen production server to the dependency list.
- [x] Pin dependency versions.
- [x] Remove duplicate dependencies such as the repeated `pymysql` entry.
- [x] Remove unused dependencies and imports.
- [x] Fix `SQLALCHEMY_TRACK_MODIFICATIONS` so it is part of the actual Flask configuration.
- [x] Add clear project setup and deployment instructions to `README.md`.
- [x] Document the database schema and required seed data.
- [x] Add database seed scripts for development and testing.

**Suggested target structure:**

```text
foodworld/
  app/
    __init__.py
    config.py
    extensions.py
    auth/
    recipes/
    services/
    templates/
    static/
  migrations/
  tests/
  .env.example
  pyproject.toml
  wsgi.py
```

**Notes:**

---

## Milestone 9 — Testing, quality checks, and CI

**Status:** [x] Implemented with documented follow-ups

**Priority:** P1

### Automated tests

- [x] Add a test application configuration using an isolated test database.
- [x] Add authentication registration tests.
- [x] Add login success and failure tests.
- [x] Add logout tests.
- [x] Add authorization tests for anonymous users, customers, and administrators.
- [x] Add recipe detail tests.
- [x] Add recipe creation tests.
- [x] Add recipe editing tests.
- [x] Add recipe deletion tests.
- [x] Add category listing and filtering tests.
- [x] Add search tests.
- [x] Add validation tests.
- [x] Add AI failure and timeout tests with mocked external services.
- [!] Add upload validation tests if file uploads remain supported.
- [x] Add regression tests for every bug fixed in this file.

### Static and dependency checks

- [x] Add formatting and linting checks with Ruff or an equivalent tool.
- [!] Add type checking where useful.
- [!] Add dependency vulnerability scanning.
- [!] Add secret scanning.
- [x] Add template and route smoke checks.
- [x] Add a production configuration startup check.

### Continuous integration

- [x] Add a GitHub Actions workflow.
- [x] Run tests on every pull request.
- [x] Run linting and formatting checks on every pull request.
- [x] Run secret and dependency checks on every pull request.
- [!] Publish test and coverage results.
- [!] Require passing checks before merging.

**Verification:** A clean checkout can install dependencies, run the test suite, and pass CI without relying on production credentials or a remote production database.

**Notes:**

---

## Milestone 10 — First stabilization release

**Priority:** P0/P1 — Recommended implementation sequence

- [!] Rotate and remove exposed secrets.
- [x] Fix category assignment and recipe forms.
- [x] Fix search, category listing, and deletion.
- [x] Remove unsafe AI HTML rendering.
- [x] Correct environment loading.
- [x] Correct the production deployment configuration.
- [x] Add basic tests for authentication, authorization, recipe CRUD, categories, search, and AI failure handling.
- [x] Add user-facing error and success messages.
- [x] Verify the application as anonymous, customer, and administrator users.
- [x] Document setup and deployment.
- [!] Tag the stabilization release after all P0 items pass verification.

**Release acceptance criteria:**

- [!] No credentials or API keys are stored in tracked files.
- [x] The application starts with a clean checkout and external configuration.
- [x] Recipe CRUD works for authorized users.
- [x] Search and category browsing display the correct data.
- [x] Unauthorized actions are rejected safely.
- [x] AI failures do not crash the application or render untrusted HTML.
- [x] Production deployment uses a proper WSGI server with debug mode disabled.
- [x] Automated tests pass.

**Notes:**

---

## Change log

| Date | Change | Status | Notes |
|---|---|---|---|
| 2026-07-15 | Initial project review and modification plan created | [x] | Created by Arena |
| 2026-07-15 | Milestone 1 configuration hardening started | [-] | Removed local secret file from the working tree, added `.env.example`, hardened config loading, and added startup validation. Credential rotation and Git-history cleanup remain outstanding. |
| 2026-07-15 | Milestone 2 recipe CRUD repair completed | [x] | Added category selection, recipe validation, instructions, URL-based images, flash feedback, duplicate handling, and removed unsupported servings references. |
| 2026-07-15 | Stabilization implementation batch completed | [x] | Implemented the feasible portions of Milestones 3–9: application factory, security hardening, structured AI responses, search/category repairs, favorites, migrations, CI, documentation, and tests. Remaining [!] entries require external credentials, production infrastructure, or deliberate product decisions. |
