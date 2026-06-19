const API_BASE = '/api';

async function apiRequest(method, path, data = null) {
    const opts = {
        method,
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
    };
    if (data) opts.body = JSON.stringify(data);
    const res = await fetch(API_BASE + path, opts);
    const json = await res.json();
    if (!res.ok) throw new Error(json.error || 'エラーが発生しました');
    return json;
}

async function getMe() {
    try {
        return await apiRequest('GET', '/auth/me');
    } catch {
        return null;
    }
}

async function requireAuth() {
    const data = await getMe();
    if (!data) {
        window.location.href = '/login.html?redirect=' + encodeURIComponent(window.location.href);
        return null;
    }
    return data.user;
}

async function renderNav() {
    const navAuth = document.getElementById('nav-auth');
    if (!navAuth) return;
    const data = await getMe();
    if (data && data.user) {
        navAuth.innerHTML = `
            <a href="/my_bookings.html">予約確認</a>
            <a href="#" id="logout-btn">ログアウト</a>
            <span class="user-name">${data.user.username} 様</span>
        `;
        document.getElementById('logout-btn').addEventListener('click', async (e) => {
            e.preventDefault();
            await apiRequest('POST', '/auth/logout');
            window.location.href = '/index.html';
        });
    } else {
        navAuth.innerHTML = `
            <a href="/login.html">ログイン</a>
            <a href="/register.html">新規登録</a>
        `;
    }
}

function showError(msg) {
    const el = document.getElementById('error-msg');
    if (el) { el.textContent = msg; el.style.display = 'block'; }
}

function getParams() {
    return Object.fromEntries(new URLSearchParams(window.location.search));
}
