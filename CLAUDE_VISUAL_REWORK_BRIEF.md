# Visual Rework Brief For Claude

## Goal

Improve the visual quality of `fclass.by` without a full redesign.

The site already has a premium foundation. Keep the First Class visual direction, but make it more coherent, readable, mobile-friendly, and conversion-oriented for a B2B audience:

- accountants
- HR teams
- directors
- office managers
- owners of small companies and individual entrepreneurs

The result should feel like a mature corporate travel service: premium, calm, reliable, and practical.

## Deployment Context

- Production is deployed on Belarusian Apache/PHP hosting.
- The site is not deployed on Vercel.
- Do not break the PHP endpoint `/api/lead-magnet.php`.
- Do not change URL structure.
- Do not change the SEO/content strategy.
- Do not turn the site into a SaaS/startup landing page.
- Main visual style: dark navy, gold, white, premium corporate travel.

## Main Issues To Fix

### 1. Home Page Hero

File: `index.html`

Desktop:

- Keep the photo background and premium mood.
- Reduce the visual heaviness of the H1.
- Improve H1 readability over the city background.
- Adjust contrast, line-height, and typography.
- Fix dense/merged text, especially around "Авиабилеты для организаций и физлиц".
- Make CTA buttons visually balanced:
  - primary: "Организовать командировку"
  - secondary: "Написать в Telegram"
- Reduce visual noise around the hero. Small helper text should support the main message, not compete with it.

Mobile:

- Treat the mobile hero as its own layout, not just a cropped desktop layout.
- Logo must remain readable.
- Header "Связаться" button must not take half the screen width.
- Burger icon must not be pressed against the viewport edge.
- H1 must fit comfortably on 360-430px widths.
- CTA buttons must be visible, balanced, and not overly tall.
- The first screen should clearly communicate: business travel and airline tickets for companies / legal entities / individual entrepreneurs.

### 2. Header And Navigation

- Make desktop navigation less cramped.
- Add more spacing and reduce visual noise.
- Ensure nav links do not visually merge or compete with the logo.
- Mobile header should be clean:
  - logo on the left
  - compact CTA, phone action, or icon if needed
  - burger on the right
- On narrow screens, hide or shorten the "Связаться" button if it damages layout.

### 3. Unified Visual System

Bring the key public pages into one coherent visual system:

- `/`
- `/komandirovki/`
- `/tickets/`
- `/tickets/aviabilety-dlya-yurlic/`
- `/komandirovochnye-kalkulyator/`
- `/resources/dogovor-template/`
- `/cases/`
- `/blog/`

Unify:

- header
- footer
- CTA blocks
- forms
- benefit cards
- buttons
- section spacing
- h1/h2/h3 styles
- color tokens

Do not rewrite all HTML if CSS and repeated block cleanup are enough.

### 4. Internal Pages

- Remove the feeling that different pages were made from unrelated templates.
- SEO pages should still feel like First Class brand pages.
- Blog articles should remain readable, but header/footer should feel consistent.
- Lead forms should look trustworthy and intentional, not like random embedded forms.

### 5. Mobile QA

Check these widths:

- 360px
- 390px
- 430px
- 768px
- 1280px

Verify:

- no horizontal scrolling
- headings do not merge or overlap
- buttons do not become too tall
- text does not overlap backgrounds or CTAs
- header does not cover the hero content
- forms are easy to fill on touch devices

## What Not To Do

- Do not change deployment/domain logic.
- Do not remove existing forms or webhook submission.
- Do not change URL structure.
- Do not add heavy libraries.
- Do not make a SaaS-style hero with white cards and abstract illustrations.
- Do not use purple/blue gradient styling.
- Do not make the site look like a B2C tourism site.
- Do not do a full rebrand.

## Expected Deliverables

After changes:

- Run a local server.
- Capture desktop and mobile screenshots of the home page.
- Capture screenshots of `/tickets/` and `/komandirovki/`.
- Briefly summarize which visual problems were fixed.

## Design Direction

The key instruction is not "make it prettier".

The key instruction is: make it more coherent, more readable, and more credible as a B2B corporate travel service.

