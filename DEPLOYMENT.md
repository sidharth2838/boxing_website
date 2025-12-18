# Deployment Guide for Boxing Project

## Important Note
Netlify is primarily for static sites and doesn't natively support full Django applications. Consider alternative hosting for better results.

## Recommended Hosting Options (in order of preference):

### 1. **Railway.app** (Recommended)
- Supports Django out of the box
- Simple GitHub integration
- Free tier available

**Steps:**
1. Push code to GitHub
2. Go to [railway.app](https://railway.app)
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your boxing_website repo
5. Add environment variables (SECRET_KEY, DEBUG, ALLOWED_HOSTS)
6. Railway auto-detects Django and deploys

### 2. **Render.com**
- Similar to Railway
- Good free tier
- Simple deployment process

### 3. **PythonAnywhere**
- Python-specific hosting
- Built-in Django support
- Good for beginners

### 4. **Heroku** (Paid only now)
- Used to have free tier
- Excellent Django support
- Use `Procfile` (already created)

## If You Must Use Netlify:

### Prerequisites
- GitHub account with code pushed
- Netlify account

### Setup Steps:

1. **Create .env file** (DO NOT COMMIT THIS):
   ```
   DEBUG=False
   SECRET_KEY=your-very-secure-random-secret-key
   ALLOWED_HOSTS=yourdomain.netlify.app,www.yourdomain.netlify.app
   DATABASE_URL=postgresql://user:pass@host:5432/dbname
   ```

2. **Create PostgreSQL Database**:
   - Use Supabase.co or Vercel PostgreSQL (free tier)
   - Get DATABASE_URL connection string

3. **Deploy to Netlify**:
   ```bash
   npm install -g netlify-cli
   netlify login
   netlify deploy --prod
   ```

4. **Set Environment Variables in Netlify**:
   - Go to Site Settings → Build & Deploy → Environment
   - Add all variables from .env

5. **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
6. **Publish Directory**: `boxing_app/static`

## For Local Development:

1. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Create .env file** (copy from .env.example)

4. **Run migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser**:
   ```bash
   python manage.py createsuperuser
   ```

6. **Start development server**:
   ```bash
   python manage.py runserver
   ```

## Database Migration:

To migrate from SQLite to PostgreSQL:

```bash
# Export from SQLite
python manage.py dumpdata > data.json

# Update settings.py (or .env) to use PostgreSQL
# Run migrations
python manage.py migrate --run-syncdb

# Load data
python manage.py loaddata data.json
```

## Important Files for Deployment:

- `requirements.txt` - Python dependencies
- `.env.example` - Environment variables template
- `Procfile` - For Heroku/Render
- `netlify.toml` - For Netlify
- `runtime.txt` - Python version

## Security Checklist:

- [ ] Change SECRET_KEY to a random string
- [ ] Set DEBUG=False in production
- [ ] Add your domain to ALLOWED_HOSTS
- [ ] Use a production database (PostgreSQL, not SQLite)
- [ ] Use HTTPS only
- [ ] Set secure CSRF settings
- [ ] Hide sensitive variables in .env (never commit .env)
