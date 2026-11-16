# Stack Notes: Implementing UI Rules per Framework

Open this after you detect the stack (SKILL.md step 1) and before you implement or review UI code. Each section lists the UI-relevant rules that agents most often get wrong. Confirm library versions in the project's lockfile before relying on version-specific APIs.

## Plain HTML and CSS (all web stacks)

- Use native elements first: `button` for actions, `a href` for navigation, `label` for inputs, `dialog` for modals where supported. ARIA repairs only what HTML cannot express.
- Icon-only buttons: `<button aria-label="Close"><svg aria-hidden="true" focusable="false">…</svg></button>`.
- Visually hidden text uses a `.sr-only` class, not `display: none` (which hides it from screen readers too).
- Set `lang` on `<html>` and `dir="rtl"` for right-to-left content.

## Tailwind CSS

| Need | Use | Red flag |
|---|---|---|
| Focus | `focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[--color-ring]` or `focus-visible:ring-2` | `outline-none` with no `focus-visible:` replacement |
| Targets | `min-h-11 min-w-11` (44 px) on touch controls | `p-1` icon buttons |
| Motion | `motion-safe:animate-…`, `motion-reduce:transition-none` | `animate-bounce` on content |
| Media | `aspect-video`, explicit `width`/`height` on `img` and `svg` | Images without dimensions |
| Text resilience | `min-w-0` on flex children, `break-words` or `wrap-anywhere` on user text | Long URLs overflowing cards |
| Colors | Semantic tokens via theme (`bg-primary`, `text-muted-foreground`) | Raw `bg-[#2563eb]` scattered in components |
| Dynamic classes | Map to complete class strings: `{ red: 'bg-red-600', blue: 'bg-blue-600' }[c]` | `bg-${color}-600` (purged at build) |
| Layers | A documented `z-*` scale | `z-[9999]` |

Tailwind v4 reads tokens from CSS (`@theme`); v3 from `tailwind.config.js`. Check which one the project uses before editing.

## React

- Every list item needs a stable `key` (an ID, not the array index for reorderable lists).
- Pass handlers, not calls: `onClick={save}`, not `onClick={save()}`.
- Derive values during render; do not mirror props into state with an effect.
- Clean up timers, listeners, and subscriptions in the effect's return function.
- Modals: trap focus, close on Escape, return focus to the trigger. Prefer a tested primitive (Radix, React Aria, Headless UI, Base UI) over a hand-rolled one.
- Label inputs with `htmlFor` and matching `id`; use `useId()` for generated IDs.
- Wrap independent regions in error boundaries so one failure shows a local error state.
- Virtualize lists above a few hundred rows (TanStack Virtual, react-window).
- React 19: form actions with `useActionState` give pending and error state; `useFormStatus` works only in a child of the `<form>`.

## Next.js (App Router)

- Server Components by default; add `'use client'` only to the interactive leaf, not the whole page.
- Every route segment that can fail or load slowly gets `loading.tsx` (skeleton) and `error.tsx` (with a `reset` action); add `not-found.tsx` where IDs can be wrong.
- `next/image` with `width`/`height` or `fill` plus `sizes`; mark only the LCP image with `priority`.
- `next/font` for self-hosted fonts with no layout shift.
- `next/link` for internal navigation; keep filters in `searchParams` so back and share work.
- Validate and authorize Server Action input on the server, then show pending and error state in the form.

## Vue 3 and Nuxt

- `v-for` always with `:key`; never put `v-if` on the same element as `v-for` (filter in a computed).
- Do not mutate props; emit an event or use `v-model` with `defineModel()`.
- Access DOM in `onMounted`; clean up in `onUnmounted`.
- Pinia: destructure with `storeToRefs(store)` to keep reactivity.
- Nuxt: wrap browser-only widgets in `<ClientOnly>` with a fallback to avoid hydration mismatch; use `<NuxtImg>` and `useHead` for `lang` and titles.

## Svelte and SvelteKit

- Svelte 5 runes: `$state`, `$derived`, `$props`, and `onclick={…}` event attributes in new code; keep legacy syntax only in untouched legacy files.
- `{#each items as item (item.id)}`: always key lists.
- Load data in `+page.ts` / `+page.server.ts` (server-only secrets in the latter); show pending UI with `{#await}` or navigation state.
- Form actions with `use:enhance` keep the page working without JavaScript; show errors from `form` props next to fields.
- Svelte's compiler emits accessibility warnings (`a11y_*`). Treat them as errors in review.

## shadcn/ui (React, Radix or Base UI primitives)

- Add components with `npx shadcn@latest add <name>`; preview with `--dry-run` before overwriting local edits.
- Theme through CSS variables in `:root` and `.dark` (`--background`, `--foreground`, `--primary`, `--ring`, …). Define both schemes fully.
- `AlertDialog` for destructive confirmation, `Dialog` for forms and details, `Sheet` for side panels.
- Mount `<Toaster />` once in the root layout and `TooltipProvider` once at app level.
- Forms: the `Form`/`Field` pattern with React Hook Form or TanStack Form, so labels, descriptions, and errors are linked with ARIA automatically.
- Keep the primitive's focus management; do not stop propagation of Escape or override `onOpenAutoFocus` without a reason.
- Use an anchor for links and a button for actions, even when styled with `buttonVariants`.

## SwiftUI

- Use system text styles (`.font(.body)`, `.title`) so Dynamic Type works; test at the largest accessibility size.
- Targets ≥ 44×44 pt: `.frame(minWidth: 44, minHeight: 44)` and `.contentShape(Rectangle())` for small icons.
- `.accessibilityLabel`, `.accessibilityHint`, and `.accessibilityElement(children: .combine)` for composite rows.
- Check `@Environment(\.accessibilityReduceMotion)` and `accessibilityReduceTransparency` before custom animation or blur.
- Semantic colors (`Color.primary`, `.secondary`, asset colors with dark variants), never hard-coded black and white.
- `LazyVStack` / `List` for long content; stable `Identifiable` IDs.
- State: `@State` for view-local values, `@Observable` models (or `@StateObject` on older targets) for owned reference types.

## Flutter

- Material 3 targets: 48×48 dp minimum (`MaterialTapTargetSize.padded`).
- `Semantics(label: …)` on custom painted or icon-only widgets; `ExcludeSemantics` for decoration; test with TalkBack and VoiceOver.
- Respect text scaling: read `MediaQuery.textScalerOf(context)`; avoid fixed-height containers around text.
- `MediaQuery.disableAnimationsOf(context)` to honor reduced motion.
- Theme via `ThemeData` and `ColorScheme.fromSeed` with both light and dark schemes; no raw `Color(0xFF…)` in widgets.
- `ListView.builder` for long lists; dispose controllers (`TextEditingController`, `AnimationController`) in `dispose()`.
- `PopScope` for back handling; `Form` plus `GlobalKey<FormState>` and `validator` for forms.
- Handle `FutureBuilder` / `StreamBuilder` states: waiting, error, empty, and data.

## Verification commands

| Check | Command or tool |
|---|---|
| Accessibility scan (web) | `npx @axe-core/cli http://localhost:3000` or `@axe-core/playwright` in an E2E test |
| Lint JSX accessibility | `eslint-plugin-jsx-a11y` (React), `eslint-plugin-vuejs-accessibility` (Vue), Svelte compiler warnings |
| Performance and CLS | `npx lighthouse http://localhost:3000 --only-categories=performance,accessibility --view` |
| Responsive screenshots | Playwright: `page.setViewportSize({ width: 375, height: 812 })` then `page.screenshot()`; repeat at 1280 |
| Flutter | `flutter test` with `meetsGuideline(androidTapTargetGuideline)` and `textContrastGuideline` |
| iOS | Xcode Accessibility Inspector audit; `XCUIApplication().performAccessibilityAudit()` (Xcode 15+) |

Sources: adapted from nextlevelbuilder/ui-ux-pro-max-skill (MIT) (`stacks/react.csv`, `nextjs.csv`, `vue.csv`, `svelte.csv`, `swiftui.csv`, `flutter.csv`, `html-tailwind.csv`, `shadcn.csv`) and general practice.
