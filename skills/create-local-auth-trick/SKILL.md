---
name: create-local-auth-trick
description: Create the local-only CAINZ auth "TRICK" (dev Firebase ID token + _wa_flag cookie) for manual testing when real CRM login is unavailable. Use for cainz-pet-portal manual local dev only; use integration/authMock.ts for automated tests.
---


# Create Local Auth TRICK (CAINZ pet portal)

Manual local-development bypass for `C:\sources\cainz\cainz-pet-portal`.
It makes the browser look like a logged-in member without CRM login.

**Never commit, deploy, or share the token. This is a local-only debug tool.**

## When to use

- Manual browsing of the member-only UI locally when real CRM/Firebase login
  is unavailable or impractical.
- Reproducing member-only bugs that need a real `encryptedMemberId` claim.

Do NOT use it for:

- Automated tests. Use `integration/authMock.ts` instead (see below).
- Shared, staging, or production environments.
- Any commit.

## Preconditions

- Working local dev server (`npm run dev`).
- A **dev-project** Firebase ID token whose JWT payload contains
  `encryptedMemberId` for a real member.
- Token TTL is short (about 1 hour); refresh it when API calls start returning
  401.
- `NODE_ENV !== "production"` locally.

## Files touched

| File | Purpose |
| --- | --- |
| `src/@cainz-next-web/components/auth/AuthHandler.tsx` | Pin token, set `_wa_flag=trick`, block anonymous overwrite |
| `src/@cainz-next-web/store/authStore.ts` | `getAuthStatus` returns `LoggedIn` |
| `src/@cainz-next-web/services/auth/clientAuthProvider.ts` | Stop token refresh from replacing the trick token |
| `src/@cainz-next-web/store/userStore.ts` | Optional dummy points / memberId logging |

## Steps

### 1. Capture a dev ID token

Sign in to the dev Firebase project and copy the ID token. Decode the payload
and confirm it has `encryptedMemberId`:

```bash
node -e "console.log(JSON.parse(Buffer.from(process.argv[1].split('.')[1], 'base64url')))" "<TOKEN>"
```

The token is a bearer credential. Do not paste it into tickets, chat, logs, or
source control.

### 2. Pin the token in `AuthHandler.tsx`

Add the imports and a single `TRICK_TOKEN` constant:

```tsx
// [TRICK] local-only — REVERT before commit
import Cookies from "js-cookie";
import { COOKIE_KEYS } from "@cainz-next-web/constants/cookie";

// [TRICK] Dev-env ID token with encryptedMemberId. Short TTL.
// REVERT before commit.
export const TRICK_TOKEN = "<PASTE_DEV_ID_TOKEN>";
```

Inside `AuthHandler`, before `useAuthIdentity()` is called, add the sentinel
effect:

```tsx
// [TRICK] Must run before the verification effect that reads the flag.
// REVERT before commit.
useEffect(() => {
  setFirebaseTokenCookie(TRICK_TOKEN);
  Cookies.set(COOKIE_KEYS.AUTH_FLAG, "trick", {
    secure: true,
    sameSite: "None"
  });
}, []);
```

Guard the real Firebase subscription so anonymous sign-in cannot overwrite the
trick token:

```tsx
const unsubscribe = onAuthStateChanged(auth, async (user) => {
  // [TRICK] — REVERT before commit
  if (Cookies.get(COOKIE_KEYS.AUTH_FLAG) === "trick") return;

  if (user) {
    user.getIdToken().then(setFirebaseTokenCookie).then(updateStatus);
  } else if (isVerified) {
    firebaseLogout().then(noop);
  }
});
```

Optional: log the claim for sanity.

```tsx
const payload = JSON.parse(
  atob(TRICK_TOKEN.split(".")[1].replace(/-/g, "+").replace(/_/g, "/"))
);
console.log("[TRICK] encryptedMemberId:", payload.encryptedMemberId);
```

### 3. Bypass `getAuthStatus`

In `authStore.ts`, after `recordMockAuthCheck()` / tracer setup:

```ts
// [TRICK] local dev has no CRM login — REVERT before commit.
const { authFlag } = getClientAuthCookies();
if (authFlag === "trick") {
  span.info("Trick auth bypass active, returning LoggedIn");
  return AuthStatus.LoggedIn;
}
```

`getClientAuthCookies` and `AuthStatus` are already imported in that file.

### 4. Freeze token refresh

In `clientAuthProvider.ts`'s `ensureUpdatedToken`, before `getCurrentUser()`:

```ts
// [TRICK] Without this the anonymous user's token overwrites the trick token.
// REVERT before commit.
if (Cookie.get(COOKIE_KEYS.AUTH_FLAG) === "trick") {
  return currentToken;
}
```

### 5. Optional UI data

In `userStore.ts`, when points should render without a CRM call:

```ts
if (isLoggedIn) {
  // [TRICK] dummy points — REVERT before commit
  if (Cookies.get(COOKIE_KEYS.AUTH_FLAG) === "trick") {
    useUserStore.setState({ userPoints: 1234 });
    return;
  }
  useUserStore.getState().fetchUserPoints().then(noop);
}
```

Do not remove `Cookies` / `COOKIE_KEYS` imports from `userStore.ts`; they are
also used for the shipping-address cache.

## Verify

1. `npm run dev`, open `http://localhost:3000`.
2. Header shows the member state; member-only blocks render.
3. Console shows `[TRICK] encryptedMemberId: ...`.
4. DevTools > Application > Cookies contains `_wa_flag=trick` and a Firebase
   token cookie.
5. Member API requests send `Authorization: Bearer ...` and do not 401.
6. Sign out / clear the flag and confirm the app returns to guest.

## Remove before commit

`[TRICK]` markers are deliberately greppable:

```bash
grep -rn "TRICK\|trick" src integration
```

- Revert every `[TRICK]` block.
- Delete `TRICK_TOKEN`.
- Remove imports only if they became unused. Check first:
  - `AuthHandler.tsx`: `Cookies` and `COOKIE_KEYS` become unused.
  - `clientAuthProvider.ts`: `Cookie` and `COOKIE_KEYS` are still used for
    `FIREBASE_TOKEN`.
  - `userStore.ts`: `Cookies` and `COOKIE_KEYS` are still used for shipping
    address.
- Run:
  - `npx tsc --noEmit`
  - `npx playwright test -c playwright.config.ts`
  - `npx playwright test -c playwright.integration.config.ts`
- `git diff` must contain no token and no `[TRICK]` marker.

If a real token was committed, treat it as leaked: revoke/rotate it immediately
and remove it from history before pushing.

## Preferred automated alternative

For tests, do not use a real token. Use the test-only mock:

```ts
import { installMockAuth } from "./authMock";

await installMockAuth(page, { status: "member", memberId: "mock-member-a" });
// or
await installMockAuth(page, { status: "guest" });
```

The mock is inert in production (`isAuthMockActive()` requires
`NODE_ENV !== "production"` and `window.__CAINZ_AUTH_MOCK__`), sets
`_wa_flag=mock`, and exposes check counters for readiness assertions.
