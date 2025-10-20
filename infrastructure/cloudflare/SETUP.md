# Cloudflare Deployment & Access Login Setup

This guide walks through deploying the Quantum Writer frontend to Cloudflare Pages and securing it with Cloudflare Access. It assumes you have already pushed the repository to GitHub (or another Git host) and can run GitHub Actions.

## 1. Prepare Cloudflare Resources

1. **Create a Pages project**
   - Log in to the Cloudflare dashboard → *Pages* → *Create project*.
   - Connect your repository or choose *Direct Upload* (GitHub workflow below assumes a connected repo).
   - Note the project name (slug). Example: `quantum-writer`.
2. **Enable Cloudflare Access**
   - Navigate to *Zero Trust* → *Access* → *Applications* → *Add an application* → *Self-hosted*.
   - Set the application domain to the Pages hostname (e.g. `quantum-writer.pages.dev`).
   - Under *Policies*, define who can log in (emails, groups, identity providers, etc.).
   - After creating the app, copy the **Audience (AUD) Tag** and note your **Team Domain** (e.g. `my-team.cloudflareaccess.com`).
3. (Optional) **Service token**
   - If you want server-to-server verification, create a service token under *Zero Trust* → *Access* → *Service Tokens*. The Client ID/Secret can be supplied to other services but are not required for the default flow.

## 2. Configure Repository Secrets & Variables

Add the following to your GitHub repository (Settings → Secrets and variables → Actions):

| Name | Type | Value |
| ---- | ---- | ----- |
| `CLOUDFLARE_API_TOKEN` | Secret | Token with `Pages:Edit` and `Pages:Deployments:Create` permissions |
| `CLOUDFLARE_ACCOUNT_ID` | Secret | Your Cloudflare account ID |
| `CLOUDFLARE_PAGES_PROJECT` | Variable | Pages project slug (e.g. `quantum-writer`) |
| `AUTH_SERVICE_URL` | Secret or Variable | Public URL to the auth service (e.g. `https://api.example.com/auth`) |
| `NEXT_PUBLIC_API_URL` | Variable | Public gateway URL (e.g. `https://api.example.com`) |
| `NEXT_PUBLIC_WS_URL` | Variable | Public websocket URL (e.g. `wss://api.example.com/ws`) |
| `NEXT_PUBLIC_CLOUDFLARE_ACCESS_LOGIN` | Variable | `true` to enable automatic Access login |
| `CLOUDFLARE_ACCESS_AUDIENCE` | Secret or Variable | Audience tag copied from the Access app |
| `CLOUDFLARE_ACCESS_TEAM_DOMAIN` | Variable | Team domain (e.g. `my-team.cloudflareaccess.com`) |
| `CLOUDFLARE_ACCESS_EMAIL_CLAIM` | Optional Variable | Override Access email claim (default: `email`) |
| `CLOUDFLARE_ACCESS_ALLOWED_EMAILS` | Optional Variable | Comma-separated email allow-list |
| `CLOUDFLARE_ACCESS_ALLOWED_DOMAINS` | Optional Variable | Comma-separated domain allow-list |

> 📌 Use organization or environment-level secrets if you manage multiple deployments.

## 3. Enable the GitHub Actions Workflow

The repository contains `.github/workflows/deploy-cloudflare-pages.yml`. Once the variables above are configured:

1. Push to the `main` branch, or
2. Trigger the workflow manually via *Actions* → *Deploy Cloudflare Pages* → *Run workflow*.

The workflow:

1. Checks out the code and installs dependencies.
2. Builds the Next.js app via `@cloudflare/next-on-pages` producing `.vercel/output`.
3. Deploys the build to your Cloudflare Pages project using the API token.

You can monitor build logs directly in GitHub Actions or the Cloudflare Pages dashboard.

## 4. Expose the Auth Service

Cloudflare Pages needs to contact the auth microservice to exchange Access tokens. Ensure:

- The auth service is reachable via HTTPS at the URL defined in `AUTH_SERVICE_URL` (e.g. behind your API gateway).
- The gateway forwards `POST /login/cloudflare` to the auth service.
- The auth service runtime includes the same Access environment variables (`CLOUDFLARE_ACCESS_*`) so it can verify JWTs.

## 5. Verify the Flow

1. Deploy the site and visit the Cloudflare Pages URL.
2. Complete the Cloudflare Access login challenge.
3. After redirection, open the browser dev tools → *Application* → *Cookies* and confirm `accessToken` / `refreshToken` are set for your site.
4. Use the app normally (create stories, generate chapters). Requests to the backend should now include the bearer token.

If you receive a `501 Cloudflare Access integration not configured` response, double-check the environment variables on both the frontend and auth service. A `403` indicates the email did not pass the allow-list; update the `CLOUDFLARE_ACCESS_ALLOWED_*` variables accordingly.

## 6. Local Development Tips

- Keep `NEXT_PUBLIC_CLOUDFLARE_ACCESS_LOGIN` unset or `false` while running locally to use the built-in login screen.
- To test Access tokens manually, run `cloudflared access login https://quantum-writer.pages.dev` and copy the `CF_Authorization` cookie into a request against `/cloudflare/session`.
- The auth service caches the JWKS for one hour. Restart the service or wait for the cache to expire if you rotate Access keys.

With these steps, the Quantum Writer frontend is deployed on Cloudflare Pages and protected by Cloudflare Access, while the backend services continue to run in your preferred environment.
