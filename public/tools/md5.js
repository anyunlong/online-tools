async function hash() {
  const t = document.getElementById('inp').value;
  if (!t) {
    document.getElementById('md5-32').textContent = '—';
    document.getElementById('md5-16').textContent = '—';
    return;
  }
  const enc = new TextEncoder().encode(t);
  const buf = await crypto.subtle.digest('MD5', enc).catch(() => null);
  if (!buf) {
    document.getElementById('md5-32').textContent = 'MD5 不支持，请使用 SHA256';
    return;
  }
  const arr = Array.from(new Uint8Array(buf));
  const hex = arr.map(b => b.toString(16).padStart(2, '0')).join('');
  document.getElementById('md5-32').textContent = hex.toUpperCase();
  document.getElementById('md5-16').textContent = hex.substring(8, 24).toUpperCase();
}
