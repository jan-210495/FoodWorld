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

- [ ] Rotate the database password because credentials are present in the tracked `appconfig.env` file.
- [ ] Rotate the Gemini API key.
- [ ] Rotate the Pexels API key.
- [x] Remove `appconfig.env` from the repository's tracked files in the working tree.
- [ ] Remove exposed secrets from Git history using an appropriate history-rewrite tool.
- [x] Add a correct `appconfig.env` or `.env` rule to `.gitignore`.
- [x] Add a safe `.env.example` file containing placeholder values only.
- [ ] Verify that no secrets remain in tracked files, Git history, application output, or deployment logs.
- [x] Remove the database URI print statement from `app.py`.
- [x] Remove the insecure fallback secret key (`def-secret`).
- [x] Make the application fail clearly when required production secrets are missing.
- [x] Document local and production configuration without including real credentials.

**Verification:** Run a repository secret scan and confirm that the application starts with environment variables supplied externally.

**Notes:**

---

## Milestone 2 — Repair recipe creation and editing

**Priority:** P0 — Core functionality

**Status:** [-] In progress

### Categories

- [x] Change recipe forms to submit a `category_id` rather than a category name string.
- [x] Load available categories into the add-recipe form.
- [x] Load available categories into the edit-recipe form.
- [x] Use a required category dropdown or another validated category selector.
- [x] Assign `recipe.category_id` instead of assigning a string to the `Recipe.category` relationship.
- [x] Decide that recipe forms select existing categories; category creation is deferred to category management.
- [ ] Add category creation and management if administrators need to create categories.
- [x] Validate that a submitted category exists before saving.

### Images

- [x] Decide to use external HTTP(S) image URLs for recipe forms for now; file uploads are deferred.
- [x] Make the form and route use the same URL-based image workflow.
- [ ] If uploads are supported later, validate file extension, MIME type, and file size.
- [ ] If uploads are supported later, generate collision-resistant upload filenames.
- [ ] If uploads are supported later, store uploaded files using a stable absolute/configured path.
- [ ] If uploads are supported later, remove or replace old uploaded files when an image is changed or a recipe is deleted.
- [x] Validate supported image URLs on the server.
- [ ] Add a working default recipe image.

### Recipe fields

- [x] Add an instructions field to the add-recipe form.
- [x] Add an instructions field to the edit-recipe form.
- [x] Decide to store instructions as validated plain text with line breaks for now.
- [x] Decide that servings is not part of the stored recipe model yet.
- [ ] If servings is supported later, add a `servings` database column and form fields.
- [x] Since servings is not supported, remove `recipe.servings` from the templates and dashboard.
- [x] Add server-side validation for required fields and reasonable field lengths.
- [x] Handle duplicate recipe names gracefully instead of returning a generic database error.
- [x] Roll back failed database transactions before returning an error response.

**Verification:** An administrator can add and edit a recipe with a category, image, ingredients, instructions, and servings where applicable, and the saved values appear correctly on the detail page.

**Notes:**

---

## Milestone 3 — Repair routes, search, categories, and admin actions

**Priority:** P0 — Core functionality

### Deletion

- [ ] Replace the delete link with a form using `method="POST"`.
- [ ] Add a confirmation step before deleting a recipe.
- [ ] Add CSRF protection to the delete form.
- [ ] Handle deletion errors and show a user-friendly message.

### Categories

- [ ] Fix `/recipes/categories` so its context matches the template it renders.
- [ ] Create a dedicated category listing template or update `categories.html` to render category records.
- [ ] Ensure each category links to its recipes.
- [ ] Render a fallback image when a category has no photo.
- [ ] Decide whether `/recipes/` with `category_id` and `/recipes/category/<id>` should both exist; remove duplication if not needed.
- [ ] Display the selected category name when viewing filtered recipes.

### Search

- [ ] Make the standard search route render actual recipe results.
- [ ] Separate normal recipe search results from AI recommendation results, or create a shared result template that supports both.
- [ ] Display the submitted query.
- [ ] Add an empty state for no matching recipes.
- [ ] Decide whether search should include recipe names, descriptions, ingredients, and categories.
- [ ] Add pagination for large result sets.
- [ ] Validate and normalize the search query.

### Missing and broken assets/routes

- [ ] Add the missing `index_canva.html` template or remove the `/user/canva` route.
- [ ] Add `static/default.jpg` or update all references to an existing fallback image.
- [ ] Add `static/img/default_food.jpg` or update the AI image fallback path.
- [ ] Check all `url_for` references against the route map.
- [ ] Test anonymous, customer, and admin navigation separately.
- [ ] Change the public navigation home link to the public home page.
- [ ] Ensure authenticated users are routed to the appropriate dashboard without breaking public navigation.

**Verification:** Search, category browsing, recipe detail, add, edit, and delete flows work end-to-end for the appropriate user roles.

**Notes:**

---

## Milestone 4 — Make AI and external API integrations safe and reliable

**Priority:** P0 — Security and reliability

### AI response handling

- [ ] Stop rendering model-generated content with `{{ result | safe }}`.
- [ ] Change the AI prompt to request a strict JSON response.
- [ ] Validate AI responses against a defined schema.
- [ ] Render validated recipe fields through normal Jinja escaping.
- [ ] Add handling for malformed, empty, blocked, or incomplete AI responses.
- [ ] Remove unnecessary HTML parsing and checkbox conversion once structured responses are used.
- [ ] Validate user input before inserting it into AI prompts.
- [ ] Limit prompt and input lengths.

### Configuration loading

- [ ] Load environment variables before initializing Gemini or Pexels clients.
- [ ] Avoid reading API keys at module import time.
- [ ] Centralize application configuration.
- [ ] Pass configuration into AI/image services or initialize them during application startup.
- [ ] Use absolute configuration paths rather than relying on the current working directory.

### External requests

- [ ] Add connection and read timeouts to Pexels requests.
- [ ] Add exception handling for network failures, API errors, rate limits, and invalid JSON.
- [ ] Handle missing API keys without crashing the application.
- [ ] Avoid making one unbounded external image request per AI-generated image.
- [ ] Add caching where appropriate.
- [ ] Return a local fallback image when the image service is unavailable.
- [ ] Add structured logging without logging secrets, prompts containing sensitive information, or user credentials.

### Abuse and cost controls

- [ ] Add rate limiting to recipe recommendation requests.
- [ ] Add rate limiting to ingredient substitution requests.
- [ ] Consider requiring authentication for expensive AI features.
- [ ] Add request quotas or usage monitoring.
- [ ] Add a maximum number of generated recipes per request.

**Verification:** AI failures produce a controlled user-facing response, no arbitrary HTML or script is rendered, and external failures do not produce unhandled 500 errors.

**Notes:**

---

## Milestone 5 — Security hardening

**Priority:** P1

### Request and session security

- [ ] Add CSRF protection to all state-changing forms and requests.
- [ ] Restrict CORS to explicitly approved origins instead of enabling it globally.
- [ ] Use secure, HTTP-only, SameSite session cookies in production.
- [ ] Configure a strong production secret key through the environment.
- [ ] Disable Flask debug mode outside local development.
- [ ] Add secure handling for the `next` parameter if post-login redirects are introduced.

### Authentication and authorization

- [ ] Create a reusable admin-only decorator.
- [ ] Apply authorization consistently to every administrative endpoint.
- [ ] Decide whether customers should be allowed to submit recipes and implement that policy consistently.
- [ ] Normalize usernames and emails before checking uniqueness.
- [ ] Add password length and strength requirements.
- [ ] Handle login failures with a user-friendly page or flash message.
- [ ] Implement the "Remember Me" checkbox by passing the selected value to `login_user`.
- [ ] Implement password reset functionality or remove the nonfunctional "Forgot password?" link.
- [ ] Decide whether email confirmation is required and implement it properly, rather than automatically confirming every user.
- [ ] Add account lockout or throttling protection for repeated failed logins.

### File and data security

- [ ] Validate and constrain uploaded files.
- [ ] Do not trust client-provided filenames or MIME types.
- [ ] Add maximum request and field sizes.
- [ ] Avoid logging passwords, tokens, database URIs, or sensitive user input.
- [ ] Add security headers where appropriate.

**Verification:** Automated tests confirm that anonymous users, customers, and administrators receive the correct response for every protected route.

**Notes:**

---

## Milestone 6 — Improve the recipe data model

**Priority:** P1

- [ ] Decide on a normalized recipe representation instead of a comma-separated ingredients text field.
- [ ] Support ingredients containing commas without corrupting the data.
- [ ] Support consistent line-break and comma input during migration from existing data.
- [ ] Consider an `Ingredient` model and a `RecipeIngredient` association model.
- [ ] Consider a structured `InstructionStep` model or JSON representation.
- [ ] Add a `servings` field if servings are a first-class recipe attribute.
- [ ] Add `author_id` if recipes should belong to users.
- [ ] Add audit fields such as `updated_by` if administrative history is needed.
- [ ] Add saved/favorite recipe relationships if the product will support favorites.
- [ ] Add appropriate indexes for recipe name, category, and search fields.
- [ ] Add explicit relationship cascade behavior where appropriate.
- [ ] Make `to_dict()` safe for unsaved or partially populated records.
- [ ] Make `to_dict()` serialize ingredients consistently.
- [ ] Use timezone-aware timestamps throughout the application.
- [ ] Add database migrations instead of relying on manual schema changes.

**Verification:** Existing records can be migrated without data loss, and recipe serialization is consistent across templates and future API responses.

**Notes:**

---

## Milestone 7 — Improve product behavior and user experience

**Priority:** P1

### Product consistency

- [ ] Review the homepage claims about sharing recipes, community favorites, saving recipes, and personalization.
- [ ] Implement promised features or revise the copy to match available functionality.
- [ ] Give customers a useful dashboard rather than showing admin-only actions.
- [ ] Decide whether users can create recipes, save recipes, rate recipes, or only browse them.
- [ ] Provide clear success and error feedback after form submissions.
- [ ] Add validation messages next to invalid fields.
- [ ] Add meaningful empty states for recipes, categories, searches, and recommendations.

### Accessibility

- [ ] Replace the hamburger `<div>` with a semantic `<button>`.
- [ ] Make the mobile navigation keyboard accessible.
- [ ] Add appropriate `aria-label` attributes to icon-only controls.
- [ ] Ensure focus states are visible.
- [ ] Ensure color contrast meets accessibility requirements.
- [ ] Use semantic headings in the correct order.
- [ ] Make errors and AI responses accessible to screen readers.
- [ ] Add useful alt text and fallback behavior for all images.

### Responsive design and performance

- [ ] Add image width and height attributes to reduce layout shift.
- [ ] Verify the layout at mobile, tablet, and desktop breakpoints.
- [ ] Avoid unbounded database queries by adding pagination.
- [ ] Add lazy loading only where it improves actual page performance.
- [ ] Consider self-hosting critical assets or providing fallbacks for external fonts and icon libraries.
- [ ] Respect `prefers-reduced-motion` for the animated hero background.
- [ ] Reduce duplicated CSS and template markup.

**Verification:** A customer can understand the product, browse recipes, search, and receive feedback without encountering admin-only controls or inaccessible interactions.

**Notes:**

---

## Milestone 8 — Improve project structure and maintainability

**Priority:** P1

- [ ] Introduce an application factory such as `create_app()`.
- [ ] Move extension initialization into a dedicated module.
- [ ] Centralize configuration classes for development, testing, and production.
- [ ] Separate authentication, recipes, categories, and administration into focused modules or blueprints.
- [ ] Move Gemini and Pexels logic into a service layer.
- [ ] Centralize validation instead of leaving `utils/validation.py` empty.
- [ ] Add reusable Jinja partials for recipe cards, category cards, forms, and flash messages.
- [ ] Remove duplicated templates and route logic.
- [ ] Add a WSGI entrypoint for deployment.
- [ ] Correct the deployment command in `Procfile`.
- [ ] Add `gunicorn` or the chosen production server to the dependency list.
- [ ] Pin dependency versions.
- [ ] Remove duplicate dependencies such as the repeated `pymysql` entry.
- [ ] Remove unused dependencies and imports.
- [ ] Fix `SQLALCHEMY_TRACK_MODIFICATIONS` so it is part of the actual Flask configuration.
- [ ] Add clear project setup and deployment instructions to `README.md`.
- [ ] Document the database schema and required seed data.
- [ ] Add database seed scripts for development and testing.

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

**Priority:** P1

### Automated tests

- [ ] Add a test application configuration using an isolated test database.
- [ ] Add authentication registration tests.
- [ ] Add login success and failure tests.
- [ ] Add logout tests.
- [ ] Add authorization tests for anonymous users, customers, and administrators.
- [ ] Add recipe detail tests.
- [ ] Add recipe creation tests.
- [ ] Add recipe editing tests.
- [ ] Add recipe deletion tests.
- [ ] Add category listing and filtering tests.
- [ ] Add search tests.
- [ ] Add validation tests.
- [ ] Add AI failure and timeout tests with mocked external services.
- [ ] Add upload validation tests if file uploads remain supported.
- [ ] Add regression tests for every bug fixed in this file.

### Static and dependency checks

- [ ] Add formatting and linting checks with Ruff or an equivalent tool.
- [ ] Add type checking where useful.
- [ ] Add dependency vulnerability scanning.
- [ ] Add secret scanning.
- [ ] Add template and route smoke checks.
- [ ] Add a production configuration startup check.

### Continuous integration

- [ ] Add a GitHub Actions workflow.
- [ ] Run tests on every pull request.
- [ ] Run linting and formatting checks on every pull request.
- [ ] Run secret and dependency checks on every pull request.
- [ ] Publish test and coverage results.
- [ ] Require passing checks before merging.

**Verification:** A clean checkout can install dependencies, run the test suite, and pass CI without relying on production credentials or a remote production database.

**Notes:**

---

## Milestone 10 — First stabilization release

**Priority:** P0/P1 — Recommended implementation sequence

- [ ] Rotate and remove exposed secrets.
- [ ] Fix category assignment and recipe forms.
- [ ] Fix search, category listing, and deletion.
- [ ] Remove unsafe AI HTML rendering.
- [ ] Correct environment loading.
- [ ] Correct the production deployment configuration.
- [ ] Add basic tests for authentication, authorization, recipe CRUD, categories, search, and AI failure handling.
- [ ] Add user-facing error and success messages.
- [ ] Verify the application as anonymous, customer, and administrator users.
- [ ] Document setup and deployment.
- [ ] Tag the stabilization release after all P0 items pass verification.

**Release acceptance criteria:**

- [ ] No credentials or API keys are stored in tracked files.
- [ ] The application starts with a clean checkout and external configuration.
- [ ] Recipe CRUD works for authorized users.
- [ ] Search and category browsing display the correct data.
- [ ] Unauthorized actions are rejected safely.
- [ ] AI failures do not crash the application or render untrusted HTML.
- [ ] Production deployment uses a proper WSGI server with debug mode disabled.
- [ ] Automated tests pass.

**Notes:**

---

## Change log

| Date | Change | Status | Notes |
|---|---|---|---|
| 2026-07-15 | Initial project review and modification plan created | [x] | Created by Arena |
| 2026-07-15 | Milestone 1 configuration hardening started | [-] | Removed local secret file from the working tree, added `.env.example`, hardened config loading, and added startup validation. Credential rotation and Git-history cleanup remain outstanding. |
| 2026-07-15 | Milestone 2 recipe CRUD repair started | [-] | Added category selection, recipe validation, instructions, URL-based images, flash feedback, duplicate handling, and removed unsupported servings references. |
