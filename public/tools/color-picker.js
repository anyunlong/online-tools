function update() {
  const v = document.getElementById('picker').value;
  document.getElementById('hex').textContent = v.toUpperCase();
  document.getElementById('preview').style.background = v;
  const r = parseInt(v.slice(1, 3), 16);
  const g = parseInt(v.slice(3, 5), 16);
  const b = parseInt(v.slice(5, 7), 16);
  document.getElementById('rgb').textContent = `(${r}, ${g}, ${b})`;
  const max = Math.max(r, g, b);
  const min = Math.min(r, g, b);
  let h = 0;
  if (max !== min) {
    const d = max - min;
    h = (max === r ? ((g - b) / d + (g < b ? 6 : 0)) : (max === g ? ((b - r) / d + 2) : ((r - g) / d + 4))) * 60;
  }
  const l = ((max + min) / 2 / 255) * 100;
  const s = max === min ? 0 : ((max - min) / (1 - Math.abs(2 * (l / 100) - 1)) / 255) * 100;
  document.getElementById('hsl').textContent = `(${Math.round(h)}°, ${Math.round(s)}%, ${Math.round(l)}%)`;
}
