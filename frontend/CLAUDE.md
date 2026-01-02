# Frontend Guidelines - Phase I

## Note for Phase I
Phase I is a console-based application, so this frontend directory is prepared for future phases.

## For Future Phases (Phase II+)
- Next.js 16+ (App Router)
- TypeScript
- Tailwind CSS

## Patterns for Later Use
- Use server components by default
- Client components only when needed (interactivity)
- API calls go through `/lib/api.ts`

## Component Structure (for Phase II+)
- `/components` - Reusable UI components
- `/app` - Pages and layouts

## Spec-Driven Development
- All UI changes must be specified in markdown files before implementation
- Reference specifications: @specs/ui/components.md
- Update specs if requirements change during development